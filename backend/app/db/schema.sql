PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    tools_allow TEXT,
    tools_deny TEXT,
    risk_level TEXT,
    model_pref TEXT,
    memory_policy TEXT,
    version INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    started_at TEXT,
    ended_at TEXT,
    active_agent_id TEXT,
    task_spec TEXT,
    model_usage TEXT,
    cost_estimate_usd REAL,
    cost_actual_usd REAL
);

CREATE TABLE IF NOT EXISTS messages (
    msg_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs (run_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_messages_run_id ON messages (run_id);

CREATE TABLE IF NOT EXISTS approvals (
    approval_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT NOT NULL,
    request TEXT NOT NULL,
    decision TEXT,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (run_id) REFERENCES runs (run_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_approvals_run_id ON approvals (run_id);
CREATE INDEX IF NOT EXISTS idx_approvals_status ON approvals (status);

CREATE TABLE IF NOT EXISTS receipts (
    receipt_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    tool TEXT NOT NULL,
    ok INTEGER NOT NULL,
    ts TEXT NOT NULL,
    request TEXT NOT NULL,
    result TEXT NOT NULL,
    diff TEXT,
    FOREIGN KEY (run_id) REFERENCES runs (run_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_receipts_run_id ON receipts (run_id);

CREATE TABLE IF NOT EXISTS memory_facts (
    mem_id TEXT PRIMARY KEY,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    source TEXT,
    confidence REAL,
    tags TEXT,
    created_at TEXT NOT NULL,
    ttl TEXT
);
CREATE INDEX IF NOT EXISTS idx_memory_key ON memory_facts (key);

CREATE TABLE IF NOT EXISTS budgets (
    month TEXT PRIMARY KEY,
    cap_usd REAL NOT NULL,
    spent_usd REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS todos (
    todo_id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rag_allowlist (
    path TEXT PRIMARY KEY,
    approval_id TEXT NOT NULL,
    approved_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rag_chunks (
    chunk_id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding TEXT,
    hash TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_path ON rag_chunks (path);

CREATE TABLE IF NOT EXISTS fs_allowlist (
    run_id TEXT NOT NULL,
    path TEXT NOT NULL,
    approval_id TEXT NOT NULL,
    approved_at TEXT NOT NULL,
    PRIMARY KEY (run_id, path),
    FOREIGN KEY (run_id) REFERENCES runs (run_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS planner_traces (
    run_id TEXT PRIMARY KEY,
    trace TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs (run_id) ON DELETE CASCADE
);
