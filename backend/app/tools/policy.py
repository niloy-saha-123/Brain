"""Tool approval policy engine (v0.1 conservative)."""
from __future__ import annotations

from typing import Dict, Any

SENSITIVE_TOOLS = {
    "filesystem.read",
    "filesystem.write",
    "terminal.run",
    "git.status",
    "git.diff",
    "git.commit",
    "web.fetch",
    "ide.patch",
}


def requires_approval(tool_name: str, args: Dict[str, Any]) -> bool:
    # v0.1: all sensitive tools require approval; todo tool is allowed.
    if tool_name in SENSITIVE_TOOLS:
        return True
    return False
