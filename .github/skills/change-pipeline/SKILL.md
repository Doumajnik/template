---
name: change-pipeline
description: "Full adversarial change pipeline for modifying existing code. Use when changing behavior, updating features, refactoring logic, restructuring, or any alteration to existing source code. Ensures impact analysis, regression safety, and full planning before any code is touched. Triggers on: change, modify, update, refactor, restructure, alter."
---

# Change Pipeline

Run the full adversarial pipeline for any modification to existing code — behavior changes, feature updates, refactoring, restructuring, parameter changes, and business rule adjustments.

## When to Use

- Modifying existing behavior: "Change X to Y", "Update this to...", "Modify the behavior of..."
- Refactoring or restructuring: "Refactor this", "Restructure how...", "Move this logic to..."
- Adjusting existing logic: "Make it so that...", "Instead of X, do Y"
- Adding/removing from existing code: "Add a parameter to...", "Remove this field from..."
- Any request that alters existing source code behavior

## When NOT to Use (use other pipelines)

- **New greenfield features** with no existing code → use `deep-implement` skill
- **Bug reports / errors / failing tests** → use Autonomous Bug Fixing (Debug Agent)
- **Questions, lookups, docs-only updates** → Trivial Task Shortcut

## Why Changes Need Their Own Pipeline

Changes are NEVER trivial. Even seemingly small modifications can have cascading effects:

- Callers that depend on the old behavior break silently
- Tests that passed before now fail for unclear reasons
- Side effects in distant modules surface days later
- Business rules that were implicitly preserved get dropped

The Change Pipeline adds **Impact Analysis** and **Regression Checklists** on top of the standard planning process to prevent these issues.

## Pipeline

Execute the full impact-aware pipeline. Every step is a sub-agent spawn.

### Phase 1 — Analysis & Impact

1. **Prompt Engineer Agent** — analyzes the change request. Produces an enriched spec in `.ai/specs/` focusing on:
   - What currently exists (current behavior, current API surface)
   - What needs to change (target behavior, new API surface)
   - What must NOT change (preserved behavior, untouched modules)
   - Edge cases introduced by the modification
   - Acceptance criteria for the change
   - Surfaces `[ASK USER]` questions for ambiguities

2. **Impact Analysis** (Librarian + Discovery) — map the blast radius:
   - Spawn the Librarian to identify all files, functions, tests, and modules affected
   - If scope is large or unclear, spawn a Discovery Agent to map dependencies
   - Output: **impact brief** with affected files, dependent modules, tests that must be updated, and potential regression risks

3. **Research Agent** — investigates best practices for the type of change (migration patterns, backward compatibility, deprecation approaches). Uses the enriched spec + impact brief as input.

4. **Dependency check** — if the change introduces or removes dependencies, map and install/uninstall them upfront.

### Phase 2 — Design & Critique

5. **Architect** — designs the change approach using enriched spec, impact brief, and research findings. Must explicitly address:
   - How to preserve existing behavior where intended
   - How to migrate callers/consumers
   - How to avoid regressions
   - Rollback strategy if the change causes issues

6. **Innovator** — reviews the change plan and proposes creative alternatives (cleaner decomposition, simpler migration path, phased rollout). Reports back to Orchestrator.

7. **Architect (revision)** — Orchestrator feeds Innovator's best ideas back to the Architect.

8. **Critic** — adversarial review with a change-specific focus. Iterate Architect↔Critic loop (max 10 rounds). **The Critic must specifically verify: "Does this change break anything that currently works?"** Checks for:
   - Regressions and breaking changes
   - Unnecessary scope creep
   - Over-engineering
   - Missing caller/consumer updates

### Phase 3 — Planning & Approval

9. **Planning Agent** — creates change plan + todo file at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`. The plan must include:
   - Function-level breakdown of what changes
   - A **regression checklist** — explicit list of existing behaviors that must still work after the change
   - List of all files to be modified with reason
   - List of all tests to be updated/added

10. **User approval (MANDATORY GATE)** — present the full change plan, impact analysis, and regression checklist. Ask for explicit approval. If rejected, restart from step 1.

See [change checklist](./references/change-checklist.md) for the full checklist of gates and deliverables.

### Phase 4 — Implementation

11. **Test Writer** (one per changed function) — writes/updates tests for:
    - The changed behavior (new expected outcomes)
    - Regression tests for unchanged behavior that might be affected
    - Minimum 15 tests per changed function
    - Mark ✅ in todo.

12. **Worker** (one per changed function) — implements the change:
    - Red-green loop until new tests pass
    - Must verify ALL existing tests still pass (not just new ones)
    - Mark ✅ in todo.

13. **Integration Tester** — writes/runs E2E tests covering:
    - The change itself
    - The boundary between changed and unchanged code
    - Cross-module flows that touch the changed code
    - Mark ✅ in todo.

### Phase 5 — Review & Audit

14. **Reviewer** — validates the change with a regression focus:
    - Regression checklist passes (every item verified)
    - No unintended side effects
    - All affected callers updated
    - No orphaned code from the old behavior
    - If fail → Worker fixes. Mark ✅.

15. **Security Agent** — audits changed code for vulnerabilities. Append to `docs/SECURITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.

16. **Code Quality Agent** — scans changed code for duplication/smells. Append to `docs/QUALITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.

### Phase 6 — Documentation & Retrospective

17. **Doc Updater** — updates all affected docs:
    - API documentation (if endpoints/signatures changed)
    - Business logic docs (if behavior changed)
    - Per-file docs in `docs/files/`
    - Code inventory (if symbols added/removed/renamed)
    - Session summary. Mark ✅.

18. **Retrospective Agent (chunked)** — reviews the change session. Appends to `docs/RETROSPECTIVE_REPORT.md` and `docs/PLAYBOOK.md`. Mark todo status ✅ Complete.

19. **Cleanup Agent (dedup pass)** — consolidates `docs/RETROSPECTIVE_REPORT.md`, `docs/PLAYBOOK.md`, and `.ai/lessons.md`. Removes duplicate entries.

## Key Rules

- **Impact analysis is mandatory.** Never skip the blast radius mapping — even for "simple" changes.
- **Regression checklist is mandatory.** The Planning Agent must produce one, and the Reviewer must verify every item.
- **All existing tests must still pass.** Workers verify the full test suite, not just new/changed tests.
- **Todo tracking:** Every agent reads the todo file, marks tasks 🔵 in-progress before starting and ✅ done when complete.
- **Granular spawning:** One Test Writer and one Worker per individual changed function — never batch.
- **Context Gateway (mandatory):** Every agent spawn MUST be preceded by a Librarian query. No agent receives raw files — only Librarian-curated context briefs. See copilot-instructions.md Context Gateway Protocol.
- **Mandatory approval gate:** Never proceed to implementation without explicit user confirmation of the change plan + regression checklist.
- **Circuit breaker:** If Worker fails 2+ functions in a row or Reviewer rejects (unintended side effects), halt and re-plan from scratch.
- **Critic's key question:** "Does this change break anything that currently works?" must be answered with evidence.

> **Relationship:** This skill implements the **Change Pipeline** defined in `copilot-instructions.md` / `AGENTS.md`. Use this skill for step-by-step detail and checklists.
