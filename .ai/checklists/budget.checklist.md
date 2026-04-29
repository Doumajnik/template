# 💰 Orchestrator Checklist — Budget Pipeline (essentials only)

> Copy this block into the session todo file at the very top. Tick: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked.

**Pipeline:** Budget Pipeline (12 steps, single Consistency Check at the end).
**Use when:** prototypes, throwaways, hackathons, "just make it work", or `BUDGET_MODE: ON` in PREFERENCES.
**BUDGET_MODE forces DEEP_MODE OFF** for the session.
**Source of truth:** [AGENTS.md → Budget Pipeline](../../AGENTS.md#budget-pipeline-budget_mode-on).

> **Don't use this for:** auth, payments, user data, production systems, incidents, or onboarding. Those need the full pipelines.

---

## Phase 0 — Session bootstrap (light)

- [ ] Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`
- [ ] Create dispatch log `.ai/sessions/{date}_{topic}.dispatch.md`
- [ ] Spawn **Librarian** in index mode (or use cached if just refreshed)

## Pipeline steps

- [ ] **Step 1** — spawn **Prompt Engineer (light)** → one-page spec; surface `[ASK USER]` items
- [ ] **Step 2** — spawn **Discovery** ONLY if new data involved (ask first)
- [ ] **Step 3** — spawn **Research** ONLY if a dependency choice is unclear
- [ ] **Step 4** — spawn **Architect (single pass)** → architecture in one shot. **No Critic, no Innovator.**
- [ ] **Step 5** — spawn **Planning Agent** → plan + todo file
- [ ] **Step 6 — 🛑 USER APPROVAL GATE** — cannot be skipped, even in budget mode
- [ ] **Step 7** — spawn **Scaffolder** → file stubs
- [ ] **Step 8** — spawn **Test Writer** (one per function) → ≥5 black-box tests/function (relaxed from 10), edge cases first
- [ ] **Step 9** — spawn **Worker** → red-green loop until tests pass
- [ ] **Step 10** — spawn **Reviewer** → check todo for skipped/incomplete tasks
- [ ] **Step 11** — spawn **Doc Updater** → update `docs/CODE_INVENTORY.md` + `docs/files/{path}.md` for changed files only (skip BUSINESS_LOGIC.md unless architecture changed)
- [ ] **Step 12** — spawn **Consistency Check (single instance, NOT sharded)** → plan ↔ code ↔ docs

## Skipped intentionally (do NOT spawn unless graduating to production)

- [x] ~~Innovator~~ — N/A: budget mode (no creative-alternative round)
- [x] ~~Critic (bottleneck + full review)~~ — N/A: budget mode
- [x] ~~Observability Engineer~~ — N/A: budget mode
- [x] ~~Threat Modeling~~ — N/A: budget mode
- [x] ~~Compliance (privacy-by-design)~~ — N/A: budget mode
- [x] ~~Analytics Instrumentation~~ — N/A: budget mode
- [x] ~~Capacity Planner~~ — N/A: budget mode
- [x] ~~Cost / FinOps~~ — N/A: budget mode
- [x] ~~Mock Data Generator~~ — N/A: budget mode
- [x] ~~Integration Tester~~ — N/A: unit tests only
- [x] ~~Security Agent~~ — N/A: defer until production
- [x] ~~Code Quality Agent~~ — N/A: defer until refactor
- [x] ~~Retrospective~~ — N/A: budget mode
- [x] ~~Doc-Site Generator~~ — N/A: prototypes have no users
- [x] ~~Cleanup (dedup pass)~~ — N/A: budget mode
- [x] ~~Consistency Check Gates 1 & 2~~ — N/A: only Gate 3 runs
- [x] ~~UI Preview / Localization / UX Research~~ — N/A: iterate on screen
