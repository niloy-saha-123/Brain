"""Simple deduplication helpers."""
from __future__ import annotations

from typing import List, Dict


def dedup(items: List[Dict], key: str = "citation") -> List[Dict]:
    seen = set()
    out = []
    for item in items:
        k = item.get(key)
        if k in seen:
            continue
        seen.add(k)
        out.append(item)
    return out
