"""Tool registry for lookup by name."""
from __future__ import annotations

from typing import Dict, List

from app.tools.base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def list(self) -> List[str]:
        return list(self._tools.keys())


registry = ToolRegistry()
