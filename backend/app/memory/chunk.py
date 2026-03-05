"""Simple text chunker for RAG."""
from __future__ import annotations

from typing import List


def chunk_text(text: str, max_chars: int = 800, overlap: int = 80) -> List[str]:
    """
    Split text into overlapping chunks sized for lightweight retrieval.
    """
    if not text:
        return []
    chunks: List[str] = []
    buffer: List[str] = []
    length = 0
    for line in text.splitlines():
        if length + len(line) + 1 > max_chars and buffer:
            chunk = "\n".join(buffer).strip()
            if chunk:
                chunks.append(chunk)
            # keep overlap from end of buffer
            overlap_text = chunk[-overlap:] if overlap else ""
            buffer = [overlap_text] if overlap_text else []
            length = len(overlap_text)
        buffer.append(line)
        length += len(line) + 1
    if buffer:
        chunk = "\n".join(buffer).strip()
        if chunk:
            chunks.append(chunk)
    return chunks
