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

### Phase 1 — Context & Research

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`
2. **Discovery Agent** — if this task involves new data, libraries, or external APIs. Ask user first.
3. **Research Agent** — research the topic: best practices, libraries, patterns, pitfalls. Produce a research brief with dependency list.
4. **Install dependencies** — based on the Research Agent's findings, install all required dependencies upfront.

### Phase 2 — Design & Critique

5. **Architect** — design the architecture. Use the Research Agent's brief as input. Identify shared utilities, base classes, constants FIRST. Run deduplication analysis against existing inventory.
6. **Innovator** — challenge assumptions, propose creative alternatives.
7. **Architect (revision)** — incorporate Innovator's best ideas.
8. **Critic** — adversarial review. Iterate Architect↔Critic loop (max 10 rounds) until approved.

### Phase 3 — Planning & Approval

9. **Planning Agent** — function-level breakdown of the approved architecture. Creates the todo file at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`.
10. **User approval (MANDATORY GATE)** — present the full plan and ask for explicit approval. If rejected, restart from step 1.

See [pipeline checklist](./references/pipeline-checklist.md) for the full checklist of gates and deliverables.

### Phase 4 — Implementation

11. **Scaffolder** — create file stubs with signatures and docstrings. Mark scaffolding tasks ✅.
12. **Test Writer** (one per function) — write 15+ tests per function that fail on stubs (red phase). Mark ✅.
13. **Worker** (one per function) — implement code, red-green loop until tests pass. Mark ✅.
14. **Integration Tester** — write and run E2E/integration tests. Mark ✅.

### Phase 5 — Review & Audit

15. **Reviewer** — validate code quality, correctness, plan adherence. If fail → Worker fixes. Mark ✅.
16. **Security Agent** — audit for vulnerabilities, append to `docs/SECURITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.
17. **Code Quality Agent** — scan for duplication/smells, append to `docs/QUALITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅.

### Phase 6 — Documentation & Retrospective

18. **Doc Updater** — update all documentation, write session summary. Mark ✅.
19. **Retrospective Agent** — review all decisions, update `docs/PLAYBOOK.md`, append to `docs/RETROSPECTIVE_REPORT.md`. Mark todo status as ✅ Complete.

## Key Rules

- **Todo tracking:** Every agent reads the todo file, marks tasks 🔵 in-progress before starting and ✅ done when complete.
- **Granular spawning:** One Test Writer and one Worker per individual function — never batch.
- **Mandatory approval gate:** Never proceed to implementation without explicit user confirmation.
- **Circuit breaker:** If Worker fails 2+ functions in a row or Reviewer rejects, halt and re-plan.
