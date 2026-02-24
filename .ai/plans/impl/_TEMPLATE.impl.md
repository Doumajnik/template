# Implementation Plan Template (Function-Level Detail)

> Save as: `.ai/plans/impl/{plan-name}_phase-{N}.impl.md`
> This is the **detailed execution contract** for a single phase.
> The implementer reads it top-to-bottom and spawns a sub-agent for every
> `[delegatable]` line. Check off `[x]` as each function is implemented.

---

## Impl: {Phase Name} (from {Parent Plan})

**Parent plan:** `.ai/plans/{YYYY-MM-DD}_{topic}.plan.md`
**Phase:** {N}
**Status:** 🟡 Draft | 🔵 In Progress | ✅ Complete

---

## Functions

<!--
  RULES:
  - Every function, class, method, constant, and type gets its own checkbox line.
  - Each line has: name, full signature, one-liner, and [delegatable] or [inline].
  - The implementer spawns one sub-agent per [delegatable] line.
  - Sub-agents receive: this line + the file path + relevant inventory/playbook context.
  - Check off [x] immediately after each item is done.
-->

### `src/{path}/{filename}.{ext}`

**Purpose:** {One-line description of what this file does}

| #   | Symbol         | Signature                                    | Description        | Mode            |
|-----|----------------|----------------------------------------------|--------------------|-----------------|
| 1   | `functionName` | `(param: Type, param2: Type) → ReturnType`   | What it does       | `[delegatable]` |
| 2   | `anotherFn`    | `(input: Type) → ReturnType`                 | What it does       | `[delegatable]` |
| 3   | `ClassName`    | —                                            | What it represents | `[inline]`      |

**Progress:**

- [ ] #1 `functionName` `[delegatable]`
- [ ] #2 `anotherFn` `[delegatable]`
- [ ] #3 `ClassName` `[inline]`
  - [ ] `constructor(deps: Type)` — initialization
  - [ ] `methodA(param: Type) → ReturnType` — what it does
  - [ ] `methodB() → void` — what it does

### `src/{path}/{another_file}.{ext}` (if multiple files in this phase)

**Purpose:** {One-line description}

**Progress:**

- [ ] #1 `symbol` `[delegatable]`

---

## Constants & Types

- [ ] `CONSTANT_NAME: Type = value` — what it holds `[delegatable]`
- [ ] `InterfaceName { field: Type }` — what it describes `[delegatable]`

---

## Dependencies

<!-- List any imports from other phases or existing inventory code -->

| Depends on | From | Status |
| --- | --- | --- |
| `existingFunction` | `src/utils/...` | exists |
| `Phase 1 output` | `src/services/...` | in progress |

---

## Notes

<!-- Any gotchas, edge cases, or decisions specific to this phase -->
