"""Repository helpers for memory_facts table."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings


def upsert_fact(fact: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "mem_id": fact["mem_id"],
        "key": fact.get("key", ""),
        "value": to_json(fact.get("value")),
        "source": fact.get("source"),
        "confidence": fact.get("confidence"),
        "tags": to_json(fact.get("tags")),
        "created_at": fact.get("created_at", now_iso()),
        "ttl": fact.get("ttl"),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO memory_facts (
                mem_id, key, value, source, confidence, tags, created_at, ttl
            )
            VALUES (
                :mem_id, :key, :value, :source, :confidence, :tags, :created_at, :ttl
            )
            ON CONFLICT(mem_id) DO UPDATE SET
                key=excluded.key,
                value=excluded.value,
                source=excluded.source,
                confidence=excluded.confidence,
                tags=excluded.tags,
                ttl=excluded.ttl;
            """,
            payload,
        )


def get_fact(mem_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM memory_facts WHERE mem_id = ?", (mem_id,)).fetchone()
        return row_to_dict(row)


def list_facts(limit: Optional[int] = None, settings: Settings | None = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM memory_facts ORDER BY created_at DESC"
    if limit:
        query += f" LIMIT {int(limit)}"
    with get_connection(settings) as conn:
        rows = conn.execute(query).fetchall()
        return [row_to_dict(row) for row in rows if row is not None]
