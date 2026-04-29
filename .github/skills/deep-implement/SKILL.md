---
name: deep-implement
description: "Full adversarial implementation pipeline for features, bug fixes, refactors, and enhancements. Use when implementing any non-trivial task that needs the complete plan-critique-implement cycle. Triggers on: implement, deep implement, build feature, full pipeline."
---

# Deep Implement

Run the full adversarial pipeline for any task — features, bug fixes, refactoring, enhancements, and updates.

## When to Use

- Implementing a new feature end-to-end
- Non-trivial bug fixes that need architecture review
- Major refactoring efforts
- Any task that benefits from plan → critique → implement → review cycle
- When the user says "deep implement" or wants the full pipeline

## Pipeline

Execute the full plan-critique-implement pipeline. Every step is a sub-agent spawn.

### Phase 1 — Analysis & Research

> **Prerequisite:** Session Startup must be completed first (see copilot-instructions.md Session Startup — read PREFERENCES, PLAYBOOK, CODE_INVENTORY, etc.).

1. **Prompt Engineer Agent** — analyzes the raw user request. Produces an enriched spec in `.ai/specs/` covering functional requirements, edge cases, data needs, security, and acceptance criteria. Surfaces `[ASK USER]` questions.
2. **Discovery Agent** — if this task involves new data, libraries, or external APIs. Ask user first.
3. **Research Agent** — research the topic: best practices, libraries, patterns, pitfalls. Produce a research brief with dependency list.
4. **Dependency mapping & install** — based on the Research Agent's findings, install all required dependencies upfront.

### Phase 2 — Design & Critique

5. **Architect** — design the architecture. Use the Research Agent's brief as input. Identify shared utilities, base classes, constants FIRST. Run deduplication analysis against existing inventory.
6. **Innovator** — challenge assumptions, propose creative alternatives.
7. **Architect (revision)** — incorporate Innovator's best ideas.
8. **Critic** — adversarial review. Iterate Architect↔Critic loop (max 10 rounds) until approved.

### Phase 3 — Planning & Approval

9. **Planning Agent** — function-level breakdown of the approved architecture. Creates the todo file at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`.
10. **UI Preview Agent** `[CONDITIONAL]` — if the task involves UI/frontend work, generates an interactive HTML/CSS preview in `.ai/previews/` with a component decomposition map. Skipped for backend-only tasks.
11. **User approval (MANDATORY GATE)** — present the full plan (and UI preview if applicable) and ask for explicit approval. Suggest opening a new chat session for implementation to keep context clean. If rejected, restart from step 1.

See [pipeline checklist](./references/pipeline-checklist.md) for the full checklist of gates and deliverables.

### Phase 4 — Implementation

12. **Scaffolder** — create file stubs with signatures and docstrings. Uses the UI Preview's component decomposition (if available) to create accurate frontend stubs. Mark scaffolding tasks ✅.
13. **Test Writer** (one per function) — write ≥12 tests per function across every applicable category of the 12-category taxonomy with per-category floors (≥2 standard, ≥3 boundary + adversarial), edge cases first, that fail on stubs (red phase). Contributes to the ≥50-tests-per-functionality floor. Cannot read source — hard-enforced by Tool Guard. Mark ✅.
14. **Worker** (one per function) — implement code, red-green loop until tests pass. Mark ✅.
15. **Integration Tester** — write and run E2E/integration tests. Mark ✅.

### Phase 5 — Review & Audit

16. **Reviewer** — validate code quality, correctness, plan adherence. If fail → Worker fixes. Mark ✅.
17. **Security Agent** — audit for vulnerabilities, append to `docs/SECURITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.
18. **Code Quality Agent** — scan for duplication/smells, append to `docs/QUALITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.

### Phase 6 — Documentation & Retrospective

19. **Doc Updater** — update all documentation, write session summary. Mark ✅.
20. **Retrospective Agent (chunked)** — review all decisions, update `docs/PLAYBOOK.md`, append to `docs/RETROSPECTIVE_REPORT.md`. Marks ✅ and sets todo status to ✅ Complete.
21. **Cleanup Agent (dedup pass)** — scans `docs/RETROSPECTIVE_REPORT.md`, `docs/PLAYBOOK.md`, and `.ai/lessons.md` for duplicate entries. Consolidates and removes redundancy.

## Key Rules

- **Context Gateway (mandatory):** Every agent spawn MUST be preceded by a Librarian query. No agent receives raw files — only Librarian-curated context briefs. See copilot-instructions.md Context Gateway Protocol.
- **Todo tracking:** Every agent reads the todo file, marks tasks 🔵 in-progress before starting and ✅ done when complete.
- **Granular spawning:** One Test Writer and one Worker per individual function — never batch.
- **Mandatory approval gate:** Never proceed to implementation without explicit user confirmation.
- **Circuit breaker:** If Worker fails 2+ functions in a row or Reviewer rejects, halt and re-plan.

> **Relationship:** This skill implements the **Planning Sequence** defined in `copilot-instructions.md` / `AGENTS.md`. Use this skill for step-by-step detail and checklists.
