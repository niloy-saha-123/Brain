
---

# 7) `PROGRESS.md`

# Progress Tracker (Single Source of Truth)

**Rule:** Every milestone branch must update this file before stopping.

## Milestones
| Milestone | Branch | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Backend skeleton + health | feat/backend-skeleton | Done | c294f18 | Start uvicorn; GET /health returns ok; GET /health/ollama returns ok or 503 gracefully | Install backend deps; Ollama optional but required for healthy ollama response; response_model annotation fixed |
| SQLite schema + repos | feat/db-schema | Done | a570184 | App startup runs migrations; tables exist (agents, runs, messages, approvals, receipts, memory_facts, budgets, todos); repo CRUD helpers in db/repo_* | DB lives under state/brain.db by default; override with BRAIN_STATE_DIR/BRAIN_DB_FILE |
| Schemas (Pydantic + JSON schema export) | feat/schemas | Done | 5700668 | Pydantic models validate; JSON schema export utility writes schema files when run; JSON schema artifacts checked in | Export via `python -m app.schemas.export` (writes to backend/app/schemas/json) |
| Ollama client (streaming) | feat/ollama-client | Done | 2b337de | POST /debug/llm streams tokens from Ollama; model registry uses env-configured models | Defaults: general/router=llama3.2:3b, coder=deepseek-coder:6.7b; override via env |
| SSE event bus | feat/sse-events | Done | 57adec7 | GET /runs/{run_id}/events streams SSE (heartbeat + events) | Uses in-process EventBus; format follows event: <type>, data: JSON |
| Tools + receipts | feat/tools-receipts | Done | c2d8362 | Tool base/registry/runner implemented; approvals + receipts endpoints exposed | Sensitive tools gated; receipts stored via repo_receipts |
| Approvals inbox + gating | feat/approvals | Done | ba0083e | Tool runner creates approval requests and emits events; approvals resolve endpoint publishes resolution | Approval required for sensitive tools; SSE gets approval_requested/resolved events |
| Orchestrator (LangGraph) | feat/orchestrator | Done | 5f94461 | Stub graph with route→rewrite→context→plan→execute→verify→finalize; run state persisted | Emits worklog/status events; completion immediate stub |
| Memory + RAG (LanceDB) | feat/memory-rag | Done | 365ab53 | Memory facts store + RAG placeholders added | LanceDB/embedding deferred; stubs in place |
| UI scaffold | feat/ui-scaffold | Not started |  |  |  |
| UI panels | feat/ui-panels | Not started |  |  |  |
| Cost meter hooks | feat/cost-meter | Not started |  |  |  |
| Tests + polish | test/polish | Not started |  |  |  |

## Current decisions (keep updated)
- Runtime: Ollama
- UI: React + Vite
- Backend: FastAPI
- Orchestrator: LangGraph
- DB: SQLite
- Vector DB: LanceDB
- Tool safety: approvals required for ALL sensitive actions
- Cloud: disabled by default; approval-gated if enabled
