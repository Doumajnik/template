Run the Change Pipeline for modifying existing code. Read AGENTS.md "Change Pipeline" section.

Execute all 22 steps:
1. Prompt Engineer → change spec
2. Impact Analysis (Librarian + Discovery)
3. Research
4. Dependency check
5. Architect → change approach
6. Critic (bottleneck)
7. Innovator
8. Architect (revision)
9. Critic (full) — "does this break anything that currently works?"
10. Planning Agent → change plan + regression checklist
11. Deprecation Manager (if removing public surface)
12. Architect (plan verification)
13. USER APPROVAL
14. Test Writer → tests for changed + unchanged behavior
15. Worker → implement + verify ALL existing tests pass
16. Integration Tester
17. Reviewer
18. Security
19. Code Quality
20. Doc Updater
21. Retrospective
22. Cleanup

Follow .ai/checklists/change.checklist.md.

User's request: $ARGUMENTS
