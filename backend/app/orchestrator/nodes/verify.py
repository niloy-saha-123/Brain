"""Verify stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def verify(state: RunState) -> RunState:
    state.add_worklog("Verified outputs (stub).")
    return state
