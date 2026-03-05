# Local-first AI Agent Operating System (MacBook Pro M4) — Product & Architecture Spec

## 0) One-sentence pitch
A local-first “AI OS” with a minimal chat UI where a Brain routes tasks to specialized agents, executes tools safely with approvals and receipts, manages local memory/RAG, runs jobs in parallel, and only uses paid APIs when explicitly approved.

---

## 1) Goals

### Primary goals
- **Local-first**: default execution uses local LLMs.
- **Mostly free**: $0 daily operation; cloud is optional and approval-gated.
- **Honest by design**: no hallucinated actions. Any claim of tool execution must reference a receipt.
- **Transparent**: user can view/edit any agent’s system prompt (“brain”) from UI.
- **Safe**: approvals for any risky action (terminal, file access/write, git commit, web POST, messaging, cloud calls).
- **Parallel**: run multiple tasks/agents concurrently without blocking chat.
- **Extensible**: user can create new agents in one step (name + description), optionally specifying tools/risk; Brain can generate optimized prompts.

### Non-goals (v0.1)
- Fully autonomous internet actions without approval (job applications, emailing, form submissions).
- Full desktop GUI automation (mouse/keyboard) by default.
- Multi-user accounts.
- Always-on huge models (30B+ with massive contexts).

---

## 2) Product UX

### UI panels (v0.1)
1. **Chat**
   - Main interaction surface
   - Shows multiple concurrent job threads
2. **Work Log stream** (always visible or expandable)
   - explicit “what the system is doing”
   - step-by-step progress messages
3. **Agents**
   - list agents
   - click agent → view/edit system prompt and permissions
   - create agent (name + description)
4. **Approvals Inbox**
   - pending approvals with details (command, files, cost estimate)
   - Approve / Deny / Edit
5. **Runs & Receipts**
   - run timeline + statuses
   - expandable receipts (tool inputs/outputs)
6. **Cost meter**
   - local vs cloud usage
   - monthly cloud spend cap and current spend

### Streaming
- Stream assistant output and Work Log events (SSE first).
- No “hidden thinking.” We expose a **Work Log** we generate explicitly:
  - planning steps, tool start/end, receipt IDs, waiting on approval, etc.

---

## 3) Core concepts

### 3.1 Brain (Router/Coordinator)
Responsible for:
- Rewrite user message into canonical task spec (compact JSON).
- Select agent(s) (user may specify @agent; Brain can suggest override).
- Decide what tools are needed.
- Decide what memory/RAG context to retrieve.
- Decide what to store long-term (“meaningful memory filter”).
- Enforce **approval gates** and **cloud budget rules**.

### 3.2 Agents
Two types:
- **Lightweight agents**: system prompt + tool permissions + policies; run inside the main process.
- **Heavyweight agents** (v0.2+): separate workers with isolated tool scope/memory.

Agents are created from:
- Name + description (required)
- Allowed tools (optional)
- Risk level (optional; otherwise Brain decides)
- Agent system prompt is generated and then user-editable.

Agents are stored:
- As files in repo workspace (source-of-truth) + indexed in SQLite.

### 3.3 Tools
Must exist in v0.1:
- filesystem read
- filesystem write (restricted; always approval)
- terminal run command (always approval)
- git status/diff/commit (commit always approval)
- web fetch (GET) + optional “search” later (always approval)
- calendar/todo (todo local; calendar integrations later)
- IDE integration (Cursor/VSCode via patch/diff workflow)
- image generation (placeholder tool; local or API later; approval if cloud)

**Every tool call produces a receipt**.

### 3.4 Approvals
Approvals are mandatory for:
- any cloud model call
- any terminal command
- any file read/write outside approved scope (v0.1: assume all file access requires approval)
- any git commit
- any web POST/form submission
- sending messages/emails
- any action involving other people/internet/security

### 3.5 Receipts (Receipts-not-narration)
A receipt stores:
- tool name
- input args
- stdout/stderr
- exit code
- files touched
- timestamps
- hashes/diffs for writes
- ok/error
- artifact paths (if produced)

Agents must cite receipts when describing actions.

---

## 4) Local-first model strategy

### v0.1 runtime
- Local inference via **Ollama** (OpenAI-compatible style HTTP endpoints).

### Multi-model (default)
- Router model: small, fast (3B-ish)
- General model: main assistant (8B/14B-ish)
- Coder model: optional (heavier) for repo tasks

### Cloud
- Optional (kept in architecture), disabled by default or requires explicit approval.
- Budget cap: default `$5/month`.
- Any cloud call requires:
  - reason
  - cost estimate
  - approval record

---

## 5) Memory and RAG

### Memory tiers
1. **Rolling session summary** (auto updated)
2. **Durable facts/preferences memory**
   - stable preferences and facts
   - auto-save based on importance filter + manual “save memory” option
3. **RAG over local files**
   - only if user approves indexing
   - sources are shown as citations

### Storage
- SQLite: system-of-record (agents, runs, messages, approvals, receipts, budgets, facts)
- LanceDB: embeddings + chunks for RAG

### Indexing policy (v0.1)
- Default memory/index folder is not fixed.
- User chooses (or approves) folders to index.
- No silent indexing outside explicitly approved folders.

---

## 6) Security model

### Permissions
- Tools are permissioned per agent.
- Risk levels (low/med/high) guide approvals.
- Default conservative mode: approvals required for all sensitive actions.

### Isolation
- v0.1: process-level isolation + strict allowlists, workspace-only writes.
- v0.2: optional Docker sandbox for shell tools.

### Secrets
- Store API keys in `.env` locally (dev) and later OS keychain.
- Never log secrets into receipts.

---

## 7) Tech stack (v0.1)

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- LangGraph (orchestrator)
- SQLite (system DB)
- LanceDB (vector DB)
- Pydantic (schemas)
- httpx (HTTP client)

### Frontend
- React + Vite
- SSE client for streaming
- Minimal UI components

---

## 8) System architecture

### Core flow
User message
→ Brain: rewrite into canonical spec
→ Orchestrator graph: route/plan/execute/verify/finalize
→ Tools (approval-gated)
→ Receipts stored
→ Response + Work Log streamed to UI
→ Memory update (importance filtered)

### Parallelism
- Multiple runs/jobs concurrently.
- Concurrency caps:
  - 1 heavy generation at a time
  - router can run concurrently
  - tool I/O can run multiple (bounded)

---

## 9) Key edge cases to handle
- Ollama down / model missing
- out-of-memory from large contexts
- tool command injection from web/RAG content
- run stuck awaiting approval
- retrieval irrelevant context
- memory pollution
- large tool outputs (truncate + store artifact)

---

## 10) Deliverables (v0.1)
- Local-first chat UI with streaming Work Log
- Agent registry UI with editable prompts
- Approvals inbox
- Receipts viewer
- Local Ollama integration
- Tools: file/terminal/git/web(todo minimal)/ide patch
- SQLite persistence
- LanceDB indexing + RAG (approved folder)
- Parallel runs with bounded concurrency