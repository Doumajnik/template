+++
id = "agents/cleanup"
title = "Cleanup Agent Rules"
agents = ["cleanup"]
technologies = ["all"]
category = "rule"
tags = ["cleanup"]
version = 2
+++

### Cleanup Guidelines

1. **Remove all unused imports** across the codebase. Unused imports add noise and can cause circular dependency issues.
2. **Remove dead code** — functions, classes, and variables that are never called or referenced. Use static analysis or search to verify before removing.
3. **Remove commented-out code** — version control preserves history, not comments. Commented code rots and misleads.
4. **Remove empty files and placeholders** — empty test files, empty modules, and placeholder files that were never filled in serve no purpose.
5. **Clean up whitespace** — trailing spaces, inconsistent line endings (CRLF vs LF), and excessive blank lines (more than 2 consecutive).
6. **Remove unused dependencies** from package manifests (`requirements.txt`, `package.json`, `pyproject.toml`). Unused deps are attack surface.
7. **Remove debug artifacts** — `print()` statements, `console.log()`, `debugger` statements, and `pdb.set_trace()` calls left from development.
8. **Remove stale TODO comments** — TODOs that reference completed work or resolved issues. Check issue trackers before removing.
9. **Verify `.gitignore` coverage** — build output, compiled files, IDE configs, `.env` files, `__pycache__/`, `node_modules/` must all be ignored.
10. **Check for orphaned test files** — test files whose corresponding source file has been deleted. These tests pass vacuously and waste CI time.
11. **Report what was removed** — provide file paths and line counts for every removal. Never delete silently. The user must be able to verify.
12. **Run tests after cleanup** — verify nothing was broken by the removal. A cleanup that breaks tests is not a cleanup, it's a regression.
