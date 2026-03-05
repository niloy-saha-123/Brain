# PR Notes — feat/v0.2-orchestrator

## Current state
- Base v0.1 merged into `main` (per FINAL_REPORT). v0.2 backlog progressing on `feat/v0.2-*` branches (current: `feat/v0.2-orchestrator`).
- Tests cover approvals/receipts/runs/health/policy/agents plus orchestrator pause/resume.
- UI wired to backend for runs/approvals/receipts/cost/agents (no new UI changes in this branch).

## v0.2 backlog plan (order)
1) Agents CRUD (backend + UI wiring) — ✅ done on feat/v0.2-backlog (commit db91211).
2) Orchestrator: real plan → tool selection → approvals → execution for >=3 tools — ✅ done on feat/v0.2-orchestrator (commit a9e49e2).
3) Memory/RAG: approved folder indexing + LanceDB + retrieval + citations.
4) Security hardening: filesystem allowlists per approval, SSRF protections, output artifacting/redaction.

### Progress
- Agents: CRUD API implemented (`api/agents.py`, repo parse/delete), ID helper, UI Agents page wired to backend (create/update/delete), tests added `test_agents.py`.
- Orchestrator: plan node now builds multi-tool steps (todo/web/folder read/terminal); execution tracks step index; approvals pause runs and resume to finish remaining steps; handles rejected approvals to fail run. Tests added in `test_runs.py`.
- Pending: RAG (index/retrieve/citations) and security hardening.

## How to verify (current branch)
1. Backend tests: `cd backend && python -m pytest app/tests`.
2. Run backend: `uvicorn app.main:app --reload`; start a run with goal containing "terminal" to trigger approval (via API or direct orchestrator call); see `/approvals` pending entry; POST approval resolve; run resumes and completes; receipts show tool calls.
3. UI unchanged this branch; prior steps still verified with `npm run dev` if needed.

## Next actions
- Begin v0.2 RAG milestone on branch `feat/v0.2-rag` (approved backlog name). Add folder approvals/indexing, LanceDB storage, retrieval, and citations. Update PROGRESS/PR_NOTES on that branch.
