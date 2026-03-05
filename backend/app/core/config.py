"""Configuration loader for the backend.

Defaults are safe for local development. Environment variables are optional and
can override the defaults when present.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List

DEFAULT_CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]


@dataclass
class Settings:
    app_name: str = "brain"
    environment: str = "dev"
    ollama_base_url: str = "http://localhost:11434"
    cors_origins: List[str] = field(default_factory=lambda: DEFAULT_CORS_ORIGINS.copy())
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls()
        settings.app_name = os.getenv("BRAIN_APP_NAME", settings.app_name)
        settings.environment = os.getenv("BRAIN_ENVIRONMENT", settings.environment)
        ollama_url_override = os.getenv("BRAIN_OLLAMA_BASE_URL")
        if ollama_url_override:
            settings.ollama_base_url = ollama_url_override.rstrip("/")
        cors_raw = os.getenv("BRAIN_CORS_ORIGINS")
        if cors_raw:
            settings.cors_origins = [origin.strip() for origin in cors_raw.split(",") if origin.strip()]
        settings.log_level = os.getenv("BRAIN_LOG_LEVEL", settings.log_level).upper()
        return settings

    def ollama_health_url(self) -> str:
        return f"{self.ollama_base_url}/api/tags"


def setup_logging(settings: Settings) -> None:
    level = getattr(logging, settings.log_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()
