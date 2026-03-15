+++
id = "agents/worker"
title = "Worker Agent Rules"
agents = ["worker"]
technologies = ["all"]
category = "rule"
tags = ["worker"]
version = 4
+++

### Worker Guidelines

- Implement exactly ONE function per invocation — never implement multiple functions at once
- Read the existing tests FIRST before writing any implementation code
- Run all tests after every change. Never mark a task complete without green tests as proof
- Follow TDD red-green-refactor: make one failing test pass at a time, then refactor
- Functions must not exceed 40 lines. If the implementation grows beyond that, decompose immediately
- Use only the dependencies already listed in the project — never install new packages without approval
- When a test fails, fix the implementation — never modify a test to make it pass (unless the test has a genuine bug)
- Check `docs/CODE_INVENTORY.md` before creating any new helper function — reuse existing utilities
- Match the code style of surrounding code — consistency trumps personal preference
- If the function requires I/O, use dependency injection for testability — don't hardcode file paths or URLs
- After the function passes all tests, verify there are no linter warnings or type errors
- Include proof of completion: paste the test output showing all tests green
- If stuck after 2 attempts, report the failure clearly — don't keep retrying the same approach
- Refactor only after green — never refactor while tests are failing. The refactor phase of red-green-refactor requires passing tests as a safety net
- Replace magic numbers and strings with named constants — no literal values embedded in logic (source: refactoring.guru "Replace Magic Number with Symbolic Constant")
- Simplify conditionals: replace nested if/else chains with guard clauses or early returns to reduce nesting depth (source: refactoring.guru "Replace Nested Conditional with Guard Clauses")
- Use Extract Method when a code block needs a comment to explain what it does — the method name replaces the comment (source: refactoring.guru "Composing Methods")
- Separate queries from commands — functions should either return a value or produce a side effect, not both (source: refactoring.guru "Separate Query from Modifier")
- When refactoring, verify behavior is preserved by running all tests after every individual change — never batch multiple refactoring steps before running tests
- Prefer pure functions over stateful methods — given the same inputs, always produce the same output without side effects
- Apply Extract Variable for complex expressions — break hard-to-read expressions into named intermediate variables that make intent self-documenting (source: refactoring.guru "Extract Variable")
- Use Preserve Whole Object — when passing multiple values from the same object as function parameters, pass the object itself instead to reduce parameter count and coupling (source: refactoring.guru "Preserve Whole Object")
- Replace Conditional with Polymorphism — when a conditional performs different actions based on object type or properties, refactor into subclasses or strategy objects with a shared interface (source: refactoring.guru "Simplifying Conditional Expressions")
- Apply Decompose Conditional for complex if/then/else — extract the condition, then-branch, and else-branch into separate named methods so the conditional reads like prose (source: refactoring.guru "Decompose Conditional")
- Never reassign function parameters — if you need to modify a parameter's value, assign it to a local variable instead to preserve the original input for debugging and clarity (source: refactoring.guru "Remove Assignments to Parameters")
- Each temporary variable should serve exactly one purpose — never reuse a variable for multiple intermediate values, as this obscures data flow and makes debugging harder (source: refactoring.guru "Split Temporary Variable")
