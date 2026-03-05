"""Repository helpers for budgets table."""
from __future__ import annotations

from typing import Any, Dict, Optional

from app.db.sqlite import get_connection, row_to_dict
from app.core.config import Settings


def upsert_budget(month: str, cap_usd: float, spent_usd: float = 0.0, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            """
            INSERT INTO budgets (month, cap_usd, spent_usd)
            VALUES (:month, :cap_usd, :spent_usd)
            ON CONFLICT(month) DO UPDATE SET
                cap_usd = excluded.cap_usd,
                spent_usd = excluded.spent_usd;
            """,
            {"month": month, "cap_usd": cap_usd, "spent_usd": spent_usd},
        )


def update_spent(month: str, spent_usd: float, settings: Settings | None = None) -> None:
    with get_connection(settings) as conn:
        conn.execute(
            "UPDATE budgets SET spent_usd = :spent_usd WHERE month = :month;",
            {"month": month, "spent_usd": spent_usd},
        )


def get_budget(month: str, settings: Settings | None = None) -> Optional[Dict[str, Any]]:
    with get_connection(settings) as conn:
        row = conn.execute("SELECT * FROM budgets WHERE month = ?", (month,)).fetchone()
        return row_to_dict(row)
