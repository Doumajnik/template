# DEEP_MODE Pipeline

> Full adversarial plan-critique-implement pipeline.
> DEEP_MODE is **permanently ON** for this project — every task goes through this pipeline.
> Reference file — the orchestrator reads this when planning any task.
> All agents below use the model defined by `AGENT_MODEL` in `.ai/PREFERENCES.md`.

---

## When to Use

Use DEEP_MODE for **ALL tasks** — every feature, fix, refactor, or change goes through the full adversarial pipeline. No exceptions. The orchestrator always runs Architect → Critic → iterate before implementation.

## Pipeline

The orchestrator spawns agents in this sequence:

1. **Research Agent** — searches the web for the topic: best practices, libraries, patterns, pitfalls, API docs. Produces a structured research brief in `docs/discoveries/`. Identifies all dependencies that will be needed.

2. **Dependency mapping & install** — based on the Research Agent's findings, the Orchestrator maps out all required dependencies and installs them upfront in the project's isolated environment before any coding begins.

3. **Architect Agent** — reads `docs/BUSINESS_LOGIC.md`, discovery summaries, and the **Research Agent's brief**. Designs the system: logic, data flow, decomposition, deduplication report. Does NOT read source code.

4. **Innovator Agent** — receives the Architect's plan and generates creative, unconventional alternatives. Challenges assumptions, suggests outside-the-box approaches. Reports ideas back to the Orchestrator.

5. **Architect (revision)** — Orchestrator feeds the Innovator's best ideas to the Architect for consideration and potential incorporation.

6. **Critic Agent** — reviews for duplication, missing decomposition, over-engineering, completeness. Returns approval or sends back for fixes.

7. **Iterate** — orchestrator re-spawns Architect with Critic's feedback. Max 10 rounds. All agents report back to the Orchestrator — no direct handoffs.

8. **Planning Agent** — breaks the approved architecture into function-level impl plans. Reads `docs/files/` for per-file context if needed. Shared utilities first, then features, then wiring. **Creates the todo file** (`.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`) — the living tracker that all subsequent agents read and update dynamically.

9. **User approval (MANDATORY GATE)** — orchestrator presents the full plan and asks for explicit approval. Suggest opening a new chat session for implementation to keep context clean. **If user does not approve**, restart the entire pipeline from step 1 to ensure no dependencies or context are missed in the revision.

> **Todo tracking:** From this point on, every agent reads the todo file, marks its task(s) 🔵 in-progress before starting and ✅ done when complete, and appends to the Progress Log.

10. **Scaffolder Agent** — creates file stubs with signatures and docstrings. Marks scaffolding tasks ✅ in todo.

11. **Test Writer Agent** per function — writes 15+ tests per function that fail on stubs (red). One instance per function. Marks test tasks ✅ in todo.

12. **Worker Agent** per function — reads source code, implements, runs red-green loop until tests pass. One instance per function. Marks each function ✅ in todo as it passes.

13. **Integration Tester Agent** — writes and runs E2E/integration tests for multi-module flows. Marks ✅ in todo.

14. **Reviewer Agent** — checks the final result for quality, correctness, adherence to plan. Checks todo for skipped/incomplete tasks. Marks review ✅ in todo.

15. **Security Agent** — audits all code for security vulnerabilities using the OWASP Top 10:2025 checklist. Appends findings to `docs/SECURITY_REPORT.md`. Marks ✅ in todo. If CRITICAL/HIGH → Workers fix → re-verify.

16. **Code Quality Agent** — scans for duplication, suboptimal code, dead code, and code smells. Appends findings to `docs/QUALITY_REPORT.md`. Marks ✅ in todo. If CRITICAL/HIGH → Workers fix → re-verify.

17. **Doc Updater Agent** — updates all documentation. Marks doc tasks ✅ in todo.

18. **Retrospective Agent** — reviews all agent decisions from this cycle, audits decision quality (what was done, why, was it the right call), identifies positive patterns and mistakes, and updates `docs/PLAYBOOK.md` with new rules. Appends findings to `docs/RETROSPECTIVE_REPORT.md`. Marks ✅ and sets todo status to ✅ Complete.

## Key Principles

- **Decomposition-first:** shared utilities and base classes are planned and built before feature code.
- **Deduplication:** every planned symbol is checked against existing inventory before creation.
- **Test-first:** tests are written before implementation (red-green loop).
- **Isolation:** each worker only edits its assigned file.

## When OFF

DEEP_MODE is **permanently ON** for this project. This section is kept for reference only. If it were ever turned off, the flow would skip Architect and Critic rounds: Planning → Scaffolder → Test Writer → Worker → Integration Tester → Reviewer → Security → Code Quality → Doc Updater → Retrospective.
