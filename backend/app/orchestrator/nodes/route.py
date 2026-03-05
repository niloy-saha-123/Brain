"""Routing stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def route(state: RunState) -> RunState:
    state.add_worklog("Routed to default agent.")
    return state
