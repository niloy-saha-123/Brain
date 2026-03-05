"""Repository helpers for approvals table."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings


def create_approval(approval: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "approval_id": approval["approval_id"],
        "run_id": approval["run_id"],
        "type": approval.get("type", ""),
        "status": approval.get("status", "pending"),
        "request": to_json(approval.get("request")),
        "decision": to_json(approval.get("decision")),
        "created_at": approval.get("created_at", now_iso()),
        "resolved_at": approval.get("resolved_at"),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO approvals (
                approval_id, run_id, type, status, request, decision, created_at, resolved_at
            )
            VALUES (
                :approval_id, :run_id, :type, :status, :request, :decision, :created_at, :resolved_at
            );
            """,
            payload,
        )


def resolve_approval(
    approval_id: str,
    decision: Dict[str, Any],
    status: str,
    resolved_at: Optional[str] = None,
    settings: Settings | None = None,
) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            UPDATE approvals
            SET decision = :decision,
                status = :status,
                resolved_at = :resolved_at
            WHERE approval_id = :approval_id;
            """,
            {
                "approval_id": approval_id,
                "decision": to_json(decision),
                "status": status,
                "resolved_at": resolved_at or now_iso(),
            },
        )


def get_approval(approval_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM approvals WHERE approval_id = ?", (approval_id,)).fetchone()
        return row_to_dict(row)


def list_pending(settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute(
            "SELECT * FROM approvals WHERE status = 'pending' ORDER BY created_at ASC"
        ).fetchall()
        return [row_to_dict(row) for row in rows if row is not None]
