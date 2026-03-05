import React from 'react'

const sample = [
  { id: 'w1', msg: 'Run started', ts: 'now' },
  { id: 'w2', msg: 'Planning stub', ts: 'now' },
]

const WorklogPage: React.FC = () => {
  return (
    <div className="panel">
      <div className="panel-header">Work Log</div>
      <div className="list">
        {sample.map((item) => (
          <div key={item.id} className="list-item">
            <div className="label">{item.ts}</div>
            <div>{item.msg}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default WorklogPage
