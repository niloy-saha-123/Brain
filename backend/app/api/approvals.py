"""Approvals placeholder endpoints (list pending, resolve)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import repo_approvals
from app.core.time import now_iso
from app.events.bus import event_bus

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
    return {"status": "ok"}
