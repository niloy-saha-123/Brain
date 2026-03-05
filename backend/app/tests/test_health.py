from fastapi.testclient import TestClient

from app.main import create_app
from app.core.config import get_settings


def test_health_ok(monkeypatch, tmp_path):
    monkeypatch.setenv("BRAIN_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("BRAIN_DB_FILE", "test.db")
    get_settings.cache_clear()
    app = create_app()
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "brain-backend"
    get_settings.cache_clear()


def test_health_ollama_unreachable(monkeypatch, tmp_path):
    monkeypatch.setenv("BRAIN_STATE_DIR", str(tmp_path))
    monkeypatch.setenv("BRAIN_DB_FILE", "test.db")
    # point to a closed port to force failure quickly
    monkeypatch.setenv("BRAIN_OLLAMA_BASE_URL", "http://127.0.0.1:1")
    get_settings.cache_clear()
    app = create_app()
    client = TestClient(app)
    resp = client.get("/health/ollama")
    assert resp.status_code == 503
    data = resp.json()
    assert data["service"] == "ollama"
    assert data["status"] in {"unreachable", "error"}
    get_settings.cache_clear()
