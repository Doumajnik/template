+++
id = "shared/anti-duplication"
title = "Anti-Duplication Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["duplication", "dedup", "code-reuse"]
version = 3
+++

### Anti-Duplication

- Before creating any new function, class, or constant, search `CODE_INVENTORY.md` for similar existing symbols
- If a match exists, reuse or extend it — never duplicate
- Extract shared logic into `src/utils/` when 2+ modules use the same pattern
- Constants used in multiple files must live in a shared constants module
- When fixing a bug, check if the same bug exists in duplicated code elsewhere
- If two functions differ only in a parameter, merge them into one with a parameter
- Never copy-paste test helper functions — extract to `tests/conftest.py` or a shared test utils module
- Before adding a new dependency, check if an existing dependency already provides the same functionality
- Database queries that appear in multiple places must be extracted into a repository/data access layer
- When reviewing code, flag any function that looks like a renamed version of an existing one
- If a type/interface is used by multiple modules, define it in `src/models/` — not locally in each file
- Configuration validation logic must be centralized — one validator per config schema, not scattered across consumers
- Error message strings that appear in multiple places must be constants in a shared errors module
- When adding a utility function, check `src/utils/` first — don't create a local helper that duplicates an existing one
- Shared test data (fixtures, factories, mock responses) belongs in `tests/fixtures/` — never inline in individual test files
- API response shapes used in tests must reference the same type definitions as production code
- Logging format strings must be consistent — define format templates in one place
- When two services need the same data transformation, extract it into a pure function in `src/utils/`
- Avoid duplicating validation logic between frontend and backend — share schemas or generate from a single source
- If a regex pattern is used in more than one file, extract it into a named constant in a shared patterns module
