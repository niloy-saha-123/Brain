import React, { useEffect, useState } from 'react'
import { fetchRuns } from '../api/client'

const WorklogPage: React.FC = () => {
  const [runs, setRuns] = useState<any[]>([])

  useEffect(() => {
    fetchRuns().then(setRuns).catch(() => setRuns([]))
  }, [])

  return (
    <div className="panel">
      <div className="panel-header">Work Log</div>
      {runs.length === 0 && <div className="empty">No runs yet</div>}
      {runs.length > 0 && (
        <div className="list">
          {runs.map((run) => (
            <div key={run.run_id} className="list-item">
              <div className="label">{run.created_at}</div>
              <div><strong>{run.run_id}</strong> — {run.status}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default WorklogPage
