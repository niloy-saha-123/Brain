# VERIFY (v0.2)

## 1) Commands to run locally (macOS)

Backend:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
(Requires Python ≥3.11 with deps from `pyproject.toml`; no extra env vars needed. Optional: set `BRAIN_STATE_DIR` to change DB location.)

UI:
```bash
cd ui
npm install   # only once or when deps change
npm run dev   # starts Vite on http://localhost:5173
```

Ollama (for LLM tests/costs):
```bash
ollama serve   # ensure a model like llama3.2:3b is pulled
```

## 2) Manual test plan (end-to-end)

1) **Start backend and UI**
   - Run commands above. Open http://localhost:5173.
   - Expected: UI loads with black sidebar; connection pills show “API: Connected” / “SSE: Connected” (or Off if SSE not yet).

2) **Start a run from Chat**
   - On `/chat`, enter goal: `list files` and click **Send**.
   - Expected: New run thread appears with status `queued` → `running`; worklog shows planning/execution messages.

3) **Observe SSE worklog/status**
   - Watch worklog list update without refresh.
   - Expected: status pill updates to `running` then `completed` (or `awaiting_approval` in next step).

4) **Trigger an approval (terminal.run)**
   - Send goal: `terminal check`.
   - Expected: Status switches to `awaiting_approval`; worklog notes approval requested; `/approvals` shows new pending item.

5) **Approve in Approvals page**
   - Navigate to `/approvals`, select the pending approval, click **Approve**.
   - Expected: Approval list refreshes; run resumes automatically (status back to `running` then `completed`).

6) **Confirm receipt creation**
   - Back on `/chat`, receipts panel shows a new receipt entry; alternatively GET `http://localhost:8000/runs/<run_id>/receipts`.
   - Expected: receipt includes tool name (`terminal.run`) and exit code 0.

7) **Create/edit agent**
   - Go to `/agents`, click **Add**, fill name/description, save.
   - Edit the same agent and change description.
   - Expected: Agent list updates; refresh page → changes persist (verified via GET `/agents`).

8) **RAG index and citations**
   - In Chat “Index folder” panel, enter a repo subfolder path (e.g., `backend/app`) and click **Index**.
   - Expected: If approval required, status shows pending with approval_id; approve in `/approvals`; after completion, status shows chunks indexed.
   - Send a goal mentioning a file term (e.g., `memory facts`); worklog completes; context panel shows RAG hits with citations like `.../file.py#chunkN`. Final output includes `Citations: ...` (from finalize node).

9) **Cost meter sanity (optional)**
   - GET `http://localhost:8000/costs/summary`.
   - Expected: JSON with budget remaining and model usage entries if Ollama calls were made.

## 3) Expected outcomes (per step)
- Backend serves 200 on `/health`, UI loads.
- Chat run statuses transition via SSE: queued → running → awaiting_approval (when triggering terminal/web) → completed.
- Approvals page lists pending, approve resolves to `approved` and clears queue.
- Receipts list shows entries with `ok: 1`, request/result payloads, artifact paths if output truncated.
- Agents CRUD persists across reloads.
- RAG search returns hits and citations appear in finalize output; artifacts stored under `backend/state/artifacts` if large.

## 4) Common failure modes & debugging
- **SSE not updating**: Check backend logs (uvicorn stdout). Verify `GET /runs/{run_id}/events` reachable; CORS allowed in `app/main.py`. Reload UI.
- **Approvals stuck**: GET `http://localhost:8000/approvals`; if pending remains, ensure approve via POST `/approvals/{id}/resolve` with `{"action":"approved"}`. Confirm run status via `GET /runs/{run_id}`.
- **Filesystem path denied**: Tools require approval allowlist per run; ensure approval granted, then rerun with `approval_id` (UI does this automatically after approval).
- **SSRF blocked**: web.fetch rejects private/loopback hosts by design; use public http/https URLs.
- **Large output missing**: Runner truncates >2000 chars and writes artifact under `backend/state/artifacts`; check that folder.
- **DB location issues**: If state dir missing permissions, set `BRAIN_STATE_DIR=/tmp/brain_state` before starting uvicorn.
