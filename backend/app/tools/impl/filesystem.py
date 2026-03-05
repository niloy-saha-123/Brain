"""Filesystem tools (read/write) — approval required upstream."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import Field

from app.tools.base import Tool, ToolArgs, ToolResult
from app.tools.policy import requires_approval
from app.db import repo_fs_allowlist
from app.core.config import get_settings


class FSReadArgs(ToolArgs):
    path: str = Field(..., description="Path to read")


class FSWriteArgs(ToolArgs):
    path: str = Field(..., description="Path to write")
    content: str = Field(..., description="Content to write")


class FilesystemReadTool:
    name = "filesystem.read"
    risk_level = "high"
    args_model = FSReadArgs

    def requires_approval(self, args: FSReadArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: FSReadArgs, context: Dict[str, Any]) -> ToolResult:
        path = _safe_path(args.path)
        _ensure_allowed(path, context)
        content = path.read_text(encoding="utf-8")
        truncated, was_truncated = _truncate(content)
        return ToolResult(
            ok=True,
            request={"path": str(path)},
            result={"content": truncated, "truncated": was_truncated},
        )


class FilesystemWriteTool:
    name = "filesystem.write"
    risk_level = "high"
    args_model = FSWriteArgs

    def requires_approval(self, args: FSWriteArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: FSWriteArgs, context: Dict[str, Any]) -> ToolResult:
        path = _safe_path(args.path)
        _ensure_allowed(path, context)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args.content, encoding="utf-8")
        return ToolResult(
            ok=True,
            request={"path": str(path)},
            result={"bytes_written": len(args.content)},
        )


def _safe_path(path_str: str) -> Path:
    base = Path.cwd().resolve()
    path = Path(path_str).expanduser().resolve()
    if not str(path).startswith(str(base)):
        raise PermissionError("Path outside workspace is not allowed")
    return path


def _ensure_allowed(path: Path, context: Dict[str, Any]) -> None:
    run_id = context.get("run_id")
    if not run_id:
        raise PermissionError("Filesystem access requires run_id")
    if repo_fs_allowlist.is_allowed(run_id, str(path)):
        return
    # For initial approval flows, allow if approval_id matches and will be persisted on resolve
    approval_id = context.get("approval_id")
    if approval_id:
        repo_fs_allowlist.allow_path(run_id, str(path), approval_id, settings=get_settings())
        return
    raise PermissionError("Path not approved for this run")


def _truncate(text: str, limit: int = 4000) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit], True
