import React from 'react'

const AgentsPage: React.FC = () => {
  const rows = [
    { name: 'Default Agent', status: 'Idle', last: '—' },
  ]
  return (
    <div className="panel">
      <div className="panel-header">Agents</div>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Last Activity</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.name}>
              <td>{r.name}</td>
              <td>{r.status}</td>
              <td>{r.last}</td>
              <td>
                <button className="btn">View config</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default AgentsPage
