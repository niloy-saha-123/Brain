"""In-memory registry for paused runs awaiting approval."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from app.orchestrator.state import RunState


@dataclass
class PendingCall:
    state: RunState
    tool_name: str
    args: Dict


_pending: Dict[str, PendingCall] = {}


def add_pending(approval_id: str, state: RunState, tool_name: str, args: Dict) -> None:
    _pending[approval_id] = PendingCall(state=state, tool_name=tool_name, args=args)


def pop_pending(approval_id: str) -> Tuple[RunState, str, Dict] | None:
    call = _pending.pop(approval_id, None)
    if not call:
        return None
    return (call.state, call.tool_name, call.args)
