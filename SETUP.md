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