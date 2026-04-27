# Plan and Implement: ${input:taskDescription}

## Full Planning Sequence (Planning Sequence steps 1–25)

> **Purpose:** Run the entire Planning Sequence — Phase A (planning, steps 1–14) AND Phase B
> (implementation, steps 15–25) — in a single chat session.
>
> **Maps to:** [AGENTS.md](../../AGENTS.md) Planning Sequence — both phases.
>
> **Use this when:**
>
> - The task is small enough that the full plan + implementation fits in one context window.
> - You want a quick end-to-end run without resuming from disk.
>
> **Do NOT use this for large tasks.** For anything non-trivial, prefer:
>
> 1. `/plan-only` (overnight, unattended) — produces the plan and stops at User Approval.
> 2. `/implement-plan {plan-path}` (fresh session, next morning) — picks up Phase B from disk.
>
> Splitting keeps context windows small, lets the user review the plan before any code is touched,
> and is the recommended workflow for production work.

---

## How this works

This prompt runs the Planning Sequence end-to-end. It is the literal concatenation of
`/plan-only` followed by `/implement-plan`, with the User Approval gate (step 14) preserved
inline rather than at a session boundary.

1. **Phase A (steps 1–14)** — follow [.github/prompts/plan-only.prompt.md](./plan-only.prompt.md) exactly,
   stopping at step 14 (User Approval).
2. **User Approval gate** — present the full plan, UI preview (if any), Cost brief, and
   Observability plan. Wait for explicit approval.
3. **Phase B (steps 15–25)** — follow [.github/prompts/implement-plan.prompt.md](./implement-plan.prompt.md)
   using the just-produced plan path, no need to re-load from disk.

All Consistency Check gates (after step 12, after step 18, after step 23) still run. All
Librarian-first rules still apply. Numeric stability of step numbers is preserved.

---

## When NOT to run this

- The task is a **change to existing code** → use the **Change Pipeline** instead (a
  separate flow with impact analysis and a regression checklist).
- The task is a **live production incident** → use the **Incident Response Pipeline**
  (declare with the Incident Commander).
- The task is a **bug fix** with a known reproduction → use **Autonomous Bug Fixing**
  (Debug Agent first).
- The codebase is **new to you** → run `/onboard-project` first.
