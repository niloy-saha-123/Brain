import React, { useEffect, useState } from 'react'
import { fetchReceipts, fetchRuns } from '../api/client'

const ReceiptsPage: React.FC = () => {
  const [runId, setRunId] = useState<string>('')
  const [runs, setRuns] = useState<any[]>([])
  const [receipts, setReceipts] = useState<any[]>([])
  const [selected, setSelected] = useState<any | null>(null)

  useEffect(() => {
    fetchRuns().then(setRuns).catch(() => setRuns([]))
  }, [])

  async function loadReceipts() {
    if (!runId) return
    try {
      const data = await fetchReceipts(runId)
      setReceipts(data)
      setSelected(data[0] || null)
    } catch {
      setReceipts([])
      setSelected(null)
    }
  }

  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Receipts</div>
        <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
          <select className="input" value={runId} onChange={(e) => setRunId(e.target.value)}>
            <option value="">Select run</option>
            {runs.map((r) => (
              <option key={r.run_id} value={r.run_id}>{r.run_id} ({r.status})</option>
            ))}
          </select>
          <button className="btn primary" onClick={loadReceipts}>Load</button>
        </div>
        <div className="list">
          {receipts.map((r: any) => (
            <div key={r.receipt_id} className="list-item" onClick={() => setSelected(r)} style={{ cursor: 'pointer' }}>
              <div className="label">{r.ts}</div>
              <div>{r.receipt_id}</div>
              <div>{r.tool}</div>
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
