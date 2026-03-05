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
    run_id: Optional[str] = Field(default=None, description="Optional run id to attribute usage/costs")
    use_cloud: bool = False
    approval_id: Optional[str] = Field(
        default=None, description="Required when use_cloud is true to satisfy approval gating."
    )


@router.post("/debug/llm", summary="Stream raw output from Ollama")
async def debug_llm(req: DebugLLMRequest, settings: Settings = Depends(get_settings)) -> StreamingResponse:
    model = req.model or settings.general_model
    client = OllamaClient(settings)
    collected_chunks: list[str] = []

    if req.use_cloud:
        if not settings.cloud_enabled:
            raise HTTPException(status_code=403, detail="Cloud calls are disabled by default")
        if not req.approval_id:
            raise HTTPException(status_code=403, detail="Approval required for cloud calls")

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
                    collected_chunks.append(chunk.text)
                    yield chunk.text
                if chunk.done and req.stream:
                    break
        except LLMError as exc:
            yield f"[error] {exc}"
        finally:
            if req.run_id:
                try:
                    from app.core.costs import record_model_usage

                    record_model_usage(
                        run_id=req.run_id,
                        model=model,
                        prompt_text=req.prompt,
                        completion_text="".join(collected_chunks),
                        is_cloud=req.use_cloud,
                        settings=settings,
                    )
                except Exception:
                    # Avoid breaking debug streaming due to accounting errors
                    pass

    return StreamingResponse(streamer(), media_type="text/plain")
