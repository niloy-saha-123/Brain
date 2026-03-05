"""Context retrieval stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def load_context(state: RunState) -> RunState:
    state.add_worklog("Loaded context (stub).")
    return state
