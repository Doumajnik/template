+++
id = "agents/critic"
title = "Critic Agent Rules"
agents = ["critic"]
technologies = ["all"]
category = "rule"
tags = ["critic"]
version = 2
+++

### Critic Guidelines

- Check for over-engineering: does the design solve the actual problem, or a hypothetical future one?
- Flag any component without a clear single responsibility
- Verify the dependency graph has no cycles — circular dependencies indicate design flaws
- Challenge every abstraction layer — each must provide real value, not just indirection
- Check for hidden coupling: shared mutable state, implicit ordering requirements, global variables
- Verify error handling coverage — every external call must have failure handling in the design
- Flag any "god class" or "god function" that knows too much or does too much
- Check that the design follows established patterns from `docs/PLAYBOOK.md` — deviations need justification
- Verify testability — can every component be tested in isolation? If not, the design needs rework
- Look for missing concerns: logging, monitoring, rate limiting, caching, graceful degradation
- Maximum 10 review rounds — if issues persist after 10, escalate to the user
- Be specific in feedback — "this is wrong" is useless. "Function X violates SRP because it does A and B" is actionable
