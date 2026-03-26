---
description: Diagnose and fix a bug from error logs, stack traces, or failing tests
agent: Debug
---

# Debug an Issue

Diagnose and fix the following bug:

**Error / Stack Trace / Symptom:** ${input:errorDescription}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — coding style and mode settings
   - `docs/PLAYBOOK.md` — architecture decisions and patterns
   - `docs/CODE_INVENTORY.md` — existing code symbols and file map

2. **Analyze the error:**
   - Parse the error message, stack trace, or failing test output
   - Identify the originating file(s), line(s), and function(s)
   - Classify the error type: runtime, logic, type, configuration, or dependency

3. **Read relevant source files:**
   - Open each file referenced in the stack trace or error
   - Trace the execution path from entry point to failure point
   - Check recent changes (`git log` / `git diff`) for potential regressions

4. **Isolate the root cause:**
   - Distinguish symptoms from root cause — fix the cause, not the symptom
   - Check for common patterns: null/undefined access, off-by-one, race conditions, missing error handling
   - Verify assumptions about inputs, state, and dependencies

5. **Apply the fix:**
   - Edit only the file(s) necessary to resolve the root cause
   - Keep the fix minimal and focused — do not refactor surrounding code
   - Ensure the fix handles edge cases introduced by the bug

6. **Verify the fix:**
   - Run the failing test(s) and confirm they now pass
   - Run the full test suite to check for regressions
   - If no tests exist for this code path, flag it for the Test Writer

7. **Report results:**
   - Root cause summary (one sentence)
   - Files modified and what changed
   - Test results: before and after
   - Any follow-up recommendations (missing tests, fragile patterns, tech debt)
