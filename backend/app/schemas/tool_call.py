"""Pydantic model for tool call envelopes."""
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, ConfigDict


class ToolCall(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    tool: str = Field(alias="tool")
    args: Dict[str, Any] = Field(default_factory=dict, alias="args")
    risk: Optional[str] = Field(default=None, alias="risk")
    needs_approval: Optional[bool] = Field(default=None, alias="needs_approval")
    reason: Optional[str] = Field(default=None, alias="reason")
    run_id: Optional[str] = Field(default=None, alias="run_id")
