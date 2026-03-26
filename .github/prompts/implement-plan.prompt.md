---
description: Resume implementation from a saved plan (produced by /plan-only). Runs the full pipeline from scaffolding through retrospective.
---

# Implement from Plan: ${input:planPath}

## Full Implementation Pipeline (Steps 13–22)

> **Purpose:** Pick up where `/plan-only` left off. Reads the saved plan artifacts from disk
> and runs the complete implementation → test → review → security → docs → retrospective pipeline.
>
> **Prerequisite:** A completed `/plan-only` run with all artifacts on disk (spec, research brief,
> architecture plan, impl plan, todo file). The plan must have status 🟢 Approved.
>
> **Designed for:** Starting a fresh session the morning after an overnight planning batch.

### Phase 0 — Load & Validate Plan

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `.ai/lessons.md`
2. **Read the plan file** at the path provided and all linked artifacts:
   - Architecture plan: `.ai/plans/{date}_{topic}.plan.md`
   - Impl plan: `.ai/plans/impl/{date}_{topic}.impl.md`
   - Todo file: `.ai/todos/{date}_{topic}.todo.md`
   - Enriched spec: `.ai/specs/{date}_{topic}.spec.md`
   - Research brief: `.ai/research/{date}_{topic}.research.md`
3. **Validate plan status** — confirm the plan is marked 🟢 Approved. If 🟡 Needs Revision, stop and inform the user.
4. **Present plan summary** — show: number of functions, files to create/modify, dependency list, phases.
5. **Install dependencies** — if the research brief lists dependencies, install them now.
6. **Ask for user approval** — *"Plan loaded: N functions across M files. Ready to implement?"*
   - If user does not approve, stop. Suggest re-running `/plan-only` to revise.

### Phase 1 — Scaffolding

7. **Scaffolder Agent** — create file stubs with signatures and docstrings per the impl plan.
   - Use the UI Preview's component decomposition (if available in `.ai/previews/`) for frontend stubs.
   - Mark scaffolding tasks ✅ in the todo file.

### Phase 2 — Test Writing

8. **Test Writer Agent** (one per function/module) — write 15+ tests per function that fail on stubs (red phase).
   - Follow the test structure from `docs/PLAYBOOK.md`
   - Mark test-writing tasks ✅ in the todo file.

### Phase 3 — Implementation

9. **Worker Agent** (one per function/module) — implement each function following the red-green loop:
   - Mark the task 🔵 in-progress in the todo file **before starting**
   - Run existing tests — confirm they fail (red) on the stub
   - Implement the function — replace stub with real logic
   - Run tests — check if they pass (green)
   - If tests fail: fix implementation (NOT tests), re-run (max 5 attempts)
   - Mark the task ✅ done in the todo file when tests pass
   - Move to the next function
10. **Verify all files on disk** — after each Worker completes, confirm output files exist. Don't trust context-window-only evidence.

### Phase 4 — Integration Testing

11. **Integration Tester Agent** — write and run E2E/integration tests for multi-module flows.
    - Cover the boundaries between new and existing code.
    - Mark ✅ in the todo file.

### Phase 5 — Review

12. **Reviewer Agent** — validate the full implementation:
    - Quality, correctness, adherence to the architecture plan
    - Check todo for skipped/incomplete tasks
    - Verify functions ≤40 lines, doc comments on exports, no silent catches
    - Mark review ✅ in the todo file.
    - If rejected → Workers fix → re-review.

### Phase 6 — Security & Quality

13. **Security Agent** — audit all code for vulnerabilities (OWASP Top 10). Append findings to `docs/SECURITY_REPORT.md`. Mark ✅. If CRITICAL/HIGH → Workers fix → re-verify.
14. **Code Quality Agent** — scan for duplication, code smells, dead code. Append findings to `docs/QUALITY_REPORT.md`. Mark ✅. If CRITICAL/HIGH → Workers fix → re-verify.

### Phase 7 — Documentation & Closure

15. **Doc Updater Agent** — update all documentation:
    - `docs/CODE_INVENTORY.md` — new symbols
    - `docs/BUSINESS_LOGIC.md` — new data flows / module responsibilities
    - `docs/files/` — per-file docs for new/modified files
    - `docs/API_DOCUMENTATION.md` — new endpoints (if applicable)
    - Write session summary to `.ai/sessions/`
    - Mark doc tasks ✅ in the todo file.
16. **Retrospective Agent (chunked)** — review the session transcript. Append findings to `docs/RETROSPECTIVE_REPORT.md` and `docs/PLAYBOOK.md`. Mark ✅. Set todo status to ✅ Complete.
17. **Cleanup Agent (dedup pass)** — scan reports and lessons for duplicate entries. Consolidate.

## Two-Phase Workflow

This prompt is designed to work with `/plan-only` as a two-phase pipeline:

```text
Session 1 (overnight / batch):    /plan-only  →  artifacts saved to .ai/
Session 2 (next morning / fresh):  /implement-plan  →  reads artifacts, implements everything
```

This separation keeps each session's context window clean and allows planning to run unattended.

## Error Recovery

- If a Worker fails 2+ functions in a row → halt, record in `.ai/lessons.md`, re-plan from the failing module.
- If the Reviewer rejects → Workers fix specific issues, re-review (don't restart the full pipeline).
- If tests reveal a plan flaw → update the impl plan, then continue from the affected function.
