"""Simplified orchestrator stub for v0.1 milestone."""
from __future__ import annotations

import asyncio
from typing import Any, Dict

from app.orchestrator.state import RunState
from app.schemas import TaskSpec
from app.events.bus import event_bus
from app.core.time import now_iso
from app.db import repo_runs


async def start_run(task_spec: TaskSpec) -> RunState:
    run_id = task_spec.id
    state = RunState(run_id=run_id, task_spec=task_spec)
    repo_runs.create_run({"run_id": run_id, "status": "running", "task_spec": task_spec.model_dump()})
    await event_bus.publish({"type": "status", "run_id": run_id, "status": "running", "ts": now_iso()})
    await event_bus.publish({"type": "worklog", "run_id": run_id, "msg": "Run started"})
    # placeholder: immediately complete
    state.status = "completed"
    repo_runs.update_run_status(run_id, "completed", ended_at=now_iso())
    await event_bus.publish({"type": "status", "run_id": run_id, "status": "completed", "ts": now_iso()})
    return state
