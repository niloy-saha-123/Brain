# PR Notes — feat/schemas

## What changed
- Added Pydantic models for task spec, agent spec, tool calls, receipts, approvals, SSE events.
- Included JSON schema export utility (`python -m app.schemas.export`) that writes schemas to `backend/app/schemas/json/`.
- Exported schema components through `app.schemas.__all__` for reuse.
- Kept previous milestones (backend skeleton, DB schema/repos) intact.

## Files touched
- backend/app/schemas/*.py (task_spec, agent, tool_call, receipt, approval, events, __init__, export)
- README.md, PROGRESS.md, PR_NOTES.md (docs)

## How to verify
1. `cd backend && python -m pip install -e ".[dev]"` (already done for earlier milestones).
2. (Optional) Generate JSON schemas: `cd backend && python -m app.schemas.export` then inspect `backend/app/schemas/json/*.json`.
3. Import models and validate sample payloads (e.g., TaskSpec with compact keys) in a Python REPL.

## Commands to run
- `cd backend && python -m pip install -e ".[dev]"` (if not already)
- `cd backend && python -m app.schemas.export` (writes JSON schemas to backend/app/schemas/json)
