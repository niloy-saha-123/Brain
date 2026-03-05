# PR Notes — feat/sse-events

## What changed
- Implemented in-process event bus and SSE streaming endpoint `/runs/{run_id}/events`.
- Added heartbeat support and SSE formatting; wired router into FastAPI app.
- Kept earlier milestones (health, DB, schemas, Ollama client) intact.

## Files touched
- backend/app/events/bus.py, backend/app/events/sse.py, backend/app/events/__init__.py
- backend/app/main.py
- README.md, PROGRESS.md, SETUP.md (docs if present)

## How to verify
1. Ensure backend deps installed and server running: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
2. In another terminal, stream events (will hang until events are published):
   ```bash
   curl -N http://localhost:8000/runs/test-run/events
   ```
   Should show `event: heartbeat` every ~15s; published events will appear as JSON lines.

## Commands to run
- `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `curl -N http://localhost:8000/runs/test-run/events`
