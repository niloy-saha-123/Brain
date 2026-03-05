"""RAG indexing and retrieval helpers."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

from app.memory.chunk import chunk_text
from app.memory.embed import embed_text
from app.memory.dedup import dedup
from app.memory import lancedb_store
from app.db import repo_rag
from app.tools.impl.filesystem import _safe_path
from app.core.time import now_iso


def _file_hash(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def index_path(path_str: str, approval_id: str | None = None) -> Dict[str, int]:
    """
    Index a folder or single file after approval. Returns chunk counts.
    """
    path = _safe_path(path_str)
    if path.is_dir():
        files = [p for p in path.rglob("*") if p.is_file()]
    else:
        files = [path]

    if approval_id:
        repo_rag.allow_path(str(path), approval_id)

    total_chunks = 0
    for file_path in files:
        if not _is_text_file(file_path):
            continue
        total_chunks += _index_file(file_path)

    return {"files": len(files), "chunks": total_chunks}


def _is_text_file(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8")
        return True
    except UnicodeDecodeError:
        return False


def _index_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    chunks = chunk_text(text)
    base_hash = _file_hash(path)
    rows = []
    for idx, chunk in enumerate(chunks):
        chunk_id = f"{path}#chunk{idx}"
        embedding = embed_text(chunk)
        rows.append(
            {
                "chunk_id": chunk_id,
                "path": str(path),
                "chunk_index": idx,
                "content": chunk,
                "embedding": embedding,
                "hash": base_hash,
                "created_at": now_iso(),
            }
        )
    repo_rag.delete_chunks_for_path(str(path))
    repo_rag.upsert_chunks(rows)
    # Optional LanceDB store
    try:
        lancedb_store.upsert(Path("state/lancedb"), rows)
    except Exception:
        pass
    return len(rows)


def retrieve(query: str, k: int = 3) -> List[Dict]:
    """Retrieve top-k chunks using cosine similarity."""
    if not query:
        return []
    q_emb = embed_text(query)
    chunks = repo_rag.list_chunks()
    scored = []
    for chunk in chunks:
        emb = chunk.get("embedding") or []
        if isinstance(emb, str):
            # stored as JSON string via row_to_dict
            import json

            emb = json.loads(emb)
        score = _cosine(q_emb, emb)
        scored.append(
            {
                "chunk_id": chunk["chunk_id"],
                "path": chunk["path"],
                "content": chunk["content"],
                "score": score,
                "citation": f"{chunk['path']}#{chunk['chunk_index']}",
            }
        )
    scored.sort(key=lambda x: x["score"], reverse=True)
    return dedup(scored[:k])


def _cosine(a: List[float], b: List[float]) -> float:
    if not a or not b:
        return 0.0
    length = min(len(a), len(b))
    num = sum(a[i] * b[i] for i in range(length))
    denom_a = sum(x * x for x in a) ** 0.5
    denom_b = sum(x * x for x in b) ** 0.5
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return num / (denom_a * denom_b)
