"""Pydantic model for agent spec (editable brain)."""
from __future__ import annotations

from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class MemoryPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    can_write_facts: bool = Field(default=True, alias="can_write_facts")
    fact_tags: List[str] = Field(default_factory=list, alias="fact_tags")
    default_ttl_days: Optional[int] = Field(default=None, alias="default_ttl_days")


class AgentSpec(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    agent_id: str = Field(alias="agent_id")
    name: str = Field(alias="name")
    description: str = Field(alias="description")
    system_prompt: str = Field(alias="system_prompt")
    tools_allow: List[str] = Field(default_factory=list, alias="tools_allow")
    tools_deny: List[str] = Field(default_factory=list, alias="tools_deny")
    risk_level: Optional[str] = Field(default=None, alias="risk_level")
    model_pref: Optional[str] = Field(default=None, alias="model_pref")
    memory_policy: Optional[MemoryPolicy] = Field(default=None, alias="memory_policy")
    created_at: Optional[str] = Field(default=None, alias="created_at")
    updated_at: Optional[str] = Field(default=None, alias="updated_at")
    version: int = Field(default=1, alias="version")
