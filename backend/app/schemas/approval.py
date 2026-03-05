"""Pydantic models for approvals."""
from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, ConfigDict


class ApprovalDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: str = Field(alias="action")
    edited_details: Optional[Dict[str, Any]] = Field(default=None, alias="edited_details")
    user_note: Optional[str] = Field(default=None, alias="user_note")


class Approval(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    approval_id: str = Field(alias="approval_id")
    run_id: str = Field(alias="run_id")
    type: str = Field(alias="type")
    status: str = Field(alias="status")
    request: Dict[str, Any] = Field(alias="request")
    decision: Optional[ApprovalDecision] = Field(default=None, alias="decision")
    created_at: str = Field(alias="created_at")
    resolved_at: Optional[str] = Field(default=None, alias="resolved_at")
