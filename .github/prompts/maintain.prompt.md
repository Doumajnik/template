---
description: "Run the Maintenance Pipeline: scan for stale playbooks/skills/checklists, research updates, and apply targeted edits"
tools: ['search', 'read', 'edit', 'agent', 'web/fetch']
---

# Maintenance Pipeline

Run this to update all playbooks, skills, checklists, and instruction files in one sweep. Scans for staleness, researches current best practices, and applies targeted edits.

## Pipeline

You are the Orchestrator. Execute these steps in order. Each step spawns one or more agents. **No source code is changed** — only knowledge infrastructure files (playbooks, skills, checklists, instructions).

### Step 1 — Freshness Scanner (detect staleness)

Spawn the **Freshness Scanner Agent** to scan all knowledge infrastructure files.

**Scope:**
- `docs/playbooks/agents/*.playbook.md`
- `docs/playbooks/shared/*.playbook.md`
- `docs/playbooks/technologies/*.playbook.md`
- `.github/instructions/*.instructions.md`
- `.github/skills/*/SKILL.md`
- `.ai/checklists/*.checklist.md`

**Output:** `docs/FRESHNESS_REPORT.md` with prioritized findings.

### Step 2 — Self-Reflection (filter noise)

Spawn the **Self-Reflection Agent** on the Freshness Report.

- Score each finding 0-10 using the standard criteria
- Drop anything below score 5.0
- Re-rank by impact
- Output: filtered findings list (what actually needs updating)

### Step 3 — Research (parallel, one per technology)

For each technology/framework flagged as stale, spawn a **Research Agent** instance:

- Fetch current best practices from official docs
- Check latest stable versions
- Note community consensus shifts
- Output: `docs/discoveries/{date}_{tech}.maintenance-research.md`

### Step 4 — Knowledge Maintainer (parallel, one per file)

For each file needing updates (from filtered findings), spawn a **Knowledge Maintainer Agent** instance:

- Read the target file + relevant Research brief
- Apply targeted edits (add/update/remove rules)
- Increment version number
- Report changes back

### Step 5 — Consistency Check (single gate)

Spawn the **Consistency Check Agent** to verify no contradictions were introduced:

- Agent files reference correct playbook versions
- Cross-references between playbooks still resolve
- Checklist steps still match pipeline sections in AGENTS.md
- No conflicting rules between shared + agent playbooks

**🛑 Gate:** Findings block step 6+ until resolved. Dispatch Knowledge Maintainer to fix.

### Step 6 — Self-Reflection (validate changes)

Spawn the **Self-Reflection Agent** on all Knowledge Maintainer changes in aggregate:

- Score each change for correctness and value
- Flag anything uncertain for human review
- Confirm no regressions introduced

### Step 7 — Cleanup (dedup)

Spawn the **Cleanup Agent** to:

- Remove duplicate rules across files (parallel KM instances may add overlapping content)
- Consolidate overlapping patterns
- Ensure no rule appears in both a shared playbook and an agent-specific playbook

### Step 8 — Report to user

Present a summary:
- Files updated (with version bumps)
- Rules added/removed/changed
- Items flagged for human review
- Any technologies that couldn't be researched (registry unreachable, etc.)
