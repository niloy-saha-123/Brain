"""Cost and usage helpers for model calls and budgets."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.config import Settings, get_settings
from app.llm.token_estimate import estimate_tokens
from app.db import repo_runs, repo_budgets
from app.core.time import now_iso


@dataclass
class ModelUsageEntry:
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_estimate_usd: float
    cloud: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def current_month() -> str:
    return datetime.utcnow().strftime("%Y-%m")


def _ensure_budget_row(month: str, settings: Settings) -> Dict[str, Any]:
    existing = repo_budgets.get_budget(month, settings=settings)
    if existing:
        return existing
    repo_budgets.upsert_budget(month, cap_usd=settings.cloud_budget_cap, spent_usd=0.0, settings=settings)
    return {"month": month, "cap_usd": settings.cloud_budget_cap, "spent_usd": 0.0}


def estimate_model_usage(
    model: str,
    prompt_text: str,
    completion_text: str = "",
    *,
    is_cloud: bool = False,
    settings: Optional[Settings] = None,
) -> ModelUsageEntry:
    settings = settings or get_settings()
    prompt_tokens = estimate_tokens(prompt_text)
    completion_tokens = estimate_tokens(completion_text)
    total_tokens = prompt_tokens + completion_tokens

    cost_estimate = 0.0
    if is_cloud:
        per_1k = settings.cloud_cost_per_1k_tokens
        cost_estimate = (total_tokens / 1000.0) * per_1k

    return ModelUsageEntry(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_estimate_usd=round(cost_estimate, 6),
        cloud=is_cloud,
    )


def record_model_usage(
    run_id: str,
    model: str,
    prompt_text: str,
    completion_text: str = "",
    *,
    is_cloud: bool = False,
    settings: Optional[Settings] = None,
) -> ModelUsageEntry:
    """Store model usage and update run/budget tracking."""
    settings = settings or get_settings()
    usage = estimate_model_usage(model, prompt_text, completion_text, is_cloud=is_cloud, settings=settings)

    # Ensure run exists to satisfy FK.
    existing = repo_runs.get_run(run_id, settings=settings)
    if not existing:
        repo_runs.create_run(
            {
                "run_id": run_id,
                "status": "running",
                "created_at": now_iso(),
                "model_usage": [usage.to_dict()],
                "cost_estimate_usd": usage.cost_estimate_usd,
            },
            settings=settings,
        )
    else:
        existing_usage_raw = existing.get("model_usage")
        existing_usage: List[Dict[str, Any]] = []
        if existing_usage_raw:
            try:
                existing_usage = json.loads(existing_usage_raw) if isinstance(existing_usage_raw, str) else existing_usage_raw
            except json.JSONDecodeError:
                existing_usage = []
        existing_usage.append(usage.to_dict())
        prev_cost_raw = existing.get("cost_estimate_usd")
        try:
            prev_cost = float(prev_cost_raw) if prev_cost_raw is not None else 0.0
        except (TypeError, ValueError):
            prev_cost = 0.0
        total_cost = prev_cost + usage.cost_estimate_usd
        repo_runs.update_run_model_usage(
            run_id,
            model_usage=existing_usage,
            cost_estimate_usd=total_cost,
            settings=settings,
        )

    if is_cloud and usage.cost_estimate_usd > 0:
        month = current_month()
        budget = _ensure_budget_row(month, settings)
        new_spent = (budget.get("spent_usd") or 0.0) + usage.cost_estimate_usd
        repo_budgets.update_spent(month, spent_usd=new_spent, settings=settings)
    else:
        _ensure_budget_row(current_month(), settings)

    return usage


def aggregate_model_usage(runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregate model usage across runs for summary stats."""
    agg: Dict[str, Dict[str, Any]] = {}
    for run in runs:
        raw = run.get("model_usage")
        if not raw:
            continue
        try:
            usage_list = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            continue
        if not isinstance(usage_list, list):
            continue
        for entry in usage_list:
            model = entry.get("model", "unknown")
            target = agg.setdefault(
                model,
                {"model": model, "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "cost_estimate_usd": 0.0, "cloud": False},
            )
            target["prompt_tokens"] += entry.get("prompt_tokens", 0)
            target["completion_tokens"] += entry.get("completion_tokens", 0)
            target["total_tokens"] += entry.get("total_tokens", 0)
            target["cost_estimate_usd"] += entry.get("cost_estimate_usd", 0.0)
            target["cloud"] = target["cloud"] or entry.get("cloud", False)
    # Round costs for display
    for val in agg.values():
        val["cost_estimate_usd"] = round(val["cost_estimate_usd"], 6)
    return list(agg.values())
