# PR Notes — feat/memory-rag

## What changed
- Added memory facts store wrapper and helper to save/list facts (persist via repo_memory).
- Added placeholders for RAG pipeline (chunk, dedup, embed, LanceDB store, retrieve stub).
- No embedding or LanceDB integration yet—stubs only.

## Files touched
- backend/app/memory/store.py, facts.py, rag.py, lancedb_store.py, embed.py, chunk.py, dedup.py
- README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. Save a fact in REPL:
   ```python
   from app.memory.facts import save_fact, list_facts
   save_fact("pref.theme", "dark")
   list_facts()
   ```
2. Check DB: `sqlite3 backend/state/brain.db "select key,value from memory_facts limit 5;"` (adjust path if state dir differs).
3. RAG retrieve stub returns empty list: `from app.memory.rag import retrieve; retrieve("test")`

## Commands to run
- `cd backend && python -m pip install -e ".[dev]"` (if not already)
- `sqlite3 backend/state/brain.db "select count(*) from memory_facts;"`
