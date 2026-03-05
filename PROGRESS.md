
---

# 7) `PROGRESS.md`

# Progress Tracker (Single Source of Truth)

**Rule:** Every milestone branch must update this file before stopping.

## Milestones
| Milestone | Branch | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Backend skeleton + health | feat/backend-skeleton | Done | c294f18 | Start uvicorn; GET /health returns ok; GET /health/ollama returns ok or 503 gracefully | Install backend deps; Ollama optional but required for healthy ollama response; response_model annotation fixed |
| SQLite schema + repos | feat/db-schema | Done | a570184 | App startup runs migrations; tables exist (agents, runs, messages, approvals, receipts, memory_facts, budgets, todos); repo CRUD helpers in db/repo_* | DB lives under state/brain.db by default; override with BRAIN_STATE_DIR/BRAIN_DB_FILE |
| Schemas (Pydantic + JSON schema export) | feat/schemas | Not started |  |  |  |
| Ollama client (streaming) | feat/ollama-client | Not started |  |  |  |
| SSE event bus | feat/sse-events | Not started |  |  |  |
| Tools + receipts | feat/tools-receipts | Not started |  |  |  |
| Approvals inbox + gating | feat/approvals | Not started |  |  |  |
| Orchestrator (LangGraph) | feat/orchestrator | Not started |  |  |  |
| Memory + RAG (LanceDB) | feat/memory-rag | Not started |  |  |  |
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
