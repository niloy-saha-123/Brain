"""Repository helpers for RAG chunks and allowlisted paths."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings


def allow_path(path: str, approval_id: str, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO rag_allowlist (path, approval_id, approved_at)
            VALUES (:path, :approval_id, :approved_at)
            ON CONFLICT(path) DO UPDATE SET
                approval_id = excluded.approval_id,
                approved_at = excluded.approved_at;
            """,
            {"path": path, "approval_id": approval_id, "approved_at": now_iso()},
        )


def is_allowed(path: str, settings: Settings | None = None) -> bool:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT 1 FROM rag_allowlist WHERE path = ?", (path,)).fetchone()
        return row is not None


def list_allowlist(settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute("SELECT * FROM rag_allowlist ORDER BY approved_at DESC").fetchall()
        return [row_to_dict(r) for r in rows if r]


def delete_chunks_for_path(path: str, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute("DELETE FROM rag_chunks WHERE path = ?", (path,))


def upsert_chunks(chunks: List[Dict[str, Any]], settings: Settings | None = None) -> None:
    if not chunks:
        return
    with get_connection(settings) as conn:
        conn.executemany(
            """
            INSERT INTO rag_chunks (
                chunk_id, path, chunk_index, content, embedding, hash, created_at
            ) VALUES (
                :chunk_id, :path, :chunk_index, :content, :embedding, :hash, :created_at
            )
            ON CONFLICT(chunk_id) DO UPDATE SET
                content = excluded.content,
                embedding = excluded.embedding,
                hash = excluded.hash,
                created_at = excluded.created_at;
            """,
            [
                {
                    "chunk_id": c["chunk_id"],
                    "path": c["path"],
                    "chunk_index": c["chunk_index"],
                    "content": c["content"],
                    "embedding": to_json(c.get("embedding")),
                    "hash": c.get("hash"),
                    "created_at": c.get("created_at", now_iso()),
                }
                for c in chunks
            ],
        )


def list_chunks(settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute("SELECT * FROM rag_chunks").fetchall()
        return [row_to_dict(r) for r in rows if r]
