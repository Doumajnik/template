# User Preferences

> This file is maintained by AI agents. They append new preferences as they learn how you work.
> Agents read this file at the start of every session to align with your style.

---

## Agent Settings

- **AGENT_MODEL: Claude Sonnet 4.6** — The **default** model for any agent without an explicit per-agent override. Per-agent model assignments are the **single source of truth** in [AGENTS.md](../AGENTS.md) under the **Sub-Agent Roster** table (between the `<!-- AGENT_MODEL_TABLE_START -->` markers). To change a model: edit AGENTS.md, then run `python scripts/update-agent-model.py` (or `.\scripts\update-agent-model.ps1`) to propagate into the `.agent.md` frontmatter. Run with `--check` in CI to catch drift.

### Model Tiers (guidance only — see AGENTS.md for assignments)

- **Claude Opus 4.7** — deepest reasoning, plan creation, creative design (Architect, Innovator, Scaffolder, Prompt Engineer, Planning).
- **Claude Opus 4.6** — strict adherence, adversarial review, debugging, high-stakes coordination (Critic, Reviewer, Security, Retrospective, Debug, Threat Modeling, Capacity Planner, Observability Engineer, Incident Commander, Consistency Check).
- **Claude Sonnet 4.6** — workhorse default for execution, audits, docs, research (everything else).

- **TURBO_MODE: ON** — Plan down to every function, mark everything possible as `[delegatable]`, mass-spawn sub-agents. Set to OFF if you prefer inline implementation with fewer sub-agents.
- **DEEP_MODE: ALWAYS ON** — Full adversarial pipeline on **every task**, no exceptions. Architect designs → Critic reviews → iterate until approved → Planner breaks down → Scaffolder creates stubs → Test Writer writes thorough tests → Workers implement with red-green loop. Never skip the Architect/Critic rounds.
- **BUDGET_MODE: OFF** — When ON, the Orchestrator runs the **Budget Pipeline** instead of the full Planning Sequence. Skips Innovator, Critic full-loop, Observability Engineer, Threat Modeling, Compliance Privacy, Analytics Instrumentation, Capacity Planner, Cost/FinOps, Mock Data Generator, Integration Tester, Security, Code Quality, Retrospective, Doc-Site Generator, Cleanup dedup, and Consistency Check Gates 1 & 2 (only Gate 3 runs at the end). Use for prototypes, throwaway experiments, hackathons, and "just make it work" tasks where the full review surface is not justified. **Mutually exclusive with DEEP_MODE** — turning BUDGET_MODE ON forces DEEP_MODE OFF for that session. See [AGENTS.md → Budget Pipeline](../AGENTS.md#budget-pipeline-budget_mode-on) for the exact step list.
- **GRANULAR SPAWNING: ON** — Spawn one Test Writer and one Worker per **cohesive module or function group**. For complex standalone functions (>20 lines with no relationship to other functions), spawn per individual function. For tightly related functions within the same module, batch them into a single agent call. This balances thoroughness with practical efficiency — spawning per-individual-function for a 120-function project is impractical.

---

## Code Style

<!-- Examples: "prefer arrow functions", "use 2-space indentation", "always use semicolons" -->

- **Never delete files to fix bugs or warnings.** Always fix the actual problem in the code. Deleting a file is not a fix — it destroys work. If a file has errors, correct the errors in place.
- **Write Markdown files correctly.** Use proper heading hierarchy (`#` → `##` → `###`), blank lines before and after headings and code blocks, proper list indentation, and valid link syntax. In tables, always use spaces around separator dashes (e.g., `| --- |` not `|---|`). Never produce malformed `.md` files.
- **Fix errors and warnings proactively.** After every code change, check for compile/lint errors and warnings and fix them immediately — don't wait for the user to point them out. The goal is zero errors and zero warnings at all times.

---

## Naming Conventions

<!-- Examples: "camelCase for variables", "PascalCase for classes", "snake_case for database columns" -->

- Use **"merge request"** (not "pull request") in all documentation, commit messages, comments, and conversation.

---

## Preferred Libraries & Tools

<!-- Examples: "use zod for validation", "prefer axios over fetch", "use vitest not jest" -->

- **Always create an isolated environment first.** At the start of any project or session, create the appropriate isolated/virtual environment for the language being used (e.g., `python -m venv .venv`, `node_modules` via `npm install`, `cargo` workspace, `dotnet` project, Go modules, etc.) and activate it before installing dependencies or running code. Never install packages globally.
- **Research and install all dependencies upfront.** Before any coding begins, the Research Agent identifies all required libraries/packages. The Orchestrator installs them all at once in the project's isolated environment. No mid-implementation dependency hunting.
- **Always use the latest versions.** When adding any dependency, library, tool, or framework, the Research Agent MUST check the web for the current latest stable version. Never assume a version — always verify. Pin to the specific latest version found.

---

## Architecture Preferences

<!-- Examples: "prefer functional over OOP", "always use dependency injection", "keep files under 200 lines" -->

- **Three-tier documentation system.** `docs/discoveries/` has structured summaries of analyzed data/codebases. `docs/BUSINESS_LOGIC.md` describes the overall system's business logic, data flows, and module responsibilities. `docs/files/` has one MD file per source file describing its purpose, public API, and dependencies. The orchestrator and planning agents read these — never raw source code.
- **Pure orchestrator model.** The main agent is a **pure dispatcher** — it NEVER writes code, reads source files, or runs tests. All actions are performed by sub-agents (model: see `AGENT_MODEL` above): Discovery, Planning, Architect, Critic, Scaffolder, Test Writer, Worker, Reviewer, Doc Updater, Research. Default to delegating everything.
- **Discovery-first for new data.** When new data/codebases/files are presented, the orchestrator asks the user first, then spawns a Discovery Agent to create a layered summary in `docs/discoveries/`. Other agents only read the summary — never raw new data.
- **Persisted todo tracking.** All task tracking MUST be persisted to `.ai/todos/{YYYY-MM-DD}_{topic}.todo.md` — never rely solely on in-memory todo lists. The Planning Agent creates the todo file, sub-agents update it as tasks complete, and the Doc Updater marks it ✅ Complete.
- **API documentation.** Whenever any agent encounters API usage in the codebase (exposed endpoints, consumed external services, SDK calls), document it in `docs/API_DOCUMENTATION.md`. One entry per API. Update on every change. Include environment variables.
- **Periodically clean context.** During long sessions, write summaries to `.ai/sessions/`, drop stale context, and re-read only what's needed for the current phase.
- **Always think about decomposition.** Every file should have one clear responsibility. Don't bundle unrelated logic together. If a file grows past ~200 lines or a function past ~40 lines, decompose. Group helpers by domain (`date_utils`, `http_utils`), not into generic dumping grounds. Layers don't skip layers (Config → Models → Services → Entry points).

---

## Communication Style

<!-- Examples: "be concise", "explain your reasoning", "ask before making big changes" -->

*No preferences learned yet.*

---

## Review Preferences

<!-- Examples: "always run tests before committing", "prefer small MRs", "squash commits" -->

- **Bulletproof testing — 10 tests per function, 50 per functionality.** Every public function must have a minimum of 10 tests across every applicable category of the 12-category taxonomy (happy path, output structure & type, boundary values, empty/null/missing, type abuse, range/domain violations, Unicode/encoding/special chars, error contract, idempotency/purity, state and side effects, concurrency/time/randomness, adversarial/abuse). Skipping a category requires a 1-line `# CATEGORY N N/A: <reason>` comment in the test file. Every functionality (feature/module) must accumulate ≥ 50 tests across all layers (unit + integration + E2E + contract). **Edge cases come first** — write boundary, null, type-abuse, range, unicode, and adversarial tests before the happy path. **Bulletproof Standard:** before reporting back, the Test Writer asks "can I imagine a wrong implementation that passes all my tests?" — if yes, more tests are added until the answer is no. Tests are written by Test Writer (black-box, hard-enforced) and Integration Tester sub-agents (model: see `AGENT_MODEL` in Agent Settings), never by the orchestrator.
- **Run tests without asking.** Test Writer and Worker agents should run tests automatically as part of their workflow — never pause to ask the user for permission to execute tests.

---

## Misc

<!-- Anything else the agent learns about how you work -->

- **Reuse existing terminals.** Never launch hidden or background terminals. Always reuse an already-open, visible terminal. Only create a new one if none exist. The user wants to see every command that runs.
