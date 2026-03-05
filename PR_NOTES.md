# PR Notes — feat/v0.2-rag

## Current state
- Base v0.1 merged into `main` (per FINAL_REPORT). v0.2 backlog progressing on `feat/v0.2-*` branches (current: `feat/v0.2-rag`).
- Tests cover approvals/receipts/runs/health/policy/agents/orchestrator + new RAG indexing test.
- UI wired to backend for runs/approvals/receipts/cost/agents; Chat page now shows RAG hits and folder index trigger.

## v0.2 backlog plan (order)
1) Agents CRUD (backend + UI wiring) — ✅ done on feat/v0.2-backlog (commit db91211).
2) Orchestrator: real plan → tool selection → approvals → execution for >=3 tools — ✅ done on feat/v0.2-orchestrator (commit a9e49e2).
3) Memory/RAG: approved folder indexing + LanceDB + retrieval + citations — ✅ done on feat/v0.2-rag (commit bc4d973).
4) Security hardening: filesystem allowlists per approval, SSRF protections, output artifacting/redaction.

### Progress
- Agents: CRUD API implemented (`api/agents.py`, repo parse/delete), ID helper, UI Agents page wired to backend (create/update/delete), tests added `test_agents.py`.
- Orchestrator: plan node now builds multi-tool steps (todo/web/folder read/terminal); execution tracks step index; approvals pause runs and resume to finish remaining steps; handles rejected approvals to fail run. Tests added in `test_runs.py`.
- RAG: new tool `rag.index` (approval-required) indexes allowlisted folders, chunks content, stores embeddings in SQLite with optional LanceDB; retrieval uses hashed embeddings; citations appended in finalize; endpoints `/rag/index`, `/rag/search`, `/memory/facts`. UI Chat shows RAG hits + index form. Test `test_rag.py` covers approval + retrieval.
- Pending: security hardening milestone.

## How to verify (current branch)
1. Backend tests: `cd backend && python -m pytest app/tests`.
2. Run backend: `uvicorn app.main:app --reload`; POST `/rag/index` with a folder under repo root -> response pending with approval_id; approve via `/approvals/{id}/resolve`; chunks indexed and `/rag/search?query=...` returns citations.
3. Chat UI: `cd ui && npm install && npm run dev`; go to `/chat`, submit goal to start run and see worklog; Context panel shows RAG hits; use "Index folder" panel to request indexing (will reflect pending/complete).

## Next actions
- Begin v0.2 security hardening on branch `feat/v0.2-security` (approved backlog name): filesystem allowlists per approval, SSRF protections, output truncation/artifacting/redaction. Update PROGRESS/PR_NOTES accordingly.
