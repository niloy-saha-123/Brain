"""Facts memory helpers."""
from __future__ import annotations

from typing import Any, Dict, List

from app.memory.store import store
from app.core.time import now_iso


def save_fact(key: str, value: Any, tags: List[str] | None = None, source: str | None = None) -> Dict[str, Any]:
    fact = {
        "mem_id": f"mem_{now_iso()}",
        "key": key,
        "value": value,
        "source": source,
        "confidence": 1.0,
        "tags": tags or [],
        "created_at": now_iso(),
    }
    store.save_fact(fact)
    return fact


def list_facts(limit: int = 20) -> List[Dict[str, Any]]:
    return store.list_facts(limit)
