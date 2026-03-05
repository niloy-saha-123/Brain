import React, { useEffect, useState } from 'react'
import { fetchApprovals, resolveApproval } from '../api/client'

type Approval = {
  approval_id: string
  request: { summary?: string; risk?: string }
  status: string
  created_at?: string
}

const ApprovalsPage: React.FC = () => {
  const [approvals, setApprovals] = useState<Approval[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const selected = approvals.find((a) => a.approval_id === selectedId)

  useEffect(() => {
    loadApprovals()
  }, [])

  async function loadApprovals() {
    try {
      const data = await fetchApprovals()
      setApprovals(data)
      if (!selectedId && data.length > 0) setSelectedId(data[0].approval_id)
    } catch {
      setApprovals([])
    }
  }

  async function handleDecision(action: string) {
    if (!selected) return
    await resolveApproval(selected.approval_id, action)
    await loadApprovals()
    setSelectedId(null)
  }

  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Queue</div>
        {approvals.length === 0 && <div className="empty">No pending approvals</div>}
        {approvals.length > 0 && (
          <div className="list">
            {approvals.map((a) => (
              <div key={a.approval_id} className="list-item" onClick={() => setSelectedId(a.approval_id)} style={{ cursor: 'pointer' }}>
                <div className="label">{a.approval_id}</div>
                <div>{a.request?.summary || a.approval_id}</div>
                <div>Risk: {a.request?.risk || 'unknown'}</div>
                <div>{a.created_at}</div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="panel">
        <div className="panel-header">Details</div>
        {selected ? (
          <div className="drawer">
            <div className="label">{selected.approval_id}</div>
            <div>{selected.request?.summary}</div>
            <div>Risk: {selected.request?.risk || 'unknown'}</div>
            <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
              <button className="btn primary" onClick={() => handleDecision('approved')}>Approve</button>
              <button className="btn" onClick={() => handleDecision('denied')}>Reject</button>
            </div>
          </div>
        ) : (
          <div className="empty">No approval selected</div>
        )}
      </div>
    </div>
  )
}

export default ApprovalsPage
