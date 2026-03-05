# PR Notes — feat/tools-receipts

## What changed
- Implemented tool base/registry/policy/runner plus core tools (filesystem read/write, terminal run, git status/diff/commit, web.fetch GET, todo add/list/complete, ide.patch placeholder).
- Added approvals endpoints (list/resolve) and receipts endpoints (list by run, get by id).
- Tool runner stores receipts via repo_receipts; approvals remain conservative (approval required for sensitive tools).

## Files touched
- backend/app/tools/**/* (base, policy, registry, runner, impl tools)
- backend/app/api/approvals.py, backend/app/api/receipts.py, backend/app/main.py
- README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. `cd backend && python -m pip install -e ".[dev]"` (if not already).
2. Start server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
3. Hit approvals/receipts endpoints (expect empty unless populated):
   - `curl http://localhost:8000/approvals`
   - `curl http://localhost:8000/runs/test-run/receipts`
4. (Optional) Invoke tool runner from Python to see receipts stored:
   ```python
   from app.tools.runner import run_tool
   import asyncio
   asyncio.run(run_tool("todo.add", {"text":"test todo"}, {"run_id":"demo"}))
   ```

## Commands to run
- `cd backend && python -m pip install -e ".[dev]"`
- `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `curl http://localhost:8000/approvals`
- `curl http://localhost:8000/runs/demo/receipts`
