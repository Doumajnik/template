+++
id = "agents/critic"
title = "Critic Agent Rules"
agents = ["critic"]
technologies = ["all"]
category = "rule"
tags = ["critic"]
version = 4
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
- Flag Primitive Obsession — when raw strings, ints, or dicts are used instead of domain-specific types (e.g., a raw string for email addresses or a float for money) (source: refactoring.guru "Bloaters")
- Flag Feature Envy — when a function accesses data from another class more than its own, the function probably belongs in that other class (source: refactoring.guru "Couplers")
- Flag Shotgun Surgery — when a single logical change requires editing many different files or classes, the design has poor cohesion (source: refactoring.guru "Change Preventers")
- Flag Data Clumps — when the same group of parameters appears together in multiple function signatures, they should be consolidated into a dataclass or parameter object (source: refactoring.guru "Bloaters")
- Flag Speculative Generality — unused abstractions, interfaces with only one implementation, or parameters that are never used indicate YAGNI violations (source: refactoring.guru "Dispensables")
- Check for Long Parameter Lists — functions with more than 3-4 parameters should use parameter objects or builder patterns to improve readability (source: refactoring.guru "Bloaters")
- Verify the design avoids Inappropriate Intimacy — classes that access each other's private internals indicate broken encapsulation boundaries (source: refactoring.guru "Couplers")
- Flag Lazy Class — classes or modules that don't do enough to justify their existence should be inlined into their callers; maintaining and understanding them costs more than they provide (source: refactoring.guru "Dispensables")
- Flag Dead Code — unused variables, parameters, fields, methods, or classes must be removed immediately; dead code misleads readers and accumulates maintenance cost (source: refactoring.guru "Dispensables")
- Flag Data Class smell — classes that contain only fields with getters and setters but no behavior are a sign that behavior is misplaced in other classes; move the relevant logic into the data class (source: refactoring.guru "Dispensables")
- Flag Refused Bequest — subclasses that ignore or override most of their parent's methods indicate a wrong inheritance hierarchy; prefer composition or extract only the shared interface (source: refactoring.guru "Dispensables")
- Flag Duplicate Code across modules — two or more code fragments that look almost identical should be extracted into a shared utility; duplication is the single most reliable sign that something needs to be refactored (source: refactoring.guru "Dispensables")
- Flag Comments as a smell — when a method is filled with explanatory comments, the code itself needs to be clarified through renaming, extracting, or restructuring rather than annotated; comments should explain WHY, not WHAT (source: refactoring.guru "Dispensables")
