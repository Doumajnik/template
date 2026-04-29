# 🧭 Orchestrator Checklist — Onboarding Pipeline (existing project audit)

> Copy this block into the session todo file at the very top. Tick: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked.

**Pipeline:** Onboarding Pipeline (Phases 1–7, three Consistency Check gates).
**Use when:** "onboard", "onboard this project", or after integrating template into existing repo.
**Read-only by default** — no code changes until user approves the resulting improvement plan.
**Source of truth:** [AGENTS.md → Onboarding Pipeline](../../AGENTS.md#onboarding-pipeline-existing-project-audit) and [.github/prompts/onboard-project.prompt.md](../../.github/prompts/onboard-project.prompt.md).

---

## Phase 0 — Session bootstrap

- [ ] Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `.ai/lessons.md`
- [ ] Create dispatch log `.ai/sessions/{date}_{topic}.dispatch.md`
- [ ] Confirm with user: "Run onboarding? This is read-only and will produce reports + an improvement plan."

## Phase 1 — Discovery

- [ ] Spawn **Discovery** (one instance per top-level module if codebase is large) → `docs/discoveries/{date}_existing-codebase.md`

## Phase 2 — Documentation

- [ ] Spawn **Doc Updater** → fill `docs/BUSINESS_LOGIC.md`, `docs/CODE_INVENTORY.md`, `docs/API_DOCUMENTATION.md`, `docs/files/{path}.md`
- [ ] Refresh **Librarian** index
- [ ] **🛑 Gate 1 — Consistency Check (5 parallel shards + 1 merge)** → docs ↔ discovery ↔ source inventory

## Phase 3 — Audits (parallel)

- [ ] Spawn **Security** → `docs/SECURITY_REPORT.md`
- [ ] Spawn **Code Quality** → `docs/QUALITY_REPORT.md`
- [ ] Spawn **Dependency** → outdated + vulnerable deps + license report
- [ ] Spawn **Error Handling** → swallowed exceptions, missing context
- [ ] Spawn **Type Safety** → any types, missing annotations, unsafe casts
- [ ] Spawn **Monitoring** → logging, health checks, alerting gaps
- [ ] Spawn **Threat Modeling** → STRIDE against current architecture
- [ ] Spawn **Compliance** → license + privacy + regulatory audit
- [ ] Spawn **Analytics Instrumentation** + **Localization** in parallel (audit-only mode)

## Phase 4 — Structure & Cleanup analysis

- [ ] **Phase 4a** — spawn **Architect (structure-review mode)** → `docs/STRUCTURE_REVIEW.md`
- [ ] **Phase 4b** — spawn **Cleanup (audit-only mode)** → `docs/CLEANUP_REPORT.md` (dead code, dead docs, dead deps)

## Phase 5 — Test harness

- [ ] **Phase 5a** — spawn **Test Writer** (one per source file) → ≥12 black-box tests per public function across 12-category taxonomy (≥2 standard, ≥3 boundary + adversarial), edge cases first
- [ ] **Phase 5b** — spawn **Integration Tester** → 15+ integration / 5+ E2E / 1+ contract per feature
- [ ] Verify every functionality reaches **≥50 tests total** across all layers
- [ ] Run full suite, save `.ai/plans/{date}_test-baseline.md` with pass/fail/skip counts
- [ ] **🛑 Gate 2 — Consistency Check (5 parallel shards + 1 merge)** → tests ↔ source files (every public function covered or explicitly deferred)

## Phase 6 — Improvement plan

- [ ] Spawn **Planning Agent** → synthesise all reports + baseline → `.ai/plans/{date}_onboarding-improvements.md` prioritised Critical / High / Medium / Low + dead-asset removal list
- [ ] **🛑 Gate 3 — Consistency Check (5 parallel shards + 1 merge)** → plan items ↔ report findings (no orphan recommendations, no missed CRITICAL/HIGH)

## Phase 7 — Present & approve

- [ ] Present to user: discovery summary, structure review, dead-asset counts, test baseline, top-5 actions, full improvement plan
- [ ] **🛑 USER APPROVAL GATE** — get explicit OK before any fix work
- [ ] Switch to fix-loop mode (each fix: Worker applies → run full suite → green → next; regression → fix regression first)
