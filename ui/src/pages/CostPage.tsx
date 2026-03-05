import React, { useEffect, useState } from 'react'
import { API_BASE } from '../api/client'

type CostSummary = {
  month: string
  budget: { cap_usd: number; spent_usd: number; remaining_usd: number }
  cloud: { enabled: boolean; cost_per_1k_tokens: number }
  runs_cost_usd: number
  models: { model: string; total_tokens: number; prompt_tokens: number; completion_tokens: number; cost_estimate_usd: number; cloud?: boolean }[]
}

const CostPage: React.FC = () => {
  const [summary, setSummary] = useState<CostSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    const fetchSummary = async () => {
      try {
        const resp = await fetch(`${API_BASE}/costs/summary`)
        if (!resp.ok) {
          throw new Error(`HTTP ${resp.status}`)
        }
        const data = (await resp.json()) as CostSummary
        if (!cancelled) {
          setSummary(data)
        }
      } catch (err) {
        if (!cancelled) {
          setError('Unable to load cost summary')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }
    fetchSummary()
    return () => {
      cancelled = true
    }
  }, [])

  const tiles = [
    { label: 'Monthly cap', value: summary ? `$${summary.budget.cap_usd.toFixed(2)}` : '$0.00' },
    { label: 'Spent', value: summary ? `$${summary.budget.spent_usd.toFixed(2)}` : '$0.00' },
    { label: 'Remaining', value: summary ? `$${summary.budget.remaining_usd.toFixed(2)}` : '$0.00' },
    { label: 'Runs cost', value: summary ? `$${summary.runs_cost_usd.toFixed(4)}` : '$0.0000' },
  ]

  return (
    <div className="panel">
      <div className="panel-header">
        <div>Cost</div>
        <div className="badge">{summary ? `Month ${summary.month}` : 'Loading'}</div>
      </div>

      {loading && <div className="panel" style={{ minHeight: 80 }}>Loading summary…</div>}
      {error && <div className="panel error">Error: {error}</div>}

      {!loading && !error && (
        <>
          <div className="grid">
            {tiles.map((t) => (
              <div key={t.label} className="panel" style={{ minHeight: 72 }}>
                <div className="label">{t.label}</div>
                <div>{t.value}</div>
              </div>
            ))}
          </div>

          <div className="panel" style={{ marginTop: 12 }}>
            <div className="panel-header">By model</div>
            {summary && summary.models.length === 0 && <div className="empty">No model usage yet</div>}
            {summary && summary.models.length > 0 && (
              <table className="table">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Tokens</th>
                    <th>Prompt</th>
                    <th>Completion</th>
                    <th>Cost</th>
                    <th>Cloud</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.models.map((m) => (
                    <tr key={m.model}>
                      <td>{m.model}</td>
                      <td>{m.total_tokens}</td>
                      <td>{m.prompt_tokens}</td>
                      <td>{m.completion_tokens}</td>
                      <td>${m.cost_estimate_usd.toFixed(6)}</td>
                      <td>{m.cloud ? 'Yes' : 'No'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          <div className="panel" style={{ marginTop: 12 }}>
            <div className="panel-header">Cloud controls</div>
            {summary && (
              <div>
                <div>Status: {summary.cloud.enabled ? 'Enabled (approval required)' : 'Disabled'}</div>
                <div>Rate (est): ${summary.cloud.cost_per_1k_tokens.toFixed(4)} per 1k tokens</div>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

export default CostPage
