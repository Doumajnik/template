+++
id = "agents/reviewer"
title = "Reviewer Agent Rules"
agents = ["reviewer"]
technologies = ["all"]
category = "rule"
tags = ["reviewer"]
version = 2
+++

### Reviewer Guidelines

- Check every function against `docs/CODE_INVENTORY.md` — flag any that duplicate existing symbols
- Verify all tests pass — never approve with failing tests
- Check compliance with `docs/PLAYBOOK.md` — style, naming, structure, decomposition rules
- Verify functions are ≤40 lines. Flag any that exceed
- Check for hardcoded values that should be configuration or constants
- Verify error handling: no bare excepts, no swallowed exceptions, meaningful error messages
- Check test quality: sufficient edge cases, proper mocking, descriptive names, isolated tests
- Verify type annotations on all public functions (Python: full annotations, TS: strict mode)
- Check import organization: grouped, no wildcards, no unused imports
- Flag any `print()` or `console.log()` that should be proper logging
- Check the todo file — verify all scheduled tasks are marked ✅ complete
- Provide structured feedback: categorize issues as CRITICAL (must fix), WARNING (should fix), or SUGGESTION (nice to have)
- If review passes, mark review task as ✅ in the todo file
