import os
import pytest

from app.core.config import get_settings
from app.db.migrate import ensure_db_ready


@pytest.fixture
def temp_settings(monkeypatch, tmp_path):
    """
    Isolate SQLite state per test by pointing BRAIN_STATE_DIR to a temp folder.
    """
    monkeypatch.setenv("BRAIN_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("BRAIN_DB_FILE", "test.db")
    # Refresh cached settings so env vars take effect
    get_settings.cache_clear()
    settings = get_settings()
    ensure_db_ready(settings)
    yield settings
    # Clear cache to avoid leaking settings between tests
    get_settings.cache_clear()


@pytest.fixture
def anyio_backend():
    """Force anyio tests to run on asyncio backend to avoid trio dependency."""
    return "asyncio"
