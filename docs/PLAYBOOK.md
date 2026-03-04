# Playbook

> **This is a living document.** AI agents append to it after making architecture decisions or discovering patterns.
> Agents read this at the start of every session to maintain consistency across the project.

**Last updated:** *(template created — no decisions yet)*

---

## Architecture Decisions

<!-- Record significant architecture choices here. Format: -->
<!-- ### {Decision Title} -->
<!-- **Date:** YYYY-MM-DD -->
<!-- **Context:** Why this decision was needed -->
<!-- **Decision:** What was chosen -->
<!-- **Alternatives considered:** What was rejected and why -->

*No architecture decisions yet.*

---

## Patterns We Use

<!-- Document recurring code patterns that should be followed consistently. -->
<!-- Example: "All API handlers follow the try/catch → mapError → respond pattern" -->

*No patterns established yet.*

---

## Patterns We Avoid

<!-- Document anti-patterns or approaches we've explicitly decided against. -->
<!-- Example: "Don't use default exports — always use named exports for better refactoring" -->

*No anti-patterns documented yet.*

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

- **Test-first (red-green loop).** Tests are written before implementation. Test Writer Agent writes 15+ failing tests, Worker Agent implements until they pass.
- **15+ tests per public function.** Covering: happy path (multiple inputs), edge cases, boundary values, empty/null/missing inputs, invalid types, large inputs, error conditions, negative logic, idempotency, combination inputs, regression cases.
- **Unit tests mirror `src/` structure.** `src/services/user-service.ts` → `tests/services/user-service.test.ts`.
- **Integration tests** for multi-module flows, written by Integration Tester Agent.
- **Run tests automatically.** Agents never pause to ask permission to run tests.

---

## Changelog

<!-- Brief log of when this playbook was updated and what changed. -->

| Date           | Change                                        |
|----------------|-----------------------------------------------|
| *(template)*   | Initial playbook created with empty sections  |
