---
name: onboard-project
description: "Full project onboarding pipeline: discover, document, audit, test, and plan improvements for an existing codebase. Use when onboarding a new project, integrating the template into an existing repo, or running a comprehensive audit. Triggers on: onboard, onboard project, onboard codebase, project audit."
---

# Onboard Existing Project

Run this after integrating the template into an existing project. It systematically discovers, documents, audits, and produces an improvement plan — without changing any code.

## When to Use

- Onboarding a new or existing project into this template system
- Running a comprehensive audit of a codebase
- First-time setup after running the integrate script
- When the user says "onboard" or "onboard this project"

## Pipeline

You are the Orchestrator. Execute these phases in order. Each phase spawns one or more agents. **No code is changed** — this is a read-only audit that produces documentation and reports.

### Phase 1 — Discovery (map the codebase)

Spawn the **Discovery Agent** to read the entire existing codebase and produce a structured summary.

**Input:** The full `src/` and `tests/` directories, plus config files (package.json, pyproject.toml, etc.)
**Output:** `docs/discoveries/{date}_existing-codebase.md`

Use the [discovery template](./references/discovery-template.md) for the output format.

The discovery summary must include:
- Project language(s), frameworks, and architecture pattern
- Directory structure and module map
- Key entry points (main, server, CLI, routes)
- Data models and their relationships
- External dependencies and integrations (APIs, databases, queues)
- Test coverage overview (what's tested, what's not)

### Phase 2 — Documentation (populate the docs)

Spawn the **Doc Updater Agent** to fill in the template's documentation from the discovery summary.

**Writes to:**
- `docs/BUSINESS_LOGIC.md` — system-level business logic, data flows, module responsibilities
- `docs/CODE_INVENTORY.md` — every exported symbol, function, class, with file paths
- `docs/API_DOCUMENTATION.md` — any exposed endpoints or consumed external APIs
- `docs/files/{path}.md` — per-file documentation for key source files

### Phase 3 — Audits (find issues)

Spawn these agents **in parallel** (they are all read-only and write to separate report files):

| Agent | Writes to | Finds |
| --- | --- | --- |
| **Security** | `docs/SECURITY_REPORT.md` | Vulnerabilities, hardcoded secrets, injection risks, auth gaps |
| **Code Quality** | `docs/QUALITY_REPORT.md` | Duplication, dead code, complexity, code smells |
| **Dependency** | `docs/DEPENDENCY_REPORT.md` | Outdated packages, vulnerabilities, license issues |
| **Error Handling** | `docs/ERROR_HANDLING_REPORT.md` | Silent catches, swallowed exceptions, missing context |
| **Type Safety** | `docs/TYPE_SAFETY_REPORT.md` | Missing types, unsafe casts, `any` abuse, schema drift |
| **Monitoring** | `docs/MONITORING_REPORT.md` | Missing logging, no health checks, alerting gaps |

See [report targets](./references/report-targets.md) for the full list of output files.

### Phase 3.5 — Structure & Cleanup Analysis

After audits, before writing tests, analyze the project's structure and identify dead assets.

**3.5a — Project Structure Review (Architect Agent):**
Spawn the **Architect Agent** in structure review mode. It analyzes the current directory layout from the Discovery summary and proposes an ideal structure following template conventions (`src/utils/`, `src/services/`, `src/models/`, `src/config/`). Outputs specific file/module moves with difficulty ratings. Writes to `docs/STRUCTURE_REVIEW.md`.

**3.5b — Dead Code & Dead Document Detection (Cleanup Agent):**
Spawn the **Cleanup Agent** in audit-only mode (read-only — no removals). It identifies:
- **Dead code:** unused functions/classes, commented-out blocks, unused imports, unreachable code, orphaned test files
- **Dead documents:** stale `docs/files/` entries, outdated discoveries, removed API endpoints in docs, orphaned `CODE_INVENTORY.md` entries
- **Dead dependencies:** packages in manifests never imported in source

Each item includes: file path, line number, description, confidence (certain/likely/possible), and removal effort (trivial/moderate). Writes to `docs/CLEANUP_REPORT.md`.

### Phase 4 — Test Harness (safety net before any changes)

Before anything gets cleaned up or fixed, write thorough tests for every existing function.

**4a — Unit Tests (Test Writer Agent):** Spawn one Test Writer Agent per source file. Each writes 15+ tests per public function.

**4b — Integration Tests (Integration Tester Agent):** Spawn for cross-module flows.

**4c — Run All Tests:** Record baseline results to `.ai/plans/{date}_test-baseline.md`.

### Phase 5 — Improvement Plan

Spawn the **Planning Agent** to produce:
- Prioritized list of improvements from all audit reports
- Structure reorganization moves from `docs/STRUCTURE_REVIEW.md` (prioritized by impact)
- Dead asset removal list from `docs/CLEANUP_REPORT.md` (certain-confidence items first)
- Estimated effort per item (small/medium/large)
- Suggested implementation order (quick wins first, then structural)
- Todo file at `.ai/todos/{date}_onboarding-improvements.todo.md`

### Phase 6 — Present Results

Present to the user:
- Summary of discovery findings
- **Proposed project structure** — current vs. ideal, with key reorganization moves
- **Dead assets summary** — dead code count, dead docs count, dead dependency count (with confidence breakdown)
- Key audit findings (critical/high items)
- Test baseline status
- Prioritized improvement plan (including structure moves and cleanup items)
- Recommendation to start with quick wins

Ask: "Tests are in place as a safety net. Want me to start fixing the Critical items? I can also reorganize the project structure and clean up dead assets. Tests will verify nothing breaks."

## Key Rules

- **Context Gateway (mandatory):** Every agent spawn MUST be preceded by a Librarian query. No agent receives raw files — only Librarian-curated context briefs. See copilot-instructions.md Context Gateway Protocol.
  - **Exception:** The Discovery Agent reads raw source directly (per Context Gateway Protocol), but still receives a Librarian brief for existing project context.
- **Read-only audit:** This pipeline does NOT change code. It produces documentation and reports only.
- **Parallel audits:** Phase 3 agents can run in parallel — they write to separate report files.

> **Relationship:** This skill implements the onboarding pipeline referenced by the `"onboard"` quick command in `copilot-instructions.md` / `AGENTS.md`.
