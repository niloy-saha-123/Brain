"""Approvals placeholder endpoints (list pending, resolve)."""
from __future__ import annotations

import json
from fastapi import APIRouter, HTTPException

from app.db import repo_approvals, repo_runs, repo_fs_allowlist
from app.core.time import now_iso
from app.events.bus import event_bus
from app.orchestrator.graph import resume_run_after_approval
from app.tools.runner import run_tool
from app.tools.base import ToolError

router = APIRouter()


@router.get("/approvals")
def list_pending():
    return repo_approvals.list_pending()


@router.post("/approvals/{approval_id}/resolve")
async def resolve_approval(approval_id: str, decision: dict):
    approval = repo_approvals.get_approval(approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="not found")
    status = decision.get("action", "approved")
    repo_approvals.resolve_approval(
        approval_id,
        decision=decision,
        status=status,
        resolved_at=now_iso(),
    )
    event = {
        "type": "approval_resolved",
        "approval_id": approval_id,
        "run_id": approval.get("run_id"),
        "status": status,
    }
    await event_bus.publish(event)
    # Attempt to resume any paused run
    await resume_run_after_approval(approval_id, status)

    # Auto-handle RAG indexing approvals
    if approval.get("type") == "rag.index" and status == "approved":
        req_raw = approval.get("request") or {}
        if isinstance(req_raw, str):
            try:
                req = json.loads(req_raw)
            except json.JSONDecodeError:
                req = {}
        else:
            req = req_raw
        details = req.get("details") or {}
        path = details.get("path")
        run_id = approval.get("run_id")
        if path and run_id:
            try:
                repo_runs.update_run_status(run_id, "running")
                await run_tool("rag.index", {"path": path}, {"run_id": run_id, "approval_id": approval_id})
                repo_runs.update_run_status(run_id, "completed", ended_at=now_iso())
            except ToolError:
                pass
    if approval.get("type") in {"filesystem.read", "filesystem.write"} and status == "approved":
        req_raw = approval.get("request") or {}
        if isinstance(req_raw, str):
            try:
                req = json.loads(req_raw)
            except json.JSONDecodeError:
                req = {}
        else:
            req = req_raw
        details = req.get("details") or {}
        path = details.get("path")
        run_id = approval.get("run_id")
        if path and run_id:
            repo_fs_allowlist.allow_path(run_id, path, approval_id)
    return {"status": "ok"}
