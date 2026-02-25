---
description: Execute an implementation plan step-by-step
agent: Worker
---

# Implement a Plan

Read and execute the implementation plan at the following path:

**Plan file:** ${input:planPath}

## Instructions

1. Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, and `docs/CODE_INVENTORY.md` first.
2. Read the plan file and understand the full scope.
3. Implement each step in order:
   - `[delegatable]` steps → the Orchestrator spawns a sub-agent with focused context
   - `[inline]` steps → implement directly
4. Check off each step in the plan file as you complete it.
5. After all steps are done, update:
   - `docs/CODE_INVENTORY.md` with all new/modified symbols
   - `docs/PLAYBOOK.md` with any new architecture decisions
   - `README.md` if structure or setup changed
   - `.gitignore` if new tooling was introduced
