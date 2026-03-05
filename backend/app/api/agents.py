"""Agents CRUD endpoints."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.db import repo_agents
from app.schemas.agent import AgentSpec
from app.core.time import now_iso
from app.core.ids import make_agent_id

router = APIRouter()


class AgentCreate(BaseModel):
    agent_id: Optional[str] = Field(default=None)
    name: str
    description: str
    system_prompt: str
    tools_allow: List[str] = Field(default_factory=list)
    tools_deny: List[str] = Field(default_factory=list)
    risk_level: Optional[str] = None
    model_pref: Optional[str] = None
    memory_policy: Optional[dict] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    tools_allow: Optional[List[str]] = None
    tools_deny: Optional[List[str]] = None
    risk_level: Optional[str] = None
    model_pref: Optional[str] = None
    memory_policy: Optional[dict] = None
    version: Optional[int] = None


@router.get("/agents", response_model=List[AgentSpec])
def list_agents():
    agents = repo_agents.list_agents()
    return [AgentSpec(**a) for a in agents]


@router.get("/agents/{agent_id}", response_model=AgentSpec)
def get_agent(agent_id: str):
    agent = repo_agents.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="not found")
    return AgentSpec(**agent)


@router.post("/agents", response_model=AgentSpec, status_code=201)
def create_agent(payload: AgentCreate):
    agent_id = payload.agent_id or make_agent_id()
    now = now_iso()
    data = {
        "agent_id": agent_id,
        "name": payload.name,
        "description": payload.description,
        "system_prompt": payload.system_prompt,
        "tools_allow": payload.tools_allow,
        "tools_deny": payload.tools_deny,
        "risk_level": payload.risk_level,
        "model_pref": payload.model_pref,
        "memory_policy": payload.memory_policy,
        "version": 1,
        "created_at": now,
        "updated_at": now,
    }
    repo_agents.upsert_agent(data)
    return AgentSpec(**data)


@router.put("/agents/{agent_id}", response_model=AgentSpec)
def update_agent(agent_id: str, payload: AgentUpdate):
    existing = repo_agents.get_agent(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail="not found")
    updated = {**existing}
    for field, value in payload.model_dump(exclude_unset=True).items():
        updated[field] = value
    updated["updated_at"] = now_iso()
    # bump version
    updated["version"] = (updated.get("version") or 1) + 1
    repo_agents.upsert_agent(updated)
    return AgentSpec(**updated)


@router.delete("/agents/{agent_id}", status_code=204)
def delete_agent(agent_id: str):
    existing = repo_agents.get_agent(agent_id)
    if not existing:
        raise HTTPException(status_code=404, detail="not found")
    repo_agents.delete_agent(agent_id)
    return {}
