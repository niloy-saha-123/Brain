
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
| UI scaffold | feat/ui-scaffold | Done | 4b6a74c | Vite/React app scaffolded with stub panels and base styling | package.json/vite config added; panels stubbed |
| UI panels | feat/ui-panels | Done | e2205c1 | Monochrome boxy layout with sidebar/topbar, routed panels, status pills | Requires npm install after dependency update |
| Cost meter hooks | feat/cost-meter | Done | 97fffcb | /costs/summary returns budget + model usage; Cost UI shows data; debug/llm records usage with run_id; cloud calls require approval flag when enabled | Cloud off by default; set BRAIN_CLOUD_ENABLED/BRAIN_CLOUD_BUDGET_USD to enable; npm install may update ui/package-lock |
| Tests + polish | test/polish | Done | 1d582b8 | python -m pytest app/tests (uses temp DB, anyio asyncio backend); health endpoints respond; orchestrator executes todo.add with events and resumes after approvals; UI wired to APIs/SSE | anyio_backend fixture pins asyncio; temp state dir per test; security guards: path normalize, SSRF block, truncation, safer git commit; fix plan tracked in PR_NOTES |

## v0.2 Milestones (backlog)
| Milestone | Branch | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Agents CRUD (backend + UI wiring) | feat/v0.2-agents | Done | db91211 | python -m pytest app/tests; UI Agents page can create/update/delete agents via API | Branch work tracked on feat/v0.2-backlog; agent_id auto if blank |
| Orchestrator planning + multi-tool execution | feat/v0.2-orchestrator | Done | a9e49e2 | python -m pytest app/tests; start run with goal 'terminal' pauses for approval; resolve approval then resume_run_after_approval completes remaining steps | Plan builds tool list (todo/web/filesystem/terminal); step index tracking resumes after approvals; supports multiple approvals |
| Memory/RAG indexing + retrieval + citations | feat/v0.2-rag | Done | bc4d973 | python -m pytest app/tests; POST /rag/index for a folder -> approval required -> resolve -> chunks stored; GET /rag/search returns citations | hash-based local embeddings; optional LanceDB fallback; allowlist records approval_id per path |
| Security hardening (paths/SSRF/redaction/artifacts) | feat/v0.2-security | Done | 00bc7e9 | python -m pytest app/tests; filesystem.read requires approval and allowlist then succeeds; web.fetch blocks 127.0.0.1; terminal output over 2k chars writes artifact | Added fs_allowlist table; receipts/artifacts truncation/redaction; stronger SSRF guard |
| Hotfix: approvals parsing + filesystem dir read | feat/v0.2-hotfix-approvals-fs | Done | d4ee0e7 | python -m pytest app/tests; approval resolve works when request stored as JSON string; filesystem.read on directory returns entries list | Added dir listing result for filesystem.read; approval resolve parses stored JSON strings |

## v0.3 Milestones
| Milestone | Branch | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Planner contracts + trace persistence | feat/v0.3-planner-v2 | Done | TBD | python -m pytest app/tests; GET /runs/{run_id}/plan returns stored trace | Adds planner schemas, planner_traces table, plan_ready/step events, trace API |
| Planner v2 execution (deterministic multi-step) | feat/v0.3-exec | Not started |  |  | Multi-step planner with approvals prediction and execution |
| UI plan visibility + approvals prediction | feat/v0.3-ui | Not started |  |  | Show plan/predicted approvals/step progress in UI |

## v0.3 Milestones (proposed)
| Milestone | Branch (to create) | Status | Last commit | Verification | Notes |
|---|---|---|---|---|---|
| Planner design + scoring model | feat/v0.3-planner | Not started |  |  | Define planner contracts, scoring factors, store planner traces |
| Planner execution engine | feat/v0.3-exec | Not started |  |  | Implement scoring-based planner selecting tools/agent, predict approvals, emit trace/worklog |
| UI surfaces for planner + approvals | feat/v0.3-ui | Not started |  |  | Show plan/trace/predicted approvals in Chat/Worklog |

## Current decisions (keep updated)
- Runtime: Ollama
- UI: React + Vite
- Backend: FastAPI
- Orchestrator: LangGraph
- DB: SQLite
- Vector DB: LanceDB
- Tool safety: approvals required for ALL sensitive actions
- Cloud: disabled by default; approval-gated if enabled
