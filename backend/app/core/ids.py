"""ID helpers."""
from __future__ import annotations

from datetime import datetime, timezone


def make_run_id(prefix: str = "run") -> str:
    ts = datetime.now(timezone.utc).isoformat()
    return f"{prefix}_{ts}"


def make_agent_id(prefix: str = "agent") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}_{ts}"
