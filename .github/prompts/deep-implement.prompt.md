---
description: Run the full DEEP_MODE adversarial pipeline for a business logic feature
agent: Architect
---

# Deep Implement: ${input:featureDescription}

## Mode: DEEP_MODE (Business Logic Only)

> **Scope check:** DEEP_MODE is for business logic, data processing, services, and algorithms.
> For GUI/UI/frontend work, use the standard `/implement-plan` workflow instead.

Full adversarial plan-critique-implement pipeline:

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`
2. **Design the architecture** for: ${input:featureDescription}
   - Think ahead: identify shared utilities, base classes, constants FIRST
   - Run deduplication analysis against existing inventory
   - Write the architecture plan to `.ai/plans/`
3. **Hand off to Critic** for review
4. Iterate until approved (max 5 rounds)
5. Critic hands off to **Planner** for function-level breakdown
6. Planner hands off to **Implementer** which:
   - Spawns **Scaffolder** to create file stubs
   - Spawns **Test Writer** (gpt-5-mini) per file to write tests
   - Spawns **Worker** (gpt-5-mini) per function to implement + red-green loop
7. **Reviewer** checks the final result

Start by reading the context files, then design the architecture.
