+++
id = "agents/cleanup"
title = "Cleanup Agent Rules"
agents = ["cleanup"]
technologies = ["all"]
category = "rule"
tags = ["cleanup"]
version = 4
+++

### Cleanup Guidelines

- **Remove all unused imports** across the codebase. Unused imports add noise and can cause circular dependency issues.
- **Remove dead code** — functions, classes, and variables that are never called or referenced. Use static analysis or search to verify before removing.
- **Remove commented-out code** — version control preserves history, not comments. Commented code rots and misleads.
- **Remove empty files and placeholders** — empty test files, empty modules, and placeholder files that were never filled in serve no purpose.
- **Clean up whitespace** — trailing spaces, inconsistent line endings (CRLF vs LF), and excessive blank lines (more than 2 consecutive).
- **Remove unused dependencies** from package manifests (`requirements.txt`, `package.json`, `pyproject.toml`). Unused deps are attack surface.
- **Remove debug artifacts** — `print()` statements, `console.log()`, `debugger` statements, and `pdb.set_trace()` calls left from development.
- **Remove stale TODO comments** — TODOs that reference completed work or resolved issues. Check issue trackers before removing.
- **Verify `.gitignore` coverage** — build output, compiled files, IDE configs, `.env` files, `__pycache__/`, `node_modules/` must all be ignored.
- **Check for orphaned test files** — test files whose corresponding source file has been deleted. These tests pass vacuously and waste CI time.
- **Report what was removed** — provide file paths and line counts for every removal. Never delete silently. The user must be able to verify.
- **Run tests after cleanup** — verify nothing was broken by the removal. A cleanup that breaks tests is not a cleanup, it's a regression.
- **Detect and remove Speculative Generality** — remove unused interfaces, abstract classes, unnecessary parameters, and methods added "just in case" for future use that never materialized. YAGNI applies to abstractions too.
- **Collapse Lazy Classes** — classes that do too little (thin wrappers, single-method pass-through delegates with no added logic) should be inlined into their callers or merged with related classes to reduce unnecessary indirection.
- **Eliminate Data Classes without behavior** — classes containing only fields and getters/setters that are manipulated entirely by external code should either gain meaningful behavior or be replaced with plain data structures or typed dicts.
- **Remove redundant type aliases and re-exports** — type aliases, barrel files, and re-export modules that don't add meaningful abstraction are noise. Remove them unless they serve a documented purpose such as public API stability.
- **Clean up obsolete configuration files** — remove configuration files for tools, CI pipelines, and services that are no longer used: old linter configs, deprecated CI workflows, unused Dockerfiles, and stale environment templates.
- **Detect and extract duplicate code across modules** — identify near-identical code blocks across different files and extract them into shared utilities. Same-file duplication is obvious; cross-module duplication is insidious and grows silently.
- **Detect and resolve Divergent Change smells** — when a single class requires changes for multiple unrelated reasons (e.g., modifying finding, displaying, and ordering logic when adding a product type), split the class into cohesive units using Extract Class so each class has exactly one reason to change.
- **Detect and resolve Shotgun Surgery smells** — when a single conceptual change requires edits scattered across many classes, consolidate the scattered responsibility into a single class using Move Method and Move Field. Shotgun Surgery is the inverse of Divergent Change — responsibility has been over-distributed.
- **Eliminate Parallel Inheritance Hierarchies** — when creating a subclass in one hierarchy always requires creating a corresponding subclass in another, merge the hierarchies or use composition to decouple them. Parallel hierarchies double the maintenance cost of every extension.
- **Remove rigid coupling between modules** — identify modules that cannot be modified independently (changing module A always forces changes in module B). Introduce interfaces, dependency injection, or event-driven communication to break the rigid coupling and restore independent deployability.
- **Detect Feature Envy and relocate misplaced behavior** — when a method in one class extensively accesses data from another class rather than its own, move the method to the class whose data it primarily uses. Feature Envy creates implicit coupling that makes both classes harder to change independently.
- **Remove Middle Man classes that only delegate** — if a class exists solely to forward calls to another class without adding any logic, inline it by having callers use the target class directly. Middle Man classes add indirection without value and obscure the actual dependency graph.
