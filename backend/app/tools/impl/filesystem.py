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
        path = Path(args.path).expanduser()
        content = path.read_text(encoding="utf-8")
        return ToolResult(
            ok=True,
            request={"path": str(path)},
            result={"content": content},
        )


class FilesystemWriteTool:
    name = "filesystem.write"
    risk_level = "high"
    args_model = FSWriteArgs

    def requires_approval(self, args: FSWriteArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: FSWriteArgs, context: Dict[str, Any]) -> ToolResult:
        path = Path(args.path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args.content, encoding="utf-8")
        return ToolResult(
            ok=True,
            request={"path": str(path)},
            result={"bytes_written": len(args.content)},
        )
