+++
id = "agents/refactor"
title = "Refactor Agent Rules"
agents = ["refactor"]
technologies = ["all"]
category = "rule"
tags = ["refactor"]
version = 2
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
