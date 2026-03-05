import React from 'react'
import Chat from '../components/Chat'
import WorkLog from '../components/WorkLog'
import AgentsPanel from '../components/AgentsPanel'
import ApprovalsInbox from '../components/ApprovalsInbox'
import RunsPanel from '../components/RunsPanel'
import ReceiptsViewer from '../components/ReceiptsViewer'
import CostMeter from '../components/CostMeter'

const App: React.FC = () => {
  return (
    <div className="app-shell">
      <header className="app-header">brain</header>
      <main className="app-main">
        <section className="panel chat"><Chat /></section>
        <section className="panel worklog"><WorkLog /></section>
        <section className="panel agents"><AgentsPanel /></section>
        <section className="panel approvals"><ApprovalsInbox /></section>
        <section className="panel runs"><RunsPanel /></section>
        <section className="panel receipts"><ReceiptsViewer /></section>
        <section className="panel cost"><CostMeter /></section>
      </main>
    </div>
  )
}

export default App
