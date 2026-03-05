import pytest

from app.orchestrator.graph import start_run
from app.schemas import TaskSpec
from app.db import repo_runs, repo_approvals
from app.orchestrator.graph import _execute_plan, resume_run_after_approval
from app.orchestrator.state import RunState


@pytest.mark.anyio("asyncio")
async def test_start_run_persists_completion(temp_settings):
    spec = TaskSpec(id="run_orch_test", g="goal", v=1)
    await start_run(spec)

    stored = repo_runs.get_run(spec.id, settings=temp_settings)
    assert stored is not None
    assert stored["status"] == "completed"


@pytest.mark.anyio("asyncio")
async def test_start_run_pauses_on_sensitive_tool(temp_settings):
    spec = TaskSpec(id="run_orch_pause", g="terminal", v=1)
    state = await start_run(spec)

    assert state.status == "awaiting_approval"
    stored = repo_runs.get_run(spec.id, settings=temp_settings)
    assert stored["status"] == "awaiting_approval"
    approvals = repo_approvals.list_pending(settings=temp_settings)
    assert len(approvals) == 1


@pytest.mark.anyio("asyncio")
async def test_resume_run_processes_remaining_plan(temp_settings):
    run_id = "run_orch_resume"
    repo_runs.create_run({"run_id": run_id, "status": "running"}, settings=temp_settings)
    state = RunState(
        run_id=run_id,
        task_spec=TaskSpec(id=run_id, g="terminal then todo", v=1),
        plan=[
            {"tool": "terminal.run", "args": {"cmd": "echo hi"}},
            {"tool": "todo.add", "args": {"text": "write report"}},
        ],
    )

    paused = await _execute_plan(state)
    assert paused is True
    approvals = repo_approvals.list_pending(settings=temp_settings)
    assert len(approvals) == 1
    approval_id = approvals[0]["approval_id"]
    repo_approvals.resolve_approval(approval_id, {"action": "approved"}, "approved", settings=temp_settings)

    resumed_state = await resume_run_after_approval(approval_id, "approved")
    assert resumed_state is not None
    assert resumed_state.status == "completed"
    assert resumed_state.current_step == len(state.plan)
    stored = repo_runs.get_run(run_id, settings=temp_settings)
    assert stored["status"] == "completed"
    assert len(resumed_state.receipts) == 2
