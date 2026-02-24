---
description: Generate an implementation plan for a new feature or task
agent: Planner
---

# Plan a Feature

Analyze the codebase and create a detailed implementation plan for the following:

**Feature:** ${input:featureDescription}

## Instructions

1. Read `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, and `docs/CODE_INVENTORY.md` first.
2. Check `.ai/PREFERENCES.md` for **DEEP_MODE**. If ON and this is business logic, suggest using `/deep-implement` instead.
3. Search the existing codebase for related functionality.
4. Produce a step-by-step plan saved to `.ai/plans/` following the template at `.ai/plans/_TEMPLATE.plan.md`.
5. Each step must specify exact files, functions, and whether it's `[delegatable]` or `[inline]`.
6. Present the plan for review before any implementation begins.
