---
description: "Onboard an existing project: discover, document, audit, and suggest improvements"
tools: ['search', 'read', 'edit', 'agent']
---

# Onboard Existing Project

Run this after integrating the template into an existing project. It systematically discovers, documents, audits, and produces an improvement plan — without changing any code.

## Pipeline

You are the Orchestrator. Execute these phases in order. Each phase spawns one or more agents. **No code is changed** — this is a read-only audit that produces documentation and reports.

### Phase 1 — Discovery (map the codebase)

Spawn the **Discovery Agent** to read the entire existing codebase and produce a structured summary.

**Input:** The full `src/` and `tests/` directories, plus config files (package.json, pyproject.toml, etc.)
**Output:** `docs/discoveries/{date}_existing-codebase.md`

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

| Agent | Reads | Writes to | Finds |
|---|---|---|---|
| **Security** | All source files | `docs/SECURITY_REPORT.md` | Vulnerabilities, hardcoded secrets, injection risks, auth gaps |
| **Code Quality** | All source files | `docs/QUALITY_REPORT.md` | Duplication, dead code, complexity, code smells |
| **Dependency** | Lock files, manifests | `docs/DEPENDENCY_REPORT.md` | Outdated packages, vulnerabilities, license issues |
| **Error Handling** | All source files | `docs/ERROR_HANDLING_REPORT.md` | Silent catches, swallowed exceptions, missing context |
| **Type Safety** | All source files | `docs/TYPE_SAFETY_REPORT.md` | Missing types, unsafe casts, `any` abuse, schema drift |
| **Monitoring** | All source files | `docs/MONITORING_REPORT.md` | Missing logging, no health checks, alerting gaps |

### Phase 4 — Structure & Cleanup Analysis

After audits, before writing tests, analyze the project's structure and identify dead assets.

**3.5a — Project Structure Review (Architect Agent)**

Spawn the **Architect Agent** in **structure review mode** — it analyzes the current directory layout (from the Discovery summary) and proposes an ideal structure.

**Input:** Discovery summary from Phase 1, `docs/CODE_INVENTORY.md`
**Output:** `docs/STRUCTURE_REVIEW.md`

The review must include:
- Current structure map (as-is)
- Proposed structure map (to-be) following template conventions (`src/utils/`, `src/services/`, `src/models/`, `src/config/`)
- Specific moves: which files/modules should migrate and where
- New directories to create (with rationale)
- Directories to consolidate or rename
- Dependency impact: which imports would need updating
- A migration difficulty rating per move (trivial / moderate / complex)

**3.5b — Dead Code & Dead Document Detection (Cleanup Agent)**

Spawn the **Cleanup Agent** in **audit-only mode** — it identifies dead assets without removing anything. This is a read-only pass that produces a report.

**Input:** All source files, `docs/`, `docs/files/`, `docs/discoveries/`, config files
**Output:** `docs/CLEANUP_REPORT.md`

The report must include:

**Dead Code:**
- Functions, classes, and constants that are never called or imported
- Commented-out code blocks
- Unused imports at the top of files
- Unreachable code paths (after early returns, unconditional throws)
- Unused variables and parameters
- Test files for source files that no longer exist

**Dead Documents:**
- `docs/files/*.md` entries referencing files that no longer exist in `src/`
- `docs/discoveries/*.md` entries that are outdated or superseded
- `docs/API_DOCUMENTATION.md` entries for removed/deprecated endpoints
- `docs/CODE_INVENTORY.md` entries for symbols that no longer exist
- README sections referencing removed features or old setup instructions
- Stale configuration files (unused env vars, deprecated config keys)

**Dead Dependencies:**
- Packages in lock files / manifests that are never imported in source
- Dev dependencies that are never used in test or build scripts

Each item must include: file path, line number (for code), what it is, confidence level (certain / likely / possible), and estimated removal effort (trivial / moderate).

### Phase 5 — Test Harness (safety net before any changes)

Before anything gets cleaned up or fixed, **write thorough tests for every existing function**. These tests capture the current behavior so that cleanup, refactoring, and fixes can be verified.

**5a — Unit Tests (Test Writer Agent)**

Spawn **one Test Writer Agent per source file** (or per key module for large projects). Each writes tests for every public function in that file.

**Coverage targets:**
- Every public function gets ≥10 tests across every applicable category of the 12-category taxonomy, edge cases first; every functionality reaches ≥50 tests total across all layers
- Happy path with multiple realistic inputs
- Edge cases: empty input, boundary values, single-element, large input, unicode
- Error handling: invalid types, out-of-range, missing args
- Return type and structure verification
- Side effects (if any): state mutations, file writes, external calls

**Output:** Test files in `tests/` mirroring the `src/` structure. Example:
- `src/services/auth.py` → `tests/services/test_auth.py`
- `src/utils/parser.js` → `tests/utils/parser.test.js`
- `src/models/user.ts` → `tests/models/user.test.ts`

**5b — Integration Tests (Integration Tester Agent)**

Spawn the **Integration Tester Agent** to write tests for cross-module flows.

**Coverage targets:**
- Happy path flows through multiple modules (e.g., request → service → database → response)
- API contract tests: request/response schemas, status codes, error formats
- Data flow tests: data transforms correctly across module boundaries
- Error propagation: errors bubble up correctly through the call chain
- Boundary conditions at integration points (empty data, timeouts, missing dependencies)

**Output:** Integration test files in `tests/integration/` or `tests/e2e/`

**5c — Run All Tests (verify baseline)**

Run the full test suite. Record the results:
- How many pass (existing behavior captured correctly)
- How many fail (reveals existing bugs — document these)
- Any that can't run (missing fixtures, external dependencies)

Save baseline results to `.ai/plans/{date}_test-baseline.md`:

```markdown
# Test Baseline — {date}

## Summary
- Unit tests written: {N}
- Integration tests written: {N}
- Passing: {N}
- Failing: {N} (existing bugs — documented below)
- Skipped: {N} (missing dependencies)

## Failing Tests (existing bugs)
- [ ] test_auth_token_expiry — token never expires (src/services/auth.py:42)
- [ ] test_parse_empty_csv — crashes on empty input (src/utils/parser.py:15)

## Skipped Tests
- test_db_connection — requires running PostgreSQL
```

### Phase 6 — Improvement Plan (prioritized recommendations)

After all audits and tests complete, synthesize findings into a prioritized action plan.

**Read all reports from Phase 3 + test baseline from Phase 5, then create `.ai/plans/{date}_onboarding-improvements.md`:**

```markdown
# Onboarding Improvement Plan

## Critical (fix immediately)
- [ ] {Security findings rated CRITICAL/HIGH}
- [ ] {Dependency vulnerabilities with CVEs}
- [ ] {Existing bugs revealed by tests}

## High Priority (this sprint)
- [ ] {Code quality issues rated HIGH}
- [ ] {Error handling gaps in critical paths}
- [ ] {Type safety issues causing runtime errors}

## Medium Priority (next sprint)
- [ ] {Code quality improvements}
- [ ] {Monitoring/logging gaps}
- [ ] {Dependency version bumps}
- [ ] {Structure reorganization moves from STRUCTURE_REVIEW.md}

## Low Priority (backlog)
- [ ] {Nice-to-have cleanups}
- [ ] {Style/convention alignment}
- [ ] {Test coverage gaps}

## Dead Assets to Remove
- [ ] {Dead code from CLEANUP_REPORT.md — certain confidence}
- [ ] {Dead documents from CLEANUP_REPORT.md}
- [ ] {Dead dependencies from CLEANUP_REPORT.md}
- [ ] {Dead code — likely confidence (review before removing)}
```

### Phase 7 — Present to User

Show the user:
1. **Discovery summary** — what was found in the codebase
2. **Structure review** — current vs. proposed structure, key moves
3. **Dead assets** — dead code count, dead docs count, dead dependency count (with confidence breakdown)
4. **Test baseline** — how many tests written, how many pass/fail
5. **Audit overview** — counts per severity across all audits
6. **Top 5 action items** — the most impactful things to fix first
7. **Full improvement plan** — link to the plan file

Ask: "Tests are in place as a safety net. Want me to start fixing the Critical items? I can also reorganize the project structure and clean up dead assets. Tests will verify nothing breaks."

---

## After Onboarding: The Fix → Verify Loop

Once the user approves fixes, the pipeline follows this pattern for each fix:

```
  Worker Agent fixes the issue
         │
         ▼
  Run full test suite
         │
         ├── All pass? ──────── ✅ Next fix
         │
         └── Regression? ────── 🔴 Fix the regression first
                                    │
                                    ▼
                               Re-run tests
                                    │
                                    ▼
                               ✅ Then continue
```

This ensures every cleanup, refactor, or fix is verified against the test harness written in Phase 5.

---

## How to Run

After integrating the template, tell the Orchestrator:

> "Onboard this project — discover, document, audit, and suggest improvements."

Or use this prompt file directly.
