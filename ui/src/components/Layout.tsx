import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import ConnectionPill from './ConnectionPill'
import SSEStatus from './SSEStatus'

const navItems = [
  { path: '/chat', label: 'Chat' },
  { path: '/worklog', label: 'Worklog' },
  { path: '/agents', label: 'Agents' },
  { path: '/approvals', label: 'Approvals' },
  { path: '/runs', label: 'Runs' },
  { path: '/receipts', label: 'Receipts' },
  { path: '/cost', label: 'Cost' },
]

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation()
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">brain</div>
        <ul className="nav-list">
          {navItems.map((item) => {
            const active = location.pathname.startsWith(item.path)
            return (
              <li key={item.path}>
                <NavLink to={item.path} className={`nav-item ${active ? 'active' : ''}`}>
                  <span>{item.label}</span>
                  <span className="nav-dot" aria-hidden />
                </NavLink>
              </li>
            )
          })}
        </ul>
      </aside>
      <div className="main-area">
        <header className="topbar">
          <div className="title">{location.pathname.replace('/', '') || 'chat'}</div>
          <div className="status-group">
            <ConnectionPill />
            <SSEStatus />
          </div>
        </header>
        <div className="page">{children}</div>
      </div>
    </div>
  )
}

export default Layout
