"""Tool base classes and args schema helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, Type

from pydantic import BaseModel


class ToolError(Exception):
    """Raised when a tool execution fails."""


class ToolArgs(BaseModel):
    """Base args schema for tools."""

    class Config:
        extra = "forbid"


@dataclass
class ToolResult:
    ok: bool
    request: Dict[str, Any]
    result: Dict[str, Any]
    diff: Optional[Any] = None


class Tool(Protocol):
    name: str
    risk_level: str
    args_model: Type[ToolArgs]

    def requires_approval(self, args: ToolArgs, context: Dict[str, Any]) -> bool:
        ...

    async def execute(self, args: ToolArgs, context: Dict[str, Any]) -> ToolResult:
        ...
