# PR Notes — feat/orchestrator

## What changed
- Added orchestrator stubs: RunState and node functions (route, rewrite, context, plan, execute, verify, finalize) plus graph starter that logs worklog/status events.
- Runs are recorded in DB and immediately marked completed (stub) while emitting events.

## Files touched
- backend/app/orchestrator/state.py
- backend/app/orchestrator/graph.py
- backend/app/orchestrator/nodes/*.py
- README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. Start backend: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
2. (Stub) call `start_run` from a REPL:
   ```python
   from app.orchestrator.graph import start_run
   from app.schemas import TaskSpec
   import asyncio
   ts = TaskSpec(id="run_orch", g="test", v=1)
   asyncio.run(start_run(ts))
   ```
3. Check run recorded: `sqlite3 ../state/brain.db "select run_id,status from runs where run_id='run_orch';"`
4. Stream events: `curl -N http://localhost:8000/runs/run_orch/events` (should show status/worklog).

## Commands to run
- `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `curl -N http://localhost:8000/runs/run_orch/events`
