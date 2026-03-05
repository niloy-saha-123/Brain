"""LLM client interfaces and shared types."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Dict, Optional, Protocol


class LLMError(Exception):
    """Raised when an LLM call fails."""


@dataclass
class LLMResponseChunk:
    text: str
    done: bool = False
    model: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


class LLMClient(Protocol):
    async def generate(
        self,
        prompt: str,
        *,
        model: str,
        stream: bool = True,
        max_context: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[LLMResponseChunk]:
        ...
