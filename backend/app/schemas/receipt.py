"""Pydantic model for tool receipts."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class ReceiptResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stdout: Optional[str] = Field(default=None, alias="stdout")
    stderr: Optional[str] = Field(default=None, alias="stderr")
    exit_code: Optional[int] = Field(default=None, alias="exit_code")
    files_touched: List[str] = Field(default_factory=list, alias="files_touched")
    artifacts: List[str] = Field(default_factory=list, alias="artifacts")


class Receipt(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    v: int = Field(default=1, alias="v")
    receipt_id: str = Field(alias="receipt_id")
    run_id: str = Field(alias="run_id")
    tool: str = Field(alias="tool")
    ok: bool = Field(alias="ok")
    ts: str = Field(alias="ts")
    request: Dict[str, Any] = Field(alias="request")
    result: ReceiptResult = Field(alias="result")
    diff: Optional[Any] = Field(default=None, alias="diff")
    redactions: List[str] = Field(default_factory=list, alias="redactions")
