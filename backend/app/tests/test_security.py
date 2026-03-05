import json
import shutil
from pathlib import Path

import pytest

from app.tools.runner import run_tool
from app.tools.base import ToolError
from app.db import repo_approvals, repo_fs_allowlist, repo_receipts, repo_runs
from app.core.time import now_iso
from app.api import approvals as approvals_api


@pytest.mark.anyio("asyncio")
async def test_filesystem_allowlist_after_approval(temp_settings):
    base = Path.cwd() / "tmp_fs"
    base.mkdir(exist_ok=True)
    file_path = base / "note.txt"
    file_path.write_text("secure content", encoding="utf-8")

    run_id = "run_fs"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)

    with pytest.raises(ToolError) as exc:
        await run_tool("filesystem.read", {"path": str(file_path)}, {"run_id": run_id})

    approval_id = str(exc.value).split("approval_id=")[1]
    repo_approvals.resolve_approval(approval_id, {"action": "approved"}, "approved", settings=temp_settings)

    await run_tool("filesystem.read", {"path": str(file_path)}, {"run_id": run_id, "approval_id": approval_id})
    assert repo_fs_allowlist.is_allowed(run_id, str(file_path), settings=temp_settings)

    receipts = repo_receipts.list_receipts_for_run(run_id, settings=temp_settings)
    assert len(receipts) == 1

    shutil.rmtree(base, ignore_errors=True)


@pytest.mark.anyio("asyncio")
async def test_web_fetch_blocks_private_hosts(temp_settings):
    run_id = "run_ssrf"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)
    with pytest.raises(PermissionError):
        await run_tool("web.fetch", {"url": "http://127.0.0.1"}, {"run_id": run_id, "approval_id": "appr_test"})


@pytest.mark.anyio("asyncio")
async def test_artifact_created_for_large_output(temp_settings):
    run_id = "run_artifact"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)
    long_cmd = "python -c \"print('a'*3005)\""
    await run_tool("terminal.run", {"cmd": long_cmd}, {"run_id": run_id, "approval_id": "appr_art"})

    receipts = repo_receipts.list_receipts_for_run(run_id, settings=temp_settings)
    assert receipts, "receipt should be stored"
    result = json.loads(receipts[0]["result"])
    artifacts = result.get("artifacts") or []
    assert artifacts, "artifact path recorded"
    artifact_path = Path(artifacts[0])
    assert artifact_path.exists()
    with artifact_path.open("r", encoding="utf-8") as f:
        content = f.read()
    assert "a" * 100 in content


@pytest.mark.anyio("asyncio")
async def test_filesystem_read_directory_returns_listing(temp_settings):
    base = Path.cwd() / "tmp_dir_list"
    base.mkdir(exist_ok=True)
    (base / "file.txt").write_text("hello", encoding="utf-8")

    run_id = "run_fs_dir"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)
    approval_id = "appr_dir"
    await run_tool("filesystem.read", {"path": str(base)}, {"run_id": run_id, "approval_id": approval_id})

    receipts = repo_receipts.list_receipts_for_run(run_id, settings=temp_settings)
    assert receipts
    result = json.loads(receipts[0]["result"])
    assert result.get("is_dir") is True
    assert "file.txt" in result.get("entries", [])
    shutil.rmtree(base, ignore_errors=True)


@pytest.mark.anyio("asyncio")
async def test_resolve_approval_parses_string_request(temp_settings):
    run_id = "run_appr_string"
    repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()}, settings=temp_settings)
    approval_id = "appr_string"
    request_payload = {"summary": "Execute tool filesystem.read", "details": {"path": "."}, "risk": "high"}
    repo_approvals.create_approval(
        {
            "approval_id": approval_id,
            "run_id": run_id,
            "type": "filesystem.read",
            "status": "pending",
            "request": request_payload,
            "decision": None,
            "created_at": now_iso(),
            "resolved_at": None,
        },
        settings=temp_settings,
    )

    await approvals_api.resolve_approval(approval_id, {"action": "approved"})

    stored = repo_approvals.get_approval(approval_id, settings=temp_settings)
    assert stored["status"] == "approved"
    assert repo_fs_allowlist.is_allowed(run_id, ".", settings=temp_settings) is True
