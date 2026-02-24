# Template Sync — Changes to Merge Back

<!-- markdownlint-disable MD024 -->

> This file collects all changes made to agent instruction and preference files during this project.
> When you want to update your template, copy the relevant sections below back to the template repo.
>
> **Format:** Each entry shows the file, the date, and the exact content to add or replace.
> Entries are appended chronologically — newest at the bottom.

---

<!-- Agents: append new entries here using this format:

## {YYYY-MM-DD} — {short description}

### File: `{relative path}`

**Action:** add | replace | remove

```
{exact content to add/replace}
```

---

-->

## 2026-02-19 — Orchestrator + Discovery Agent architecture overhaul

### File: `.github/copilot-instructions.md`

**Action:** replace (full rewrite)

Major changes:

- Main agent is now a **pure Orchestrator** — never writes code, never reads source files
- All sub-agents use **Opus 4.6** (replaced gpt-5-mini)
- Added **Discovery Agent** — triggered on new data, creates 3-layer summaries in `docs/discoveries/`
- Orchestrator must ASK user before running Discovery Agent
- Added mandatory pipeline: Discovery → Planning → Architect → Critic → Scaffolder → Test Writer → Worker → Reviewer → Doc Updater
- Updated documentation hierarchy to 3-tier (added `docs/discoveries/`)
- Added trace entries for Discovery, Doc Updater, and Research agents

### File: `AGENTS.md`

**Action:** replace (full rewrite)

Same changes as above, mirrored for cross-tool compatibility.

### File: `.ai/PREFERENCES.md`

**Action:** replace (Architecture Preferences section)

- Three-tier documentation system (added `docs/discoveries/`)
- Pure orchestrator model (explicit: never writes code)
- Discovery-first workflow for new data
- Updated test reference from "Worker sub-agents" to "Test Writer and Worker sub-agents (Opus 4.6)"

### File: `.ai/TRACE_TEMPLATE.md`

**Action:** replace (participants and examples)

- Added participants: Orchestrator, Discovery, Planning, Doc Updater, Research
- Removed: Planner (renamed to Planning), Implementer (merged into Orchestrator)
- Updated all trace examples to use `O` (Orchestrator) as the hub

### File: `docs/discoveries/_TEMPLATE.discovery.md`

**Action:** add (new file)

Template for Discovery Agent summaries with 3 layers: Overview, Structure Map, Detailed Notes.

---

## 2026-02-19 — Todo persistence + API documentation + subagent reinforcement

### File: `.github/copilot-instructions.md`

**Action:** add (3 sections)

- Added **Todo Persistence (MANDATORY)** section under Planning Agent instructions — all task tracking must be persisted to `.ai/todos/` markdown files, not just in-memory
- Added **API Documentation (MANDATORY when APIs are found)** section — agents must document all exposed/consumed APIs in `docs/API_DOCUMENTATION.md`
- Updated Doc Updater Agent checklist to include `docs/API_DOCUMENTATION.md` and `.ai/todos/` completion
- Updated Doc Updater Agent roster description to include `docs/API_DOCUMENTATION.md`

### File: `AGENTS.md`

**Action:** add (same 3 sections, mirrored)

Same todo persistence, API documentation, and Doc Updater updates as copilot-instructions.md.

### File: `.ai/PREFERENCES.md`

**Action:** add (2 preferences under Architecture Preferences)

- Persisted todo tracking preference
- API documentation preference

### File: `docs/API_DOCUMENTATION.md`

**Action:** add (new file)

Template for documenting exposed and consumed APIs. Includes entry formats for both types, models, error handling, rate limits, and environment variables.

### File: `.ai/todos/_TEMPLATE.todo.md`

**Action:** add (new file)

Template for persisted todo files. Includes task checklist, progress log, blockers, and notes sections.

### File: `.ai/plans/_TEMPLATE.plan.md`

**Action:** replace (Post-Implementation Checklist)

Added `docs/API_DOCUMENTATION.md` and `.ai/todos/` completion to the checklist.

### File: `README.md`

**Action:** replace (project structure)

Added `API_DOCUMENTATION.md` to docs listing. Updated .ai description to include "todos".

### File: `.gitignore`

**Action:** add (1 line)

Added `!.ai/todos/` to tracked-folders section.

---

## 2026-02-19 — Prompt optimization: shorten system prompts, move content to agent files

### File: `.github/copilot-instructions.md`

**Action:** replace (full rewrite — 375 → ~107 lines)

- Removed all GUI/UI/color/visual design sections entirely
- Moved Discovery Agent behavior → `.github/agents/discovery.agent.md`
- Moved Planning Agent instructions + Todo Persistence → `.github/agents/planner.agent.md`
- Moved DEEP_MODE pipeline → `.ai/DEEP_MODE.md`
- Moved anti-duplication/extraction/decomposition rules → `docs/PLAYBOOK.md`
- Moved execution tracing details → reference to `.ai/TRACE_TEMPLATE.md`
- Moved API documentation rules → reference to `docs/API_DOCUMENTATION.md`
- Moved testing rules (15 categories) → reference to `.github/agents/test-writer.agent.md`
- Moved Doc Updater checklist → `.github/agents/doc-updater.agent.md`
- Core remains: Orchestrator Identity, Sub-Agent Roster (with file links), Session Startup, Discovery trigger, Planning Sequence, Doc Hierarchy, Role Separation, Core Rules (compact)

### File: `AGENTS.md`

**Action:** replace (full rewrite — 483 → ~131 lines)

Same restructuring as copilot-instructions.md, mirrored for cross-tool compatibility.

### File: `.github/agents/discovery.agent.md`

**Action:** add (new file)

Full Discovery Agent behavior moved here from main instruction files.

### File: `.github/agents/doc-updater.agent.md`

**Action:** add (new file)

Doc Updater Agent with full 14-item documentation checklist.

### File: `.github/agents/research.agent.md`

**Action:** add (new file)

Research Agent with systematic search workflow.

### File: `.github/agents/implementer.agent.md`

**Action:** remove (deleted)

Implementer role is now handled by the orchestrator dispatching sub-agents directly.

### File: `.github/agents/planner.agent.md`

**Action:** replace (renamed to Planning, model → opus-4.6, added todo file creation, removed Implementer handoff)

### File: `.github/agents/worker.agent.md`

**Action:** replace (model → opus-4.6, trace targets O instead of I, added API documentation flagging)

### File: `.github/agents/test-writer.agent.md`

**Action:** replace (model → opus-4.6, trace targets O instead of I)

### File: `.github/agents/scaffolder.agent.md`

**Action:** replace (trace targets O instead of I)

### File: `.github/agents/reviewer.agent.md`

**Action:** replace (trace targets O instead of I/U)

### File: `.github/agents/architect.agent.md`

**Action:** replace (removed "NOT for GUI/UI" line)

### File: `.ai/DEEP_MODE.md`

**Action:** add (new file)

Full DEEP_MODE adversarial pipeline reference, moved from main instruction files.

### File: `docs/PLAYBOOK.md`

**Action:** add (Anti-Duplication Rules section)

Moved anti-duplication, extraction, one-copy rule, and decomposition rules from main instruction files into PLAYBOOK.md.

### File: `.ai/PREFERENCES.md`

**Action:** replace (removed GUI & Visual Design Preferences section, removed "not GUI/UI" from DEEP_MODE description)

---
