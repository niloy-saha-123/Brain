"""Verify stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def verify(state: RunState) -> RunState:
    if state.context_rag and (not state.output or "Citations:" not in state.output):
        state.add_worklog("Verification: missing citations, adding placeholder.")
        citations = ", ".join(hit["citation"] for hit in state.context_rag)
        existing = state.output or ""
        state.output = f"{existing}\nCitations: {citations}".strip()
    state.add_worklog("Verified outputs.")
    return state
