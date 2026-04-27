---
name: testing-rules
description: "Testing conventions, TDD rules, and test quality standards. Use when writing tests, reviewing test code, setting up test infrastructure, or discussing test strategy. Covers unit tests, integration tests, test pyramid, parameterization, fixtures, and coverage targets."
---

# Testing Rules

## When to Use

- Writing unit tests for new or existing functions
- Reviewing test code for quality and coverage
- Setting up test infrastructure (fixtures, factories, mocking)
- Planning test strategy for a feature or module
- Debugging flaky or slow tests
- Writing integration or E2E tests

## Rules

### Black-box first

- **Test Writers and Integration Testers are black-box agents.** They never read source files (`src/`). The `scripts/tool-guard.py` PreToolUse hook physically blocks `read_file` / `grep_search` / `semantic_search` calls targeting `src/` paths from these agents.
- Tests are written from **contracts only**: function signatures, docstrings, type annotations, `docs/API_DOCUMENTATION.md`, `docs/BUSINESS_LOGIC.md`, and the Librarian's context brief.
- **Why:** A tester who reads the implementation writes tests that mirror the code's structure — same blind spots, same bugs. Black-box testing catches what the implementer didn't think of.
- If the contract is too vague to test thoroughly, the tester flags it as a **Contract Gap** in the report — they do NOT silently skip the test or peek at the source.

### Test count and category coverage

- **Minimum 20 tests per function** for unit tests, distributed across the 12-category taxonomy below. Functions with strings, side effects, or state typically need 30–40.
- **Minimum 15 integration tests per feature**, **5 E2E tests per user-facing feature**, **1 contract test per consumer↔provider pair**. Below these counts means a category was skipped, not "sufficient".
- **The 12 unit-test categories** every Test Writer must consider for every function:
  1. **Happy path** — typical realistic inputs, exact output assertions (3+)
  2. **Output structure & type** — type, shape, ordering, length (2+)
  3. **Boundary values** — zero, one, max, min, off-by-one (3+)
  4. **Empty / null / missing** — empty collection, `None`, default vs explicit (2+)
  5. **Type abuse** — wrong type per parameter, verify documented exception (2+)
  6. **Range / domain violations** — negatives, out-of-range enums, bad dates (2+)
  7. **Unicode / encoding / special chars** — emoji, RTL, NULL bytes, very long (2+ if string-handling)
  8. **Error contract** — every documented exception type, error message shape, no swallowing (3+)
  9. **Idempotency / purity** — same input → same output, no input mutation (2+ if relevant)
  10. **State and side effects** — exact-once semantics, cleanup on failure (2+ if stateful)
  11. **Concurrency / time / randomness** — frozen clock, seeded RNG, no shared-state corruption (1+ if relevant)
  12. **Adversarial / abuse** — SQL/path/command injection shapes, NaN, Inf, deeply nested, circular refs (2+)

### Adversarial mindset

- Before writing tests, run a **60-second adversarial brainstorm**: imagine the function/system being attacked by a hostile user, a confused user, a fuzzer, a security researcher, a sleep-deprived developer copy-pasting it, a regulator, and a clock that just changed time zones. Write tests for what each of them would break.
- For integration / E2E: imagine flaky network, slow DB, duplicate webhook, partial outage of one downstream, malformed queue message, clock skew, retried request arriving twice, mid-deployment with old + new versions running side-by-side.
- The Test Writer's value is the bugs the implementer didn't anticipate. If your tests look like the implementation's structure, you're doing it wrong.

### Assertion strength

- No test may pass if the function returns a constant default (`None`, `0`, `[]`, `""`). If it would, the assertion is too weak — strengthen it to assert exact value.
- **Specific, not vague:** `assert result == [1, 2, 3]` — never `assert result is not None`.
- The expected value must be what a **correct** implementation would return — not what "any" implementation would return.
- Tests must fail before implementation exists (red phase) — verify against the stub.

### Naming

- Test names follow `test_<function>_<scenario>_<expected_result>` and read as specifications: `test_create_user_returns_201_when_valid_email`, `test_checkout_returns_402_when_card_declined_and_does_not_decrement_inventory`.
- Parametrized tests must have descriptive IDs — not `test[0]`, `test[1]`.

### Test file layout

- Unit tests mirror source: `src/utils/foo.py` → `tests/utils/test_foo.py`.
- Integration tests: `tests/integration/`.
- E2E tests: `tests/e2e/`.
- Contract tests: `tests/contracts/` (Pact files, Pact provider verifications).
- Don't mix layers in one file — they have different runtime / dependency / size profiles.

### General rules

- Each test should test ONE thing — one logical assertion per behavior.
- Use fixtures and factories for test data setup — avoid duplicating setup across tests.
- Mock external dependencies (APIs, databases, file system) for unit tests — never make real network calls.
- For integration tests, use **wire-level stubs** (WireMock, MSW, `responses`) — never code-level mocks. Wire-level stubs catch request-construction and response-parsing bugs.
- Tests must be deterministic — no random data without seeds, no time-dependent assertions without frozen clocks.
- Integration tests go in a separate directory or are clearly marked — don't mix with unit tests.
- Coverage target: 80%+ for new code. 100% for critical paths (auth, payments, data integrity).
- Tests should run in under 5 seconds for unit tests. Flag slow tests with markers.
- Never test private/internal methods directly — test through the public API.
- Don't test framework behavior — test YOUR logic.
- Arrange-Act-Assert pattern: separate setup, execution, and verification with blank lines.
- Test data should not depend on database state — each test creates its own data.
- Use `pytest.raises` (Python) or `expect(...).toThrow` (TS) to test error conditions — never try/catch in tests.
- Snapshot tests are allowed for serialized output (JSON, HTML) but must be reviewed on every update.
- Never assert on object identity (===) when testing value equality — use deep equality.
- Test timeout: unit tests ≤5s, integration tests ≤30s, E2E tests ≤5min. Flag slow tests with markers.
- Test environment must be isolated — never share state between tests. Reset mocks after each test.
- Use in-memory databases or containers for integration tests — never test against shared dev databases.
- Flaky test policy: a test that fails intermittently must be fixed or quarantined within 24 hours — never ignored.
- Code under test must not import test utilities — the dependency flows one way: tests → production code.
- Test names should read as specifications: "test_create_user_returns_201_when_valid_email" tells the story.
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
