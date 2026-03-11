+++
id = "shared/code-style"
title = "Code Style Convention"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["style", "readability", "formatting"]
version = 3
+++

### Code Style

- Functions must not exceed 40 lines. If longer, decompose into smaller functions
- Use descriptive names — avoid abbreviations. `get_user_by_id()` > `get_uid()`
- Doc comments on all exported functions, classes, and constants
- No hardcoded secrets — use environment variables or `.env` files (must be in `.gitignore`)
- Structure: `src/utils/`, `src/services/`, `src/models/`, `src/config/` — tests mirror `src/` in `tests/`
- Readable over clever — no ternary chains, no nested comprehensions beyond 1 level
- One statement per line. No semicolons to combine statements
- Constants in UPPER_SNAKE_CASE, functions/variables in lower_snake_case (Python) or camelCase (JS/TS)
- No wildcard imports (`from x import *`). Import only what you need
- Group imports: stdlib → third-party → local, separated by blank lines
- Prefer early returns over deeply nested conditionals
- Maximum file length: 300 lines. If longer, split into modules with clear responsibilities
- No commented-out code in commits — use version control for history, not comments
- Trailing whitespace and trailing newlines must be consistent — configure editor to strip trailing whitespace
- Use `TODO(username):` format for todos — never bare `TODO` or `FIXME` without attribution
- Boolean parameters in function signatures are a code smell — prefer named options or separate functions
- Avoid deep nesting (>3 levels) — refactor with early returns, guard clauses, or extracted functions
- End all files with a single newline character
- No unused variables or imports — configure linter to error on unused code
- String constants that represent configuration keys should be centralized, not scattered as inline strings
- Use consistent spacing around operators and after commas — enforce with formatter
- Prefer named function expressions over anonymous functions for better stack traces and debugging
- Keep conditional expressions simple — complex conditions should be extracted into named boolean variables
