# PR Notes — feat/approvals

## What changed
- Tool runner now creates approval requests (DB + SSE `approval_requested`) when sensitive tools are invoked without approval.
- Approvals resolve endpoint publishes `approval_resolved` events; receipts publish events too.
- Keeps prior tools/receipts functionality intact.

## Files touched
- backend/app/tools/runner.py
- backend/app/api/approvals.py
- README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. Run backend: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
2. Trigger a sensitive tool without approval (e.g., terminal.run) from a REPL:
   ```python
   from app.tools.runner import run_tool
   import asyncio
   try:
       asyncio.run(run_tool("terminal.run", {"cmd":"echo hi"}, {"run_id":"demo"}))
   except Exception as e:
       print(e)
   ```
   -> should raise approval required with approval_id.
3. List approvals: `curl http://localhost:8000/approvals` (should show pending).
4. Resolve: `curl -X POST http://localhost:8000/approvals/<id>/resolve -H 'Content-Type: application/json' -d '{"action":"approved"}'`

## Commands to run
- `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `curl http://localhost:8000/approvals`
- `curl -X POST http://localhost:8000/approvals/<id>/resolve -H 'Content-Type: application/json' -d '{"action":"approved"}'`
