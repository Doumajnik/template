+++
id = "shared/code-style"
title = "Code Style Convention"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["style", "readability", "formatting"]
version = 5
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
- Never use mutable objects (lists, dicts, sets) as default parameter values — use `None` and assign inside the function body (Google Python Style Guide, §2.12)
- Minimize the amount of code inside `try`/`except` blocks — the larger the try body, the more likely an unexpected exception gets caught (Google Python Style Guide, §2.4)
- Use implicit boolean evaluation for collections: `if not users:` instead of `if len(users) == 0:` — empty containers are falsy in Python (Google Python Style Guide, §2.14)
- Don't vertically align tokens (=, #, :) on consecutive lines — it creates maintenance burden when names change length (Google Python Style Guide, §3.6)
- Use context managers (`with` statement) for all file handles, sockets, database connections, and similar stateful resources — never rely on garbage collection for cleanup (Google Python Style Guide, §3.11)
- Comprehensions must be simple: no multiple `for` clauses or complex filter expressions — use a regular loop if the comprehension doesn't fit on one conceptual line (Google Python Style Guide, §2.7)
- Add type annotations to all public API function signatures — type hints improve readability, enable static analysis, and catch bugs before runtime (Google Python Style Guide, §2.21)
- Maximum line length is 80 characters — exceptions allowed for long import statements, URLs in comments, and lint-disable directives; use implicit line joining inside parentheses instead of backslash continuations (Google Python Style Guide, §3.2)
- Detect and break import cycles: if module A imports module B and module B imports module A, refactor to eliminate the circular dependency — use dependency inversion, extract a shared interface module, or defer imports inside functions (Google Python Style Guide, §3.19.14)
- Avoid mutable global state — module-level mutable variables make code hard to test and can introduce subtle concurrency bugs; if global state is unavoidable, make it internal (`_prefixed`) and access through functions (Google Python Style Guide, §2.5)
- Use default iterators and operators for types that support them: prefer `for key in adict:` over `for key in adict.keys():` and `if obj in alist:` over manual index searching (Google Python Style Guide, §2.8)
- Avoid power features (metaclasses, dynamic inheritance, bytecode manipulation, `__del__` methods, import hacks) unless absolutely necessary — they make code harder to understand, debug, and maintain (Google Python Style Guide, §2.19)
- Use %-formatting or lazy evaluation in logging calls instead of f-strings — logging frameworks skip string interpolation when the log level is disabled, improving performance: `logger.info('User %s logged in', username)` not `logger.info(f'User {username} logged in')` (Google Python Style Guide, §3.10.1)
