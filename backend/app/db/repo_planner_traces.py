"""Repository helpers for planner_traces table."""
from __future__ import annotations

from typing import Any, Dict, Optional

from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings
from app.core.time import now_iso


def upsert_trace(trace: Dict[str, Any], settings: Settings | None = None) -> None:
    trace_payload = trace.get("trace") or trace
    payload = {
        "run_id": trace["run_id"],
        "trace": to_json(trace_payload),
        "created_at": trace.get("created_at", now_iso()),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO planner_traces (run_id, trace, created_at)
            VALUES (:run_id, :trace, :created_at)
            ON CONFLICT(run_id) DO UPDATE SET
                trace = excluded.trace,
                created_at = excluded.created_at;
            """,
            payload,
        )


def get_trace(run_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM planner_traces WHERE run_id = ?", (run_id,)).fetchone()
        return row_to_dict(row)
