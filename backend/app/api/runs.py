"""Runs endpoints: start a run, list runs, get run, stream via SSE is elsewhere."""
from __future__ import annotations

import asyncio
import json
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas import TaskSpec
from app.core.ids import make_run_id
from app.orchestrator.graph import start_run
from app.db import repo_runs, repo_planner_traces

router = APIRouter()


class RunCreateRequest(BaseModel):
    goal: str = Field(..., min_length=1, description="Goal/command for the run")
    run_id: Optional[str] = Field(default=None, description="Optional run id override")


@router.post("/runs")
async def create_run(req: RunCreateRequest):
    run_id = req.run_id or make_run_id("run")
    task = TaskSpec(id=run_id, g=req.goal, v=1)
    # Fire-and-forget orchestration so SSE can stream live.
    asyncio.create_task(start_run(task))
    return {"run_id": run_id, "status": "queued"}


@router.get("/runs")
def list_runs():
    return repo_runs.list_runs()


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    run = repo_runs.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="not found")
    return run


@router.get("/runs/{run_id}/plan")
def get_run_plan(run_id: str):
    trace = repo_planner_traces.get_trace(run_id)
    if not trace:
        raise HTTPException(status_code=404, detail="plan not found")
    trace_data = trace.get("trace")
    if isinstance(trace_data, str):
        try:
            trace_data = json.loads(trace_data)
        except json.JSONDecodeError:
            trace_data = trace_data
    return {"run_id": run_id, "trace": trace_data, "created_at": trace.get("created_at")}
