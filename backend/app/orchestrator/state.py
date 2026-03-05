"""Run state container."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.schemas import TaskSpec


@dataclass
class RunState:
    run_id: str
    task_spec: TaskSpec
    status: str = "running"
    worklog: List[str] = field(default_factory=list)
    receipts: List[str] = field(default_factory=list)
    approvals: List[str] = field(default_factory=list)
    output: Optional[str] = None
    plan: List[Dict[str, Any]] = field(default_factory=list)
    current_step: int = 0

    def add_worklog(self, msg: str) -> None:
        self.worklog.append(msg)
