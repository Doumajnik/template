# Architecture Plan Template (DEEP_MODE)

> Save as: `.ai/plans/{YYYY-MM-DD}_{short-topic}.architecture.md`
> Written by the **Architect** agent, reviewed by the **Critic** agent.
> After approval, the **Planner** breaks this into function-level impl plans.

---

## Architecture: {Short Topic}

**Date:** {YYYY-MM-DD}
**Status:** 🟡 Draft | 🔴 In Review | 🟢 Approved
**Rounds:** 0/5

## Objective
<!-- 2-3 sentences. What are we building and why? -->

---

## Entities & Data Flow

<!-- 
  Core objects, their relationships, and how data moves between them.
  Use a simple diagram or list format.
-->

### Entities

| Entity | Purpose | Key Fields |
|--------|---------|------------|
|        |         |            |

### Data Flow
<!-- How data moves through the system: input → processing → output -->

---

## Decomposition Strategy

<!-- 
  CRITICAL: What gets built first? Shared pieces before consumers.
  This determines the phase order in the impl plans.
-->

### Build Order

1. **Shared foundations** — constants, config, types, shared utils
2. **Core logic** — the main business rules
3. **Services** — orchestration layer
4. **Wiring** — entry points, initialization

### Shared Utilities Identified
<!-- Utilities that ≥2 features will use — these get built in Phase 0 -->
| Utility | Used By | Purpose |
|---------|---------|---------|
|         |         |         |

### Base Classes / Interfaces
<!-- Abstractions that multiple implementations will extend -->
| Abstraction   | Implementations | Purpose |
|---------------|-----------------|---------|
|               |                 |         |

---

## Deduplication Report

<!-- MANDATORY. Search CODE_INVENTORY.md and src/ for every planned symbol. -->

### Existing Code to Reuse

| Planned Symbol | Existing Match | Action |
| --- | --- | --- |
| | | `REUSE` / `EXTEND` / `CONSOLIDATE` |

### New Code (no existing match)

| Symbol | File | Justification (why it's truly new) |
|--------|------|------------------------------------|
|        |      |                                    |

---

## Module Breakdown

### `src/{path}/{file}.{ext}`

**Purpose:** {one-liner}

**Public API:**

| Function/Method | Signature | Description |
|-----------------|-----------|-------------|
|                 |           |             |

<!-- Repeat for each file -->

---

## Error Handling Strategy
<!-- How errors propagate, what gets caught where, what bubbles up to the caller -->

---

## Optimization Notes
<!-- Performance considerations — only real ones, no premature optimization -->

---

## Critique Log

<!-- Filled by the Critic agent. One row per review round. -->

| Round | Verdict | Issues Found | Resolution |
|-------|---------|--------------|------------|
| 1     |         |              |            |
| 2     |         |              |            |
| 3     |         |              |            |
| 4     |         |              |            |
| 5     |         |              |            |

**Final Verdict:** ⏳ Pending
