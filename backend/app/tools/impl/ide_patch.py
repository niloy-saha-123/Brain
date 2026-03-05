"""IDE patch tool placeholder."""
from __future__ import annotations

from pydantic import Field

from app.tools.base import ToolArgs, ToolResult
from app.tools.policy import requires_approval


class IDEPatchArgs(ToolArgs):
    patch: str = Field(..., description="Unified diff patch content")


class IDEPatchTool:
    name = "ide.patch"
    risk_level = "high"
    args_model = IDEPatchArgs

    def requires_approval(self, args: IDEPatchArgs, context):
        return requires_approval(self.name, args.dict())

    async def execute(self, args: IDEPatchArgs, context):
        # Placeholder: store patch content; actual apply occurs elsewhere with approval.
        return ToolResult(ok=True, request={"patch": args.patch[:100]}, result={"stored": True})
