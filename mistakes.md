# Mistakes & Debug Log (for the coding agent)

Purpose:
- Track recurring mistakes the coding agent makes while implementing this repo.
- For each mistake: record symptom → root cause → fix → prevention rule.

---

## Format (always use this template)

### Mistake #N — <short title>
**Date:**  
**Area:** backend/ui/llm/tools/orchestrator/db  
**Symptom:**  
**What we expected:**  
**What happened instead:**  
**Root cause:**  
**Fix applied:**  
**Files changed:**  
**How we verified:**  
**Prevention rule:**  
**Notes / alternate fixes tried:**  

---

## Known likely pitfalls (pre-fill)

### Mistake #1 — SSE streaming freezes or drops events
**Symptom:** UI stops updating mid-run.  
**Likely causes:** blocking sync code in async path; generator exceptions; buffering; CORS.  
**Fix ideas:** asyncio.Queue per run; heartbeat events; reconnect logic; test with curl.  
**Prevention:** heartbeat event every 5s.

### Mistake #2 — Approvals deadlock (run never resumes)
**Symptom:** run stuck in `awaiting_approval`.  
**Likely causes:** approval resolved but orchestrator not notified; wrong run_id.  
**Fix ideas:** store approval->run mapping; resume event; idempotent resume endpoint.  
**Prevention:** integration test approval resolves.

### Mistake #3 — Tool claims without receipts
**Symptom:** assistant says “I ran X” but no record.  
**Fix ideas:** enforce verify node: any action claim must cite receipt ids.  
**Prevention:** hard rule in finalizer.

### Mistake #4 — File access escapes workspace
**Symptom:** tool reads/writes outside allowed area.  
**Fix ideas:** path normalization; explicit approvals for non-workspace paths.  
**Prevention:** tests for path traversal.

### Mistake #5 — RAG becomes noisy
**Symptom:** irrelevant chunks.  
**Fix ideas:** top-k small; de-dup; metadata filter.  
**Prevention:** retrieval budget enforcement.

### Mistake #6 — Ollama model missing
**Symptom:** model not found errors.  
**Fix ideas:** startup checks; user instructions.  
**Prevention:** setup doc.

### Mistake #7 — Concurrency causes slowdowns/OOM
**Symptom:** system becomes very slow or crashes.  
**Fix ideas:** semaphores; dynamic context caps; pause indexing during heavy inference.  
**Prevention:** global concurrency limit.