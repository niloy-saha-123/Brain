"""Memory + RAG endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.memory import facts, rag
from app.core.ids import make_run_id
from app.tools.runner import run_tool
from app.tools.base import ToolError
from app.db import repo_runs, repo_rag
from app.core.time import now_iso

router = APIRouter()


class FactCreate(BaseModel):
    key: str
    value: str
    tags: list[str] = []
    source: str | None = None


@router.get("/memory/facts")
def list_facts(limit: int = 20):
    return facts.list_facts(limit=limit)


@router.post("/memory/facts")
def create_fact(body: FactCreate):
    return facts.save_fact(body.key, body.value, tags=body.tags, source=body.source)


class RagIndexRequest(BaseModel):
    path: str = Field(..., description="Folder or file path to index")
    run_id: str | None = None


@router.post("/rag/index")
async def rag_index(req: RagIndexRequest):
    run_id = req.run_id or make_run_id("rag")
    if not repo_runs.get_run(run_id):
        repo_runs.create_run({"run_id": run_id, "status": "running", "created_at": now_iso()})
    try:
        result = await run_tool("rag.index", {"path": req.path}, {"run_id": run_id})
        repo_runs.update_run_status(run_id, "completed", ended_at=now_iso())
        return {"status": "indexed", "run_id": run_id, **result.result}
    except ToolError as exc:
        msg = str(exc)
        if "approval_id=" in msg:
            approval_id = msg.split("approval_id=")[1]
            repo_runs.update_run_status(run_id, "awaiting_approval")
            return {"status": "pending", "run_id": run_id, "approval_id": approval_id}
        raise HTTPException(status_code=400, detail=msg)


@router.get("/rag/search")
def rag_search(query: str, k: int = 3):
    hits = rag.retrieve(query, k=k)
    return {"query": query, "hits": hits}


@router.get("/rag/allowlist")
def rag_allowlist():
    return repo_rag.list_allowlist()
