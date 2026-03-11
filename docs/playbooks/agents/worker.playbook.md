+++
id = "agents/worker"
title = "Worker Agent Rules"
agents = ["worker"]
technologies = ["all"]
category = "rule"
tags = ["worker"]
version = 2
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
