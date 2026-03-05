"""Optional LanceDB storage for RAG embeddings."""
from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from app.core.time import now_iso

try:  # optional dependency
    import lancedb  # type: ignore
except ImportError:  # pragma: no cover - optional path
    lancedb = None


def available() -> bool:
    return lancedb is not None


def get_table(db_path: Path, table_name: str = "rag_chunks"):
    if not available():
        raise ImportError("lancedb not installed")
    db_path.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(db_path))
    if table_name not in db.table_names():
        return db.create_table(
            table_name,
            data=[
                {"chunk_id": "init", "path": "init", "content": "init", "embedding": [0.0], "created_at": now_iso()},
            ],
            mode="overwrite",
        )
    return db.open_table(table_name)


def upsert(db_path: Path, rows: List[Dict[str, Any]]) -> None:
    if not available():
        return
    table = get_table(db_path)
    table.merge_insert(
        predicate="chunk_id == chunk_id",
        source=rows,
        on="chunk_id",
    )


def search(db_path: Path, embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
    if not available():
        return []
    table = get_table(db_path)
    results = table.search(embedding).limit(k).to_list()
    return results
