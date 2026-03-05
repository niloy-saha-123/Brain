import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from '../components/Layout'
import ChatPage from './ChatPage'
import WorklogPage from './WorklogPage'
import AgentsPage from './AgentsPage'
import ApprovalsPage from './ApprovalsPage'
import RunsPage from './RunsPage'
import ReceiptsPage from './ReceiptsPage'
import CostPage from './CostPage'

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/worklog" element={<WorklogPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/approvals" element={<ApprovalsPage />} />
          <Route path="/runs" element={<RunsPage />} />
          <Route path="/receipts" element={<ReceiptsPage />} />
          <Route path="/cost" element={<CostPage />} />
          <Route path="*" element={<Navigate to="/chat" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
