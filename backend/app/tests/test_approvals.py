import pytest

from app.tools.runner import run_tool
from app.tools.base import ToolError
from app.db import repo_approvals, repo_runs
from app.core.time import now_iso


@pytest.mark.anyio("asyncio")
async def test_sensitive_tool_triggers_approval(temp_settings):
    run_id = "run_approval"
    # Ensure run exists to satisfy FK
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)

    with pytest.raises(ToolError) as exc:
        await run_tool("terminal.run", {"cmd": "echo hi"}, {"run_id": run_id})

    msg = str(exc.value)
    assert "Approval required" in msg
    assert "approval_id=" in msg
    approval_id = msg.split("approval_id=")[1]

    approval = repo_approvals.get_approval(approval_id, settings=temp_settings)
    assert approval is not None
    assert approval["status"] == "pending"
    assert approval["type"] == "terminal.run"
