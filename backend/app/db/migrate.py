"""Simple migration runner for SQLite using the schema.sql file."""
from __future__ import annotations

from pathlib import Path

from app.core.config import Settings, get_settings
from app.db.sqlite import connect

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def apply_migrations(settings: Settings | None = None) -> None:
    """Create tables if they do not exist."""
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect(settings) as conn:
        conn.executescript(schema_sql)
        conn.commit()


def ensure_db_ready(settings: Settings | None = None) -> None:
    """Alias for clarity at startup."""
    apply_migrations(settings or get_settings())
