"""Pydantic model for the canonical task spec (compact keys)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class TaskBudget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ctx_tok: int = Field(default=1200, alias="ctx_tok")
    out_tok: int = Field(default=600, alias="out_tok")
    cloud_usd_cap: float = Field(default=5, alias="cloud_usd_cap")


class TaskContextRefs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mem: List[str] = Field(default_factory=list, alias="mem")
    rag: List[str] = Field(default_factory=list, alias="rag")
    rcpt: List[str] = Field(default_factory=list, alias="rcpt")


class TaskPolicies(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allow_web: bool = Field(default=False, alias="allow_web")
    allow_cloud: bool = Field(default=False, alias="allow_cloud")
    require_approval: bool = Field(default=True, alias="require_approval")


class TaskSpec(BaseModel):
    """Compact, versioned task specification produced by the router."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    id: str = Field(alias="id")
    g: str = Field(alias="g")
    u: Optional[str] = Field(default=None, alias="u")
    a: Optional[str] = Field(default=None, alias="a")
    c: Dict[str, Any] = Field(default_factory=dict, alias="c")
    o: Dict[str, Any] = Field(default_factory=dict, alias="o")
    pol: TaskPolicies = Field(default_factory=TaskPolicies, alias="pol")
    ctx: TaskContextRefs = Field(default_factory=TaskContextRefs, alias="ctx")
    bdg: TaskBudget = Field(default_factory=TaskBudget, alias="bdg")
