# task_v0.3.md — Build Plan (v0.3)

## Theme
**Planner v2: multi-step plans + trace + UI visibility**

We are upgrading from “simple/rule-based plan” to a deterministic, traceable planner that:
- selects an agent (even if agents are basic)
- produces a 2–4 step plan using existing tools and/or LLM steps
- predicts which steps require approval
- persists a planner trace per run
- streams plan + progress to UI
- shows planned steps + predicted approvals in UI

## Constraints (non-negotiable)
- **No new tools** (reuse existing tool set).
- **No cloud calls** (local-only).
- Keep approvals gating behavior as-is (planner predicts/visualizes, but existing pause/resume remains source of truth).
- All existing tests must still pass.
- Add new tests for planner behavior and trace persistence.

## Definition of Done (v0.3)
A run created from the UI must:
1) show the full planned steps before execution begins
2) show predicted approvals on those steps
3) stream step-by-step progress events
4) pause on approvals and resume correctly
5) persist the planner trace and allow viewing it after completion
6) successfully complete at least one **multi-step run**:
   - Example A: filesystem.read → LLM summarize → filesystem.write (approval)
   - Example B: web.fetch → LLM summarize → todo.add

---

## Branching rules for v0.3
- Work on a dedicated branch: **feat/v0.3-planner-v2**
- Do not merge to main until user verifies.

---

## Milestone 1 — Planner contracts + trace persistence (backend only)

### Goals
- Define planner input/output schemas
- Add “PlannerTrace” persistence in SQLite
- Add SSE event types to stream plan and step progress
- Ensure traces are viewable via API

### Backend changes
1) Add schemas:
   - `PlannerStep`
   - `PlannerDecision`
   - `PlannerTrace`
   - `PredictedApproval`
2) Update DB schema:
   - Add table `planner_traces` (run_id PK, trace JSON, created_at)
3) Add repos:
   - `repo_planner_traces.py` with upsert/get methods
4) Add API:
   - `GET /runs/{run_id}/plan` → returns trace
   - (optional) `GET /runs/{run_id}/trace` alias
5) SSE events:
   - `plan_ready` event once plan generated
   - `step_started` event when a step begins
   - `step_completed` event when a step finishes
   - `step_paused_for_approval` when approval triggered
6) Ensure this does not break current run system.

### Required fields (planner output contract)
Planner output must include:
- `selected_agent_id` (string or "default")
- `skills` (array, empty for now)
- `steps` (2–4 steps)
- `predicted_approvals` (array mapping step_id → required approval types/tools)

### Tests
- Unit test: planner trace saved and loadable for a run
- Unit test: plan_ready event emitted

### Acceptance
- Starting a run generates a stored trace, retrievable via `/runs/{id}/plan`

---

## Milestone 2 — Planner v2 implementation (deterministic heuristics + tests)

### Goals
- Implement planner that outputs **2–4 steps**
- Use deterministic heuristics (no ML, no big scoring model)
- Predict approvals correctly based on tool policy

### Implementation requirements
Planner must handle at least these goal patterns:

1) **"list files"**
   - step 1: filesystem.read (directory listing path; approval predicted)
   - step 2: todo.add (“review files list”) (optional)
2) **"summarize X" where X is a file**
   - step 1: filesystem.read (approval predicted)
   - step 2: LLM summarize (no approval)
3) **"save summary to Y"**
   - step 3: filesystem.write (approval predicted)
4) **"fetch URL and summarize"**
   - step 1: web.fetch (approval predicted)
   - step 2: LLM summarize (no approval)
5) **"terminal check"**
   - step 1: terminal.run (approval predicted)
   - step 2: todo.add (optional)

#### Step types
A planner step can be:
- `tool` (calls an existing tool)
- `llm` (calls local LLM for transform/summarize)
- `noop` (rare; allowed for placeholders)

### Execute engine updates
- The orchestrator execute node must:
  - iterate steps
  - emit step_started/step_completed
  - pause/resume on approvals with step context
  - continue after approval resolution

### Tests
- Unit test: given goal “summarize README and save to notes.txt” produces ≥3 steps
- Unit test: approvals predicted for filesystem.read + filesystem.write
- Integration-style backend test: run pauses for approval and resumes to completion

### Acceptance
- Planner produces multi-step plans and the run actually executes them end-to-end.

---

## Milestone 3 — UI: plan visibility + approvals prediction + step progress

### Goals
- UI shows planned steps before execution
- UI shows predicted approvals
- UI shows step progress live
- UI can open and view planner trace for a completed run

### UI requirements
1) Chat page:
   - After starting a run, show:
     - “Plan” section listing steps (with step status: pending/running/paused/completed)
     - “Predicted approvals” markers per step
   - Update step status live via SSE events
2) Worklog page:
   - show run list (existing)
   - add “View plan” action that opens plan trace
3) Runs page:
   - add link to plan/trace view
4) No need for fancy animations; must be functional.

### Acceptance
- You can start a multi-step run and watch steps change in UI.
- You can refresh and still view the stored plan trace.

---

## Verification checklist update (must update VERIFY.md)
Add v0.3 verification steps:
1) Start run “summarize backend/app/main.py and save summary to /tmp/brain_summary.txt”
2) Confirm plan shows ≥3 steps before execution.
3) Confirm predicted approvals are shown on read/write steps.
4) Approve read/write when prompted.
5) Run completes and trace is viewable after refresh.

---

## Notes / Out of scope for v0.3
- No full skill library integration yet (skills[] reserved only)
- No new tools
- No cloud model routing
- No packaging as a desktop app
