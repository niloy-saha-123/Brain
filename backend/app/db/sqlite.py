"""SQLite helpers for the brain backend."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator

from app.core.config import Settings, get_settings


def _ensure_state_dir(state_dir: Path) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)


def get_db_path(settings: Settings | None = None) -> Path:
    settings = settings or get_settings()
    state_dir = Path(settings.state_dir).expanduser().resolve()
    _ensure_state_dir(state_dir)
    return state_dir / settings.db_file


def connect(settings: Settings | None = None) -> sqlite3.Connection:
    db_path = get_db_path(settings)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_connection(settings: Settings | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(settings)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def row_to_dict(row: sqlite3.Row | None) -> Dict[str, Any] | None:
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> Iterable[Dict[str, Any]]:
    for row in rows:
        yield row_to_dict(row)  # type: ignore[arg-type]


def to_json(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value)


def from_json(value: str | None) -> Any:
    if value is None:
        return None
    return json.loads(value)
