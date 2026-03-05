# Build Plan (v0.2) — Backlog Milestones

Order (must follow):
1) Agents CRUD (backend + UI wiring)
2) Orchestrator: real plan → tool selection → approvals → execution for at least 3 tools
3) Memory/RAG: approved folder indexing + LanceDB + retrieval + citations
4) Security hardening: filesystem allowlists per approval, SSRF protections, output artifacting/redaction

Rules:
- Work on branches matching `feat/v0.2-*` (one per milestone).
- Do not merge to main until each milestone is verified.
- Update PROGRESS.md and PR_NOTES.md after each milestone.
