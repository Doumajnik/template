+++
id = "agents/test-writer"
title = "Test Writer Agent Rules"
agents = ["test-writer"]
technologies = ["all"]
category = "rule"
tags = ["test-writer"]
version = 4
+++

### Test Writer Guidelines

- **BLACK-BOX TESTING ONLY:** Never read source/implementation files (`src/`). Write tests exclusively from Librarian-provided function signatures, docstrings, and descriptions. This is enforced by the Tool Manifest.
- Write minimum 15 tests per function covering: happy paths (3+), edge cases (5+), error conditions (5+), boundary values (2+)
- Tests must fail before implementation exists (red phase) — verify against the stub
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Each test tests ONE behavior — one logical assertion per test
- Test edge cases: empty input, None/null, zero, negative numbers, max int, empty strings, Unicode, special characters
- Test error conditions: verify correct exception types, exception messages include context, and the function doesn't silently swallow errors
- Use parametrize/data-driven tests for variations of the same behavior — don't copy-paste tests
- Use fixtures for shared setup — never duplicate setup code across tests
- Mock ALL external dependencies — network, filesystem, database, time, random
- Never import from test files into production code — dependency flows one way
- Test boundary values: off-by-one, max length, min length, exact boundary
- Verify idempotency where relevant — calling the function twice with the same input should produce the same result
- Test that functions don't mutate their input arguments when they shouldn't
- Mark test-writing tasks as ✅ complete in the todo file after creation
- Follow the Arrange-Act-Assert (AAA) pattern in every test — clearly separate setup, execution, and verification into distinct blocks (source: Martin Fowler, "Practical Test Pyramid")
- Test observable behavior, not implementation details — if refactoring internal code without changing behavior breaks your tests, the tests are too tightly coupled to the implementation (source: Martin Fowler, "Practical Test Pyramid")
- Prefer sociable unit tests (using real collaborators) over solitary tests (all mocks) when collaborators are fast and deterministic — mock only slow, non-deterministic, or external dependencies (source: Martin Fowler, "Practical Test Pyramid")
- Write contract tests for every external service integration — verify that your mocks and stubs match the real service's API contract so fakes don't drift from reality (source: Martin Fowler, "Practical Test Pyramid")
- Avoid test duplication across pyramid levels — if a behavior is fully covered by unit tests, don't re-test the same logic in integration tests. Push tests as far down the pyramid as possible (source: Martin Fowler, "Practical Test Pyramid")
- Never test trivial code (simple getters, setters, direct pass-throughs with no logic) — focus testing effort on code with conditional logic and business rules (source: Martin Fowler, "Practical Test Pyramid")
- Test code is production-quality code — apply the same readability, naming, and structure standards. "This is only test code" is never a valid excuse for sloppy code (source: Martin Fowler, "Practical Test Pyramid")
- Place shared fixtures in `conftest.py` at the appropriate directory level — never duplicate fixture definitions across test files; pytest discovers `conftest.py` fixtures automatically without requiring imports (source: pytest docs, "How to use fixtures")
- Choose the correct fixture scope (`function`, `class`, `module`, `session`) based on setup cost — use broader scopes only for expensive, stateless, or read-only resources; default to `function` scope for anything that mutates state (source: pytest docs, "Fixture scopes")
- Use `yield` fixtures for teardown — place cleanup code after the `yield` statement to guarantee it runs even when tests fail, replacing manual try/finally blocks (source: pytest docs, "Teardown/Cleanup")
- Use factory fixtures (fixtures that return a function) when a single test needs multiple distinct instances of test data — this avoids parametrize overhead and gives the test explicit control over creation (source: pytest docs, "Factories as fixtures")
- Avoid `autouse=True` fixtures unless the fixture genuinely applies to ALL tests in its scope — implicit setup hides test dependencies and makes individual tests harder to understand in isolation (source: pytest docs, "Autouse fixtures")
- Keep fixtures minimal and composable — each fixture should perform exactly one setup step; build complex test scenarios by composing small fixtures rather than creating monolithic setup functions (source: pytest docs, "Safe fixture structure")
