# 🚀 Orchestrator Checklist — Super Greedy Pipeline (maximum quality)

> Copy this block into the session todo file at the very top. Tick: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked.

**Pipeline:** Super Greedy Pipeline (40+ steps, 5 Consistency Check gates, continuous auditing).
**Use when:** unlimited LLM resources, maximum quality required, mission-critical production code, or `GREEDY_MODE: ON` in PREFERENCES.
**GREEDY_MODE forces DEEP_MODE ON** and is **mutually exclusive with BUDGET_MODE**.
**Source of truth:** [AGENTS.md → Super Greedy Pipeline](../../AGENTS.md#super-greedy-pipeline-greedy_mode-on).

> **Cost warning:** This pipeline uses 10–50× more LLM calls than the standard Planning Sequence. Only use when you genuinely have unlimited resources and maximum quality justifies the spend.

---

## Phase 0 — Session bootstrap + Model Discovery

- [ ] Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `.ai/lessons.md`
- [ ] Scan `.ai/plans/` for in-progress plans, `.ai/todos/` for incomplete todos
- [ ] Create dispatch log `.ai/sessions/{date}_{topic}.dispatch.md`
- [ ] **Model Discovery** — query the LLM provider API to enumerate all available models (Claude Opus 4, Claude Sonnet 4, Claude Haiku, GPT-4o, Gemini 2.5 Pro, etc.). Record discovered models in `.ai/sessions/{date}_available-models.md`
- [ ] **Assign Council Tiers** — based on discovered models, assign:
  - **Tier 1 (deepest reasoning):** top 2–3 models → Architecture, Planning, Security decisions
  - **Tier 2 (strong execution):** next 2–3 models → Implementation, Testing, Reviews
  - **Tier 3 (fast validation):** remaining models → Linting, formatting, quick checks
- [ ] Spawn **Librarian** in index mode (refresh knowledge base)
- [ ] Confirm `GREEDY_MODE: ON`, `BUDGET_MODE: OFF` in PREFERENCES

## Phase A — Planning (multi-model consensus, no code)

- [ ] **Step 1** — spawn **Prompt Engineer** (dispatched to ALL Tier 1 models in parallel) → each produces an enriched spec → **LLM Council** synthesizes the best spec from all outputs
- [ ] **Step 1a** — spawn **Adversarial Red Team** → attempts to find ambiguities, contradictions, and missing requirements in the synthesized spec. Feeds findings back to Prompt Engineer for revision
- [ ] **Step 2** — spawn **Discovery** if user introduced new data (ask first)
- [ ] **Step 3** — spawn **Research** (dispatched to 2+ models) → synthesize research briefs into unified recommendation
- [ ] **Step 4** — install dependencies upfront
- [ ] **Step 5** — spawn **Architect** (dispatched to ALL Tier 1 models independently) → each produces an architecture → **LLM Council** evaluates, scores, and merges the best elements into a unified design
- [ ] **Step 5a** — spawn **Mock Data Generator** if new domain entities
- [ ] **Step 6** — spawn **Observability Engineer** → telemetry plan (SLOs, metrics, traces, logs)
- [ ] **Step 6a** — spawn **Threat Modeling** (dispatched to 2+ models) → independent STRIDE analyses merged
- [ ] **Step 6b** — spawn **Compliance** (privacy-by-design) if user data involved
- [ ] **Step 6c** — spawn **Analytics Instrumentation** if user-facing
- [ ] **Step 6d** — spawn **Capacity Planner** (dispatched to 2+ models) → independent load models merged
- [ ] **Step 7** — spawn **Critic** (bottleneck scan) + **Cost / FinOps** in parallel
- [ ] **Step 7a** — spawn **Security** (pre-implementation audit) → review architecture for security flaws BEFORE any code
- [ ] **Step 8** — spawn **Innovator** (dispatched to ALL Tier 1 models) → each proposes creative alternatives → **LLM Council** selects/combines
- [ ] **Step 9** — spawn **Architect (revision)** incorporating Council-selected innovations
- [ ] **Step 10** — spawn **Critic (full review)** (dispatched to 2+ models independently) → mediate Architect↔Critic loop (max 15 rounds, extended from 10)
- [ ] **Step 10a** — **Continuous Audit Checkpoint** — spawn Security + Code Quality + Type Safety in parallel reviewing the architecture plan
- [ ] **Step 11** — spawn **Planning Agent** → plan + todo file
- [ ] **Step 12** — spawn **Architect (plan verification)** (dispatched to 2+ models) → each independently verifies → must reach consensus
- [ ] **🛑 Gate 1 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
  - [ ] Plan-vs-Code shard
  - [ ] Code-vs-Docs shard
  - [ ] References & Path Integrity shard
  - [ ] Roster & Pipeline shard
  - [ ] Orphan & Dead Files shard
  - [ ] Merge instance
- [ ] **Step 13** — spawn **UI Preview** + **Localization** + **UX Research** + **Accessibility (pre-scaffold)** if UI
- [ ] **Step 14 — 🛑 USER APPROVAL GATE** — present multi-model consensus plan

## Phase B — Implementation (N-version, continuous audit)

- [ ] **Step 15** — spawn **Scaffolder** → file stubs
- [ ] **Step 16** — spawn **Architect (scaffold review)** → verify stubs match plan
- [ ] **Step 16a** — **Continuous Audit Checkpoint** — Security + Type Safety review scaffolded interfaces
- [ ] **Step 17** — spawn **Test Writer** (one per function, parallel, dispatched to 2 models each) → ≥25 black-box tests/function, edge cases first. **LLM Council** merges test suites, removing duplicates and adding any edge cases either model missed
- [ ] **Step 17a** — spawn **Adversarial Red Team** → reviews tests for "can a wrong implementation pass these?" — adds defeating tests
- [ ] **Step 18** — spawn **Worker** (N-version: critical functions dispatched to 2–3 models independently) → each implements → **LLM Council** selects best implementation OR synthesizes a hybrid. Non-critical functions: single model with immediate review
- [ ] **Step 18a** — **Continuous Audit Checkpoint** — Security + Code Quality + Error Handling + Type Safety review each implemented function immediately
- [ ] **Step 18b** — spawn **Performance** → profile every implemented function for algorithmic complexity, flag O(n²)+ immediately
- [ ] **🛑 Gate 2 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] Refresh **Librarian** index
- [ ] **Step 19** — spawn **Integration Tester** (dispatched to 2 models) → 20+ integration / 10+ E2E / 3+ contract per feature (raised from standard)
- [ ] **Step 19a** — spawn **Mutation Testing** validation → run mutation testing framework (mutmut/stryker) to verify test suite kills ≥90% of mutants. If <90%, loop back to Test Writer
- [ ] **Step 20** — spawn **Reviewer** (dispatched to ALL Tier 1 models independently) → each reviews → **LLM Council** consolidates findings (union of all findings, not intersection)
- [ ] **Step 20a** — spawn **Cross-File Coherence Review** → every source file reviewed against every other file for: naming consistency, pattern adherence, import conventions, error handling patterns, logging patterns, type usage patterns. Reports drift
- [ ] **🛑 Gate 3 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] **Step 21** — spawn **Security** (full audit, dispatched to 2+ models independently) → union of all findings
- [ ] **Step 21a** — spawn **Threat Modeling** (post-implementation) → verify mitigations from pre-implementation model are correctly implemented
- [ ] **Step 22** — spawn **Code Quality** (dispatched to 2 models) → union of findings
- [ ] **Step 22a** — spawn **Performance** (full profiling) → benchmark suite, memory analysis, identify regressions
- [ ] **Step 22b** — spawn **Accessibility** (if UI) → WCAG AAA compliance (not just AA)
- [ ] **Step 22c** — spawn **Load Testing** → design and run load scenarios against SLOs
- [ ] **Step 23** — spawn **Doc Updater** → update all docs
- [ ] **Step 23a** — spawn **Doc-Site Generator** → user-facing docs for any public surface
- [ ] **🛑 Gate 4 — Consistency Check (5 parallel shards + 1 merge)** → must return clean
- [ ] **Step 24** — spawn **Cross-File Coherence Review (final)** → re-run with all code + docs finalized, fix any remaining drift
- [ ] **🛑 Gate 5 — Consistency Check (final, 5 parallel shards + 1 merge)** → must return clean
- [ ] **Step 25** — spawn **Retrospective** (chunked) → deep review of entire session
- [ ] **Step 25a** — spawn **LLM Council (meta-review)** → reviews the Retrospective's findings, adds cross-model perspective
- [ ] **Step 26** — spawn **Cleanup** (dedup pass) → consolidate all reports
- [ ] Mark plan status 🟢 Complete
- [ ] Verify ≥100 tests per functionality across all layers

## Continuous audit summary

At the end of the pipeline, the Orchestrator produces a **Quality Scorecard** in `.ai/sessions/{date}_quality-scorecard.md`:

- [ ] Security audit passes (0 CRITICAL/HIGH)
- [ ] Code quality score (0 CRITICAL/HIGH smells)
- [ ] Type safety coverage (100% — no `any` types, no unsafe casts)
- [ ] Error handling audit (0 silent catches, 0 missing context)
- [ ] Test mutation score ≥90%
- [ ] Cross-file coherence score (0 drift findings after final pass)
- [ ] Performance baseline established (no O(n²)+ unless justified)
- [ ] Load test SLOs met
- [ ] Accessibility WCAG AAA (if UI)
- [ ] Multi-model consensus achieved on all critical decisions
