"""Finalize stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def finalize(state: RunState) -> RunState:
    state.add_worklog("Finalized response (stub).")
    return state
