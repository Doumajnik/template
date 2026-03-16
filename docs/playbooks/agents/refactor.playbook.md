+++
id = "agents/refactor"
title = "Refactor Agent Rules"
agents = ["refactor"]
technologies = ["all"]
category = "rule"
tags = ["refactor"]
version = 4
+++

### Refactor Guidelines

- Behavior must be preserved exactly — refactoring changes structure, not functionality
- Run all tests before AND after refactoring — both must pass with the same results
- Refactor in small, testable steps — never make a massive change in one commit
- Common refactorings: extract function, extract class, rename, move, inline, replace conditional with polymorphism
- Check that all callers are updated when renaming or moving symbols
- Verify no new dependencies are introduced — refactoring should simplify, not add complexity
- Update `docs/CODE_INVENTORY.md` if any public symbols change names or locations
- Update `docs/files/` documentation for any files that changed significantly
- If refactoring reveals a bug, fix it in a separate commit — don't mix refactoring and bug fixes
- Verify no performance regression — refactoring should not make things slower
- Flag any code that can't be safely refactored due to tight coupling — report to Architect
- Use the IDE's refactoring tools when available — manual text replacement is error-prone
- Apply "Replace Nested Conditional with Guard Clauses" — flatten deeply nested if/else blocks by returning early for special cases, improving readability and reducing indentation depth
- Use "Introduce Parameter Object" when 3+ parameters travel together — group related parameters into a data class, named tuple, or config object to reduce parameter list length and clarify intent
- Apply "Separate Query from Modifier" (Command-Query Separation) — ensure functions either return a value OR produce a side effect, never both; this makes code easier to reason about and test
- Prefer "Replace Conditional with Polymorphism" over adding branches — when a switch/if-else chain grows beyond 3 cases, consider type-based dispatch or strategy pattern instead of another branch
- Apply "Extract Class" when a class has multiple distinct responsibilities — split so each class has a single reason to change; watch for classes with groups of fields/methods that only relate to each other
- Ensure each refactoring step is independently committable — if the refactoring is interrupted midway, the codebase must still compile, pass tests, and be in a deployable state
- Apply "Decompose Conditional" — extract complex conditional expressions (the condition itself, the then-branch, and the else-branch) into well-named methods that describe WHAT is being checked and WHAT happens, not HOW (ref: refactoring.guru)
- Apply "Consolidate Conditional Expression" — when multiple conditionals lead to the same result or action, merge them into a single expression or extract into a named method; scattered identical outcomes indicate a missing abstraction
- Apply "Consolidate Duplicate Conditional Fragments" — when identical code appears in all branches of a conditional (if/else/switch), move that code outside the conditional entirely; duplicated fragments across branches are a maintenance hazard
- Apply "Remove Control Flag" — replace boolean variables used as loop control flags (`found`, `done`, `shouldContinue`) with direct `break`, `continue`, or `return` statements; control flags add indirection that obscures the actual control flow
- Apply "Introduce Null Object" — when code has repeated null/None checks for a specific type, create a null object class that implements the same interface with safe default behavior; this eliminates scattered null-check conditionals
- Apply "Introduce Assertion" — when a code section depends on assumptions about input state that aren't enforced, add explicit assertions or precondition checks; make implicit assumptions visible and fail-fast rather than silently producing wrong results
