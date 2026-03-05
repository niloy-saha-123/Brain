"""Execute stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def execute(state: RunState) -> RunState:
    state.add_worklog("Executed plan (stub, no tools).")
    return state
