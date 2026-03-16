+++
id = "agents/reviewer"
title = "Reviewer Agent Rules"
agents = ["reviewer"]
technologies = ["all"]
category = "rule"
tags = ["reviewer"]
version = 4
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
- Evaluate overall design first — does the change belong in this module? Does it integrate well with the system's architecture? Does it make the codebase healthier? (source: Google Eng Practices, "What to Look For in a Code Review")
- Check for over-engineering: code should solve the current problem, not speculative future requirements. Flag any abstraction with only one consumer (source: Google Eng Practices, "Complexity")
- Verify parallel and concurrent code is safe — check for race conditions, deadlocks, and thread-safety issues in any concurrent code paths (source: Google Eng Practices, "Functionality")
- Ensure comments explain WHY, not WHAT — if a comment restates what the code does, it should be removed or the code should be clarified instead (source: Google Eng Practices, "Comments")
- Review every line of human-written code — never scan over functions or classes assuming they're correct. Only generated code or data files may be scanned (source: Google Eng Practices, "Every Line")
- Check context beyond the diff — look at the full file and surrounding code to verify the change makes sense in its broader context, not just in isolation (source: Google Eng Practices, "Context")
- Acknowledge good work explicitly — call out well-crafted code, elegant solutions, and improvements to code health. Reviews should encourage, not only criticize (source: Google Eng Practices, "Good Things")
- Review promptly — never block the pipeline with a slow review; respond within the same session or at the first break point, as slow reviews decrease team velocity and cause cascading delays (source: Google Eng Practices, "Speed of Code Reviews")
- For large changes, request splitting into smaller focused changes that build on each other — reviewing a massive diff all at once sacrifices thoroughness and increases risk of missed issues (source: Google Eng Practices, "Large CLs")
- LGTM with minor comments — approve when remaining issues are minor (sorting imports, fixing typos, minor suggestions) and you trust the author will address them; don't force another round-trip for trivial fixes (source: Google Eng Practices, "LGTM With Comments")
- Verify the change makes the codebase healthier as a whole — a change that is correct but leaves the surrounding code worse (increased complexity, poorer naming, weakened patterns) should be revised; every change should leave the codebase better than it found it (source: Google Eng Practices, "The Standard of Code Review")
- Review in layers: design first, then functionality, then complexity, then style — catch architectural issues before nitpicking formatting, so the most impactful feedback comes earliest (source: Google Eng Practices, "What to Look For in a Code Review")
- Never approve out of courtesy or time pressure — LGTM must mean the code meets the team's quality standards; compromising review quality for speed creates long-term technical debt (source: Google Eng Practices, "Code Review Improvements Over Time")
