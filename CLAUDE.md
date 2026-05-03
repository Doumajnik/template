# CLAUDE.md

> **This file is a thin pointer for Claude Code.** The single source of truth lives in [AGENTS.md](AGENTS.md).
>
> Claude Code reads this file automatically. Other tools read `AGENTS.md` directly or via their own pointer files.

---

## Read this first

**Read [AGENTS.md](AGENTS.md) in full at session start.** It contains all orchestrator rules, pipelines, agent roster, and core rules.

## Claude Code–specific configuration

### Memory

Claude Code uses `~/.claude/CLAUDE.md` for global instructions and this file for project-level. This file IS the project-level memory — all project context lives in `AGENTS.md`, `.ai/`, and `docs/`.

### Custom Commands

Claude Code slash commands live in `.claude/commands/`. These map to the Quick Commands in AGENTS.md:

- `/project:plan` → Planning Sequence (Phase A only)
- `/project:implement` → Planning Sequence (Phase B from saved plan)
- `/project:change` → Change Pipeline
- `/project:onboard` → Onboarding Pipeline
- `/project:incident` → Incident Response Pipeline
- `/project:budget` → Budget Pipeline
- `/project:greedy` → Super Greedy Pipeline
- `/project:maintain` → Maintenance Pipeline

### Hooks

Claude Code hooks are configured in `.claude/settings.json`. The template uses:
- **PreToolUse** → `scripts/tool-guard.py` (blocks Test Writer/Integration Tester from reading source)
- **PostToolUse** → optional audit logging

### Model Selection

In Super Greedy mode (`GREEDY_MODE: ON`), Claude Code Max provides the unlimited tokens needed for multi-model dispatch. Use the `--model` flag or `/model` command to switch between Opus (Tier 1), Sonnet (Tier 2), and Haiku (Tier 3) as the Council requires.

### Task Tool (Sub-Agent Dispatch)

Claude Code's native `Task` tool is the equivalent of Copilot's `runSubagent`. The Orchestrator uses it to spawn sub-agents with isolated context. Each task gets only the Librarian brief relevant to its scope.

---

## Core Rules (always active)

All rules from [AGENTS.md → Core Rules](AGENTS.md#core-rules-pass-to-all-sub-agents) apply. Key highlights:

- Never delete files to fix bugs
- Functions ≤40 lines
- Zero errors, zero warnings
- Spawn sub-agents for all concrete work
- Librarian-first context gateway
- Black-box testing enforced by tool-guard
