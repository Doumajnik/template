+++
id = "agents/test-writer"
title = "Test Writer Agent Rules"
agents = ["test-writer"]
technologies = ["all"]
category = "rule"
tags = ["test-writer"]
version = 2
+++

### Test Writer Guidelines

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
