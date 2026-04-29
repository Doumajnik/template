# 🎯 Orchestrator Checklist — Planning Sequence (full pipeline)

> Copy this block into the session todo file at the very top. Tick each box as you go: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked. Skipped steps stay in the list and get marked `[x] ~~step~~ — N/A: <reason>`.

**Pipeline:** Full Planning Sequence (steps 1–25, three Consistency Check gates).
**Use when:** new feature, greenfield code, anything non-trivial that touches production.
**Source of truth:** [AGENTS.md → Planning Sequence](../../AGENTS.md#planning-sequence-non-trivial-tasks).

---

## Phase 0 — Session bootstrap

- [ ] Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `.ai/lessons.md`
- [ ] Scan `.ai/plans/` for in-progress plans, `.ai/todos/` for incomplete todos, `docs/RETROSPECTIVE_REPORT.md` for action items
- [ ] Create dispatch log `.ai/sessions/{date}_{topic}.dispatch.md` from template
- [ ] Spawn **Librarian** in index mode (refresh knowledge base)
- [ ] Confirm `BUDGET_MODE: OFF` in PREFERENCES (otherwise switch to budget checklist)

## Phase A — Planning (no code)

- [ ] **Step 1** — spawn **Prompt Engineer** → enriched spec in `.ai/specs/`; surface `[ASK USER]` items
- [ ] **Step 2** — spawn **Discovery** if user introduced new data (ask first)
- [ ] **Step 3** — spawn **Research** → research brief + dependency list
- [ ] **Step 4** — install dependencies upfront (delegate to Worker)
- [ ] **Step 5** — spawn **Architect** → architecture plan
- [ ] **Step 5a** — spawn **Mock Data Generator** if new domain entities
- [ ] **Step 6** — spawn **Observability Engineer** → telemetry plan (SLOs, metrics, traces, logs)
- [ ] **Step 6a** — spawn **Threat Modeling** in parallel with Observability → STRIDE + OWASP report
- [ ] **Step 6b** — spawn **Compliance** (privacy-by-design) in parallel if user data is collected/processed
- [ ] **Step 6c** — spawn **Analytics Instrumentation** in parallel if user-facing or has KPIs
- [ ] **Step 7** — spawn **Critic** (bottleneck scan) + **Cost / FinOps** in parallel → bottleneck brief
- [ ] **Step 7a** — spawn **Capacity Planner** in parallel with Innovator → load + sizing report
- [ ] **Step 8** — spawn **Innovator** → creative alternatives addressing bottlenecks
- [ ] **Step 9** — spawn **Architect (revision)** → incorporate Innovator + Critic + Cost
- [ ] **Step 10** — spawn **Critic (full review)**, mediate Architect↔Critic loop (max 10 rounds)
- [ ] **Step 11** — spawn **Planning Agent** → plan + todo file
- [ ] **Step 12** — spawn **Architect (plan verification)** → confirm plan ↔ architecture
- [ ] **🛑 Gate 1 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
  - [ ] Plan-vs-Code shard
  - [ ] Code-vs-Docs shard
  - [ ] References & Path Integrity shard
  - [ ] Roster & Pipeline shard
  - [ ] Orphan & Dead Files shard
  - [ ] Merge instance → consolidated `docs/CONSISTENCY_REPORT.md` entry
- [ ] **Step 13** — spawn **UI Preview** + **Localization** + **UX Research** if UI/user-facing (else mark N/A)
- [ ] **Step 14 — 🛑 USER APPROVAL GATE** — present plan + UI preview, get explicit OK (or restart from Step 1)

## Phase B — Implementation

- [ ] **Step 15** — spawn **Scaffolder** → file stubs from plan + UI component map
- [ ] **Step 16** — spawn **Architect (scaffold review)** → verify stubs match plan
- [ ] **Step 17** — spawn **Test Writer** (one per function, parallel) → ≥12 black-box tests/function across 12-category taxonomy (≥2 per standard category, ≥3 boundary + adversarial), edge cases first
- [ ] **Step 18** — spawn **Worker** (one per function, parallel) → red-green loop + telemetry instrumentation
- [ ] **🛑 Gate 2 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] Refresh **Librarian** index after Worker completes
- [ ] **Step 19** — spawn **Integration Tester** → 15+ integration / 5+ E2E / 1+ contract per feature
- [ ] **Step 20** — spawn **Reviewer** → if fail, loop back to Worker
- [ ] **Step 21** — spawn **Security** → audit + report; CRITICAL/HIGH → Workers fix → re-verify
- [ ] **Step 22** — spawn **Code Quality** → smell scan + report; CRITICAL/HIGH → Workers fix → re-verify
- [ ] **Step 23** — spawn **Doc Updater** → update all docs, write session summary, commit
- [ ] **🛑 Gate 3 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] **Step 24** — spawn **Retrospective** (chunked, one per transcript chunk + 1 merge) → updates Playbook + lessons
- [ ] **Step 24a** — spawn **Doc-Site Generator** in parallel if public surface added/changed
- [ ] **Step 25** — spawn **Cleanup** (dedup pass) → consolidate retrospective + playbook + lessons reports
- [ ] Mark plan status 🟢 Complete in `.ai/plans/`
- [ ] Verify ≥50 tests per functionality across all layers (sum unit + integration + E2E + contract)
