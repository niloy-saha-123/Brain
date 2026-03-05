"""Repository helpers for filesystem allowlists per run."""
from __future__ import annotations

from typing import Dict, List

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict
from app.core.config import Settings


def allow_path(run_id: str, path: str, approval_id: str, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO fs_allowlist (run_id, path, approval_id, approved_at)
            VALUES (:run_id, :path, :approval_id, :approved_at)
            ON CONFLICT(run_id, path) DO UPDATE SET
                approval_id = excluded.approval_id,
                approved_at = excluded.approved_at;
            """,
            {"run_id": run_id, "path": path, "approval_id": approval_id, "approved_at": now_iso()},
        )


def is_allowed(run_id: str, path: str, settings: Settings | None = None) -> bool:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT 1 FROM fs_allowlist WHERE run_id = ? AND path = ?", (run_id, path)).fetchone()
        return row is not None


def list_allowlist(run_id: str | None = None, settings: Settings | None = None) -> List[Dict]:
    query = "SELECT * FROM fs_allowlist"
    params = ()
    if run_id:
        query += " WHERE run_id = ?"
        params = (run_id,)
    with get_connection(settings) as conn:
        rows = conn.execute(query, params).fetchall()
        return [row_to_dict(r) for r in rows if r]
