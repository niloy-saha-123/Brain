"""Pydantic model for SSE events."""
from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, Field, ConfigDict


class Event(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    run_id: str = Field(alias="run_id")
    ts: str = Field(alias="ts")
    type: str = Field(alias="type")
    data: Dict[str, Any] = Field(default_factory=dict, alias="data")
