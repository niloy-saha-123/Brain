"""In-memory store wrapper (placeholder)."""
from __future__ import annotations

from typing import Any, Dict, List

from app.db import repo_memory


class MemoryStore:
    def save_fact(self, fact: Dict[str, Any]) -> None:
        repo_memory.upsert_fact(fact)

    def list_facts(self, limit: int = 20) -> List[Dict[str, Any]]:
        return repo_memory.list_facts(limit=limit)


store = MemoryStore()
