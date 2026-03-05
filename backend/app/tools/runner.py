"""Tool runner that handles approvals and receipts."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

from app.tools.registry import registry
from app.tools.policy import requires_approval
from app.tools.base import ToolResult, ToolError
from app.db import repo_receipts, repo_runs
from app.core.time import now_iso
from app.db.sqlite import to_json


async def run_tool(tool_name: str, args: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
    tool = registry.get(tool_name)
    args_obj = tool.args_model(**args)

    if requires_approval(tool_name, args):
        raise ToolError("Approval required before executing tool.")

    result = await tool.execute(args_obj, context)
    receipt_id = context.get("receipt_id", f"r_{now_iso()}")
    await _store_receipt(receipt_id, tool_name, result, context)
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
