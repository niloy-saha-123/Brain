# PR Notes — feat/ui-scaffold

## What changed
- Added Vite/React scaffold with entrypoint, App page, and stub panels (Chat, WorkLog, Agents, Approvals, Runs, Receipts, Cost Meter).
- Added basic styling shell and API base placeholders.

## Files touched
- ui/index.html, package.json, tsconfig.json, vite.config.ts
- ui/src/main.tsx, src/pages/App.tsx, src/components/*.tsx, src/api/*.ts, src/styles.css
- README.md, PROGRESS.md, PR_NOTES.md

## How to verify
1. Install deps (user-run): `cd ui && npm install` (or pnpm/yarn).
2. `npm run dev` and open http://localhost:5173 — should render stub panels grid.

## Commands to run
- `cd ui && npm install`
- `npm run dev`
