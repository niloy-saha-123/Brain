"""RAG indexing tool (approval required)."""
from __future__ import annotations

from typing import Any, Dict

from pydantic import Field

from app.memory import rag
from app.tools.base import Tool, ToolArgs, ToolResult
from app.tools.policy import requires_approval


class RagIndexArgs(ToolArgs):
    path: str = Field(..., description="Folder or file path to index")


class RagIndexTool:
    name = "rag.index"
    risk_level = "high"
    args_model = RagIndexArgs

    def requires_approval(self, args: RagIndexArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: RagIndexArgs, context: Dict[str, Any]) -> ToolResult:
        approval_id = context.get("approval_id")
        result = rag.index_path(args.path, approval_id=approval_id)
        return ToolResult(
            ok=True,
            request={"path": args.path},
            result={"chunks_indexed": result["chunks"], "files": result["files"]},
        )
