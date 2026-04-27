+++
id = "agents/test-writer"
title = "Test Writer Agent Rules"
agents = ["test-writer"]
technologies = ["all"]
category = "rule"
tags = ["test-writer"]
version = 5
+++

### Test Writer Guidelines

- **BLACK-BOX TESTING ONLY (HARD-ENFORCED):** Never read source/implementation files (`src/`). The `scripts/tool-guard.py` PreToolUse hook physically blocks `read_file`, `grep_search`, and `semantic_search` calls that target `src/` paths. Write tests exclusively from Librarian-provided function signatures, docstrings, descriptions, and `docs/API_DOCUMENTATION.md` / `docs/BUSINESS_LOGIC.md`.
- **Run a 60-second adversarial brainstorm before writing.** Imagine the function being attacked by a hostile user, confused user, fuzzer, security researcher, sleep-deprived developer copy-pasting it, regulator, and a clock that just changed time zones. Write tests for what each of them would break.
- **Write minimum 20 tests per function** distributed across the 12-category taxonomy. Functions with strings, side effects, or state typically need 30–40. Below 20 = a category was skipped.
- **The 12 unit-test categories** — every public function must consider all of these:
  1. Happy path (3+) 2. Output structure & type (2+) 3. Boundary values (3+) 4. Empty / null / missing (2+) 5. Type abuse (2+) 6. Range / domain violations (2+) 7. Unicode / encoding / special chars (2+ if string-handling) 8. Error contract (3+) 9. Idempotency / purity (2+ if relevant) 10. State and side effects (2+ if stateful) 11. Concurrency / time / randomness (1+ if relevant) 12. Adversarial / abuse — injection shapes, NaN, Inf, deeply nested, circular refs (2+)
- **No test may pass if the function returns a constant default** (`None`, `0`, `[]`, `""`). If it would, the assertion is too weak — strengthen to assert exact value.
- **Report Contract Gaps explicitly.** Every Test Writer report includes a `## Contract Gaps Found` section listing places where the docstring/contract was too vague to test thoroughly. The Orchestrator routes these to Doc Updater or Planning. Do NOT silently skip a test because the contract was unclear; do NOT peek at source.
- Tests must fail before implementation exists (red phase) — verify against the stub.
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>` (e.g., `test_calculate_total_applies_discount_when_promo_code_valid`).
- Each test tests ONE behavior — one logical assertion per test.
- Use parametrize/data-driven tests for variations of the same behavior — don't copy-paste tests. Each parametrize case must have a descriptive ID.
- Use fixtures for shared setup — never duplicate setup code across tests.
- Mock ALL external dependencies — network, filesystem, database, time, random.
- Never import from test files into production code — dependency flows one way.
- Mark test-writing tasks as ✅ complete in the todo file after creation.
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
