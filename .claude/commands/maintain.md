# Maintenance Pipeline

Run the Maintenance Pipeline from AGENTS.md. This scans all playbooks, skills, checklists, and instruction files for staleness and applies targeted updates in one sweep.

## Steps

1. Freshness Scanner — detect stale content
2. Self-Reflection — filter noise, rank by impact
3. Research (parallel) — one per flagged technology
4. Knowledge Maintainer (parallel) — one per file needing updates
5. Consistency Check — verify no contradictions
6. Self-Reflection — validate changes
7. Cleanup — deduplicate rules
8. Report to user

## Instructions

Follow the Maintenance Pipeline section in AGENTS.md exactly. Use the checklist from `.ai/checklists/maintenance.checklist.md`.
