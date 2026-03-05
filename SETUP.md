# Setup (Dev) — brain

This project is **dev-first**: run backend + UI locally.  
The codebase **does not** install system dependencies for you.

---

## 0) Prerequisites
- macOS
- Python 3.11+
- Node.js 18+
- pnpm (recommended)
- Git
- Ollama installed and running

Optional (later):
- Docker (only if enabling high-security shell sandbox mode)

---

## 1) Install Ollama (manual)

Option A — install the Ollama macOS app and ensure `ollama` CLI is in your PATH.  
Option B — install via script:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 2) Backend Python environment (manual)
Create or activate your Python 3.11 environment (conda/venv — managed by you). Then install backend dependencies (use `python -m pip` to avoid zsh globbing and ensure the env’s pip is used):

```bash
cd backend
python -m pip install -e ".[dev]"
```

---

## 3) Run the backend (local)

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health checks:
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/health/ollama`

---

## Environment variables
No required variables for milestone 4. Optional overrides (place in `backend/.env` or export in your shell):
- `BRAIN_APP_NAME` — app title; default `brain`
- `BRAIN_ENVIRONMENT` — runtime label; default `dev`
- `BRAIN_OLLAMA_BASE_URL` — Ollama base URL; default `http://localhost:11434`
- `BRAIN_CORS_ORIGINS` — comma-separated origins allowed for CORS; default `http://localhost:5173,http://127.0.0.1:5173`
- `BRAIN_LOG_LEVEL` — logging level; default `INFO`
- `BRAIN_STATE_DIR` — folder for local state (SQLite + artifacts); default `state` at repo root
- `BRAIN_DB_FILE` — SQLite filename; default `brain.db`
- `BRAIN_ROUTER_MODEL` — model for routing; default `llama3.2:3b`
- `BRAIN_GENERAL_MODEL` — model for general assistant; default `llama3.2:3b`
- `BRAIN_CODER_MODEL` — coder model; default `deepseek-coder:6.7b`
- `BRAIN_OLLAMA_TIMEOUT` — request timeout seconds; default `30`
- `BRAIN_OLLAMA_CTX` — max context window tokens; default `4096`
- `BRAIN_CLOUD_ENABLED` — set to `true` to allow cloud model paths (default `false`, still approval-gated)
- `BRAIN_CLOUD_BUDGET_USD` — monthly cloud spend cap; default `5`
- `BRAIN_CLOUD_COST_PER_1K` — estimated cloud cost per 1k tokens; default `0.0` (set if you enable cloud)

---

## Debug LLM endpoint
- Run backend, then POST/stream to `http://localhost:8000/debug/llm` with JSON body:
  ```json
  { "prompt": "Hello", "model": "deepseek-coder:6.7b", "stream": true }
  ```
  Response streams plain text tokens.
