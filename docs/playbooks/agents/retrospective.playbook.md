+++
id = "agents/retrospective"
title = "Retrospective Agent Rules"
agents = ["retrospective"]
technologies = ["all"]
category = "rule"
tags = ["retrospective"]
version = 2
+++

### Retrospective Guidelines

1. **Review all agent decisions** from the session — were they correct, efficient, and well-justified? Flag unjustified decisions.
2. **Identify success patterns** — what approaches worked well? Document them so they can be repeated.
3. **Identify failure patterns** — what approaches failed? Why? Document them so they can be avoided.
4. **Check for recurring issues** — did the same type of problem come up multiple times? Recurring issues need systemic fixes, not patches.
5. **Update `docs/PLAYBOOK.md`** with new rules or patterns discovered during the session. The Playbook evolves with every retrospective.
6. **Append findings to `docs/RETROSPECTIVE_REPORT.md`** with: date, session topic, patterns identified, and rules added or modified.
7. **Review the dispatch log** — were agents spawned in the right order? Were any spawns unnecessary? Could the pipeline have been shorter?
8. **Check for wasted effort** — was context lost and re-gathered? Were tasks redone? Context waste is the most expensive inefficiency.
9. **Identify process improvements** — should the pipeline order change? Should new checks be added? Should existing checks be removed?
10. **Review error recovery** — when things went wrong, was recovery swift and effective? Were there unnecessary retries?
11. **Check `.ai/lessons.md`** — does it need updating with new lessons learned? Are existing lessons still accurate?
12. **Be specific and constructive** — "improve error handling" is useless. "Add retry logic to embedding client for 429 responses" is actionable.
13. **Mark the retrospective task ✅** and set the todo file status to ✅ Complete when finished.
