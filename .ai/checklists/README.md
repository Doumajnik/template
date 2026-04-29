# Orchestrator Pipeline Checklists

These files exist so the **Orchestrator** behaves the same way every time, even when it's running on a weaker model. Instead of trying to remember every step of a long pipeline from the prose in [AGENTS.md](../../AGENTS.md), the Orchestrator copies one of these checklists into the session todo file and ticks each step as it goes.

## How the Orchestrator uses these

At session startup, after detecting which pipeline the user's request maps to, the Orchestrator MUST:

1. Pick the right checklist:
   - User says "implement", "build", "add feature" with no existing code → [planning.checklist.md](planning.checklist.md)
   - User says "change", "modify", "update", "refactor" existing code → [change.checklist.md](change.checklist.md)
   - User says "onboard", "audit this project" → [onboarding.checklist.md](onboarding.checklist.md)
   - User says "incident", "down", "outage", "prod is broken" → [incident.checklist.md](incident.checklist.md)
   - User says "budget", "quick", "prototype", or `BUDGET_MODE: ON` → [budget.checklist.md](budget.checklist.md)
2. Copy the chosen checklist into the session's todo file (`.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`) **above** any other todos. Keep the heading and intro text intact.
3. Mark each checkbox as it progresses:
   - `- [ ]` — not started
   - `- [~]` — in progress
   - `- [x]` — done
   - `- [!]` — blocked / needs attention (must be resolved before pipeline continues)
4. Never delete steps. Skipped steps must be marked `- [x] ~~Step text~~ — N/A: <reason>` so the audit trail shows the choice was deliberate.
5. The checklist is the **Orchestrator's own todo**. It coexists with the per-agent task list that the Planning Agent generates (those are the agents' todos). The Orchestrator owns the checklist; sub-agents own their per-task rows.

## Why this exists

A weaker model may forget a step like "spawn the Threat Modeling agent in parallel with Observability" or "Consistency Check is sharded into 5 instances". The checklist makes those steps explicit and visible. Instead of hallucinating a workflow from memory, the model just walks down the list.

This also gives the user a single document to look at and answer the question "where are we in the pipeline right now?".

## Maintenance

If a pipeline step is added, removed, or renumbered in [AGENTS.md](../../AGENTS.md), the matching checklist file MUST be updated in the same commit. The Consistency Check Agent (Roster & Pipeline shard) verifies these stay in sync.
