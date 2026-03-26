# DEEP_MODE Pipeline

> Full adversarial plan-critique-implement pipeline.
> DEEP_MODE is **permanently ON** for this project — every task goes through this pipeline.
> Reference file — the orchestrator reads this when planning any task.
> All agents below use the model defined by `AGENT_MODEL` in `.ai/PREFERENCES.md`.

---

## When to Use

Use DEEP_MODE for **ALL tasks** — every feature, fix, refactor, or change goes through the full adversarial pipeline. No exceptions. The orchestrator always runs Architect → Critic → iterate before implementation.

## Pipeline

The orchestrator spawns agents in this sequence. This mirrors the Planning Sequence in AGENTS.md — keep in sync.

1. **Prompt Engineer Agent** — analyzes the raw user request. Produces an enriched spec in `.ai/specs/` covering functional requirements, edge cases, data needs, security, UI, and acceptance criteria. Surfaces `[ASK USER]` questions. Orchestrator presents questions to user before proceeding.

2. **Discovery Agent** — if new data involved (ask first).

3. **Research Agent** — searches the web for the topic: best practices, libraries, patterns, pitfalls, API docs. Uses the enriched spec as input. Produces a research brief with recommended approach and dependency list.

4. **Dependency mapping & install** — based on the Research Agent's findings, the Orchestrator maps out all required dependencies and installs them upfront in the project's isolated environment before any coding begins.

5. **Architect Agent** — reads `docs/BUSINESS_LOGIC.md`, discovery summaries, and the **Research Agent's brief**. Designs the system: logic, data flow, decomposition, deduplication report. Does NOT read source code.

6. **Innovator Agent** — receives the Architect's plan and generates creative, unconventional alternatives. Challenges assumptions, suggests outside-the-box approaches. Reports ideas back to the Orchestrator.

7. **Architect (revision)** — Orchestrator feeds the Innovator's best ideas to the Architect for consideration and potential incorporation.

8. **Critic Agent** — reviews for duplication, missing decomposition, over-engineering, completeness. Returns approval or sends back for fixes.

9. **Iterate** — orchestrator re-spawns Architect with Critic's feedback. Max 10 rounds. All agents report back to the Orchestrator — no direct handoffs.

10. **Planning Agent** — breaks the approved architecture into function-level impl plans. Reads `docs/files/` for per-file context if needed. Shared utilities first, then features, then wiring. **Creates the todo file** (`.ai/todos/{YYYY-MM-DD}_{topic}.todo.md`) — the living tracker that all subsequent agents read and update dynamically.

11. **UI Preview Agent** — `[CONDITIONAL]` if the task involves UI/frontend work, generates an interactive HTML/CSS preview in `.ai/previews/` with a component decomposition map. Skipped for backend-only tasks.

12. **User approval (MANDATORY GATE)** — orchestrator presents the full plan (and UI preview if applicable) and asks for explicit approval. Suggest opening a new chat session for implementation to keep context clean. **If user does not approve**, restart the entire pipeline from step 1 to ensure no dependencies or context are missed in the revision.

> **Todo tracking:** From this point on, every agent reads the todo file, marks its task(s) 🔵 in-progress before starting and ✅ done when complete, and appends to the Progress Log.

13. **Scaffolder Agent** — creates file stubs with signatures and docstrings. Uses the UI Preview's component decomposition (if available) to create accurate frontend stubs. Marks scaffolding tasks ✅ in todo.

14. **Test Writer Agent** per function — writes 15+ tests per function that fail on stubs (red). One instance per cohesive module or function group. Marks test tasks ✅ in todo.

15. **Worker Agent** per function — reads source code, implements, runs red-green loop until tests pass. One instance per cohesive module or function group. Marks each function ✅ in todo as it passes.

16. **Integration Tester Agent** — writes and runs E2E/integration tests for multi-module flows. Marks ✅ in todo.

17. **Reviewer Agent** — checks the final result for quality, correctness, adherence to plan. Checks todo for skipped/incomplete tasks. Marks review ✅ in todo.

18. **Security Agent** — audits all code for security vulnerabilities using the OWASP Top 10:2025 checklist. Appends findings to `docs/SECURITY_REPORT.md`. Marks ✅ in todo. If CRITICAL/HIGH → Workers fix → re-verify.

19. **Code Quality Agent** — scans for duplication, suboptimal code, dead code, and code smells. Appends findings to `docs/QUALITY_REPORT.md`. Marks ✅ in todo. If CRITICAL/HIGH → Workers fix → re-verify.

20. **Doc Updater Agent** — updates all documentation. Marks doc tasks ✅ in todo.

21. **Retrospective Agent (chunked)** — the Orchestrator partitions the session transcript into chunks and spawns one Retrospective instance per chunk. Each reads its transcript slice deeply (every tool call, command, response, decision) and appends findings to `docs/RETROSPECTIVE_REPORT.md` and `docs/PLAYBOOK.md`. A final merge pass writes the session summary and cross-chunk patterns. Marks ✅ and sets todo status to ✅ Complete.

22. **Cleanup Agent (dedup pass)** — scans `docs/RETROSPECTIVE_REPORT.md`, `docs/PLAYBOOK.md`, and `.ai/lessons.md` for duplicate entries, overlapping rules, and superseded lessons. Consolidates and removes redundancy.

## Key Principles

- **Decomposition-first:** shared utilities and base classes are planned and built before feature code.
- **Deduplication:** every planned symbol is checked against existing inventory before creation.
- **Test-first:** tests are written before implementation (red-green loop).
- **Isolation:** each worker only edits its assigned file.

## When OFF

DEEP_MODE is **permanently ON** for this project. This section is kept for reference only. If it were ever turned off, the flow would skip Architect and Critic rounds: Planning → Scaffolder → Test Writer → Worker → Integration Tester → Reviewer → Security → Code Quality → Doc Updater → Retrospective.
