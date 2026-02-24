# DEEP_MODE Pipeline

> Full adversarial plan-critique-implement pipeline.
> Enabled when `DEEP_MODE: ON` in `.ai/PREFERENCES.md`.
> Reference file — the orchestrator reads this when DEEP_MODE is active.

---

## When to Use

Use DEEP_MODE for non-trivial **business logic** features: services, data processing, algorithms, APIs, core logic.

## Pipeline

The orchestrator spawns agents in this sequence:

1. **Architect Agent** (Opus 4.6) — reads `docs/BUSINESS_LOGIC.md` and discovery summaries. Designs the system: logic, data flow, decomposition, deduplication report. Does NOT read source code.

2. **Critic Agent** (Opus 4.6) — reviews for duplication, missing decomposition, over-engineering, completeness. Returns approval or sends back for fixes.

3. **Iterate** — orchestrator re-spawns Architect with Critic's feedback. Max 5 rounds.

4. **Planning Agent** (Opus 4.6) — breaks the approved architecture into function-level impl plans. Reads `docs/files/` for per-file context if needed. Shared utilities first, then features, then wiring.

5. **User approval** — orchestrator presents the plan, revises if needed.

6. **Scaffolder Agent** (Opus 4.6) — creates file stubs with signatures and docstrings.

7. **Test Writer Agent** (Opus 4.6) per file — writes 15+ tests per function that fail on stubs (red).

8. **Worker Agent** (Opus 4.6) per function — reads source code, implements, runs red-green loop until tests pass.

9. **Reviewer Agent** (Opus 4.6) — checks the final result for quality, correctness, adherence to plan.

10. **Doc Updater Agent** (Opus 4.6) — updates all documentation.

## Key Principles

- **Decomposition-first:** shared utilities and base classes are planned and built before feature code.
- **Deduplication:** every planned symbol is checked against existing inventory before creation.
- **Test-first:** tests are written before implementation (red-green loop).
- **Isolation:** each worker only edits its assigned file.

## When OFF

Use the standard plan-then-implement flow (skip Architect and Critic rounds). Go straight from Planning → Scaffolder → Test Writer → Worker → Reviewer → Doc Updater.
