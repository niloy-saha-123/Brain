## 0) Release candidate
- Branch/commit: `test/polish` @ `199e129` (latest; includes tests, doc updates, clean tree). This is the most complete branch and tagged as Done in `PROGRESS.md`.
- Package manager: npm is the documented and tested choice (see `SETUP.md` prereqs and `ui/README.md`). `ui/package-lock.json` is committed and current.

## 1) Repo map (high-level)
- Top-level:  
  - `backend/` – FastAPI backend, tools, orchestrator, DB repos, tests.  
  - `ui/` – React/Vite monochrome UI.  
  - Docs/spec: `idea.md`, `ARCHITECTURE.md`, `task.md`, `README.md`, `SETUP.md`, `PROGRESS.md`, `PR_NOTES.md`, `mistakes.md`.
- Backend app tree (key files):  
  - `app/main.py` (FastAPI app + router wiring)  
  - `app/api/{health,llm,receipts,approvals,costs}.py`, `events/sse.py`  
  - `app/tools/{base.py,policy.py,registry.py,runner.py,impl/*}`  
  - `app/db/{schema.sql,migrate.py,repo_*.py,sqlite.py}`  
  - `app/schemas/*.py` (task spec, agent, tool_call, receipt, approval, events)  
  - `app/orchestrator/{graph.py,state.py}`  
  - `app/memory/{facts.py,rag.py,...}` (stubs/placeholders)  
  - `app/llm/{ollama.py,router.py,token_estimate.py}`  
  - `app/core/{config.py,ids.py,time.py,costs.py,errors.py}`  
  - `app/tests/*`
- UI src tree (key files):  
  - `ui/src/main.tsx`, `ui/src/styles.css`  
  - `ui/src/components/{Layout.tsx,ConnectionPill.tsx,SSEStatus.tsx}`  
  - `ui/src/pages/{App.tsx,ChatPage.tsx,WorklogPage.tsx,AgentsPage.tsx,ApprovalsPage.tsx,RunsPage.tsx,ReceiptsPage.tsx,CostPage.tsx}`  
  - `ui/src/api/{client.ts,sse.ts}`

## 2) Feature inventory
Each item lists what/where/how/limitations.

### 2.1 UI features
- **Chat UX (multi-run threads)**  
  - What: Stub page with two-column layout ready for thread list + active chat (boxy rectangles).  
  - Where: `ui/src/pages/ChatPage.tsx` (panels, composer), layout in `components/Layout.tsx`, styles in `styles.css`.  
  - Verify: `npm run dev`, open `/chat`; see thread list stub left, conversation right with message boxes and composer.  
  - Limitations: No real data wiring or send logic; worklog/receipts not injected.
- **Streaming output**  
  - What: UI reserves header text “Streaming…” and uses SSE status pill; no live token stream.  
  - Where: `ChatPage.tsx` header; `components/SSEStatus.tsx`.  
  - Verify: Open `/chat`; observe “Streaming…” label and SSE pill.  
  - Limitations: No actual SSE hookup to chat text.
- **Work Log stream**  
  - What: Worklog panel stub with boxed list rows.  
  - Where: `ui/src/pages/WorklogPage.tsx`.  
  - Verify: `/worklog` shows empty-state boxed message.  
  - Limitations: No event consumption; details drawer stub only.
- **Agents panel**  
  - What: Table of agents with status/actions; modal/drawer placeholders.  
  - Where: `ui/src/pages/AgentsPage.tsx`.  
  - Verify: `/agents` renders table rows with stub data and action buttons.  
  - Limitations: No CRUD wiring to backend; prompts/permissions not persisted.
- **Approvals inbox**  
  - What: Two-column queue + detail pane with Approve/Reject buttons (UI only).  
  - Where: `ui/src/pages/ApprovalsPage.tsx`.  
  - Verify: `/approvals` shows boxed list and detail panel with buttons.  
  - Limitations: Not connected to `/approvals` API; counts static.
- **Runs panel + receipts viewer**  
  - What: Runs table with detail drawer; receipts page with list + JSON viewer.  
  - Where: `ui/src/pages/RunsPage.tsx`, `ui/src/pages/ReceiptsPage.tsx`.  
  - Verify: `/runs` and `/receipts` render tables and JSON block.  
  - Limitations: Static data; no API wiring.
- **Cost meter**  
  - What: Cost summary tiles, model usage table, cloud status box fed by backend `/costs/summary`.  
  - Where: `ui/src/pages/CostPage.tsx`.  
  - Verify: Start backend, open `/cost`; tiles show budget 5/0 spend, model table updates after debug LLM call.  
  - Limitations: Displays what backend reports; no charts; only budget/model summary.

### 2.2 Backend API endpoints
- `GET /health` – returns `{status, service, ts}`. Handler: `app/api/health.py::health`. No request body.  
- `GET /health/ollama` – pings Ollama tags; 200 ok or 503 with error detail. Handler: `health.py::health_ollama`.  
- `POST /debug/llm` – body `DebugLLMRequest` (prompt, model?, stream?, max_context?, options{}, run_id?, use_cloud?, approval_id?). Streams text/plain tokens. Handler: `app/api/llm.py::debug_llm`.  
- `GET /receipts/{receipt_id}` – returns single receipt dict or 404. Handler: `app/api/receipts.py::get_receipt`.  
- `GET /runs/{run_id}/receipts` – list receipts for run. Handler: `app/api/receipts.py::list_receipts`.  
- `GET /approvals` – list all approvals (pending & others). Handler: `app/api/approvals.py::list_approvals`.  
- `POST /approvals/{id}/resolve` – body `{"action": "approved"|"denied"|"edited", "decision": ...}`; updates approval and publishes event. Handler: `approvals.py::resolve_approval`.  
- `GET /runs/{run_id}/events` – SSE stream of events/heartbeat for run. Handler: `events/sse.py::sse_events`.  
- `GET /costs/summary` – returns budget, spend, model usage list, cloud config. Handler: `app/api/costs.py::get_cost_summary`.  
_(Other API stubs exist but not wired: `api/runs.py`, `api/chat.py`, etc.)_

### 2.3 Orchestrator behavior
- Nodes implemented: `start_run` simply marks run started/completed; no real route/rewrite/context/plan/execute logic.  
  - Where: `app/orchestrator/graph.py`, state container in `orchestrator/state.py`.  
  - Verify: call `start_run(TaskSpec(...))`; run persisted with status `completed` in SQLite (`runs` table).  
  - Limitations: No pausing/resuming on approvals, no concurrency caps, no multi-node graph execution.

### 2.4 Tools
- Registry and runner: `app/tools/registry.py` registers tools; `runner.py::run_tool` handles approval check, execution, receipt creation + events. Policy: `tools/policy.py` with `SENSITIVE_TOOLS` set.
- **filesystem.read** – approval required; reads file text. Path: `tools/impl/filesystem.py::FilesystemReadTool`. Verify: call `run_tool("filesystem.read", {"path": ...}, ctx)` after approval; returns `content`. Limitations: no path allowlist/normalization beyond expanduser; no traversal guard.  
- **filesystem.write** – approval required; writes text. `FilesystemWriteTool`. Verify similarly; returns bytes_written. Limitations: same safety gaps.  
- **terminal.run** – approval required. `tools/impl/terminal.py::TerminalTool`. Executes command via asyncio subprocess, returns stdout/stderr/exit_code. Limitations: no cwd/path guard; approval gate only.  
- **git.status / git.diff / git.commit** – approval required. `tools/impl/git.py::{GitStatusTool,GitDiffTool,GitCommitTool}`. Run git CLI; returns stdout/stderr/exit_code. Limitations: no repo validation, commit uses `git commit -am` (all tracked files).  
- **web.fetch (GET only)** – approval required. `tools/impl/web.py::WebFetchTool`. Returns status_code, headers, text. Limitations: no SSRF/hostname allowlist, no size cap.  
- **todo.add/list/complete** – no approval. `tools/impl/todo.py`. In-memory store; returns todo objects. Limitations: non-persistent.  
- **ide.patch** – approval required. `tools/impl/ide_patch.py` (creates patch text artifact). Verify via run_tool; returns patch string. Limitations: does not apply patch automatically.  
- Receipt fields: every tool returns `ToolResult` with request/result/diff (diff mostly None). Runner writes `receipts` table (see `db/repo_receipts.py`) with `ok`, timestamps, tool name.

### 2.5 Approvals system
- Types: whatever tool name requested; typically terminal/filesystem/git/web/cloud.  
- Creation: `run_tool` calls `_create_approval` when `policy.requires_approval` true and no `approval_id` in context; stored via `db/repo_approvals.py`.  
- Resolution: `POST /approvals/{id}/resolve` sets status/decision and publishes `approval_resolved` event (see `api/approvals.py`).  
- Resume behavior: orchestrator does not currently resume runs; runner simply raises `ToolError` with approval_id.  
- UI: Approvals inbox page stub (`ui/src/pages/ApprovalsPage.tsx`) shows list/detail/actions but not wired to API.

### 2.6 Receipts system
- Schema: `app/schemas/receipt.py`; DB table `receipts` in `db/schema.sql`; repos in `db/repo_receipts.py`. Stored fields: receipt_id, run_id, tool, ok, ts, request JSON, result JSON, diff.  
- Storage: `runner._store_receipt` inserts into SQLite, auto-creates run if missing. Optional JSONL artifact path not implemented.  
- Truncation: not implemented; full stdout/text stored.  
- Enforcement: No explicit “claim must cite receipt” logic; verify node is stubbed, so enforcement not active (limitation).

### 2.7 Memory + RAG
- Facts/preferences: `memory/facts.py` with `save_fact`, `list_facts`; table `memory_facts` in SQLite. Verify via Python REPL saving a fact and querying table.  
- Rolling summary: not implemented (limitation).  
- Folder indexing/RAG: stubs in `memory/{rag.py,lancedb_store.py,embed.py,chunk.py,dedup.py}`; no LanceDB dependency used. No approval flow for indexing implemented beyond planned comments.  
- Retrieval/citations/UI: not implemented.

### 2.8 Cost/budget
- Tracking: token heuristic (`llm/token_estimate.py`), model usage recording (`core/costs.py::record_model_usage`), cost summary endpoint (`api/costs.py`). Costs stored per run in `runs.model_usage` JSON + `cost_estimate_usd`; budgets table `budgets` in SQLite via `repo_budgets.py`.  
- Cloud disabled by default: `Settings.cloud_enabled=False`; `/debug/llm` enforces approval_id when `use_cloud=True`.  
- Approval gate for cloud: enforced only on `debug/llm` parameters; no other cloud tools present.  
- Limitations: Cost per 1k tokens default 0.0; no actual cloud calls or spend updates unless `is_cloud` passed.

## 3) Spec compliance checklist
| Requirement | Implemented? | Evidence | Notes |
| --- | --- | --- | --- |
| Health endpoints `/health`, `/health/ollama` | Yes | `api/health.py` | Ollama check returns 503 if down |
| SQLite tables (agents, runs, messages, approvals, receipts, memory_facts, budgets, todos) | Yes | `db/schema.sql`, `db/migrate.py` | LanceDB not used |
| Pydantic schemas (TaskSpec, AgentSpec, ToolCall, Receipt, Approval) + JSON export | Yes | `schemas/*.py`, `schemas/export.py` | Export utility present |
| Ollama streaming client + `/debug/llm` | Yes | `llm/ollama.py`, `api/llm.py` | No router selection logic beyond defaults |
| SSE event bus `/runs/{id}/events` | Yes | `events/bus.py`, `events/sse.py` | Heartbeat only; no run events emitted in practice |
| Tools + receipts with approval gating | Partial | `tools/*`, `runner.py`, `policy.py` | Approval created but run resume not wired; safety gaps (path/SSRF) |
| Approvals inbox endpoints | Yes | `api/approvals.py` | UI not wired |
| Orchestrator graph route→finalize | Partial | `orchestrator/graph.py` stub completes immediately | No real planning/execution/resume |
| Memory + RAG placeholders | Partial | `memory/*` | No real indexing/retrieval |
| UI scaffold/panels monochrome | Yes | `ui/src/pages/*`, `styles.css` | Data static |
| Cost meter hooks | Yes | `core/costs.py`, `api/costs.py`, `ui/src/pages/CostPage.tsx` | Costs heuristic only |
| Tests for approvals/receipts/runs/health/policy | Yes | `app/tests/*` | Integration/UI tests missing |

## 4) Test coverage
- Files:  
  - `tests/test_health.py` – health endpoints (ok + Ollama unreachable).  
  - `tests/test_policy.py` – approval policy sensitive vs safe.  
  - `tests/test_approvals.py` – approval created for terminal.run (FK-safe).  
  - `tests/test_receipts.py` – receipt recorded for todo.add.  
  - `tests/test_runs.py` – `start_run` persists completed status.  
  - `tests/conftest.py` – temp DB fixture, anyio backend fixture.
- Command: `cd backend && python -m pytest app/tests` (expects 7 passed, minor Pydantic warnings).
- Missing: end-to-end API/UI integration, SSE streaming content, filesystem/web/git tool execution tests, memory/RAG tests.

## 5) Security + safety review
- Path traversal protections: **Not implemented**. Filesystem tools use raw paths (expanduser only). TODO: normalize/resolve against approved roots and enforce allowlist.  
- Shell injection: Minimal; `terminal.run` uses `shlex.split` and subprocess exec; still executes arbitrary commands once approved. TODO: strict allowlist or sandbox.  
- SSRF protections: **Missing**. `web.fetch` allows arbitrary URLs (including localhost/file/metadata). TODO: deny localhost/169.254/::1/file schemes, add size/time limits.  
- Secrets redaction: Not implemented; receipts store full stdout/stderr/headers. TODO: redaction filters + truncation.  
- Approval bypass risks: Approval required for sensitive tools via `policy.py`, but orchestrator does not pause/resume; caller must supply approval_id manually. TODO: enforce run-state gating and block execution without resolved approval.  
- Git safety: `git.commit` commits all tracked changes (`-am`), no path restriction.  
- Cloud safety: Cloud disabled by default; cloud calls require `use_cloud`+`approval_id` on debug endpoint. No other cloud paths.

## 6) Manual verification checklist
1) **Backend install**  
   - `cd backend`  
   - `python -m pip install -e ".[dev]"`  
2) **Run backend**  
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`  
3) **Health**  
   - `curl http://localhost:8000/health` → status ok  
   - `curl http://localhost:8000/health/ollama` → ok (if Ollama up) or 503 (acceptable if down)  
4) **Cost summary baseline**  
   - `curl http://localhost:8000/costs/summary` → cap 5, spent 0, models []  
5) **LLM call + cost update**  
   - `curl -N -X POST http://localhost:8000/debug/llm -H "Content-Type: application/json" -d '{"prompt":"hi","run_id":"run_cost"}'`  
   - `curl http://localhost:8000/costs/summary` → models list includes llama3.2:3b with tokens ~8  
6) **Approval flow**  
   - `python - <<'PY'\nimport asyncio\nfrom app.tools.runner import run_tool\ntry:\n    asyncio.run(run_tool(\"terminal.run\", {\"cmd\":\"echo hi\"}, {\"run_id\":\"demo\"}))\nexcept Exception as e:\n    print(e)\nPY`  
   - `curl http://localhost:8000/approvals` → pending approval for terminal.run  
7) **Resolve approval** (choose approval_id from previous step)  
   - `curl -X POST "http://localhost:8000/approvals/<approval_id>/resolve" -H 'Content-Type: application/json' -d '{"action":"approved"}'` → {"status":"ok"}  
8) **Receipt check**  
   - `python - <<'PY'\nimport asyncio\nfrom app.tools.runner import run_tool\nasyncio.run(run_tool(\"todo.add\", {\"text\":\"test\"}, {\"run_id\":\"demo\"}))\nPY`  
   - `curl http://localhost:8000/runs/demo/receipts` → list contains todo.add receipt ok=1  
9) **SSE heartbeat**  
   - `curl -N http://localhost:8000/runs/test-run/events` → heartbeat events (stub)  
10) **Tests**  
    - `python -m pytest app/tests` → 7 passed  
11) **UI**  
    - `cd ui && npm install && npm run dev`  
    - Open `http://localhost:5173` and click through Chat, Worklog, Agents, Approvals, Runs, Receipts, Cost; Cost panel shows summary values.

## 7) What’s not done (v0.2 backlog)
- Full orchestrator graph (real route/rewrite/context/plan/execute/verify/finalize with tool calls and approvals resume).  
- Real chat/runs/agents/approvals UI wiring and data fetching.  
- Memory/RAG indexing, embeddings, retrieval, and citation display.  
- Robust safety: path normalization, SSRF blocking, output truncation/redaction, tighter git/terminal controls.  
- Cloud model integration and accurate cost tracking.  
- Worklog streaming of real events/tokens; richer SSE handling.  
- Rolling summaries and persisted todo store.  
- Integration tests and UI e2e tests.  
