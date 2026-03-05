# PR Notes — test/polish (v0.1-fix plan)

## Current state (baseline)
- Tests cover approvals/receipts/runs/health/policy (unit-level).
- UI panels are monochrome but stubbed.
- Orchestrator is a stub; approvals require manual approval_id injection; security hardening incomplete.

## v0.1 fix plan (must-do, in priority order)
1) **Orchestrator real graph**: implement route → rewrite → context → plan → execute → verify → finalize with event emissions (worklog/token/receipt/status). Runs must actually execute tool calls.
2) **Approvals flow**: tool execution should pause runs awaiting approval and auto-resume after `/approvals/{id}/resolve`. Remove need for manual approval_id in callers.
3) **UI wiring**: hook Chat/Worklog/Approvals/Runs/Receipts to backend REST + SSE; remove static data; display live events/approvals/receipts.
4) **Security hardening**:
   - Path traversal controls for filesystem.* (normalize/allowlist approved roots).
   - SSRF guard for web.fetch (block localhost/metadata/file, enforce size/time limits).
   - Output truncation + artifact storage for large tool outputs.
   - Basic redaction of secrets in receipts/logs.
   - Safer git commit (no global `-am`; allow message + explicit paths or read-only default).
5) **Cost/completion polish**: keep cost tracking but ensure cloud calls remain approval-gated; update docs after fixes.

## Files touched (baseline tests & docs)
- backend/app/tests/conftest.py
- backend/app/tests/test_{approvals,health,policy,receipts,runs}.py
- README.md, SETUP.md, ui/README.md, FINAL_REPORT.md

## How to verify baseline
1. `cd backend && python -m pytest app/tests`
2. (Existing) `uvicorn app.main:app --reload` then `curl http://localhost:8000/health`

## Next actions
- Implement fix plan above on new milestone branch (do not merge to main yet).
