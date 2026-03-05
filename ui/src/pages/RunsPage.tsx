import React from 'react'

const RunsPage: React.FC = () => {
  const rows = [
    { id: 'run_orch', status: 'completed', agent: '-', started: 'now', duration: '0.1s', cost: '$0.00' },
  ]
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
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.status}</td>
              <td>{r.id}</td>
              <td>{r.agent}</td>
              <td>{r.started}</td>
              <td>{r.duration}</td>
              <td>{r.cost}</td>
              <td><button className="btn">Details</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RunsPage
