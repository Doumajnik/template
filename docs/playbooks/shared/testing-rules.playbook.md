+++
id = "shared/testing-rules"
title = "Testing Rules"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["testing", "tdd", "coverage"]
version = 5
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
- Follow the Test Pyramid: write many fast unit tests, fewer integration tests, and minimal end-to-end tests — avoid the "ice cream cone" anti-pattern where most tests are slow E2E tests (Martin Fowler, Practical Test Pyramid)
- Test observable behavior, not implementation details — tests should verify "given input X, output is Y", not internal method call sequences, so they survive refactoring without breaking (Martin Fowler, Practical Test Pyramid)
- Avoid test duplication across pyramid levels: if a lower-level test already covers an edge case, don't duplicate it in a higher-level test — higher-level tests should only add confidence the lower levels can't provide (Martin Fowler, Avoid Test Duplication)
- Push tests as far down the pyramid as possible — if something can be verified with a unit test, don't write an integration test for it; reserve integration tests for actual integration points (Martin Fowler, Practical Test Pyramid)
- Write integration tests for every serialization/deserialization boundary: REST API calls, database reads/writes, queue messages, and file I/O — these are where real-world failures occur (Martin Fowler, Integration Tests)
- For external API dependencies, use Consumer-Driven Contract tests (CDC) to verify that your stubs match the real service behavior — tools like Pact formalize this (Martin Fowler, Contract Tests)
- Schedule regular exploratory testing sessions — manual, creative testing catches usability issues, design flaws, and edge cases that automated tests miss (Martin Fowler, Exploratory Testing)
- Treat test code with the same quality standards as production code — refactor tests for readability, apply DRY within reason (prefer DAMP: Descriptive And Meaningful Phrases), and never excuse sloppy code as "just tests" (Martin Fowler, Writing Clean Test Code)
- Categorize tests by size: Small tests (unit) run in a single process with no I/O, complete in <5s; Medium tests (integration) may use localhost services, complete in <30s; Large tests (E2E) may use external resources, complete in <5min — enforce size limits with test runner timeouts (Google Testing, Test Sizes)
- Tests must be hermetic: each test creates its own complete environment and tears it down afterward — never depend on state left by a previous test, shared databases, or external services that may be unavailable (Google Testing, Hermetic Testing)
- Track and fix flaky tests systematically: maintain a flakiness dashboard or report, quarantine flaky tests into a separate suite within 24 hours, and treat the root cause as a high-priority bug — flaky tests erode trust in the entire test suite (Google Testing, Test Flakiness)
- Manage test data explicitly: use builder patterns or factory functions to construct test objects with sensible defaults and only override the fields relevant to each test — avoid loading large fixture files that couple many tests to a single data shape (Google Testing, Test Data Management)
- Design code for testability using seams: inject dependencies through constructor parameters or function arguments so tests can substitute fakes — avoid `new` operators, static method calls, and global singletons in business logic that make mocking impossible (Google Testing, Test Seams)
- Test state, not interactions: verify the end result (return value, final state, output) rather than asserting that specific internal methods were called in a specific order — interaction-based tests are brittle and break on refactoring without catching real bugs (Google Testing, State vs Interaction Testing)
- Treat test infrastructure (fixtures, factories, custom assertions, test utilities) as shared library code: version it, review it, document it, and don't let it grow organically — poor test infrastructure is a top cause of slow, flaky, and unmaintainable test suites (Google Testing, Test Infrastructure)
