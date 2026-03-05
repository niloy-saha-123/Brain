"""Approvals placeholder endpoints (list pending, resolve)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import repo_approvals
from app.core.time import now_iso

router = APIRouter()


@router.get("/approvals")
def list_pending():
    return repo_approvals.list_pending()


@router.post("/approvals/{approval_id}/resolve")
def resolve_approval(approval_id: str, decision: dict):
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
    return {"status": "ok"}
