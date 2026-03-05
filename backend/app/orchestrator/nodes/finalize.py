"""Finalize stub."""
from __future__ import annotations

from app.orchestrator.state import RunState


def finalize(state: RunState) -> RunState:
    if state.context_rag:
        citations = ", ".join(hit["citation"] for hit in state.context_rag)
        if state.output:
            state.output += f"\nCitations: {citations}"
    state.add_worklog("Finalized response with citations.")
    return state
