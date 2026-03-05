"""Repository helpers for runs table."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings


def create_run(run: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "run_id": run["run_id"],
        "status": run.get("status", "queued"),
        "created_at": run.get("created_at", now_iso()),
        "started_at": run.get("started_at"),
        "ended_at": run.get("ended_at"),
        "active_agent_id": run.get("active_agent_id"),
        "task_spec": to_json(run.get("task_spec")),
        "model_usage": to_json(run.get("model_usage")),
        "cost_estimate_usd": run.get("cost_estimate_usd"),
        "cost_actual_usd": run.get("cost_actual_usd"),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO runs (
                run_id, status, created_at, started_at, ended_at, active_agent_id,
                task_spec, model_usage, cost_estimate_usd, cost_actual_usd
            )
            VALUES (
                :run_id, :status, :created_at, :started_at, :ended_at, :active_agent_id,
                :task_spec, :model_usage, :cost_estimate_usd, :cost_actual_usd
            );
            """,
            payload,
        )


def update_run_status(
    run_id: str,
    status: str,
    started_at: Optional[str] = None,
    ended_at: Optional[str] = None,
    settings: Settings | None = None,
) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            UPDATE runs
            SET status = :status,
                started_at = COALESCE(:started_at, started_at),
                ended_at = COALESCE(:ended_at, ended_at)
            WHERE run_id = :run_id;
            """,
            {
                "run_id": run_id,
                "status": status,
                "started_at": started_at,
                "ended_at": ended_at,
            },
        )


def update_run_costs(
    run_id: str,
    cost_estimate_usd: Optional[float] = None,
    cost_actual_usd: Optional[float] = None,
    settings: Settings | None = None,
) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            UPDATE runs
            SET cost_estimate_usd = COALESCE(:cost_estimate_usd, cost_estimate_usd),
                cost_actual_usd = COALESCE(:cost_actual_usd, cost_actual_usd)
            WHERE run_id = :run_id;
            """,
            {"run_id": run_id, "cost_estimate_usd": cost_estimate_usd, "cost_actual_usd": cost_actual_usd},
        )


def get_run(run_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        return row_to_dict(row)


def list_runs(settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall()
        return [row_to_dict(row) for row in rows if row is not None]
