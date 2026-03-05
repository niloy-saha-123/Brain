import React, { useEffect, useState } from 'react'
import { postRun, fetchReceipts, searchRag, indexRag, fetchFacts } from '../api/client'
import { subscribeToRun, RunEvent } from '../api/sse'

type Message = { role: string; text: string }

const ChatPage: React.FC = () => {
  const [goal, setGoal] = useState('')
  const [runId, setRunId] = useState<string | null>(null)
  const [status, setStatus] = useState('idle')
  const [worklog, setWorklog] = useState<string[]>([])
  const [messages, setMessages] = useState<Message[]>([])
  const [receipts, setReceipts] = useState<any[]>([])
  const [ragHits, setRagHits] = useState<any[]>([])
  const [facts, setFacts] = useState<any[]>([])
  const [indexPath, setIndexPath] = useState('')
  const [indexStatus, setIndexStatus] = useState<string | null>(null)

  useEffect(() => {
    if (!runId) return
    const stop = subscribeToRun(runId, handleEvent)
    return () => stop()
  }, [runId])

  useEffect(() => {
    fetchFacts().then(setFacts).catch(() => setFacts([]))
  }, [])

  async function handleSubmit() {
    if (!goal.trim()) return
    const newRun = await postRun(goal.trim())
    setRunId(newRun)
    setStatus('queued')
    setWorklog([])
    setMessages([{ role: 'user', text: goal.trim() }])
    setReceipts([])
    setGoal('')
    searchRag(goal.trim()).then((res) => setRagHits(res.hits || [])).catch(() => setRagHits([]))
  }

  function handleEvent(ev: RunEvent) {
    if (ev.type === 'status') {
      setStatus(ev.status)
      if (ev.status === 'completed' && runId) {
        fetchReceipts(runId).then(setReceipts).catch(() => {})
      }
    }
    if (ev.type === 'worklog' && ev.msg) {
      setWorklog((w) => [...w, ev.msg])
    }
    if (ev.type === 'receipt') {
      setWorklog((w) => [...w, `Receipt created: ${ev.receipt_id}`])
    }
    if (ev.type === 'approval_requested') {
      setWorklog((w) => [...w, `Approval requested: ${ev.approval_id}`])
      setStatus('awaiting_approval')
    }
  }

  async function handleIndex() {
    if (!indexPath.trim()) return
    setIndexStatus('pending')
    try {
      const res = await indexRag(indexPath.trim())
      if (res.status === 'pending') {
        setIndexStatus(`pending approval ${res.approval_id}`)
      } else {
        setIndexStatus(`indexed ${res.chunks_indexed} chunks`)
      }
    } catch {
      setIndexStatus('failed')
    }
  }

  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Threads</div>
        {runId ? (
          <div className="list">
            <div className="list-item">
              <div><strong>{runId}</strong></div>
              <div>Status: {status}</div>
            </div>
          </div>
        ) : (
          <div className="empty">No threads yet</div>
        )}
      </div>
      <div className="panel">
        <div className="panel-header">
          <div>Conversation</div>
          <span className="pill" style={{ marginLeft: 8 }}>Status: {status}</span>
        </div>
        <div className="list" style={{ minHeight: 200 }}>
          {messages.length === 0 && <div className="empty">No messages yet</div>}
          {messages.map((m, idx) => (
            <div key={idx} className="list-item">
              <strong>{m.role}</strong>
              <div>{m.text}</div>
            </div>
          ))}
          {worklog.map((w, idx) => (
            <div key={`wl-${idx}`} className="list-item">
              <strong>Worklog</strong>
              <div>{w}</div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 12 }}>
          <textarea className="textarea" rows={3} placeholder="Type a message" value={goal} onChange={(e) => setGoal(e.target.value)} />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn primary" onClick={handleSubmit}>Send</button>
            <button className="btn" onClick={() => setGoal('')}>Clear</button>
          </div>
        </div>
        {receipts.length > 0 && (
          <div className="panel" style={{ marginTop: 12 }}>
            <div className="panel-header">Receipts</div>
            {receipts.map((r: any) => (
              <div key={r.receipt_id} className="code-block">
                {JSON.stringify(r, null, 2)}
              </div>
            ))}
          </div>
        )}
        <div className="panel" style={{ marginTop: 12 }}>
          <div className="panel-header">Context</div>
          {ragHits.length === 0 && <div className="empty">No RAG hits</div>}
          {ragHits.length > 0 && (
            <div className="list">
              {ragHits.map((hit, idx) => (
                <div key={idx} className="list-item">
                  <div className="label">{hit.citation}</div>
                  <div>{hit.content}</div>
                  <div>Score: {hit.score?.toFixed(2)}</div>
                </div>
              ))}
            </div>
          )}
          {facts.length > 0 && (
            <div className="panel" style={{ marginTop: 8 }}>
              <div className="panel-header">Facts</div>
              <div className="list">
                {facts.map((f: any) => (
                  <div key={f.mem_id} className="list-item">
                    <div className="label">{f.key}</div>
                    <div>{String(f.value)}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div className="panel" style={{ marginTop: 12 }}>
          <div className="panel-header">Index folder</div>
          <input className="input" placeholder="/path/to/folder" value={indexPath} onChange={(e) => setIndexPath(e.target.value)} />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button className="btn primary" onClick={handleIndex}>Index</button>
            {indexStatus && <span className="label">{indexStatus}</span>}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
