import React from 'react'

const receipts = [
  { id: 'r_1', tool: 'terminal.run', ts: 'now', run: 'demo' },
]

const ReceiptsPage: React.FC = () => {
  const selected = receipts[0]
  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Receipts</div>
        <div className="list">
          {receipts.map((r) => (
            <div key={r.id} className="list-item">
              <div className="label">{r.id}</div>
              <div>{r.tool}</div>
              <div>{r.ts}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="panel">
        <div className="panel-header">Details</div>
        {selected ? (
          <div className="code-block">{JSON.stringify(selected, null, 2)}</div>
        ) : (
          <div className="empty">Select a receipt</div>
        )}
        <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
          <button className="btn">Copy JSON</button>
          <button className="btn">Download</button>
        </div>
      </div>
    </div>
  )
}

export default ReceiptsPage
