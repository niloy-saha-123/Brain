"""Web fetch tool (GET only)."""
from __future__ import annotations

from typing import Any, Dict

import httpx
from pydantic import Field

from app.tools.base import ToolArgs, ToolResult
from app.tools.policy import requires_approval


class WebFetchArgs(ToolArgs):
    url: str = Field(..., description="URL to fetch")
    timeout: float = Field(default=10.0, description="Timeout seconds")


class WebFetchTool:
    name = "web.fetch"
    risk_level = "high"
    args_model = WebFetchArgs

    def requires_approval(self, args: WebFetchArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: WebFetchArgs, context: Dict[str, Any]) -> ToolResult:
        async with httpx.AsyncClient(timeout=args.timeout) as client:
            resp = await client.get(args.url)
        return ToolResult(
            ok=resp.status_code < 400,
            request={"url": args.url},
            result={
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "text": resp.text,
            },
        )
