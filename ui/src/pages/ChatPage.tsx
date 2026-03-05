import React from 'react'

const ChatPage: React.FC = () => {
  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Threads</div>
        <div className="empty">No threads yet</div>
      </div>
      <div className="panel">
        <div className="panel-header">Conversation <span className="pill" style={{ marginLeft: 8 }}>Streaming…</span></div>
        <div className="list" style={{ minHeight: 200 }}>
          <div className="list-item"><strong>User</strong><div>Say hello</div></div>
          <div className="list-item"><strong>Assistant</strong><div>Hello! (stub)</div></div>
        </div>
        <div style={{ marginTop: 12 }}>
          <textarea className="textarea" rows={3} placeholder="Type a message" />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn primary">Send</button>
            <button className="btn">Attach</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
