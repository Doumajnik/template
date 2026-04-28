# Agentic Project Template

A repository template that gives AI coding agents a **50-agent roster**, **four named pipelines**, **black-box testing**, **persistent memory**, and **adversarial review** out of the box. Designed for use with GitHub Copilot, Cursor, Windsurf, Claude Code, Codex, and any other tool that reads `AGENTS.md` or `.github/copilot-instructions.md`.

> **License:** Proprietary. Personal use is free; **business use requires written permission from the author.** See [LICENSE](LICENSE).

---

## What this is

This is **not** an application. It is a structured set of markdown files — agent definitions, prompts, playbooks, skills, instructions, and protocols — that together turn a generic AI coding assistant into a disciplined, auditable, multi-agent software engineering team:

- **One Orchestrator** — pure dispatcher, never writes code itself.
- **50 specialised sub-agents** — Architect, Critic, Test Writer, Worker, Security, Threat Modeling, Cost/FinOps, Capacity Planner, Incident Commander, etc. Each is invoked for a single responsibility.
- **Four named pipelines** — Planning Sequence (greenfield, 25 steps), Change Pipeline (modifications, 22 steps), Onboarding Pipeline (existing project audit, 7 phases), Incident Response Pipeline (live production, 7 phases).
- **Three Consistency Check gates** at every phase boundary, with hard-enforced re-verification after fixes.
- **Black-box testing** — Test Writer and Integration Tester are physically blocked from reading source code by a PreToolUse hook. They write tests against documented contracts only.

The full source of truth is [AGENTS.md](AGENTS.md). The Copilot-specific entry point is [.github/copilot-instructions.md](.github/copilot-instructions.md) (a thin pointer to AGENTS.md).

---

## Quick start

1. **Use this template** — click "Use this template" on GitHub, or clone and remove `.git/`.
2. **Run the setup script** — `scripts\setup.ps1` (Windows) or `scripts/setup.sh` (Unix). Installs git hooks, creates standard directories, sets up the playbook validation pre-commit hook.
3. **Open in your AI tool** — `AGENTS.md` and `.github/copilot-instructions.md` are loaded automatically by Copilot, Cursor, Windsurf, Claude Code, and Codex.
4. **Run a Quick Command** — say one of:
   - `onboard` — full onboarding pipeline against an existing codebase
   - `plan only` *describe-the-task* — Phase A planning, no code
   - `implement plan` *path-to-plan* — Phase B implementation from a saved plan
   - `plan and implement` *describe-the-task* — full Planning Sequence in one session
   - `change` *describe-the-change* — Change Pipeline with impact analysis
   - `incident` / `down` / `outage` — Incident Response Pipeline
5. **Read the dispatch log** afterwards in `.ai/sessions/{date}_{topic}.dispatch.md` — every sub-agent call is logged for audit.

---

## What you get

| Capability | Where it lives |
| --- | --- |
| 50 specialised agents | `.github/agents/{name}.agent.md` (one per agent) |
| 50 paired playbooks | `docs/playbooks/agents/{name}.playbook.md` |
| Shared playbooks (telemetry, cost-aware design, etc.) | `docs/playbooks/shared/` |
| Slash commands | `.github/prompts/*.prompt.md` |
| Skills (loaded on-demand by trigger) | `.github/skills/{skill}/SKILL.md` |
| Language-scoped instructions | `.github/instructions/{lang}.instructions.md` |
| Tool-restriction enforcement | `.ai/TOOL_MANIFEST.md` + `scripts/tool-guard.py` |
| Persistent reports (security, quality, retrospective, consistency, etc.) | `docs/*_REPORT.md` |
| Per-file documentation | `docs/files/{path}.md` |
| Code symbol registry | `docs/CODE_INVENTORY.md` |
| Architecture decisions / patterns | `docs/PLAYBOOK.md` |
| Living todo trackers | `.ai/todos/{date}_{topic}.todo.md` |
| Plan files | `.ai/plans/{date}_{topic}.plan.md` |
| Session memory | `.ai/sessions/{date}_{topic}.dispatch.md` |

---

## Pipelines at a glance

| Pipeline | Trigger | Scope | Steps |
| --- | --- | --- | --- |
| **Planning Sequence** | Greenfield non-trivial work | Spec → research → architecture → adversarial review → plan → approval → scaffold → test → implement → review → docs → retrospective | Phase A: 1–14, Phase B: 15–25 |
| **Change Pipeline** | Modifying existing code | Spec → impact analysis → research → architecture → adversarial review → plan → deprecation timeline → approval → tests → implement → review → docs → retrospective | 22 steps |
| **Onboarding Pipeline** | Existing project audit | Discovery → documentation → audits (security/quality/deps/types/error-handling/monitoring) → structure & cleanup → test harness → improvement plan | 7 phases |
| **Incident Response Pipeline** | Live production incident | Declare → stabilise → investigate (Debug + Performance + Security + Database) → root cause → permanent fix (Change Pipeline) → resolution → blameless postmortem | 7 phases |

Each pipeline has **three Consistency Check gates** that block progress until drift between plan, code, docs, and test harness is resolved. See [AGENTS.md](AGENTS.md) for the full step-by-step flow and the canonical workflow diagram.

---

## Key design decisions

- **Orchestrator is a pure dispatcher.** It reads only `docs/`, `.ai/`, and `README.md`. Every concrete action is delegated to a sub-agent.
- **Librarian is the single context gateway.** No agent receives raw files — only Librarian-curated briefs. Enforced for every spawn (with a fast-mode shortcut during SEV1 incidents).
- **Black-box testing is hard-enforced.** Test Writer and Integration Tester cannot `read_file` / `grep_search` / `semantic_search` against `src/` paths — the PreToolUse hook (`scripts/tool-guard.py`) physically blocks the call. Tests are written from contracts in `docs/API_DOCUMENTATION.md`, `docs/BUSINESS_LOGIC.md`, and the Librarian's brief.
- **Test minimums are bulletproof.** ≥ 10 unit tests per function across the 12-category taxonomy (happy path, structure, boundaries, empty/null, type abuse, range, unicode, error contract, idempotency, state, time/concurrency, adversarial — edge cases first). 15+ integration tests per feature. 5+ E2E tests per user-facing feature. 1+ contract test per consumer↔provider pair. **≥ 50 tests per functionality** summed across all layers — a feature is not done until the total reaches 50.
- **Numeric stability of pipeline step numbers.** Steps are stable identifiers referenced from prompt files and lessons. Inserts use letter suffixes (e.g. `13a`, `13b`); renumbering is reserved for major restructures.
- **No agent-to-agent handoffs.** Every agent reports back to the Orchestrator. The Orchestrator decides what runs next.
- **Parallel sub-agent dispatch (fan-out).** Whenever work splits cleanly along an independent axis (drift category, transcript chunk, source module, function, audit dimension), the Orchestrator fans out multiple instances of the same agent in parallel and runs one merge instance. Test Writer, Worker, Retrospective, Onboarding audits, and every Consistency Check gate already work this way.

---

## Project structure

```text
AGENTS.md                          # Single source of truth — read first
LICENSE                            # Proprietary; business use requires permission
README.md                          # This file
TEMPLATE_README.md                 # Template documentation (full agent list, customisation)

.github/
├── copilot-instructions.md        # Thin pointer to AGENTS.md
├── agents/         (50 .agent.md) # Per-agent system prompts
├── prompts/        (slash commands) # /plan-only, /implement-plan, /onboard-project, etc.
├── skills/         (skill bundles) # On-demand domain knowledge
├── instructions/   (lang scoped)  # Python, TypeScript, Go, Rust, .NET, Django, FastAPI, etc.
└── hooks/                          # tool-guard.json (PreToolUse hook config)

.ai/
├── PREFERENCES.md                  # User-learned coding style, AGENT_MODEL setting
├── DEEP_MODE.md                    # Adversarial pipeline reference
├── TOOL_MANIFEST.md                # Per-agent tool restrictions
├── DISPATCH_LOG_TEMPLATE.md        # Session dispatch log structure
├── SESSION_TRANSCRIPT_TEMPLATE.md  # Optional full transcript with workflow diagram
├── TRACE_TEMPLATE.md               # Execution trace template
├── lessons.md                      # Lessons from past corrections
├── sessions/                       # Per-session dispatch logs and transcripts
├── plans/                          # Implementation plans
├── todos/                          # Living todo trackers
├── specs/                          # Prompt Engineer enriched specs
└── lounge/                         # Shared notes between agents

docs/
├── PLAYBOOK.md                     # Architecture decisions & patterns
├── CODE_INVENTORY.md               # Symbol registry for deduplication
├── BUSINESS_LOGIC.md               # System logic, data flows, modules
├── API_DOCUMENTATION.md            # Public/consumed API contracts
├── SECURITY_CHECKLIST.md           # Security Agent checks every item against every file
├── SECURITY_REPORT.md              # Persistent security audit trail
├── QUALITY_REPORT.md               # Persistent code quality trail
├── REVIEW_REPORT.md                # Persistent code review trail
├── RETROSPECTIVE_REPORT.md         # Decision audit & improvement log
├── CLEANUP_REPORT.md               # Onboarding cleanup analysis
├── STRUCTURE_REVIEW.md             # Onboarding structure analysis
├── _TEMPLATE.*.md                  # Templates for the above
├── discoveries/                    # Structured summaries of analysed data/codebases
├── files/                          # Per-file documentation (one MD per source file)
└── playbooks/
    ├── agents/   (50 playbooks)    # Per-agent rules included in every Librarian brief
    ├── shared/                     # Cross-agent rules (telemetry, cost-aware design, etc.)
    └── technologies/               # Language/framework conventions

scripts/
├── setup.ps1 / setup.sh            # Initial repo setup
├── install-hooks.ps1               # Install git hooks
├── integrate.ps1 / integrate.sh    # Integrate template into existing repo
├── tool-guard.py                   # PreToolUse hook — hard-enforces tool restrictions
├── validate-playbooks.py           # CI: validate TOML frontmatter on every .playbook.md
└── hooks/                          # Git hooks (commit-msg, post-commit, pre-commit, pre-push)

src/                                # Application source code (you fill this in)
tests/                              # Mirrors src/ — plus integration/, e2e/, contracts/
ideas/                              # Pre-planning idea staging
feedback/                           # Optional template-improvement feedback collection
```

---

## Documentation

- **[AGENTS.md](AGENTS.md)** — single source of truth: orchestrator identity, 50-agent roster, all four pipelines, Cross-Pipeline Step Matrix, Consistency Check gates, Core Rules.
- **[TEMPLATE_README.md](TEMPLATE_README.md)** — detailed template documentation: full agent list, slash commands, customisation guide.
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** — Copilot entry point (pointer to AGENTS.md).
- **[.ai/DEEP_MODE.md](.ai/DEEP_MODE.md)** — adversarial pipeline reference.
- **[.ai/TOOL_MANIFEST.md](.ai/TOOL_MANIFEST.md)** — per-agent tool restrictions and enforcement.

---

## License

This software is **proprietary**. Personal, evaluation, and academic use are free under the conditions in [LICENSE](LICENSE). **Business use requires written permission from the author** — contact **Dominik Haspra <dominik.haspra@gmail.com>** to obtain a Business Use license.
