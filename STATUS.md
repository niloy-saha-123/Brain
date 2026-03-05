# STATUS

**Branch:** feat/v0.3-planner-v2  
**Latest commit:** 4f8ac9a7e9c8b3c3d1e2f6d31c2c7d0cbe9abf4b

## v0.2 Milestones (from task_v0.2.md)
| Milestone | Status | Evidence |
|---|---|---|
| Agents CRUD (backend + UI wiring) | Done | `backend/app/api/agents.py` (create/update/delete), `backend/app/db/repo_agents.py`, UI `ui/src/pages/AgentsPage.tsx`, tests `backend/app/tests/test_agents.py` |
| Orchestrator: plan → tool selection → approvals → execution (>=3 tools) | Done | `backend/app/orchestrator/graph.py` (step tracking/pause-resume), `backend/app/orchestrator/nodes/plan.py`, tests `backend/app/tests/test_runs.py` |
| Memory/RAG: approved folder indexing + LanceDB + retrieval + citations | Done | `backend/app/tools/impl/rag_index.py`, `backend/app/memory/rag.py`, `backend/app/api/memory.py`, tests `backend/app/tests/test_rag.py`, UI `ui/src/pages/ChatPage.tsx` |
| Security hardening: fs allowlists, SSRF, artifacts/redaction | Done | `backend/app/db/repo_fs_allowlist.py`, `backend/app/tools/impl/filesystem.py`, `backend/app/tools/impl/web.py`, `backend/app/tools/runner.py`, tests `backend/app/tests/test_security.py` |
| Hotfix: approval parsing + filesystem dir read | Done | `backend/app/api/approvals.py` (parse JSON string request), `backend/app/tools/impl/filesystem.py` (dir listing), tests `backend/app/tests/test_security.py` |
| Planner contracts + trace persistence (v0.3 M1) | Done | `backend/app/schemas/planner.py`, `backend/app/db/repo_planner_traces.py`, `backend/app/api/runs.py` (/runs/{id}/plan), events `plan_ready/step_*`, tests `backend/app/tests/test_planner.py` |

## Spec Checklist (ARCHITECTURE.md)
| Requirement | Status | Key files / functions |
|---|---|---|
| Health endpoints & CORS | Implemented | `backend/app/api/health.py`, `backend/app/main.py` |
| SQLite schema + repos for runs/approvals/receipts/memory/todos | Implemented | `backend/app/db/schema.sql`, `backend/app/db/repo_*.py` |
| Tool system with approvals + receipts (todo/filesystem/git/web/terminal/ide patch/rag.index) | Implemented | `backend/app/tools/impl/*`, `backend/app/tools/runner.py`, `backend/app/tools/policy.py` |
| Approvals inbox & resume behavior | Implemented | `backend/app/api/approvals.py`, `backend/app/orchestrator/graph.py` |
| Orchestrator route→rewrite→context→plan→execute→verify→finalize with SSE worklog/status | Implemented | `backend/app/orchestrator/*`, `backend/app/events/bus.py`, `backend/app/events/sse.py` |
| Memory facts store + RAG retrieval with citations | Implemented | `backend/app/memory/facts.py`, `backend/app/memory/rag.py`, `backend/app/api/memory.py` |
| RAG indexing requires approval & path allowlist | Implemented | `backend/app/tools/impl/rag_index.py`, `backend/app/api/approvals.py`, `backend/app/db/repo_fs_allowlist.py` |
| SSRF protections for web.fetch | Implemented | `backend/app/tools/impl/web.py` |
| Output truncation/artifact storage & redaction in receipts | Implemented | `backend/app/tools/runner.py` |
| filesystem.read returns directory listing for folders | Implemented | `backend/app/tools/impl/filesystem.py` |
| UI monochrome layout with routed panels (chat/worklog/agents/approvals/runs/receipts/cost) | Implemented | `ui/src/pages/*.tsx`, `ui/src/components/Layout.tsx`, `ui/src/styles.css` |
| Cost meter & budgets | Implemented | `backend/app/api/costs.py`, `ui/src/pages/CostPage.tsx` |
| Tests covering health/approvals/receipts/runs/agents/rag/security | Implemented | `backend/app/tests/*.py` |

## Next 5 Tasks (v0.3 path)
1) Verify planner trace: start a run (`list files`), then `curl http://localhost:8000/runs/<run_id>/plan` returns stored trace with steps and predicted_approvals.
2) Watch SSE for plan/step events via `/runs/<run_id>/events` (expect `plan_ready`, `step_started`, `step_completed`, `step_paused_for_approval` when approval required).
3) Confirm no regressions: `cd backend && python -m pytest app/tests` (18 pass; Pydantic deprecation warnings expected).
4) Decide scope/acceptance for v0.3 Milestones 2–3 (planner execution heuristics, UI plan view).
5) After approval, branch off for Milestone 2 implementation (`feat/v0.3-exec`).
