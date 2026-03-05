"""Filesystem tools (read/write) — approval required upstream."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import Field

from app.tools.base import Tool, ToolArgs, ToolResult
from app.tools.policy import requires_approval


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


def _truncate(text: str, limit: int = 4000) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit], True
