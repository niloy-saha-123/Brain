"""Receipts endpoints (minimal list/read)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.db import repo_receipts

router = APIRouter()


@router.get("/receipts/{receipt_id}")
def get_receipt(receipt_id: str):
    rec = repo_receipts.get_receipt(receipt_id)
    if not rec:
        raise HTTPException(status_code=404, detail="not found")
    return rec


@router.get("/runs/{run_id}/receipts")
def list_receipts(run_id: str):
    return repo_receipts.list_receipts_for_run(run_id)
