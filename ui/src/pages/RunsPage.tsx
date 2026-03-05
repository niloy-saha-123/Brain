import React, { useEffect, useState } from 'react'
import { fetchRuns } from '../api/client'

const RunsPage: React.FC = () => {
  const [rows, setRows] = useState<any[]>([])

  useEffect(() => {
    fetchRuns().then(setRows).catch(() => setRows([]))
  }, [])

  return (
    <div className="panel">
      <div className="panel-header">Runs</div>
      <table className="table">
        <thead>
          <tr>
            <th>Status</th>
            <th>Run ID</th>
            <th>Agent</th>
            <th>Started</th>
            <th>Duration</th>
            <th>Cost est.</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr><td colSpan={7}>No runs yet</td></tr>
          )}
          {rows.map((r) => (
            <tr key={r.run_id}>
              <td>{r.status}</td>
              <td>{r.run_id}</td>
              <td>{r.active_agent_id || '-'}</td>
              <td>{r.started_at || r.created_at}</td>
              <td>{r.ended_at ? 'done' : '-'}</td>
              <td>{r.cost_estimate_usd ?? 0}</td>
              <td><a className="btn" href={`/receipts?run_id=${r.run_id}`}>Receipts</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RunsPage
