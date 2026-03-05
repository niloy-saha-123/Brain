import React from 'react'

const approvals = [
  { id: 'appr_1', summary: 'terminal.run "echo hi"', risk: 'high', ts: 'now' },
]

const ApprovalsPage: React.FC = () => {
  const selected = approvals[0]
  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Queue</div>
        <div className="list">
          {approvals.map((a) => (
            <div key={a.id} className="list-item">
              <div className="label">{a.id}</div>
              <div>{a.summary}</div>
              <div>Risk: {a.risk}</div>
              <div>{a.ts}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="panel">
        <div className="panel-header">Details</div>
        {selected ? (
          <div className="drawer">
            <div className="label">{selected.id}</div>
            <div>{selected.summary}</div>
            <div>Risk: {selected.risk}</div>
            <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
              <button className="btn primary">Approve</button>
              <button className="btn">Reject</button>
              <button className="btn">View receipt</button>
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
