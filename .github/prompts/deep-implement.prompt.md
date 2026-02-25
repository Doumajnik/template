---
description: Run the full DEEP_MODE adversarial pipeline for any task (feature, bug fix, refactor, enhancement)
agent: Architect
---

# Deep Implement: ${input:taskDescription}

## Mode: DEEP_MODE (All Tasks)

> **Scope:** DEEP_MODE applies to every type of change — features, bug fixes, refactoring, enhancements, and updates. The full adversarial pipeline runs for all work.

Full adversarial plan-critique-implement pipeline:

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`
2. **Orchestrator spawns Architect** to design the architecture for: ${input:taskDescription}
   - Think ahead: identify shared utilities, base classes, constants FIRST
   - Run deduplication analysis against existing inventory
   - Write the architecture plan to `.ai/plans/`
3. **Orchestrator spawns Innovator** to challenge assumptions and propose creative alternatives
4. **Orchestrator spawns Architect** again to incorporate Innovator's best ideas
5. **Orchestrator spawns Critic** for adversarial review — iterate until approved (max 5 rounds)
6. **Orchestrator spawns Planning** agent for function-level breakdown
7. **Orchestrator spawns Scaffolder** to create file stubs
8. **Orchestrator spawns Test Writer** (Opus 4.6) per file to write 15+ tests per function
9. **Orchestrator spawns Worker** (Opus 4.6) per function to implement + red-green loop
10. **Orchestrator spawns Reviewer** to check the final result
11. **Orchestrator spawns Doc Updater** to update all documentation

Start by reading the context files, then design the architecture.
