"""Utility to export Pydantic model JSON schemas."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Tuple, Type

from pydantic import BaseModel

from app.schemas import (
    AgentSpec,
    Approval,
    ApprovalDecision,
    Event,
    MemoryPolicy,
    Receipt,
    ReceiptResult,
    TaskSpec,
    TaskBudget,
    TaskContextRefs,
    TaskPolicies,
    ToolCall,
)


SCHEMAS: Iterable[Tuple[str, Type[BaseModel]]] = (
    ("task_spec", TaskSpec),
    ("task_budget", TaskBudget),
    ("task_policies", TaskPolicies),
    ("task_context_refs", TaskContextRefs),
    ("agent_spec", AgentSpec),
    ("memory_policy", MemoryPolicy),
    ("tool_call", ToolCall),
    ("receipt", Receipt),
    ("receipt_result", ReceiptResult),
    ("approval", Approval),
    ("approval_decision", ApprovalDecision),
    ("event", Event),
)


def export_json_schemas(output_dir: str | Path) -> None:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    for name, model in SCHEMAS:
        schema = model.model_json_schema()  # type: ignore[arg-type]
        (path / f"{name}.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")


if __name__ == "__main__":
    default_dir = Path(__file__).parent / "json"
    export_json_schemas(default_dir)
