+++
id = "agents/code-quality"
title = "Code Quality Agent Rules"
agents = ["code-quality"]
technologies = ["all"]
category = "rule"
tags = ["code-quality"]
version = 4
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
- Detect "Shotgun Surgery" — flag changes that require modifying many different classes simultaneously, indicating responsibility is scattered across the codebase instead of cohesive
- Flag "Speculative Generality" — identify abstractions, parameters, or extension points added for hypothetical future use that increase complexity without delivering current value
- Check for "Inappropriate Intimacy" — flag classes that excessively access internals of other classes (private fields, implementation details), violating encapsulation boundaries
- Detect "Message Chains" (Law of Demeter violations) — flag long chains of method calls like `a.getB().getC().getD()` that create brittle coupling across multiple objects
- Flag "Divergent Change" — identify classes that are modified for multiple unrelated reasons, violating the Single Responsibility Principle; each class should have one reason to change
- Assess cognitive complexity, not just cyclomatic complexity — deeply nested conditionals and non-linear control flow (breaks, continues, early returns inside loops) are harder to understand than sequential branches with the same branch count
- Penalize nesting depth more heavily than branch count — each additional level of nesting multiplies cognitive load; a method with 3 levels of nested if/for/while is harder to understand than one with 6 sequential branches at the same level (SonarSource Cognitive Complexity)
- Treat switch/match statements as a single complexity unit — unlike cyclomatic complexity which increments per case, a well-structured switch is cognitively simple; flag switch statements only when they contain nested logic or side effects within cases
- Flag compound boolean expressions with 3+ operators — conditions like `(a && b || c && !d)` are hard to reason about; recommend extracting into named boolean variables or predicate methods that describe the business intent
- Measure complexity at the class/module level, not just per-method — a class with 20 trivial methods and zero logic should score near zero; a class with 5 logic-heavy methods should score high; method-only metrics miss the forest for the trees
- Track code health trends over time, not just snapshots — a single quality scan reveals current state, but comparing scores across commits reveals whether quality is improving or degrading; flag modules with consistently worsening trends for priority attention
- Distinguish between testability and understandability metrics — cyclomatic complexity measures how many test cases are needed (testability), while cognitive complexity measures how hard the code is to read (understandability); report both and optimize for understandability first
