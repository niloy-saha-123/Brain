import pytest

from app.orchestrator.graph import start_run
from app.schemas import TaskSpec
from app.db import repo_runs


@pytest.mark.anyio("asyncio")
async def test_start_run_persists_completion(temp_settings):
    spec = TaskSpec(id="run_orch_test", g="goal", v=1)
    await start_run(spec)

    stored = repo_runs.get_run(spec.id, settings=temp_settings)
    assert stored is not None
    assert stored["status"] == "completed"
