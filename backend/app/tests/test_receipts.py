import pytest

from app.tools.runner import run_tool
from app.db import repo_receipts


@pytest.mark.anyio("asyncio")
async def test_run_tool_records_receipt(temp_settings):
    run_id = "run_receipts"
    result = await run_tool("todo.add", {"text": "test"}, {"run_id": run_id})
    assert result.ok

    receipts = repo_receipts.list_receipts_for_run(run_id, settings=temp_settings)
    assert len(receipts) == 1
    rec = receipts[0]
    assert rec["tool"] == "todo.add"
    assert rec["ok"] == 1
