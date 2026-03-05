"""Health endpoints for the backend and Ollama service."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

import httpx
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.core.config import Settings, get_settings

router = APIRouter()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/health", summary="Backend health check")
async def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "brain-backend",
        "ts": _now_iso(),
    }


@router.get("/health/ollama", summary="Check connectivity to local Ollama")
async def health_ollama(settings: Settings = Depends(get_settings)) -> JSONResponse | Dict[str, Any]:
    url = settings.ollama_health_url()
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url)
    except httpx.RequestError as exc:  # covers connection errors and timeouts
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unreachable",
                "service": "ollama",
                "endpoint": url,
                "detail": str(exc),
                "ts": _now_iso(),
            },
        )

    models_count = 0
    detail: Any | None = None
    try:
        payload = response.json()
        models_count = len(payload.get("models", [])) if isinstance(payload, dict) else 0
        detail = payload
    except ValueError:
        detail = response.text

    if response.is_success:
        return {
            "status": "ok",
            "service": "ollama",
            "endpoint": url,
            "ts": _now_iso(),
            "models": models_count,
        }

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "error",
            "service": "ollama",
            "endpoint": url,
            "detail": detail,
            "ts": _now_iso(),
        },
    )
