"""Orchestrator that runs the simple graph and handles approvals/resume."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from app.orchestrator.state import RunState
from app.schemas import TaskSpec
from app.events.bus import event_bus
from app.core.time import now_iso
from app.db import repo_runs
from app.tools.runner import run_tool
from app.tools.base import ToolError
from app.orchestrator import pending
from app.orchestrator.nodes import route, rewrite, load_context, plan, execute, verify, finalize


async def start_run(task_spec: TaskSpec) -> RunState:
    run_id = task_spec.id
    state = RunState(run_id=run_id, task_spec=task_spec)
    existing = repo_runs.get_run(run_id)
    if existing:
        repo_runs.update_run_status(run_id, "running", started_at=now_iso())
        repo_runs.update_run_costs(run_id, cost_estimate_usd=existing.get("cost_estimate_usd"))
    else:
        repo_runs.create_run(
            {"run_id": run_id, "status": "running", "task_spec": task_spec.model_dump(), "created_at": now_iso()}
        )
    await _publish_status(run_id, "running")
    await _publish_worklog(run_id, "Run started")

    # Graph: route -> rewrite -> context -> plan -> execute -> verify -> finalize
    route(state)
    rewrite(state)
    load_context(state)
    plan(state)
    paused = await _execute_plan(state)
    if paused:
        return state
    verify(state)
    finalize(state)

    state.status = "completed"
    repo_runs.update_run_status(run_id, "completed", ended_at=now_iso())
    await _publish_status(run_id, "completed")
    return state


async def _execute_plan(state: RunState) -> bool:
    """Run the planned steps sequentially. Returns True if paused awaiting approval."""
    run_id = state.run_id
    for idx in range(state.current_step, len(state.plan)):
        step = state.plan[idx]
        state.current_step = idx
        tool_name = step["tool"]
        args = step.get("args", {})
        await _publish_worklog(run_id, f"Executing tool {tool_name}")
        receipt_id = f"r_{now_iso()}"
        try:
            result = await run_tool(tool_name, args, {"run_id": run_id, "receipt_id": receipt_id})
            state.receipts.append(receipt_id)
            await _publish_worklog(run_id, f"Tool {tool_name} ok")
            state.current_step = idx + 1
            if tool_name == "todo.add":
                state.output = f"Recorded todo: {result.result.get('todo', {}).get('text', '')}"
            elif tool_name == "web.fetch":
                state.output = result.result.get("text", "")[:200]
            elif tool_name == "filesystem.read":
                state.output = result.result.get("content", "")[:200]
        except ToolError as exc:
            msg = str(exc)
            if "approval_id=" in msg:
                approval_id = msg.split("approval_id=")[1]
                state.approvals.append(approval_id)
                pending.add_pending(approval_id, state, tool_name, args, idx)
                state.status = "awaiting_approval"
                repo_runs.update_run_status(run_id, "awaiting_approval")
                await _publish_status(run_id, "awaiting_approval")
                await _publish_worklog(run_id, f"Paused awaiting approval {approval_id}")
                return True
            else:
                state.add_worklog(f"Tool {tool_name} failed: {msg}")
                state.status = "failed"
                repo_runs.update_run_status(run_id, "failed", ended_at=now_iso())
                await _publish_status(run_id, "failed")
                return True
    return False


async def resume_run_after_approval(approval_id: str, decision: str) -> Optional[RunState]:
    pending_call = pending.pop_pending(approval_id)
    if not pending_call:
        return None
    state, tool_name, args, step_idx = pending_call
    run_id = state.run_id
    await _publish_worklog(run_id, f"Approval {approval_id} resolved: {decision}")

    if decision != "approved":
        state.status = "failed"
        repo_runs.update_run_status(run_id, "failed", ended_at=now_iso())
        await _publish_status(run_id, "failed")
        return state

    repo_runs.update_run_status(run_id, "running")
    await _publish_status(run_id, "running")
    receipt_id = f"r_{now_iso()}"
    result = await run_tool(tool_name, args, {"run_id": run_id, "approval_id": approval_id, "receipt_id": receipt_id})
    state.receipts.append(receipt_id)
    await _publish_worklog(run_id, f"Tool {tool_name} ok after approval")
    if tool_name == "todo.add":
        state.output = f"Recorded todo: {result.result.get('todo', {}).get('text', '')}"
    elif tool_name == "web.fetch":
        state.output = result.result.get("text", "")[:200]
    elif tool_name == "filesystem.read":
        state.output = result.result.get("content", "")[:200]

    state.current_step = step_idx + 1
    paused = await _execute_plan(state)
    if paused:
        return state

    verify(state)
    finalize(state)
    state.status = "completed"
    repo_runs.update_run_status(run_id, "completed", ended_at=now_iso())
    await _publish_status(run_id, "completed")
    return state


async def _publish_worklog(run_id: str, msg: str) -> None:
    await event_bus.publish({"type": "worklog", "run_id": run_id, "msg": msg, "ts": now_iso()})


async def _publish_status(run_id: str, status: str) -> None:
    await event_bus.publish({"type": "status", "run_id": run_id, "status": status, "ts": now_iso()})
