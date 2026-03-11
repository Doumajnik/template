+++
id = "agents/code-quality"
title = "Code Quality Agent Rules"
agents = ["code-quality"]
technologies = ["all"]
category = "rule"
tags = ["code-quality"]
version = 2
+++

### Code Quality Guidelines

- Scan for functions exceeding 40 lines and flag them for decomposition
- Detect duplicated code blocks (3+ lines identical or near-identical) across the codebase
- Flag functions with cyclomatic complexity > 10 — these need decomposition
- Check for code smells: feature envy, long parameter lists, data clumps, primitive obsession
- Verify naming consistency: do similar things have similar names? Are conventions followed?
- Check for dead code: unused functions, unreachable branches, commented-out code
- Verify import hygiene: no unused imports, no circular imports, proper grouping
- Check for magic numbers and string literals that should be named constants
- Flag any `print`/`console.log` statements that should be proper logging
- Verify error handling patterns are consistent across the codebase
- Write findings to `docs/QUALITY_REPORT.md` with severity: CRITICAL, HIGH, MEDIUM, LOW
- CRITICAL findings (duplicated logic, broken patterns) must be fixed before release
- Check test quality: sufficient coverage, proper mocking, meaningful assertions
