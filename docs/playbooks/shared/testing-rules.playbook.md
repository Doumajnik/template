+++
id = "shared/testing-rules"
title = "Testing Rules"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["testing", "tdd", "coverage"]
version = 3
+++

### Testing Rules

- Minimum 15 tests per function: happy paths, edge cases, error conditions, boundary values
- Tests mirror source structure: `src/utils/foo.py` → `tests/utils/test_foo.py`
- Test function names follow `test_<function>_<scenario>` pattern
- Each test should test ONE thing — one assertion per behavior
- Use fixtures and factories for test data setup — avoid duplicating setup across tests
- Mock external dependencies (APIs, databases, file system) — never make real network calls in unit tests
- Test edge cases: empty inputs, None/null, maximum values, boundary conditions, Unicode
- Tests must be deterministic — no random data, no time-dependent assertions without mocking
- Test error paths: verify that errors raise with correct types, messages, and context
- Integration tests go in a separate directory or are clearly marked — don't mix with unit tests
- Coverage target: 80%+ for new code. 100% for critical paths (auth, payments, data integrity)
- Tests should run in under 5 seconds for unit tests. Flag slow tests with markers
- Never test private/internal methods directly — test through the public API
- Don't test framework behavior — test YOUR logic
- Arrange-Act-Assert pattern: separate setup, execution, and verification with blank lines
- Test data should not depend on database state — each test creates its own data
- Use `pytest.raises` (Python) or `expect(...).toThrow` (TS) to test error conditions — never try/catch in tests
- Snapshot tests are allowed for serialized output (JSON, HTML) but must be reviewed on every update
- Never assert on object identity (===) when testing value equality — use deep equality
- Test timeout: unit tests ≤5s, integration tests ≤30s. Flag slow tests with markers
- Test environment must be isolated — never share state between tests. Reset mocks after each test
- Use in-memory databases or containers for integration tests — never test against shared dev databases
- Parameterized tests must have descriptive test IDs — not just `test[0]`, `test[1]`
- Flaky test policy: a test that fails intermittently must be fixed or quarantined within 24 hours — never ignored
- Code under test must not import test utilities — the dependency flows one way: tests → production code
- Test names should read as specifications: "test_create_user_returns_201_when_valid_email" tells the story
