"""Planning node: choose a simple plan of tool calls based on goal."""
from __future__ import annotations

from app.orchestrator.state import RunState


def plan(state: RunState) -> RunState:
    goal = state.task_spec.g.lower()
    steps = []
    # naive rule-based selection
    if "todo" in goal or "task" in goal:
        steps.append({"tool": "todo.add", "args": {"text": state.task_spec.g}})
    if "terminal" in goal or "shell" in goal:
        steps.append({"tool": "terminal.run", "args": {"cmd": "echo hi"}})
    if "list files" in goal or "ls " in goal:
        steps.append({"tool": "filesystem.read", "args": {"path": "."}})
    if "fetch" in goal or "http" in goal:
        steps.append({"tool": "web.fetch", "args": {"url": "https://example.com"}})
    if not steps:
        steps.append({"tool": "todo.add", "args": {"text": state.task_spec.g}})
    state.plan = steps
    state.add_worklog(f"Planned {len(steps)} step(s).")
    return state
