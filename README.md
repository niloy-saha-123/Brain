# brain

Local-first AI agent operating system for macOS: modular agents, approvals + receipts, parallel runs, and local memory/RAG. Local by default (Ollama), cloud only with explicit approval.

## What this is
A minimal chat UI backed by a Brain/Router that:
- rewrites requests into canonical task specs
- selects specialized agents
- runs tools safely with approvals
- logs receipts for every action
- keeps local memory + RAG
- can run multiple tasks concurrently

## Development workflow (IMPORTANT: no work on main)

### Branch rules
- Never commit to `main`.
- Work is done in milestone branches only (see list below).
- After each milestone, update `README.md` with a “Verified step …” note.

### Milestone branch names
- feat/backend-skeleton
- feat/db-schema
- feat/schemas
- feat/ollama-client
- feat/sse-events
- feat/tools-receipts
- feat/approvals
- feat/orchestrator
- feat/memory-rag
- feat/ui-scaffold
- feat/ui-panels
- feat/cost-meter
- test/polish

### Merge checklist (you do this manually)
For each milestone branch:
1) Pull latest main
2) Merge milestone branch into main (or create PR and merge)
3) Confirm it runs locally
4) Tag the milestone as done in PROGRESS.md (see below)

---

## Progress tracking (so the AI never loses state)
We use **PROGRESS.md** as the single source of truth for what’s done.
Every milestone must update:
- status (Not started / In progress / Done)
- commit hash(es)
- what was verified
- any manual setup steps

If you switch IDEs or the AI loses context, the next AI reads PROGRESS.md and continues correctly.

## Setup
See `SETUP.md`.

## Verified steps
- Verified step 0: repo initialized with specs + workflow files.
- Verified step 1: backend skeleton with health endpoints and CORS is in place.
- Verified step 2: SQLite schema, migrations, and DB repos are implemented.
- Verified step 3: Pydantic schemas added with JSON schema export utility.
- Verified step 4: Ollama client with streaming and /debug/llm endpoint is available.
- Verified step 5: SSE event bus with /runs/{run_id}/events streaming endpoint is available.
- Verified step 6: Tool system skeleton with approvals/receipts endpoints is available.
- Verified step 7: Approval gating publishes requests/resolutions and is wired to events/runner.
- Verified step 8: Orchestrator stubs (route→rewrite→context→plan→execute→verify→finalize) and run state are in place.
- Verified step 9: Memory/RAG placeholders added (facts store + RAG stubs).
