# Build Plan (v0.1) — Step-by-step Task List

## 0) Repo setup
- Keep `idea.md`, `task.md`, `mistakes.md`, `SETUP.md`, `PROGRESS.md` updated.
- Never work directly on `main`.

---

## 1) Backend skeleton (FastAPI)
- Create backend skeleton.
- Add:
  - `GET /health`
  - `GET /health/ollama` (pings Ollama)
- Add CORS for UI.

Acceptance:
- Server starts and health endpoints return.

---

## 2) SQLite schema + repos
Create tables:
- agents
- runs
- messages
- approvals
- receipts
- memory_facts
- budgets

Acceptance:
- Tables created; basic CRUD functions exist.

---

## 3) Schemas
Add Pydantic models:
- TaskSpec (compact keys)
- AgentSpec
- ToolCall
- Receipt
- ApprovalRequest/Decision
Export JSON schemas into `backend/app/schemas/`.

Acceptance:
- Validation works; invalid payloads rejected.

---

## 4) Ollama client
Implement streaming Ollama client.
Add model registry:
- router_model
- general_model
- coder_model (optional)
Add dynamic context cap per request.

Acceptance:
- `POST /debug/llm` streams output.

---

## 5) SSE events (Work Log + tokens + receipts)
Implement SSE event bus:
- events: worklog/token/receipt/status/approval_requested
Add `GET /runs/{run_id}/events`

Acceptance:
- curl and UI can stream events.

---

## 6) Tools + receipts (approval-gated)
Tools:
- file read (approval required)
- file write (approval required; restricted to workspace unless path approved)
- terminal (approval required; any command)
- git status/diff (approval required)
- git commit (approval required)
- web fetch GET (approval required)
- todo tool (local; no approval)
- IDE patch tool (produces patch artifacts; approval to apply)

Receipts store:
- input args, stdout/stderr, exit code, timestamps, files touched, diffs/hashes

Acceptance:
- Tools execute only after approval; receipts viewable.

---

## 7) Approvals inbox
- `GET /approvals` (pending)
- `POST /approvals/{id}/resolve` (approve/deny/edit)
- Orchestrator pauses runs awaiting approvals and resumes after resolve.

Acceptance:
- tool call triggers approval; approving resumes.

---

## 8) Orchestrator graph (LangGraph)
Nodes:
- route → rewrite → context → plan → execute → verify → finalize

Acceptance:
- Run shows phases and emits Work Log + receipts.

---

## 9) Memory + RAG (LanceDB)
- Index user-approved folder(s)
- Chunk/embed/store
- Retrieve top-k small (3–6) with de-dup
- Cite sources `source_uri#chunk_id`

Acceptance:
- Ask question; answer cites sources.

---

## 10) UI scaffold (React + Vite)
Panels:
- Chat (+ SSE)
- Work Log inline
- Agents list + editor + create agent
- Approvals inbox
- Runs/Receipts viewer
- Cost meter panel

Acceptance:
- Full loop works end-to-end.

---

## 11) Cost meter hooks
- Track model used
- Estimate tokens
- Cloud disabled by default; approval-gated if enabled

Acceptance:
- Cloud path blocked unless approved; budget shown.

---

## 12) Tests + polish
- approvals required tests
- receipts integrity tests
- basic run lifecycle tests
- README + SETUP updates

Acceptance:
- Minimal tests pass; docs accurate.