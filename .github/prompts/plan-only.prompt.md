---
description: Run ONLY the planning phases (overnight-safe). Produces all artifacts needed for implementation in a separate session.
---

# Plan Only: ${input:taskDescription}

## Planning-Only Pipeline (Steps 1–12)

> **Purpose:** Run the full adversarial planning pipeline WITHOUT implementation.
> Designed for overnight or batch runs — produces all artifacts to disk so implementation
> can happen in a fresh session using `/implement-plan`.
>
> **Output:** spec, research brief, architecture plan, critique log, implementation plan, todo file, UI preview (if applicable).
> **Does NOT:** scaffold, write tests, implement code, or run reviews.

### Phase A — Analysis & Research

1. **Read context** — `.ai/PREFERENCES.md`, `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `.ai/lessons.md`
2. **Prompt Engineer Agent** — analyze the request deeply. Produce an enriched spec at `.ai/specs/{YYYY-MM-DD}_{topic}.spec.md` covering:
   - Functional requirements, edge cases, data needs, security, UI, acceptance criteria
   - `[ASK USER]` questions (if any — present and wait for answers before proceeding)
3. **Discovery Agent** — `[CONDITIONAL]` if new data, libraries, or external APIs are involved. Ask user first.
4. **Research Agent** — search for best practices, libraries, patterns, pitfalls. Produce a research brief at `.ai/research/{YYYY-MM-DD}_{topic}.research.md` with:
   - Recommended approach, dependency list, trade-offs, risks
5. **Dependency mapping** — list all required dependencies in the research brief. Do NOT install yet (that happens at implementation time).

### Phase B — Architecture & Adversarial Review

6. **Architect Agent** — design the system using the enriched spec + research brief. Produce architecture plan at `.ai/plans/{YYYY-MM-DD}_{topic}.plan.md` with:
   - System design, data flow, module decomposition, deduplication report
   - Innovator Log section (filled in step 8)
   - Critique Log section (filled in steps 9-10)
7. **Innovator Agent** — review the architecture plan, propose creative alternatives. Append to the plan's Innovator Log.
8. **Architect (revision)** — incorporate Innovator's best ideas. Update the plan.
9. **Critic Agent** — adversarial review. Focus on: duplication, missing decomposition, over-engineering, completeness, regressions.
10. **Iterate** — Architect↔Critic loop, max 10 rounds. All feedback appended to the plan's Critique Log. Continue until Critic approves or max rounds reached.

### Phase C — Implementation Planning

11. **Planning Agent** — break the approved architecture into function-level implementation plans:
    - Shared utilities first, then features, then wiring
    - **Deduplication pass (MANDATORY):** check every planned function against `CODE_INVENTORY.md` and `src/`
    - Mark matches as `[REUSE: existing_symbol]` or `[EXTEND: existing_symbol]`
    - Produce detailed impl plan at `.ai/plans/impl/{YYYY-MM-DD}_{topic}.impl.md`
    - **Create the todo file** at `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md` with tasks for every pipeline step and every function
12. **UI Preview Agent** — `[CONDITIONAL]` if frontend work is involved, generate HTML/CSS preview in `.ai/previews/`.

### Phase D — Approval Gate

13. **Present plan to user** — show the full plan summary:
    - Phases, functions, dependencies, files to create/modify
    - Deduplication results (what's reused vs new)
    - Critique rounds summary (how many, what was challenged)
    - UI preview link (if applicable)
    - **Suggest:** *"Planning complete. All artifacts saved to `.ai/`. To implement, open a new chat and use `/implement-plan`."*
    - Mark the plan status as 🟢 Approved (or 🟡 Needs Revision if user requests changes)

## Artifacts Produced

After this pipeline completes, the following files exist on disk:

| Artifact | Path | Purpose |
| --- | --- | --- |
| Enriched spec | `.ai/specs/{date}_{topic}.spec.md` | Requirements, edge cases, acceptance criteria |
| Research brief | `.ai/research/{date}_{topic}.research.md` | Best practices, dependencies, trade-offs |
| Architecture plan | `.ai/plans/{date}_{topic}.plan.md` | System design with Innovator + Critique logs |
| Impl plan | `.ai/plans/impl/{date}_{topic}.impl.md` | Function-level breakdown with phases |
| Todo file | `.ai/todos/{date}_{topic}.todo.md` | Living tracker for implementation |
| UI preview | `.ai/previews/{date}_{topic}/` | `[CONDITIONAL]` HTML/CSS mockups |

## Multi-Round Planning (Overnight Mode)

To run multiple planning rounds overnight:

1. Queue multiple `/plan-only` invocations — one per task/feature
2. Each produces independent artifacts in `.ai/`
3. Next morning, review all plans and approve/revise
4. For each approved plan, run `/implement-plan` in separate sessions

Plans can be revised by running `/plan-only` again with the same topic — the agents will read the existing artifacts and iterate.
