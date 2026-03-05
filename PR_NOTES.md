# PR Notes — feat/cost-meter

## What changed
- Added cost tracking helpers (token estimates, model usage, monthly budgets) and `/costs/summary` API.
- Wired debug LLM endpoint to record model usage when a `run_id` is provided.
- Exposed cloud controls in config (disabled by default, approval still required if enabled).
- Updated UI Cost panel to pull live summary and show budget/model usage in monochrome boxy layout.

## Files touched
- backend/app/core/costs.py (new), backend/app/api/costs.py (new)
- backend/app/api/llm.py, backend/app/core/config.py, backend/app/db/repo_runs.py, backend/app/main.py
- ui/src/pages/CostPage.tsx, ui/src/styles.css
- README.md, SETUP.md, PR_NOTES.md

## How to verify
1. Backend running: `cd backend && uvicorn app.main:app --reload`.
2. (Optional) Track a debug LLM call to a run:  
   `curl -N -X POST http://localhost:8000/debug/llm -H "Content-Type: application/json" -d '{"prompt":"hi","run_id":"run_cost"}'`
3. Fetch summary: `curl http://localhost:8000/costs/summary` — should show budget cap 5, spent 0 (or updated), model usage if step 2 ran.
4. UI: `cd ui && npm install` (if not already) then `npm run dev` and open Cost panel to see budget/model data.

## Commands to run
- Backend: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Cost summary: `curl http://localhost:8000/costs/summary`
- UI: `npm install` (once) then `npm run dev`
