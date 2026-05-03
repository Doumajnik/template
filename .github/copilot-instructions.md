# Repository System Instructions (Copilot)

> **This file is a thin pointer.** The single source of truth for the orchestrator identity, the sub-agent roster, every pipeline (Planning, Change, Discovery, Onboarding, Budget, Super Greedy, Incident Response, Maintenance), the Context Gateway protocol, the Consistency Check gates, and all Core Rules lives in [AGENTS.md](../AGENTS.md) at the repository root.
>
> Copilot reads this file automatically because of its location in `.github/`. Other tools (Cursor, Windsurf, Claude Code, Codex) read `AGENTS.md` directly. Keeping the content in **one place** prevents drift between the two files.

---

## Read this first

**Read [AGENTS.md](../AGENTS.md) in full at session start.** It contains:

- The Orchestrator identity and pure-dispatcher rule
- The full Sub-Agent Roster (53 agents) with paths to each `.agent.md`
- The canonical workflow diagram (Full Planning Sequence) with all three Consistency Check gates
- Session Startup checklist
- Discovery, Planning, Change, Onboarding, Budget, Super Greedy, Incident Response, and Maintenance pipelines
- Context Gateway Protocol (Librarian-first rule)
- Documentation Hierarchy
- Role Separation rules
- Error Recovery, Circuit Breaker, Self-Improvement, Autonomous Bug Fixing
- Quick Commands
- Conflict Resolution
- Pipeline Abort
- All Core Rules (passed to every sub-agent)
- Project Structure
- Context Management

---

## Copilot-specific notes

These are the only items that are NOT covered by `AGENTS.md` and are specific to GitHub Copilot:

- **Custom agents** live in `.github/agents/{name}.agent.md`. Copilot loads them automatically.
- **Prompt files** live in `.github/prompts/{name}.prompt.md`. Invoke via Copilot Chat slash commands.
- **Instruction files** live in `.github/instructions/{lang}.instructions.md`. Copilot scopes them by `applyTo` glob.
- **Skills** live in `.github/skills/{skill}/SKILL.md`. Loaded on-demand when a skill matches the user request.
- **Tool restrictions** are enforced at runtime by `scripts/tool-guard.py` (PreToolUse hook). The denied-tool list per agent lives in `.ai/TOOL_MANIFEST.md`.

Everything else — agent behavior, pipeline ordering, dispatch rules, Core Rules — comes from [AGENTS.md](../AGENTS.md). Do not duplicate content here.

---

## Maintenance rule

If you find yourself wanting to add a rule, agent, pipeline step, or workflow note here: **add it to `AGENTS.md` instead.** This file stays small on purpose.
