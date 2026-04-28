---
description: Run the full adversarial pipeline for any task (feature, bug fix, refactor, enhancement)
---

# Deep Implement: ${input:taskDescription}

## Full Pipeline

> **Scope:** The full adversarial pipeline runs for all work — features, bug fixes, refactoring, enhancements, and updates.

Execute the full plan-critique-implement pipeline as defined in the Planning Sequence:

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`
2. **Discovery Agent** — if this task involves new data, libraries, or external APIs. Ask user first.
3. **Research Agent** — research the topic: best practices, libraries, patterns, pitfalls. Produce a research brief with dependency list.
4. **Install dependencies** — based on the Research Agent's findings, install all required dependencies upfront.
5. **Architect** — design the architecture for: ${input:taskDescription}
   - Use the Research Agent's brief as input
   - Identify shared utilities, base classes, constants FIRST
   - Run deduplication analysis against existing inventory
6. **Innovator** — challenge assumptions, propose creative alternatives
7. **Architect (revision)** — incorporate Innovator's best ideas
8. **Critic** — adversarial review. Iterate Architect↔Critic loop (max 10 rounds) until approved.
9. **Planning Agent** — function-level breakdown of the approved architecture. **Creates the todo file** at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md` with a task for every pipeline step and every function.
10. **User approval (MANDATORY GATE)** — present the full plan summary and ask for explicit approval:
    - Show: phases, functions, dependencies, files to create/modify, estimated scope
    - Suggest: *"Plan is ready. I recommend opening a new chat session for implementation to keep context clean. Approve to proceed?"*
    - **If user does not approve:** restart the entire pipeline from step 1 (re-read context, re-run Research, re-run Architect, etc.) to ensure no dependencies or context are missed in the revision. Do NOT skip steps on restart.
    - **Only proceed to step 11 after explicit user confirmation.**

> **Todo tracking:** From this point on, every agent reads the todo file, marks its tasks as 🔵 in-progress before starting, marks them ✅ done when complete, and appends to the Progress Log. The todo file is the **single source of truth** for what's done and what remains.

11. **Scaffolder** — create file stubs with signatures and docstrings. Mark scaffolding tasks ✅ in todo.
12. **Test Writer** (one per function) — write ≥10 tests per function across every applicable category of the 12-category taxonomy, edge cases first, that fail on stubs (red phase). Contributes to the ≥50-tests-per-functionality floor. Cannot read source — hard-enforced by Tool Guard. Mark test tasks ✅ in todo.
13. **Worker** (one per function) — implement code, red-green loop until tests pass. Mark each function ✅ in todo as it passes.
14. **Integration Tester** — write and run E2E/integration tests for multi-module flows. Mark ✅ in todo.
15. **Reviewer** — validate code quality, correctness, plan adherence. If fail → Worker fixes. Mark ✅ in todo.
16. **Security Agent** — audit for vulnerabilities, append to `docs/SECURITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅ in todo.
17. **Code Quality Agent** — scan for duplication/smells, append to `docs/QUALITY_REPORT.md`. If CRITICAL/HIGH → fix and re-verify. Mark ✅ in todo.
18. **Doc Updater** — update all documentation, write session summary. Mark ✅ in todo.
19. **Retrospective Agent** — review all decisions, update `docs/PLAYBOOK.md`, append to `docs/RETROSPECTIVE_REPORT.md`. Mark todo status as ✅ Complete.

Start by reading the context files, then proceed with Discovery/Research.
