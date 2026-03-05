"""Rewrite stub to produce TaskSpec."""
from __future__ import annotations

from app.schemas import TaskSpec, TaskPolicies, TaskContextRefs, TaskBudget
from app.orchestrator.state import RunState


def rewrite(state: RunState) -> RunState:
    # Already have TaskSpec; stub adds worklog.
    state.add_worklog("Rewrote input into task spec.")
    return state
