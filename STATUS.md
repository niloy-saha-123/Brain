# STATUS

**Branch:** feat/v0.2-security  
**Latest commit:** a1191a0315623b2179415abbc6923fdc184a0805

## v0.2 Milestones (from task_v0.2.md)
| Milestone | Status | Evidence |
|---|---|---|
| Agents CRUD (backend + UI wiring) | Done | `backend/app/api/agents.py` (create/update/delete), `backend/app/db/repo_agents.py`, UI `ui/src/pages/AgentsPage.tsx`, tests `backend/app/tests/test_agents.py` |
| Orchestrator: plan → tool selection → approvals → execution (>=3 tools) | Done | `backend/app/orchestrator/graph.py` (step tracking/pause-resume), `backend/app/orchestrator/nodes/plan.py`, tests `backend/app/tests/test_runs.py` |
| Memory/RAG: approved folder indexing + LanceDB + retrieval + citations | Done | `backend/app/tools/impl/rag_index.py`, `backend/app/memory/rag.py`, `backend/app/api/memory.py`, tests `backend/app/tests/test_rag.py`, UI `ui/src/pages/ChatPage.tsx` |
| Security hardening: fs allowlists, SSRF, artifacts/redaction | Done | `backend/app/db/repo_fs_allowlist.py`, `backend/app/tools/impl/filesystem.py`, `backend/app/tools/impl/web.py`, `backend/app/tools/runner.py`, tests `backend/app/tests/test_security.py` |

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
| UI monochrome layout with routed panels (chat/worklog/agents/approvals/runs/receipts/cost) | Implemented | `ui/src/pages/*.tsx`, `ui/src/components/Layout.tsx`, `ui/src/styles.css` |
| Cost meter & budgets | Implemented | `backend/app/api/costs.py`, `ui/src/pages/CostPage.tsx` |
| Tests covering health/approvals/receipts/runs/agents/rag/security | Implemented | `backend/app/tests/*.py` |

## Next 5 Tasks (minimal path to v0.2 completion)
1) Verify end-to-end on macOS: `cd backend && python -m pytest app/tests`; `uvicorn app.main:app --reload`; `cd ui && npm install && npm run dev`.
2) Manual approval/resume check: start run with goal containing “terminal”, resolve approval via `/approvals/{id}/resolve`, confirm run completes.
3) RAG flow check: `POST /rag/index` on a repo folder, approve, then `GET /rag/search?query=...` shows citations; confirm artifacts written under `backend/state/artifacts`.
4) UI smoke: in dev server visit `/chat` to start run, see worklog/status, RAG hits panel, and receipt list; visit `/approvals`, `/runs`, `/receipts`, `/cost`.
5) Prepare PRs from `feat/v0.2-*` branches into main (no merge yet); ensure PROGRESS.md/PR_NOTES.md align and note Pydantic v2 warnings as follow-up.
