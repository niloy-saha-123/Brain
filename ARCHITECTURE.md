# ARCHITECTURE.md — brain (v0.1)

**Status:** Implementation spec (source of truth)  
**Target:** macOS, local-first, Python backend + React/Vite UI  
**Design goals:** safe-by-default, receipts not narration, approvals for sensitive actions, parallel runs, local memory/RAG, optional cloud with explicit approval.

---

## 1) System overview

### 1.1 What “brain” is
A local-first AI agent operating system that provides:
- Minimal chat UI
- Brain/Router that chooses agents/tools/models and rewrites input into canonical task specs
- Agents with editable system prompts and tool permissions
- Tool execution with approval gates and receipts
- Local memory (facts/preferences) + RAG over approved folders
- Parallel jobs and live progress (Work Log)
- Optional cloud calls (approval + budget + reason + estimate)

### 1.2 What “brain” is NOT (v0.1)
- No silent autonomy. Anything risky requires user approval.
- No full GUI automation (mouse/keyboard).
- No multi-user accounts.

---

## 2) Repository layout (required)

```

brain/
idea.md
task.md
mistakes.md
ARCHITECTURE.md
README.md
SETUP.md
PROGRESS.md
LICENSE
.gitignore

backend/
pyproject.toml
app/
main.py
core/
config.py
ids.py
time.py
errors.py
api/
health.py
chat.py
runs.py
agents.py
approvals.py
receipts.py
memory.py
config.py
db/
sqlite.py
migrate.py
schema.sql
repo_agents.py
repo_runs.py
repo_messages.py
repo_approvals.py
repo_receipts.py
repo_memory.py
repo_budgets.py
schemas/
task_spec.py
agent.py
tool_call.py
receipt.py
approval.py
events.py
llm/
base.py
ollama.py
router.py
prompt_templates.py
token_estimate.py
orchestrator/
graph.py
state.py
nodes/
route.py
rewrite.py
context.py
plan.py
execute.py
verify.py
finalize.py
tools/
base.py
registry.py
policy.py
runner.py
impl/
filesystem.py
terminal.py
git.py
web.py
todo.py
ide_patch.py
memory/
store.py
facts.py
rag.py
lancedb_store.py
embed.py
chunk.py
dedup.py
events/
bus.py
sse.py
tests/
test_health.py
test_policy.py
test_approvals.py
test_receipts.py
test_runs.py

ui/
package.json
vite.config.ts
src/
main.tsx
api/
client.ts
sse.ts
components/
Chat.tsx
WorkLog.tsx
AgentsPanel.tsx
AgentEditor.tsx
ApprovalsInbox.tsx
RunsPanel.tsx
ReceiptsViewer.tsx
CostMeter.tsx
pages/
App.tsx
styles.css

```

---

## 3) Core data contracts (schemas)

All internal and API payloads must validate via Pydantic models.

### 3.1 Canonical Task Spec (compact keys)

**Purpose:** minimize tokens + create deterministic runtime contract.

```json
{
  "v": 1,
  "id": "tsk_...",
  "g": "goal string",
  "u": "original user message (optional, may be truncated)",
  "a": "agent_id or null",
  "c": { "constraints": "..." },
  "o": { "output_requirements": "..." },
  "pol": {
    "allow_web": false,
    "allow_cloud": false,
    "require_approval": true
  },
  "ctx": {
    "mem": ["mem_id..."],
    "rag": ["source#chunk_id..."],
    "rcpt": ["r_id..."]
  },
  "bdg": {
    "ctx_tok": 1200,
    "out_tok": 600,
    "cloud_usd_cap": 5
  }
}
```

Rules:

* `v` required.
* `id` required and stable for a run.
* Use short keys internally; UI can display expanded labels.
* The Brain/Router produces this object.

### 3.2 Agent Spec (editable brain)

Stored both as file (`agents/<agent_id>.json` in v0.1) and indexed in SQLite.

```json
{
  "v": 1,
  "agent_id": "agent_code",
  "name": "Code Agent",
  "description": "Writes patches and explains changes.",
  "system_prompt": "Full system prompt text (editable).",
  "tools_allow": ["filesystem.read", "git.diff"],
  "tools_deny": [],
  "risk_level": "medium",
  "model_pref": "general",
  "memory_policy": {
    "can_write_facts": true,
    "fact_tags": ["project", "preference"],
    "default_ttl_days": null
  },
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "version": 1
}
```

Rules:

* `system_prompt` is visible and editable in UI.
* Tool permissions enforced by policy engine.
* `risk_level` influences required approvals.

### 3.3 Tool Call

```json
{
  "v": 1,
  "tool": "terminal.run",
  "args": { "cmd": "ls -la", "cwd": "/some/path" },
  "risk": "high",
  "needs_approval": true,
  "reason": "User requested listing files.",
  "run_id": "run_..."
}
```

### 3.4 Receipt (tool receipt)

Every tool invocation generates a receipt, stored in SQLite and optionally mirrored as JSONL in `state/receipts.jsonl`.

```json
{
  "v": 1,
  "receipt_id": "r_000123",
  "run_id": "run_...",
  "tool": "terminal.run",
  "ok": true,
  "ts": "ISO8601",
  "request": { "cmd": "ls -la", "cwd": "/..." },
  "result": {
    "stdout": "...",
    "stderr": "",
    "exit_code": 0,
    "files_touched": [],
    "artifacts": []
  },
  "diff": null,
  "redactions": ["..."]
}
```

Rules:

* Never store secrets in receipts.
* Large outputs may be truncated; full output saved as artifact with path in `artifacts`.

### 3.5 Approval request / decision

```json
{
  "v": 1,
  "approval_id": "appr_...",
  "run_id": "run_...",
  "type": "terminal|file_read|file_write|git_commit|web_fetch|cloud_call|message_send|web_post",
  "status": "pending|approved|denied|edited",
  "created_at": "ISO8601",
  "resolved_at": null,
  "request": {
    "summary": "Run terminal command: git status",
    "details": { "...": "..." },
    "risk": "high",
    "cost_estimate_usd": 0.02
  },
  "decision": {
    "action": "approve|deny|edit",
    "edited_details": null,
    "user_note": ""
  }
}
```

Rules:

* If `type=cloud_call`, must include cost estimate (rough is ok in v0.1).
* If edited, tool args must be replaced with edited version.

### 3.6 Event stream (SSE)

All events follow:

```json
{
  "v": 1,
  "run_id": "run_...",
  "ts": "ISO8601",
  "type": "worklog|token|status|receipt|approval_requested|error",
  "data": { }
}
```

Event types:

* `worklog`: `{ "msg": "Planning step 1/4: ..." }`
* `token`: `{ "text": "partial model output" }`
* `status`: `{ "status": "running|awaiting_approval|completed|failed|cancelled" }`
* `receipt`: `{ "receipt_id": "r_..." }`
* `approval_requested`: `{ "approval_id": "appr_..." }`
* `error`: `{ "message": "...", "where": "node/tool/etc" }`

---

## 4) Runtime components & responsibilities

### 4.1 Backend (FastAPI)

* Provides REST endpoints
* Maintains in-process run manager and event bus
* Orchestrates runs via LangGraph
* Stores everything in SQLite
* Talks to Ollama
* Executes tools through Tool Runner

### 4.2 UI (React/Vite)

* Consumes REST + SSE
* Displays chat + multi-run threads
* Shows Work Log messages in-line
* Has Agents panel with prompt editor
* Approvals inbox
* Runs + receipts viewer
* Cost meter

### 4.3 Local LLM (Ollama)

* Local-first inference.
* Router/general/coder models configured in backend config.
* Cloud optional, approval-gated.

---

## 5) Database schema (SQLite)

SQLite file stored under `state/` (default), path configurable via `BRAIN_STATE_DIR`.

### 5.1 Tables

#### agents

* agent_id TEXT PK
* name TEXT
* description TEXT
* system_prompt TEXT
* tools_allow JSON TEXT
* tools_deny JSON TEXT
* risk_level TEXT
* model_pref TEXT
* memory_policy JSON TEXT
* version INT
* created_at TEXT
* updated_at TEXT

#### runs

* run_id TEXT PK
* status TEXT
* created_at TEXT
* started_at TEXT
* ended_at TEXT
* active_agent_id TEXT NULL
* task_spec JSON TEXT
* model_usage JSON TEXT
* cost_estimate_usd REAL
* cost_actual_usd REAL

#### messages

* msg_id TEXT PK
* run_id TEXT
* role TEXT (user|assistant|system|agent)
* content TEXT
* created_at TEXT

#### approvals

* approval_id TEXT PK
* run_id TEXT
* type TEXT
* status TEXT
* request JSON TEXT
* decision JSON TEXT NULL
* created_at TEXT
* resolved_at TEXT NULL

#### receipts

* receipt_id TEXT PK
* run_id TEXT
* tool TEXT
* ok INT
* ts TEXT
* request JSON TEXT
* result JSON TEXT
* diff TEXT NULL

#### memory_facts

* mem_id TEXT PK
* key TEXT
* value JSON/TEXT
* source TEXT
* confidence REAL
* tags JSON TEXT
* created_at TEXT
* ttl TEXT NULL

#### budgets

* month TEXT PK (YYYY-MM)
* cap_usd REAL
* spent_usd REAL

#### todos

* todo_id TEXT PK
* text TEXT
* status TEXT (open|done)
* created_at TEXT
* updated_at TEXT

---

## 6) Approvals policy (hard rules)

Approvals are required for:

* any cloud model call
* any terminal command
* any filesystem read (v0.1 conservative)
* any filesystem write
* any git commit
* any web fetch (GET) (v0.1 conservative)
* any web POST/form submission
* any messaging/email action
* any action involving other people or security-sensitive operations

Policy engine should decide:

* allow (no approval) — only safe local actions like todo add, internal computations
* require approval — default for almost everything in v0.1
* deny — disallowed tools or disallowed paths

---

## 7) Tool system

### 7.1 Tool registry

Tools implement a base interface:

* `name`
* `risk_level`
* `args_schema` (Pydantic)
* `requires_approval(args, context)` -> bool
* `execute(args, context)` -> Receipt

### 7.2 Tools (v0.1)

* `filesystem.read`
* `filesystem.write`
* `terminal.run`
* `git.status`
* `git.diff`
* `git.commit`
* `web.fetch` (GET only)
* `todo.add` / `todo.list` / `todo.complete`
* `ide.patch` (generates patch artifact)

### 7.3 File access rules (v0.1)

* No fixed workspace path.
* Tool must ask approval before accessing any path.
* If approved, that single path (or folder) is temporarily allowlisted for the run.
* Writes default to a configured workspace root if set, otherwise only to explicitly approved paths.

### 7.4 Tool runner (execution)

* v0.1: run tools in-process for simplicity.
* Ensure terminal tool:

  * never interpolates user text into shell unsafely
  * uses subprocess with args list when possible
  * logs receipts and truncates large outputs
* v0.2: optional Docker sandbox.

---

## 8) Orchestration (LangGraph)

### 8.1 Run state machine

Run statuses:

* `queued`
* `running`
* `awaiting_approval`
* `completed`
* `failed`
* `cancelled`

### 8.2 Graph nodes

#### route

Inputs: user message, optional @agent
Outputs: selected agent_id + initial worklog
Rules:

* If @agent specified, use it.
* If Brain believes mismatch, it emits a worklog suggestion but proceeds.

#### rewrite

Outputs canonical task spec (compact JSON).
Must emit worklog explaining what it inferred.

#### context

Retrieves:

* relevant memory_facts (by tags/keys)
* RAG chunks if enabled and user approved indexing
  Limits: top-k 3–6; enforce token budget.

#### plan

Produces a minimal plan (not chain-of-thought):

* list of steps
* expected tool calls
  Emits worklog steps.

#### execute

Executes plan:

* before each tool call, policy check:

  * if approval needed -> create approval, emit approval_requested, set run awaiting, stop execution
  * else execute tool and create receipt event
* resumes after approval resolution

#### verify

Ensures:

* any tool claim references receipts
* citations exist for RAG claims
  If missing, corrects response or asks user.

#### finalize

Creates final assistant output and stores:

* messages
* memory updates if deemed important
  Emits status completed.

---

## 9) Memory & RAG

### 9.1 Facts/preferences memory

* Stored in `memory_facts`.
* Auto-save based on importance filter:

  * user preferences (tone, approvals, formatting)
  * agent definitions
  * stable project facts
* Provide UI button “Save to memory” that forces storing selected content.

### 9.2 RAG indexing

* Requires user approval per folder.
* Chunk text and code separately.
* Use local embeddings only.
* Store in LanceDB with metadata: source path, hash, timestamps.

### 9.3 Retrieval

* Retrieve top-k 3–6.
* De-dup by similarity.
* Cite sources as `path#chunk_id`.

---

## 10) Cost meter & budgets

### 10.1 Local usage

* Estimate token usage for display (rough ok).
* Track model calls count.

### 10.2 Cloud usage (optional)

* Disabled by default.
* If enabled, every call requires approval and records:

  * estimate cost
  * final cost if provider returns usage
* Enforce monthly cap (default $5).

---

## 11) UI behavior details

### 11.1 Chat view

* Shows multiple run threads in chronological order.
* Each run shows:

  * assistant output (streamed tokens)
  * Work Log (streamed events)
  * receipts references
  * approval requests inline with actions

### 11.2 Agents panel

* List agents
* Create agent:

  * name + description
  * optional tool list + risk
* Edit agent:

  * system prompt text editor
  * tool allow/deny lists
  * model preference
  * save creates new version

### 11.3 Approvals inbox

* List pending approvals
* Expand shows:

  * command/path/url/tool args
  * risk level
  * cost estimate if cloud
* Buttons:

  * approve
  * deny
  * edit args then approve

### 11.4 Runs/Receipts panel

* Select run_id
* Show receipts list with expand to view stdout/stderr, exit code, artifacts.

### 11.5 Cost meter

* Show:

  * local model used
  * (optional) cloud spend and cap

---

## 12) Testing requirements (minimum)

* Approvals required for each sensitive tool.
* Receipt created for every tool execution.
* Run transitions:

  * running -> awaiting_approval -> running -> completed
* SSE event stream:

  * emits worklog/status/approval_requested
* RAG indexing requires approval.

---

## 13) Implementation constraints for Codex

* Never commit to main.
* Branch per milestone.
* Update PROGRESS.md and README verified notes per milestone.
* No system installs; write instructions in SETUP.md.
