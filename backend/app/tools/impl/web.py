"""Web fetch tool (GET only)."""
from __future__ import annotations

from typing import Any, Dict
import ipaddress

import httpx
from pydantic import Field

from app.tools.base import ToolArgs, ToolResult
from app.tools.policy import requires_approval
from urllib.parse import urlparse


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
        _guard_url(args.url)
        async with httpx.AsyncClient(timeout=args.timeout) as client:
            resp = await client.get(args.url)
        text = resp.text
        truncated, was_truncated = _truncate(text)
        return ToolResult(
            ok=resp.status_code < 400,
            request={"url": args.url},
            result={
                "status_code": resp.status_code,
                "headers": dict(resp.headers),
                "text": truncated,
                "truncated": was_truncated,
            },
        )


def _guard_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http/https URLs are allowed")
    host = (parsed.hostname or "").lower()
    blocked_hosts = {"localhost", "127.0.0.1", "0.0.0.0"}
    if host in blocked_hosts or host.startswith("::1") or host.startswith("169.254."):
        raise PermissionError("Access to local/metadata addresses is blocked")
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
            raise PermissionError("Access to private addresses is blocked")
    except ValueError:
        # non-literal host; allow but still block obvious patterns
        if host.endswith(".local"):
            raise PermissionError("Access to local domains is blocked")


def _truncate(text: str, limit: int = 4000) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit], True
