---
description: Generate an implementation plan for a new feature or task
agent: Planning
---

# Plan a Feature

Create a detailed implementation plan for the following:

**Feature:** ${input:featureDescription}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — user's coding style, TURBO_MODE and DEEP_MODE settings
   - `docs/PLAYBOOK.md` — current architecture decisions and patterns
   - `docs/CODE_INVENTORY.md` — existing code symbols to avoid duplication

2. **Read the approved architecture plan** (always present since DEEP_MODE is always ON):
   - Review any Innovator Log and Critique Log sections for design decisions

3. **Decomposition-first breakdown** — plan shared pieces first, consumers second:
   - **Phase 0 — Shared foundations:** constants, config, types/models, shared utilities
   - **Phase 1–N — Feature phases:** in dependency order, each building on earlier phases
   - **Final Phase — Wiring & integration:** connect modules, entry points

4. **Deduplication pass (mandatory):**
   - For every planned function, search `CODE_INVENTORY.md` and `src/` for existing similar logic
   - Mark matches as `[REUSE: existing_symbol]` or `[EXTEND: existing_symbol]`

5. **Produce two-level plans:**
   - **Level 1** — High-level plan in `.ai/plans/{YYYY-MM-DD}_{topic}.plan.md` (use `_TEMPLATE.plan.md`)
   - **Level 2** — Detailed impl plans in `.ai/plans/impl/` with function-level checkboxes

6. **Create a todo file** at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`:
   - Use the template at `.ai/todos/_TEMPLATE.todo.md`
   - Add a checkbox task for **every pipeline step and every function** with its assigned agent
   - Group tasks by phase (planning, scaffolding, testing, implementation, review, docs)
   - This file is the **living tracker** — all agents will read and update it throughout the pipeline

7. **Present plan to user for explicit approval.** Do NOT proceed until the user confirms.
   - Show the full plan summary: phases, functions, dependencies, and estimated scope
   - Suggest: *"Ready to implement? I recommend opening a new chat session and using `/deep-implement` or `/implement-plan` to keep context clean."*
   - **If user does not approve:** restart the pipeline from step 1 — re-read context, re-run deduplication, and revise the plan to address feedback. This ensures no dependencies or context are missed in the revision.
