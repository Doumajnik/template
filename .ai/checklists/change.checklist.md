# 🔧 Orchestrator Checklist — Change Pipeline (modifying existing code)

> Copy this block into the session todo file at the very top. Tick: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked. Skipped steps stay marked `[x] ~~step~~ — N/A: <reason>`.

**Pipeline:** Change Pipeline (steps 1–22, three Consistency Check gates).
**Use when:** modifying existing behavior, refactoring logic, restructuring, renaming, deprecating, ANY alteration to existing source.
**Source of truth:** [AGENTS.md → Change Pipeline](../../AGENTS.md#change-pipeline-modifications-to-existing-code).

> Changes are **never** trivial. Even one-line fixes go through this pipeline.

---

## Phase 0 — Session bootstrap

- [ ] Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `.ai/lessons.md`
- [ ] Create dispatch log `.ai/sessions/{date}_{topic}.dispatch.md`
- [ ] Spawn **Librarian** in index mode

## Phase A — Plan the change (no code yet)

- [ ] **Step 1** — spawn **Prompt Engineer** → enriched spec covering: what exists, what changes, what must NOT change, regression risks
- [ ] **Step 2** — spawn **Librarian** (impact mode) + **Discovery** if scope unclear → impact brief: affected files, dependents, tests at risk
- [ ] **Step 3** — spawn **Research** → migration / backward-compat / deprecation patterns
- [ ] **Step 4** — install/uninstall dependencies if change introduces or removes any
- [ ] **Step 4a** — spawn **Mock Data Generator** if entity shapes change
- [ ] **Step 5** — spawn **Architect** → change approach with explicit migration + regression-prevention plan
- [ ] **Step 5a** — spawn **Threat Modeling** if auth / data flows touched
- [ ] **Step 5b** — spawn **Compliance (privacy-by-design)** if user data flows change
- [ ] **Step 5c** — spawn **Analytics Instrumentation** if user-flow change
- [ ] **Step 5d** — spawn **Capacity Planner** if traffic / data volume changes
- [ ] **Step 6** — spawn **Critic (bottleneck scan)** → focused brief
- [ ] **Step 7** — spawn **Innovator** → creative alternatives + cleaner migration paths
- [ ] **Step 8** — spawn **Architect (revision)** → incorporate Innovator + Critic
- [ ] **Step 9** — spawn **Critic (full review)** → "does this break anything that currently works?"; loop max 10 rounds
- [ ] **Step 10** — spawn **Planning Agent** → change plan + todo + **regression checklist**
- [ ] **Step 11** — spawn **Deprecation Manager** if removing/replacing public surface → announce → warn → remove timeline + migration guide
- [ ] **Step 12** — spawn **Architect (plan verification)** → confirm plan ↔ impact ↔ regression ↔ deprecation entries
- [ ] **🛑 Gate 1 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] **Step 13 — 🛑 USER APPROVAL GATE** — present plan, impact, regression checklist, deprecation entries

## Phase B — Implementation

- [ ] **Step 14** — spawn **Test Writer** (one per changed function) → ≥12 tests for new behaviour (≥2 standard, ≥3 boundary + adversarial) + regression tests for unchanged behaviour
- [ ] **Step 15** — spawn **Worker** (one per changed function) → red-green loop; verify ALL existing tests still pass, not just new ones
- [ ] **🛑 Gate 2 — Consistency Check (5 parallel shards + 1 merge)** → must return clean (no scope creep, no unrelated edits)
- [ ] Refresh **Librarian** index after Worker completes
- [ ] **Step 16** — spawn **Integration Tester** → cover changed/unchanged boundary
- [ ] **Step 17** — spawn **Reviewer** → check regression checklist passes, no unintended side effects
- [ ] **Step 18** — spawn **Security** → audit changed code; CRITICAL/HIGH → fix → re-verify
- [ ] **Step 19** — spawn **Code Quality** → smell scan changed code
- [ ] **Step 20** — spawn **Doc Updater** → API docs, business logic, file docs, code inventory, deprecation log
- [ ] **🛑 Gate 3 — Consistency Check (5 parallel shards + 1 merge)** → must return clean (no stale references to old behavior)
- [ ] **Step 21** — spawn **Retrospective** (chunked) → update Playbook + lessons
- [ ] **Step 21a** — spawn **Doc-Site Generator** if public surface changed
- [ ] **Step 22** — spawn **Cleanup** (dedup pass) → consolidate reports
- [ ] Verify regression checklist 100% green
- [ ] Mark plan status 🟢 Complete
