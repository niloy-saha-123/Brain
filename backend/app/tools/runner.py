"""Tool runner that handles approvals and receipts."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from app.tools.registry import registry
from app.tools.policy import requires_approval
from app.tools.base import ToolResult, ToolError
from app.db import repo_receipts, repo_runs, repo_approvals
from app.core.time import now_iso
from app.events.bus import event_bus


async def run_tool(tool_name: str, args: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
    tool = registry.get(tool_name)
    args_obj = tool.args_model(**args)

    if requires_approval(tool_name, args):
        existing_approval = context.get("approval_id")
        if not existing_approval:
            approval_id = await _create_approval(tool_name, args_obj, context)
            raise ToolError(f"Approval required before executing tool. approval_id={approval_id}")

    result = await tool.execute(args_obj, context)
    receipt_id = context.get("receipt_id", f"r_{now_iso()}")
    await _store_receipt(receipt_id, tool_name, result, context)
    await event_bus.publish({"type": "receipt", "run_id": context.get("run_id"), "receipt_id": receipt_id})
    return result


async def _store_receipt(receipt_id: str, tool_name: str, result: ToolResult, context: Dict[str, Any]) -> None:
    run_id = context.get("run_id", "unknown")
    # Ensure run exists to satisfy FK; create stub if missing.
    existing = repo_runs.get_run(run_id)
    if not existing:
        repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()})
    payload = {
        "receipt_id": receipt_id,
        "run_id": run_id,
        "tool": tool_name,
        "ok": result.ok,
        "ts": now_iso(),
        "request": result.request,
        "result": result.result,
        "diff": result.diff,
    }
    # Using sync repo via thread to avoid blocking loop
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, repo_receipts.create_receipt, payload)


async def _create_approval(tool_name: str, args_obj: Any, context: Dict[str, Any]) -> str:
    run_id = context.get("run_id", "unknown")
    approval_id = context.get("approval_id", f"appr_{now_iso()}")
    payload = {
        "approval_id": approval_id,
        "run_id": run_id,
        "type": tool_name,
        "status": "pending",
        "request": {
            "summary": f"Execute tool {tool_name}",
            "details": args_obj.dict(),
            "risk": "high",
        },
        "decision": None,
        "created_at": now_iso(),
        "resolved_at": None,
    }
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, repo_approvals.create_approval, payload)
    await event_bus.publish({"type": "approval_requested", "approval_id": approval_id, "run_id": run_id})
    return approval_id
