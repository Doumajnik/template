---
description: Execute an implementation plan step-by-step
agent: Worker
---

# Implement a Plan

Read and implement the plan at the following path:

**Plan file:** ${input:planPath}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — user's coding style preferences
   - `docs/PLAYBOOK.md` — architecture patterns to follow
   - `docs/CODE_INVENTORY.md` — existing symbols for reference

2. **Read the plan file** and understand the full scope.

3. **Read the todo file** in `.ai/todos/` that corresponds to this plan:
   - This is your **living checklist** — follow it task by task
   - If no todo file exists, create one using `.ai/todos/_TEMPLATE.todo.md` with a task for every function in the plan

4. **Ask for explicit user approval before starting implementation.**
   - Present a summary: number of functions, files to create/modify, dependencies required
   - Suggest: *"This plan has N functions across M files. I recommend opening a new chat session for implementation to keep context clean. Ready to proceed?"*
   - **If user does not approve:** stop. Do NOT implement anything. Inform the user they should re-run the full planning pipeline (`/plan-feature` or `/deep-implement`) from the beginning to revise the plan — this ensures no dependencies or context are missed.
   - **Only proceed to step 5 after explicit user confirmation.**

5. **For each function in the plan**, follow the red-green loop:
   - Mark the task as 🔵 in-progress in the todo file **before starting**
   - Read the stub file (created by the Scaffolder)
   - Run the existing tests — confirm they fail (red) on the stub
   - Implement the function — replace the stub with real logic
   - Run the tests again — check if they pass
   - If tests fail: read output, fix implementation (not tests), re-run (max 5 attempts)
   - If tests pass (green): mark the task as ✅ done in the todo file and append to its Progress Log
   - Move to the next function

6. **Check off each step** in the plan file as you complete it.

7. **After all functions pass:**
   - Check for errors and warnings in all modified files — fix all of them
   - Ensure every exported function has a doc comment
   - Keep functions under ~40 lines
   - Handle errors explicitly — no silent catches

8. **Update the todo file** — verify all your function tasks are marked ✅ done. Do NOT mark the overall todo status as ✅ Complete — the Retrospective Agent (final pipeline step) handles that.

9. **Report back** with: files modified, symbols implemented, test results.

> **Note:** This prompt covers the Worker phase only. After the Worker completes, the Orchestrator proceeds with the remaining pipeline steps: Integration Tester → Reviewer → Security → Code Quality → Doc Updater → Retrospective.
