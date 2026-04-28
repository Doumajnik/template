# Playbook

> **This is a living document.** AI agents append to it after making architecture decisions or discovering patterns.
> Agents read this at the start of every session to maintain consistency across the project.

**Last updated:** 2026-03-15

---

## Architecture Decisions

### Playbook Chunk Format (TOML Frontmatter)

**Date:** 2026-03-11
**Context:** Needed a structured, machine-parseable format for playbook rules that agents can query.
**Decision:** Use `+++` TOML frontmatter delimiters in `.playbook.md` files. Required fields: `id`, `title`, `agents`, `technologies`, `category`, `tags`, `version`. Valid categories: `pattern`, `anti-pattern`, `rule`, `convention`, `decision`, `strategy`.
**Alternatives considered:** YAML frontmatter (rejected — ambiguous with markdown), JSON sidecar files (rejected — extra file management).

### Playbook Knowledge System

**Date:** 2026-03-11
**Context:** Needed structured delivery of playbook rules to agents via the Librarian.
**Decision:** Playbook rules stored as `.playbook.md` files with TOML frontmatter. Parsed into structured chunks by `playbook_parser.py`. Librarian filters by metadata (agent, technology, category) and assembles context briefs.
**Alternatives considered:** JSON sidecar files (rejected — extra file management), unstructured markdown (rejected — no machine-parseable metadata).

---

## Patterns We Use

<!-- Document recurring code patterns that should be followed consistently. -->
<!-- Example: "All API handlers follow the try/catch → mapError → respond pattern" -->

### Pre-Report File Verification

**Date:** 2026-03-15
**Context:** Review/Security/Quality reports referenced 6 files that did not exist on disk, creating phantom audit records. Agents generated detailed audits for code that existed only in the chat context window but was never persisted to disk. This creates false confidence that code has been reviewed and is secure — downstream agents trust these reports, and when files don't actually exist, the project has audit records for nothing.
**Pattern:** Before generating any audit report, the agent MUST verify every file it references actually exists on disk by reading the file or listing the directory. If a file does not exist, flag it as missing in the report — never audit code from a context window without on-disk confirmation. Always verify file existence before auditing.

### Adversarial Architecture Review

**Date:** 2026-03-15
**Context:** The Architect↔Critic loop caught 3 critical contradictions and 6 additional issues in the playbook pipeline architecture, improving the design substantially before any code was written.
**Pattern:** Every non-trivial architecture goes through at least one Architect→Innovator→Critic cycle. The Critic's rejection is a feature — it catches contradictions, missing edge cases, and over-engineering before implementation begins. Expect 1-2 rounds. Maximum 10.

---

## Patterns We Avoid

<!-- Document anti-patterns or approaches we've explicitly decided against. -->
<!-- Example: "Don't use default exports — always use named exports for better refactoring" -->

### Abandoned Dispatch Logs

**Date:** 2026-03-15
**Problem:** The dispatch log covered only the planning phase (9 entries). All implementation dispatches were unlogged, making it impossible to reconstruct the implementation timeline or audit agent decisions.
**Why it's bad:** The retrospective agent cannot audit decisions that were never recorded. Pipeline failures are invisible. Accountability is lost.
**Instead:** Every sub-agent spawn gets a dispatch log entry — no exceptions. When continuing across sessions, chain dispatch logs with cross-references.

### Stale Todo Trackers

**Date:** 2026-03-15
**Problem:** All ~90 todo tasks remained ⬜ unchecked despite partial implementation existing on disk. The todo became useless as a progress indicator.
**Why it's bad:** Other agents checking the todo see no progress and may redo work. The Orchestrator cannot determine project state. Session continuity breaks.
**Instead:** Agents mark tasks 🔵 before starting and ✅ on completion. The Orchestrator verifies todo updates after each agent reports back.

---

## Anti-Duplication Rules (MANDATORY for all agents)

> These rules are referenced from the main instruction files. All sub-agents that create or modify code must follow them.

### Before Creating Anything New

1. Search `docs/CODE_INVENTORY.md` for similar functionality.
2. Search across `src/` with grep/semantic search.
3. Reuse or extend existing code if possible. Only create new if fundamentally different.

### Extraction Rules

When the same logic appears in ≥2 places, **extract first, then use**:

- Same helper used by ≥2 files → `src/utils/`. Never copy-paste.
- Same HTTP logic (retry, session, auth) → one shared client in `src/utils/`.
- Same constant/magic value → define once in `src/config/`.
- Same pattern in one file → extract a private helper.
- Same structural loop across classes → base class with overrides.

### One-Copy Rule

Every piece of logic exists in **exactly one place**. If you write the same 3+ lines a second time, stop and extract. No exceptions.

### Decomposition Rules

Before writing or modifying code, always ask: **does this belong here?**

- **One responsibility per file.** If it handles two unrelated concerns, split it.
- **One responsibility per function.** If it does two unrelated things, split it.
- **Group by domain.** `date_utils`, `string_utils`, `http_utils` — not a single `helpers` dumping ground.
- **Models, services, and config are separate.** Never mix data definitions with business logic or configuration.
- **Files > ~200 lines → decompose.** Find natural seams and split.
- **Functions > ~40 lines → decompose.** Extract sub-steps into well-named helpers.
- **Shared vs. private.** One file uses it → keep private. Two files need it → `src/utils/`.
- **Layers don't skip layers.** Config → Models → Services → Entry points. No reverse imports.

---

## Markdown Formatting Rules (MANDATORY for all agents)

> All generated or edited `.md` files must follow these rules to pass linting.

- **Blank lines around lists.** Always put an empty line before and after any bulleted or numbered list.
- **Blank lines around fenced code blocks.** Always put an empty line before and after ` ``` ` fences.
- **Blank lines around headings.** Always put an empty line before and after `#` headings.
- **Language on code fences.** Always specify a language after ` ``` ` (e.g., ` ```python `, ` ```text `, ` ```mermaid `).
- **No trailing whitespace.** Strip trailing spaces from every line.
- **Single trailing newline.** Files end with exactly one newline character.
- **No duplicate headings** unless explicitly disabled with `<!-- markdownlint-disable MD024 -->`.

---

## Error Handling Strategy

<!-- How errors are handled across the project. -->

- **Never catch and swallow silently.** Every catch block must log, re-throw, or return a meaningful error.
- **Use typed/custom errors** when the language supports it (e.g., custom `AppError` class with error codes).
- **Fail fast in config/startup.** Missing environment variables or invalid config should crash immediately with a clear message.
- **Graceful degradation in runtime.** Non-critical failures (e.g., optional cache miss) should degrade gracefully, not crash.
- **Always include context in error messages.** Include what was attempted, what failed, and any relevant IDs/values.

---

## Dependencies Policy

<!-- Rules for adding new dependencies. -->
<!-- Example: "Prefer stdlib over packages. Every new dependency needs justification in a plan file." -->

- Prefer standard library / built-in solutions over adding new dependencies.
- When a dependency is added, document the justification here.

---

## Naming Conventions

<!-- Project-wide naming rules beyond what's in PREFERENCES.md. -->

- **Files:** `kebab-case` for filenames (e.g., `user-service.ts`, `date_utils.py`). Match the language's convention.
- **Functions/methods:** descriptive verbs (e.g., `calculateTotal`, `validate_input`, `fetchUserById`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`).
- **Types/classes:** `PascalCase` (e.g., `UserProfile`, `HttpClient`).
- **Boolean variables:** prefix with `is`, `has`, `should`, `can` (e.g., `isActive`, `hasPermission`).
- See `.ai/PREFERENCES.md` for user-specific style overrides.

---

## File Organization Rules

<!-- Rules about where code goes. -->

- **Utility functions** → `src/utils/` (never scattered in service files)
- **Business logic** → `src/services/`
- **Data models / schemas** → `src/models/`
- **Configuration** → `src/config/` (never hardcoded in source files)
- **Tests** → `tests/` (mirror `src/` structure)
- **Scripts** → `scripts/` (build, deploy, automation)

---

## Testing Strategy

<!-- How we test. What tools. What coverage expectations. -->

- **Test-first (red-green loop).** Tests are written before implementation. Test Writer Agent writes ≥10 failing tests per function across the 12-category taxonomy (edge cases first); the functionality must reach ≥50 tests across all layers. Worker Agent implements until they pass.
- **≥ 10 tests per public function across every applicable category of the 12-category taxonomy, edge cases first.** Categories: happy path, structure / shape, boundary values, empty/null/missing inputs, type abuse, range / overflow, unicode / encoding, error contract, idempotency, state transitions, time / concurrency, adversarial inputs. Skipping a category requires a 1-line `# CATEGORY N N/A: <reason>` comment.
- **≥ 50 tests per functionality (feature/module)** summed across all layers (unit + integration + E2E + contract). The feature is not done until the total reaches 50.
- **Bulletproof Standard:** before tests are accepted, ask "can I imagine a wrong implementation that passes all of these?" If yes, the suite is incomplete — add more.
- **Unit tests mirror `src/` structure.** `src/services/user-service.ts` → `tests/services/user-service.test.ts`.
- **Integration tests** for multi-module flows, written by Integration Tester Agent.
- **Run tests automatically.** Agents never pause to ask permission to run tests.

---

## Playbook Chunk Format

Playbook knowledge is stored as individual chunk files in `docs/playbooks/`. Each file uses `+++` TOML frontmatter delimiters and contains a single rule, pattern, or convention.

- **Location:** `docs/playbooks/{shared,agents,technologies}/`
- **One file per chunk** — each file is a self-contained unit of knowledge
- **Required TOML frontmatter fields:** `id`, `title`, `agents`, `technologies`, `category`, `tags`, `version`
- **Valid categories:** `pattern`, `anti-pattern`, `rule`, `convention`, `decision`, `strategy`
- **Body:** Markdown content below the closing `+++` delimiter — the actual rule or pattern text

Example structure:

```toml
+++
id = "anti-duplication-001"
title = "Anti-Duplication Rules"
agents = ["worker", "scaffolder", "refactor"]
technologies = ["all"]
category = "rule"
tags = ["duplication", "DRY", "extraction"]
version = 1
+++
```

---

## Playbook System

The playbook system provides structured coding rules and patterns to all agents via the Librarian.

- **Parser:** `src/utils/playbook_parser.py` — parses `.playbook.md` files with TOML frontmatter into structured chunk dicts
- **Validation:** `scripts/validate-playbooks.py` — runs `parse_all_playbooks()` as a pre-commit gate; exits non-zero on any malformed playbook
- **Rules location:** `docs/playbooks/` — organized by `shared/` (all agents) and `agents/` (agent-specific)
- **How playbooks reach agents:** The Librarian reads `.playbook.md` files, filters by agent name and technology, and includes relevant rules in the context brief passed to each agent at spawn time. Agents never read playbooks directly — they receive only the Librarian-curated subset.

---

## Changelog

<!-- Brief log of when this playbook was updated and what changed. -->

| Date           | Change                                        |
|----------------|-----------------------------------------------|
| 2026-03-15     | Cleanup: Removed phantom file entries, consolidated pattern/anti-pattern, updated architecture decisions, marked planned components |
| 2026-03-15     | Retrospective: Added Pre-Report File Verification and Adversarial Architecture Review patterns. Added 3 anti-patterns (Phantom File Audits, Abandoned Dispatch Logs, Stale Todo Trackers). |
| 2026-03-11     | Added Playbook Chunk Format and Knowledge Index sections |
| *(template)*   | Initial playbook created with empty sections  |
