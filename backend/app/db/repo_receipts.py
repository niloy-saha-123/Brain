"""Repository helpers for receipts table."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.db.sqlite import get_connection, row_to_dict, to_json
from app.core.time import now_iso
from app.core.config import Settings


def create_receipt(receipt: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "receipt_id": receipt["receipt_id"],
        "run_id": receipt["run_id"],
        "tool": receipt.get("tool", ""),
        "ok": int(bool(receipt.get("ok", True))),
        "ts": receipt.get("ts", now_iso()),
        "request": to_json(receipt.get("request")),
        "result": to_json(receipt.get("result")),
        "diff": to_json(receipt.get("diff")),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO receipts (
                receipt_id, run_id, tool, ok, ts, request, result, diff
            )
            VALUES (
                :receipt_id, :run_id, :tool, :ok, :ts, :request, :result, :diff
            );
            """,
            payload,
        )


def get_receipt(receipt_id: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM receipts WHERE receipt_id = ?", (receipt_id,)).fetchone()
        return row_to_dict(row)


def list_receipts_for_run(run_id: str, settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute(
            "SELECT * FROM receipts WHERE run_id = ? ORDER BY ts ASC", (run_id,)
        ).fetchall()
        return [row_to_dict(row) for row in rows if row is not None]
