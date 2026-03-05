export const SSE_BASE = 'http://localhost:8000'

export type RunEvent =
  | { type: 'status'; status: string; ts?: string; run_id: string }
  | { type: 'worklog'; msg: string; ts?: string; run_id: string }
  | { type: 'receipt'; receipt_id: string; run_id: string }
  | { type: 'approval_requested'; approval_id: string; run_id: string }
  | { type: 'approval_resolved'; approval_id: string; status: string; run_id: string }
  | { type: 'heartbeat'; run_id: string }
  | { type: string; [key: string]: any }

export function subscribeToRun(runId: string, onEvent: (ev: RunEvent) => void): () => void {
  const es = new EventSource(`${SSE_BASE}/runs/${runId}/events`)
  const handlers = ['status', 'worklog', 'receipt', 'approval_requested', 'approval_resolved', 'message']
  handlers.forEach((name) =>
    es.addEventListener(name, (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data)
        onEvent(data as RunEvent)
      } catch {
        /* ignore */
      }
    })
  )
  es.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data)
      onEvent(data as RunEvent)
    } catch {
      /* ignore */
    }
  }
  es.addEventListener('heartbeat', () => onEvent({ type: 'heartbeat', run_id: runId }))
  return () => es.close()
}
