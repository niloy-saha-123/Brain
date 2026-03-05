import pytest

from app.orchestrator.graph import start_run
from app.schemas import TaskSpec
from app.db import repo_planner_traces, repo_runs
from app.api import runs as runs_api
from app.core.time import now_iso


@pytest.mark.anyio("asyncio")
async def test_plan_trace_persisted(temp_settings):
    run_id = "run_plan_trace"
    spec = TaskSpec(id=run_id, g="list files", v=1)
    await start_run(spec)

    trace = repo_planner_traces.get_trace(run_id, settings=temp_settings)
    assert trace is not None
    trace_data = trace.get("trace")
    assert trace_data is not None


def test_plan_endpoint_returns_trace(temp_settings):
    run_id = "run_plan_endpoint"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)
    repo_planner_traces.upsert_trace(
        {"run_id": run_id, "trace": {"steps": [{"step_id": "step1", "name": "todo.add"}]}, "created_at": now_iso()},
        settings=temp_settings,
    )

    result = runs_api.get_run_plan(run_id)
    assert result["run_id"] == run_id
    assert result["trace"]["steps"]
