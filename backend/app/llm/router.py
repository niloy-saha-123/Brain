"""Simple model registry/selector for local models."""
from __future__ import annotations

from app.core.config import Settings, get_settings


def get_model(kind: str = "general", settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    kind = kind.lower()
    if kind == "router":
        return settings.router_model
    if kind == "coder":
        return settings.coder_model or settings.general_model
    return settings.general_model
