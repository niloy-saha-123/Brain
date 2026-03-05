"""Context retrieval using facts + RAG."""
from __future__ import annotations

from app.orchestrator.state import RunState
from app.memory import facts, rag


def load_context(state: RunState) -> RunState:
    retrieved_facts = facts.list_facts(limit=5)
    rag_hits = rag.retrieve(state.task_spec.g, k=3)
    state.context_facts = retrieved_facts
    state.context_rag = rag_hits
    state.add_worklog(f"Loaded context: {len(retrieved_facts)} fact(s), {len(rag_hits)} RAG hit(s).")
    return state
