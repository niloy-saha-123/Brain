
---

# 7) `PROGRESS.md`

```markdown
# Progress Tracker (Single Source of Truth)

**Rule:** Every milestone branch must update this file before stopping.

## Milestones
| Milestone | Branch | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Backend skeleton + health | feat/backend-skeleton | Not started |  |  |  |
| SQLite schema + repos | feat/db-schema | Not started |  |  |  |
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