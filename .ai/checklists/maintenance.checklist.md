# Maintenance Pipeline Checklist

> Copy this into the session todo file when running the Maintenance Pipeline.
> Source of truth: [AGENTS.md → Maintenance Pipeline](../../AGENTS.md#maintenance-pipeline-knowledge-infrastructure-upkeep)

## Steps

- [ ] **Step 1 — Freshness Scanner** — scan all playbooks, skills, checklists, instruction files for staleness → `docs/FRESHNESS_REPORT.md`
- [ ] **Step 2 — Self-Reflection (filter)** — score findings, drop noise (<5), re-rank by impact
- [ ] **Step 3 — Research (parallel)** — one Research Agent per flagged technology/framework → `docs/discoveries/{date}_{tech}.maintenance-research.md`
- [ ] **Step 4 — Knowledge Maintainer (parallel)** — one instance per file to update → apply edits, bump versions, report changes
- [ ] **Step 5 — Consistency Check** — verify no contradictions across files, cross-refs resolve, checklist steps match pipelines
  - [ ] 🛑 Gate: findings block step 6+ until resolved
- [ ] **Step 6 — Self-Reflection (validate)** — second pass reviewing all changes in aggregate, flag uncertain items
- [ ] **Step 7 — Cleanup (dedup)** — consolidate overlapping rules, remove duplicates from parallel KM instances
- [ ] **Step 8 — Report to user** — present summary: files updated, versions bumped, items flagged for review
