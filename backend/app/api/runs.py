"""Runs endpoints: start a run, list runs, get run, stream via SSE is elsewhere."""
from __future__ import annotations

import asyncio
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas import TaskSpec
from app.core.ids import make_run_id
from app.orchestrator.graph import start_run
from app.db import repo_runs

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
