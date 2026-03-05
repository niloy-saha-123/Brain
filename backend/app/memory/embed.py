"""Lightweight local embedding (hash-based) to avoid external models."""
from __future__ import annotations

import math
from typing import List


def embed_text(text: str, dim: int = 64) -> List[float]:
    """
    Deterministic bag-of-words hashing to a fixed vector.
    Not semantic-quality, but sufficient for lightweight similarity.
    """
    vec = [0.0] * dim
    for tok in text.split():
        h = hash(tok) % dim
        vec[h] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec
