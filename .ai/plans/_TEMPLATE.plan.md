# Plan Template (High-Level)

> Save as: `.ai/plans/{YYYY-MM-DD}_{short-topic}.plan.md`
> This is the **high-level execution plan**. Each phase links to a detailed
> implementation plan in `.ai/plans/impl/` that breaks it down to functions.

---

## Plan: {Short Topic}

**Date:** {YYYY-MM-DD}
**Status:** 🟡 Draft | 🟢 Approved | 🔵 In Progress | ✅ Complete

## Objective
<!-- 2-3 sentences. What are we building and why? -->

## Existing Code to Reuse
<!-- Search CODE_INVENTORY.md FIRST. List anything that can be reused. -->
| Symbol | File | Reuse how |
|--------|------|-----------|
|        |      |           |

---

## Phases

<!-- 
  Each phase is a logical chunk of work.
  Each phase gets a detailed impl plan in .ai/plans/impl/{plan-name}_phase-{N}.impl.md
  Mark phases done as their impl plans are fully checked off.
-->

- [ ] **Phase 1: {Name, e.g. "Shared Utilities"}** `[delegatable]`
  - Scope: {what this phase delivers}
  - Files: `src/utils/{name}.{ext}`
  - Impl plan: `.ai/plans/impl/{plan-name}_phase-1.impl.md`

- [ ] **Phase 2: {Name, e.g. "Models / Types"}** `[delegatable]`
  - Scope: {what this phase delivers}
  - Files: `src/models/{name}.{ext}`
  - Impl plan: `.ai/plans/impl/{plan-name}_phase-2.impl.md`

- [ ] **Phase 3: {Name, e.g. "Core Logic / Services"}** `[inline]`
  - Scope: {what this phase delivers}
  - Files: `src/services/{name}.{ext}`
  - Impl plan: `.ai/plans/impl/{plan-name}_phase-3.impl.md`

- [ ] **Phase 4: {Name, e.g. "Tests"}** `[delegatable]`
  - Scope: {what this phase delivers}
  - Files: `tests/{mirror path}`
  - Impl plan: `.ai/plans/impl/{plan-name}_phase-4.impl.md`

- [ ] **Phase 5: Wiring & Integration** `[inline]`
  - Scope: connect all modules, verify end-to-end
  - Files: entry point / main service

---

## Post-Implementation Checklist

- [ ] `docs/CODE_INVENTORY.md` updated with all new symbols
- [ ] `docs/API_DOCUMENTATION.md` updated with any API usage found
- [ ] `docs/PLAYBOOK.md` updated with any new decisions
- [ ] `README.md` updated if structure/setup/features changed
- [ ] `.gitignore` updated if new tooling/dirs introduced
- [ ] `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md` marked ✅ Complete
- [ ] `.ai/sessions/{YYYY-MM-DD}_{topic}.md` summary written
- [ ] Git commit with conventional message

## Critique Log (DEEP_MODE only)

<!-- Filled by the Architect and Critic agents during their review loop -->
<!-- Architecture plan: .ai/plans/{YYYY-MM-DD}_{topic}.architecture.md -->

| Round | Issues Found | Resolution | Verdict |
|-------|--------------|------------|---------|
|       |              |            |         |

---

## Acceptance Criteria

- [ ] {Specific criteria for this feature}
- [ ] All functions have doc comments
- [ ] No duplication with existing inventory
- [ ] Tests pass
- [ ] Deduplication report reviewed (DEEP_MODE)
