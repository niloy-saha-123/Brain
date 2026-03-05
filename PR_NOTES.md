# PR Notes — feat/db-schema

## What changed
- Added SQLite schema with migrations (state/brain.db by default) and startup hook.
- Implemented repository helpers for agents, runs, messages, approvals, receipts, memory_facts, budgets.
- Extended config with state dir/db filename options; added time utility.
- Retained backend skeleton (health endpoints, CORS) and updated SETUP for safe installs.

## Files touched
- backend/app/db/schema.sql, sqlite.py, migrate.py
- backend/app/db/repo_agents.py, repo_runs.py, repo_messages.py, repo_approvals.py, repo_receipts.py, repo_memory.py, repo_budgets.py
- backend/app/core/config.py, backend/app/core/time.py, backend/app/main.py
- SETUP.md, README.md, PROGRESS.md

## How to verify
1. `cd backend && python -m pip install -e ".[dev]"`
2. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (startup runs migrations)
3. `sqlite3 ../state/brain.db ".tables"` (or equivalent) shows agents, runs, messages, approvals, receipts, memory_facts, budgets, todos.
4. Health endpoints: `curl http://localhost:8000/health` and `curl http://localhost:8000/health/ollama` (should be ok if Ollama running; otherwise 503 JSON).

## Commands to run
- `cd backend && python -m pip install -e ".[dev]"`
- `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `sqlite3 ../state/brain.db ".tables"`  (or use another SQLite viewer)
- `curl http://localhost:8000/health`
- `curl http://localhost:8000/health/ollama`
