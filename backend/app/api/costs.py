"""Cost meter endpoints (summary + budget)."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.costs import aggregate_model_usage, current_month
from app.db import repo_runs, repo_budgets

router = APIRouter()


def _parse_run_cost(run: Dict[str, Any]) -> float:
    if run.get("cost_actual_usd") is not None:
        return float(run.get("cost_actual_usd"))
    if run.get("cost_estimate_usd") is not None:
        return float(run.get("cost_estimate_usd"))
    return 0.0


@router.get("/costs/summary", summary="Get cost and budget summary")
def get_cost_summary(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    month = current_month()
    budget = repo_budgets.get_budget(month, settings=settings)
    if not budget:
        repo_budgets.upsert_budget(month, cap_usd=settings.cloud_budget_cap, spent_usd=0.0, settings=settings)
        budget = {"month": month, "cap_usd": settings.cloud_budget_cap, "spent_usd": 0.0}

    runs = repo_runs.list_runs(settings=settings)
    total_runs_cost = sum(_parse_run_cost(r) for r in runs)
    model_usage = aggregate_model_usage(runs)

    return {
        "month": month,
        "budget": {
            "cap_usd": budget.get("cap_usd", settings.cloud_budget_cap),
            "spent_usd": budget.get("spent_usd", 0.0),
            "remaining_usd": max(budget.get("cap_usd", settings.cloud_budget_cap) - budget.get("spent_usd", 0.0), 0.0),
        },
        "cloud": {
            "enabled": settings.cloud_enabled,
            "cost_per_1k_tokens": settings.cloud_cost_per_1k_tokens,
        },
        "runs_cost_usd": round(total_runs_cost, 6),
        "models": model_usage,
    }
