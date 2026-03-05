import React, { useEffect, useState } from 'react'
import { fetchAgents, createAgent, updateAgent, deleteAgent } from '../api/client'

type Agent = {
  agent_id: string
  name: string
  description: string
  system_prompt: string
  tools_allow: string[]
  tools_deny: string[]
  risk_level?: string
  model_pref?: string
}

const emptyForm = {
  agent_id: '',
  name: '',
  description: '',
  system_prompt: '',
  tools_allow: '',
  tools_deny: '',
  risk_level: '',
  model_pref: '',
}

const AgentsPage: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [form, setForm] = useState(emptyForm)
  const [statusMsg, setStatusMsg] = useState<string | null>(null)

  useEffect(() => {
    loadAgents()
  }, [])

  async function loadAgents() {
    try {
      const data = await fetchAgents()
      setAgents(data)
      if (data.length > 0 && !selectedId) {
        handleSelect(data[0])
      }
    } catch (e: any) {
      setStatusMsg(e.message || 'Failed to load agents')
    }
  }

  function handleSelect(agent: Agent) {
    setSelectedId(agent.agent_id)
    setForm({
      agent_id: agent.agent_id,
      name: agent.name,
      description: agent.description,
      system_prompt: agent.system_prompt,
      tools_allow: agent.tools_allow.join(', '),
      tools_deny: agent.tools_deny.join(', '),
      risk_level: agent.risk_level || '',
      model_pref: agent.model_pref || '',
    })
  }

  function parseList(input: string): string[] {
    return input
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
  }

  async function handleCreate() {
    setStatusMsg(null)
    const payload = {
      agent_id: form.agent_id || undefined,
      name: form.name,
      description: form.description,
      system_prompt: form.system_prompt,
      tools_allow: parseList(form.tools_allow),
      tools_deny: parseList(form.tools_deny),
      risk_level: form.risk_level || undefined,
      model_pref: form.model_pref || undefined,
    }
    const created = await createAgent(payload)
    setStatusMsg(`Created agent ${created.agent_id}`)
    setForm(emptyForm)
    setSelectedId(created.agent_id)
    await loadAgents()
  }

  async function handleUpdate() {
    if (!selectedId) return
    setStatusMsg(null)
    const payload = {
      name: form.name,
      description: form.description,
      system_prompt: form.system_prompt,
      tools_allow: parseList(form.tools_allow),
      tools_deny: parseList(form.tools_deny),
      risk_level: form.risk_level || undefined,
      model_pref: form.model_pref || undefined,
    }
    const updated = await updateAgent(selectedId, payload)
    setStatusMsg(`Updated ${updated.agent_id}`)
    await loadAgents()
  }

  async function handleDelete() {
    if (!selectedId) return
    await deleteAgent(selectedId)
    setStatusMsg(`Deleted ${selectedId}`)
    setSelectedId(null)
    setForm(emptyForm)
    await loadAgents()
  }

  function onChange(field: string, value: string) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  return (
    <div className="split">
      <div className="panel">
        <div className="panel-header">Agents</div>
        {agents.length === 0 && <div className="empty">No agents yet</div>}
        {agents.length > 0 && (
          <div className="list">
            {agents.map((a) => (
              <div
                key={a.agent_id}
                className="list-item"
                style={{ cursor: 'pointer', background: selectedId === a.agent_id ? '#f5f5f5' : '#fff' }}
                onClick={() => handleSelect(a)}
              >
                <div className="label">{a.agent_id}</div>
                <div><strong>{a.name}</strong></div>
                <div>{a.description}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel">
        <div className="panel-header">Details</div>
        <div className="drawer">
          <div className="label">Agent ID (auto if blank)</div>
          <input className="input" value={form.agent_id} onChange={(e) => onChange('agent_id', e.target.value)} placeholder="Optional on create" />
          <div className="label">Name</div>
          <input className="input" value={form.name} onChange={(e) => onChange('name', e.target.value)} />
          <div className="label">Description</div>
          <input className="input" value={form.description} onChange={(e) => onChange('description', e.target.value)} />
          <div className="label">System prompt</div>
          <textarea className="textarea" rows={4} value={form.system_prompt} onChange={(e) => onChange('system_prompt', e.target.value)} />
          <div className="label">Tools allow (comma separated)</div>
          <input className="input" value={form.tools_allow} onChange={(e) => onChange('tools_allow', e.target.value)} />
          <div className="label">Tools deny (comma separated)</div>
          <input className="input" value={form.tools_deny} onChange={(e) => onChange('tools_deny', e.target.value)} />
          <div className="label">Risk level</div>
          <input className="input" value={form.risk_level} onChange={(e) => onChange('risk_level', e.target.value)} placeholder="low/medium/high" />
          <div className="label">Model preference</div>
          <input className="input" value={form.model_pref} onChange={(e) => onChange('model_pref', e.target.value)} />

          <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
            <button className="btn primary" onClick={handleCreate}>Create</button>
            <button className="btn" onClick={handleUpdate} disabled={!selectedId}>Update</button>
            <button className="btn" onClick={handleDelete} disabled={!selectedId}>Delete</button>
          </div>
          {statusMsg && <div className="label" style={{ marginTop: 8 }}>{statusMsg}</div>}
        </div>
      </div>
    </div>
  )
}

export default AgentsPage
