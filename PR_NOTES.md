# PR Notes — feat/ollama-client

## What changed
- Implemented Ollama client with streaming support and dynamic context window options.
- Added LLM base types and simple model registry (router/general/coder).
- Exposed POST `/debug/llm` endpoint to stream raw tokens for debugging.
- Extended config/env to set model names, context window, and timeout; updated setup/docs.
- Kept prior milestones (health, DB, schemas) intact.

## Files touched
- backend/app/llm/*.py (base, ollama, router, token_estimate, __init__)
- backend/app/api/llm.py
- backend/app/main.py
- backend/app/core/config.py
- backend/app/schemas/json/* (already present; unchanged)
- SETUP.md, README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. `cd backend && python -m pip install -e ".[dev]"` (if not already).
2. Ensure Ollama is running and models exist: `ollama list`.
3. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
4. Stream debug output:
   ```bash
   curl -N -X POST http://localhost:8000/debug/llm \
     -H 'Content-Type: application/json' \
     -d '{"prompt":"Hello","model":"deepseek-coder:6.7b","stream":true}'
   ```
   You should see streamed tokens; errors surface as `[error] ...`.

## Commands to run
- `cd backend && python -m pip install -e ".[dev]"`
- `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- `curl -N -X POST http://localhost:8000/debug/llm -H 'Content-Type: application/json' -d '{"prompt":"Hello","stream":true}'`
