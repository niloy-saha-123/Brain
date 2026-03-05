# Build Plan (v0.3) — Proposal

## Theme
**Smarter planner & tool chooser (one big upgrade).**  
Goal: move from rule-based plan selection to a scored planner that picks the best agent + tool sequence with clearer approvals and UI visibility.

## Milestones (proposed order)
1) **Planner design + scoring model**  
   - Document planner inputs/outputs, scoring factors (goal match, tool risk, approval cost, token cost).  
   - Add schema/contracts for planner decisions and store planner traces.
2) **Planner execution engine**  
   - Implement scoring-based planner that selects agent and an ordered tool plan (>=3 tools supported).  
   - Integrate approval pre-checks (predict which steps will pause).  
   - Persist planner trace per run and emit worklog/status events for each decision.
3) **UI surfaces for planner + approvals**  
   - Show planned steps, predicted approvals, and live progress in Chat/Worklog.  
   - Allow viewing planner trace per run; highlight paused/approved/completed steps.

## Constraints
- No new tools; reuse existing tool set.  
- Keep approvals gating as-is; planner only predicts/visualizes.  
- No cloud calls; local-only.  
- No main merge until approved and verified.

## Success criteria
- Planner chooses between at least todo/web/filesystem/terminal based on goal text.  
- Planner trace stored and viewable; events reflect decisions.  
- Approvals predicted and shown before execution; actual pauses/resumes still work.  
- All existing tests pass; new planner/unit tests added.
