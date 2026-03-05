from fastapi.testclient import TestClient

from app.main import create_app
from app.core.config import get_settings


def test_agents_crud(temp_settings, monkeypatch):
    # ensure settings use temp db
    get_settings.cache_clear()
    app = create_app()
    client = TestClient(app)

    payload = {
        "name": "Code Agent",
        "description": "Writes code",
        "system_prompt": "You are a coder.",
        "tools_allow": ["terminal.run"],
        "tools_deny": [],
        "risk_level": "medium",
    }

    resp = client.post("/agents", json=payload)
    assert resp.status_code == 201
    agent = resp.json()
    agent_id = agent["agent_id"]

    resp_list = client.get("/agents")
    assert resp_list.status_code == 200
    agents = resp_list.json()
    assert len(agents) == 1

    resp_get = client.get(f"/agents/{agent_id}")
    assert resp_get.status_code == 200
    assert resp_get.json()["name"] == "Code Agent"

    resp_update = client.put(f"/agents/{agent_id}", json={"name": "Coder X"})
    assert resp_update.status_code == 200
    assert resp_update.json()["name"] == "Coder X"

    resp_del = client.delete(f"/agents/{agent_id}")
    assert resp_del.status_code == 204

    resp_list2 = client.get("/agents")
    assert resp_list2.status_code == 200
    assert resp_list2.json() == []

    get_settings.cache_clear()
