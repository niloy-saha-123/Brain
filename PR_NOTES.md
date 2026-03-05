# PR Notes — feat/v0.2-security

## Current state
- Base v0.1 merged into `main` (per FINAL_REPORT). v0.2 backlog progressing on `feat/v0.2-*` branches (current: `feat/v0.2-security`).
- Tests cover approvals/receipts/runs/health/policy/agents/orchestrator + RAG + new security tests.
- UI wired to backend for runs/approvals/receipts/cost/agents; Chat page shows RAG hits and indexing form (unchanged this branch).

## v0.2 backlog plan (order)
1) Agents CRUD (backend + UI wiring) — ✅ done on feat/v0.2-backlog (commit db91211).
2) Orchestrator: real plan → tool selection → approvals → execution for >=3 tools — ✅ done on feat/v0.2-orchestrator (commit a9e49e2).
3) Memory/RAG: approved folder indexing + LanceDB + retrieval + citations — ✅ done on feat/v0.2-rag (commit bc4d973).
4) Security hardening: filesystem allowlists per approval, SSRF protections, output artifacting/redaction — ✅ done on feat/v0.2-security (commit 0ab23cb).

### Progress
- Agents: CRUD API implemented (`api/agents.py`, repo parse/delete), ID helper, UI Agents page wired to backend (create/update/delete), tests added `test_agents.py`.
- Orchestrator: plan node builds multi-tool steps (todo/web/folder read/terminal); approvals pause runs and resume to finish remaining steps; handles rejected approvals to fail run. Tests in `test_runs.py`.
- RAG: tool `rag.index` (approval-required) indexes allowlisted folders, chunks content, stores embeddings in SQLite with optional LanceDB; retrieval uses hashed embeddings; citations appended in finalize; endpoints `/rag/index`, `/rag/search`, `/memory/facts`. UI Chat shows RAG hits + index form. Test `test_rag.py`.
- Security: filesystem allowlist per run (`fs_allowlist` table + repo); resolve approvals auto-allow paths; web.fetch blocks private/loopback hosts; receipts now redact sensitive keys, truncate long strings with artifacts under `state/artifacts`; new tests in `test_security.py`.
- Pending: none for v0.2 backlog.

## How to verify (current branch)
1. Backend tests: `cd backend && python -m pytest app/tests`.
2. Security checks: start backend then hit `/rag/index` to trigger approval; approve via `/approvals/{id}/resolve`; filesystem.read only works after approval (check allowlist via `fs_allowlist` table). `/approvals` resolution for web.fetch/terminal unaffected.
3. Chat UI: `cd ui && npm install && npm run dev`; `/chat` still functions with runs/worklog/approvals; RAG panel present from prior branch.

## Next actions
- No pending backlog items; next steps depend on new requirements (v0.3?).
