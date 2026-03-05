"""Planning node: choose a simple plan of tool calls based on goal."""
from __future__ import annotations

from app.orchestrator.state import RunState
from app.schemas.planner import PlannerStep, PlannerDecision, PredictedApproval
from app.tools.policy import requires_approval


def plan(state: RunState) -> RunState:
    goal = state.task_spec.g.lower()
    steps: list[dict] = []
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

    planner_steps = []
    predicted = []
    for idx, step in enumerate(steps):
        step_id = f"step{idx+1}"
        planner_steps.append(
            PlannerStep(
                step_id=step_id,
                kind="tool",
                name=step["tool"],
                args=step.get("args", {}),
                description=f"Execute {step['tool']}",
            )
        )
        if requires_approval(step["tool"], step.get("args", {})):
            predicted.append(
                PredictedApproval(
                    step_id=step_id,
                    tool=step["tool"],
                    reason="policy requires approval",
                )
            )

    decision = PlannerDecision(selected_agent_id="default", steps=planner_steps, predicted_approvals=predicted)

    serialized_steps = []
    for step in planner_steps:
        step_dict = step.model_dump()
        step_dict["tool"] = step.name
        serialized_steps.append(step_dict)

    state.plan = serialized_steps
    state.planner_decision = decision.model_dump()
    state.add_worklog(f"Planned {len(steps)} step(s).")
    return state
