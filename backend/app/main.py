"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.core.config import get_settings, setup_logging
from app.db.migrate import ensure_db_ready


API_VERSION = "0.1.0"


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings)
    ensure_db_ready(settings)

    app = FastAPI(title=settings.app_name, version=API_VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)

    return app


app = create_app()
