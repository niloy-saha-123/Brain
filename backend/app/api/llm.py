"""Debug LLM endpoint for streaming from Ollama."""
from __future__ import annotations

from typing import Any, Dict, Optional, AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.llm.ollama import OllamaClient
from app.llm.base import LLMError

router = APIRouter()


class DebugLLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: Optional[str] = None
    stream: bool = True
    max_context: Optional[int] = Field(default=None, ge=128)
    options: Dict[str, Any] = Field(default_factory=dict)


@router.post("/debug/llm", summary="Stream raw output from Ollama")
async def debug_llm(req: DebugLLMRequest, settings: Settings = Depends(get_settings)) -> StreamingResponse:
    model = req.model or settings.general_model
    client = OllamaClient(settings)

    async def streamer() -> AsyncIterator[str]:
        try:
            async for chunk in client.generate(
                req.prompt,
                model=model,
                stream=req.stream,
                max_context=req.max_context,
                options=req.options or None,
            ):
                if chunk.text:
                    yield chunk.text
                if chunk.done and req.stream:
                    break
        except LLMError as exc:
            yield f"[error] {exc}"

    return StreamingResponse(streamer(), media_type="text/plain")
