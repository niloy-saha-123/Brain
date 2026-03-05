"""Repository helpers for agents table."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.config import Settings


def upsert_agent(agent: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "agent_id": agent["agent_id"],
        "name": agent.get("name", ""),
        "description": agent.get("description", ""),
        "system_prompt": agent.get("system_prompt", ""),
        "tools_allow": to_json(agent.get("tools_allow")) or json.dumps([]),
        "tools_deny": to_json(agent.get("tools_deny")) or json.dumps([]),
        "risk_level": agent.get("risk_level"),
        "model_pref": agent.get("model_pref"),
        "memory_policy": to_json(agent.get("memory_policy")),
        "version": agent.get("version", 1),
        "created_at": agent.get("created_at", now_iso()),
        "updated_at": agent.get("updated_at", now_iso()),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO agents (
                agent_id, name, description, system_prompt, tools_allow, tools_deny,
                risk_level, model_pref, memory_policy, version, created_at, updated_at
            )
            VALUES (
                :agent_id, :name, :description, :system_prompt, :tools_allow, :tools_deny,
                :risk_level, :model_pref, :memory_policy, :version, :created_at, :updated_at
            )
            ON CONFLICT(agent_id) DO UPDATE SET
                name=excluded.name,
                description=excluded.description,
                system_prompt=excluded.system_prompt,
                tools_allow=excluded.tools_allow,
                tools_deny=excluded.tools_deny,
                risk_level=excluded.risk_level,
                model_pref=excluded.model_pref,
                memory_policy=excluded.memory_policy,
                version=excluded.version,
                updated_at=excluded.updated_at;
            """,
            payload,
        )


def get_agent(agent_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,)).fetchone()
        return _parse_agent_row(row)


def list_agents(settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute("SELECT * FROM agents ORDER BY created_at ASC").fetchall()
        return [_parse_agent_row(row) for row in rows if row is not None]


def delete_agent(agent_id: str, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute("DELETE FROM agents WHERE agent_id = ?", (agent_id,))


def _parse_agent_row(row: Any) -> Optional[Dict[str, Any]]:
    data = row_to_dict(row)
    if data is None:
        return None
    for field in ("tools_allow", "tools_deny", "memory_policy"):
        val = data.get(field)
        if val:
            try:
                data[field] = json.loads(val) if isinstance(val, str) else val
            except json.JSONDecodeError:
                data[field] = [] if "tools" in field else None
        else:
            data[field] = [] if "tools" in field else None
    return data
