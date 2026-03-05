"""Repository helpers for messages table."""
from __future__ import annotations

from typing import Any, Dict, List

from app.core.time import now_iso
from app.db.sqlite import get_connection, row_to_dict
from app.core.config import Settings


def add_message(message: Dict[str, Any], settings: Settings | None = None) -> None:
    payload = {
        "msg_id": message["msg_id"],
        "run_id": message["run_id"],
        "role": message.get("role", "assistant"),
        "content": message.get("content", ""),
        "created_at": message.get("created_at", now_iso()),
    }
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO messages (msg_id, run_id, role, content, created_at)
            VALUES (:msg_id, :run_id, :role, :content, :created_at);
            """,
            payload,
        )


def list_messages(run_id: str, settings: Settings | None = None) -> List[Dict[str, Any]]:
    with get_connection(settings) as conn:
        rows = conn.execute(
            "SELECT * FROM messages WHERE run_id = ? ORDER BY created_at ASC", (run_id,)
        ).fetchall()
        return [row_to_dict(row) for row in rows if row is not None]
