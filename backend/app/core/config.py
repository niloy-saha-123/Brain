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
    state_dir: str = "state"
    db_file: str = "brain.db"
    router_model: str = "llama3.2:3b"
    general_model: str = "llama3.2:3b"
    coder_model: str = "deepseek-coder:6.7b"
    ollama_timeout: float = 30.0
    ollama_context_window: int = 4096
    cloud_enabled: bool = False
    cloud_budget_cap: float = 5.0
    cloud_cost_per_1k_tokens: float = 0.0

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
        settings.state_dir = os.getenv("BRAIN_STATE_DIR", settings.state_dir)
        settings.db_file = os.getenv("BRAIN_DB_FILE", settings.db_file)
        settings.router_model = os.getenv("BRAIN_ROUTER_MODEL", settings.router_model)
        settings.general_model = os.getenv("BRAIN_GENERAL_MODEL", settings.general_model)
        settings.coder_model = os.getenv("BRAIN_CODER_MODEL", settings.coder_model)
        settings.ollama_timeout = float(os.getenv("BRAIN_OLLAMA_TIMEOUT", settings.ollama_timeout))
        settings.ollama_context_window = int(
            os.getenv("BRAIN_OLLAMA_CTX", settings.ollama_context_window)
        )
        settings.cloud_enabled = os.getenv("BRAIN_CLOUD_ENABLED", str(settings.cloud_enabled)).lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        settings.cloud_budget_cap = float(os.getenv("BRAIN_CLOUD_BUDGET_USD", settings.cloud_budget_cap))
        settings.cloud_cost_per_1k_tokens = float(
            os.getenv("BRAIN_CLOUD_COST_PER_1K", settings.cloud_cost_per_1k_tokens)
        )
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
