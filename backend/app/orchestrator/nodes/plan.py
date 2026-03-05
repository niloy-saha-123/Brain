"""Planning stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def plan(state: RunState) -> RunState:
    state.add_worklog("Planned execution (stub).")
    return state
