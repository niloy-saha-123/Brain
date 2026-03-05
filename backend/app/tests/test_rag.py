import shutil
from pathlib import Path

import pytest

from app.tools.runner import run_tool
from app.tools.base import ToolError
from app.db import repo_approvals, repo_rag, repo_runs
from app.memory import rag
from app.core.time import now_iso


@pytest.mark.anyio("asyncio")
async def test_rag_index_requires_approval_and_indexes(temp_settings):
    data_dir = Path.cwd() / "tmp_rag"
    data_dir.mkdir(exist_ok=True)
    file_path = data_dir / "note.txt"
    file_path.write_text("hello world\nthis is a test document\nhello world again", encoding="utf-8")

    run_id = "run_rag"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)

    with pytest.raises(ToolError) as exc:
        await run_tool("rag.index", {"path": str(data_dir)}, {"run_id": run_id})

    msg = str(exc.value)
    approval_id = msg.split("approval_id=")[1]
    approval = repo_approvals.get_approval(approval_id, settings=temp_settings)
    assert approval is not None
    assert approval["type"] == "rag.index"
    assert approval["status"] == "pending"

    repo_approvals.resolve_approval(approval_id, {"action": "approved"}, "approved", settings=temp_settings)
    await run_tool("rag.index", {"path": str(data_dir)}, {"run_id": run_id, "approval_id": approval_id})

    chunks = repo_rag.list_chunks(settings=temp_settings)
    assert any(c["path"].endswith("note.txt") for c in chunks)
    hits = rag.retrieve("hello world", k=2)
    assert len(hits) >= 1

    shutil.rmtree(data_dir, ignore_errors=True)
