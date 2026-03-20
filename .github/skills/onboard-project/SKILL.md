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

### Phase 4 — Test Harness (safety net before any changes)

Before anything gets cleaned up or fixed, write thorough tests for every existing function.

**4a — Unit Tests (Test Writer Agent):** Spawn one Test Writer Agent per source file. Each writes 15+ tests per public function.

**4b — Integration Tests (Integration Tester Agent):** Spawn for cross-module flows.

**4c — Run All Tests:** Record baseline results to `.ai/plans/{date}_test-baseline.md`.

### Phase 5 — Improvement Plan

Spawn the **Planning Agent** to produce:
- Prioritized list of improvements from all audit reports
- Estimated effort per item (small/medium/large)
- Suggested implementation order (quick wins first, then structural)
- Todo file at `.ai/todos/{date}_onboarding-improvements.todo.md`

### Phase 6 — Present Results

Present to the user:
- Summary of discovery findings
- Key audit findings (critical/high items)
- Test baseline status
- Prioritized improvement plan
- Recommendation to start with quick wins
