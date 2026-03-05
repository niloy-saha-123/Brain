from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class PlannerStep(BaseModel):
    step_id: str
    kind: Literal["tool", "llm", "noop"]
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = None


class PredictedApproval(BaseModel):
    step_id: str
    tool: str
    reason: Optional[str] = None


class PlannerDecision(BaseModel):
    selected_agent_id: str = "default"
    skills: List[str] = Field(default_factory=list)
    steps: List[PlannerStep] = Field(default_factory=list)
    predicted_approvals: List[PredictedApproval] = Field(default_factory=list)
    created_at: Optional[str] = None


class PlannerTrace(BaseModel):
    run_id: str
    decision: PlannerDecision
    created_at: str
