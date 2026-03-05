export const API_BASE = 'http://localhost:8000'

export async function postRun(goal: string): Promise<string> {
  const resp = await fetch(`${API_BASE}/runs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ goal }),
  })
  if (!resp.ok) {
    throw new Error(`Failed to start run: ${resp.status}`)
  }
  const data = await resp.json()
  return data.run_id
}

export async function fetchRuns() {
  const resp = await fetch(`${API_BASE}/runs`)
  if (!resp.ok) throw new Error('Failed to fetch runs')
  return resp.json()
}

export async function fetchApprovals() {
  const resp = await fetch(`${API_BASE}/approvals`)
  if (!resp.ok) throw new Error('Failed to fetch approvals')
  return resp.json()
}

export async function resolveApproval(approvalId: string, action: string) {
  const resp = await fetch(`${API_BASE}/approvals/${approvalId}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action }),
  })
  if (!resp.ok) throw new Error('Failed to resolve approval')
  return resp.json()
}

export async function fetchReceipts(runId: string) {
  const resp = await fetch(`${API_BASE}/runs/${runId}/receipts`)
  if (!resp.ok) throw new Error('Failed to fetch receipts')
  return resp.json()
}
