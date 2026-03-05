import React from 'react'

const CostPage: React.FC = () => {
  return (
    <div className="panel">
      <div className="panel-header">Cost</div>
      <div className="grid">
        {['Today', '7d', '30d', 'By model'].map((label) => (
          <div key={label} className="panel" style={{ minHeight: 60 }}>
            <div className="label">{label}</div>
            <div>$0.00</div>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 12 }}>
        <table className="table">
          <thead>
            <tr>
              <th>Day</th>
              <th>Spend</th>
              <th>Run</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Today</td>
              <td>$0.00</td>
              <td>-</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CostPage
