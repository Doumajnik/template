# DEEP_MODE Pipeline

> Full adversarial plan-critique-implement pipeline.
> DEEP_MODE is **permanently ON** for this project — every task goes through this pipeline.
> Reference file — the orchestrator reads this when planning any task.

---

## When to Use

Use DEEP_MODE for **ALL tasks** — every feature, fix, refactor, or change goes through the full adversarial pipeline. No exceptions. The orchestrator always runs Architect → Critic → iterate before implementation.

## Pipeline

The orchestrator spawns agents in this sequence:

1. **Architect Agent** (Opus 4.6) — reads `docs/BUSINESS_LOGIC.md` and discovery summaries. Designs the system: logic, data flow, decomposition, deduplication report. Does NOT read source code.

2. **Innovator Agent** (Opus 4.6) — receives the Architect's plan and generates creative, unconventional alternatives. Challenges assumptions, suggests outside-the-box approaches. Reports ideas back to the Orchestrator.

3. **Architect (revision)** — Orchestrator feeds the Innovator's best ideas to the Architect for consideration and potential incorporation.

4. **Critic Agent** (Opus 4.6) — reviews for duplication, missing decomposition, over-engineering, completeness. Returns approval or sends back for fixes.

5. **Iterate** — orchestrator re-spawns Architect with Critic's feedback. Max 5 rounds. All agents report back to the Orchestrator — no direct handoffs.

6. **Planning Agent** (Opus 4.6) — breaks the approved architecture into function-level impl plans. Reads `docs/files/` for per-file context if needed. Shared utilities first, then features, then wiring.

7. **User approval** — orchestrator presents the plan, revises if needed.

8. **Scaffolder Agent** (Opus 4.6) — creates file stubs with signatures and docstrings.

9. **Test Writer Agent** (Opus 4.6) per file — writes 15+ tests per function that fail on stubs (red).

10. **Worker Agent** (Opus 4.6) per function — reads source code, implements, runs red-green loop until tests pass.

11. **Reviewer Agent** (Opus 4.6) — checks the final result for quality, correctness, adherence to plan.

12. **Doc Updater Agent** (Opus 4.6) — updates all documentation.

## Key Principles

- **Decomposition-first:** shared utilities and base classes are planned and built before feature code.
- **Deduplication:** every planned symbol is checked against existing inventory before creation.
- **Test-first:** tests are written before implementation (red-green loop).
- **Isolation:** each worker only edits its assigned file.

## When OFF

DEEP_MODE is **permanently ON** for this project. This section is kept for reference only. If it were ever turned off, the flow would skip Architect and Critic rounds: Planning → Scaffolder → Test Writer → Worker → Reviewer → Doc Updater.
