---
description: Refactor existing code for better structure, readability, or performance
agent: Refactor
---

# Refactor Code

Refactor the following target for improved structure, readability, or performance:

**Refactor Target:** ${input:refactorTarget}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — coding style and mode settings
   - `docs/PLAYBOOK.md` — architecture decisions, patterns, and anti-duplication rules
   - `docs/CODE_INVENTORY.md` — existing symbols to avoid duplication

2. **Analyze the target code:**
   - Read the file(s) or module identified in the refactor target
   - Map all callers, dependents, and consumers of the target code
   - Identify the current structure: responsibilities, coupling, cohesion

3. **Identify refactoring opportunities:**
   - Long functions (>40 lines) — decompose into smaller, focused functions
   - Duplicated logic — extract shared utilities to `src/utils/`
   - Mixed responsibilities — separate into distinct modules or layers
   - Complex conditionals — simplify with guard clauses or strategy patterns
   - Dead code or unused imports — flag for removal

4. **Impact analysis (mandatory before any changes):**
   - List all files that import or depend on the target code
   - Identify tests that cover the target code
   - Note any public API or interface changes required
   - Create a regression checklist of behaviors that must not change

5. **Plan the refactoring:**
   - Break the refactor into small, verifiable steps
   - Each step must keep tests passing (no red phase allowed)
   - Preserve all existing behavior — refactoring changes structure, not behavior

6. **Implement the refactoring:**
   - Apply changes incrementally, running tests after each step
   - Update all callers and dependents to use the new structure
   - Ensure every exported function has a doc comment
   - Keep functions under ~40 lines

7. **Verify the refactoring:**
   - Run the full test suite — all tests must pass
   - Confirm no behavior has changed (same inputs produce same outputs)
   - Check for new lint errors or warnings — fix all of them

8. **Report results:**
   - Summary of structural changes made
   - Before/after comparison (complexity, line count, responsibilities)
   - Test results confirming no regressions
   - Any follow-up recommendations
