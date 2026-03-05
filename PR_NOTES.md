# PR Notes — feat/v0.2-backlog

## Current state
- Base v0.1 merged into `main` (per FINAL_REPORT). Working on v0.2 backlog branches `feat/v0.2-*` (current: `feat/v0.2-backlog`).
- Tests cover approvals/receipts/runs/health/policy/agents (unit-level).
- UI wired to backend for runs/approvals/receipts/cost and now agents CRUD.

## v0.2 backlog plan (order)
1) Agents CRUD (backend + UI wiring) — ✅ done on feat/v0.2-backlog (commit db91211).
2) Orchestrator: real plan → tool selection → approvals → execution for >=3 tools.
3) Memory/RAG: approved folder indexing + LanceDB + retrieval + citations.
4) Security hardening: filesystem allowlists per approval, SSRF protections, output artifacting/redaction.

### Progress
- Agents: CRUD API implemented (`api/agents.py`, repo parse/delete), ID helper, UI Agents page wired to backend (create/update/delete), tests added `test_agents.py`.
- Existing orchestration/approvals/security guards from v0.1 fix remain.
- Pending: orchestrator multi-tool plan, RAG, stronger security/artifacts.

## How to verify (current branch)
1. Backend tests: `cd backend && python -m pytest app/tests` (includes agents CRUD).
2. Run backend: `uvicorn app.main:app --reload`; hit `GET /agents` (empty), `POST /agents` to create, then list/update/delete.
3. UI: `cd ui && npm install && npm run dev`; open `/agents`, create/update/delete agent and see list refresh.

## Next actions
- Start v0.2 orchestrator milestone (plan/tool selection/approvals resume for >=3 tools) on branch `feat/v0.2-orchestrator` (or continue on feat/v0.2-backlog if preferred), then update PROGRESS/PR_NOTES accordingly.
