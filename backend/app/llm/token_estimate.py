"""Lightweight token estimation helpers (rough)."""
from __future__ import annotations


def estimate_tokens(text: str) -> int:
    # Rough heuristic: ~4 chars per token
    if not text:
        return 0
    return max(1, len(text) // 4)


def pick_context_window(total_available: int, prompt: str, desired_output_tokens: int = 512) -> int:
    prompt_tokens = estimate_tokens(prompt)
    return min(total_available, prompt_tokens + desired_output_tokens)
