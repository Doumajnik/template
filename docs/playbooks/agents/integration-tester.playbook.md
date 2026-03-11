+++
id = "agents/integration-tester"
title = "Integration Tester Agent Rules"
agents = ["integration-tester"]
technologies = ["all"]
category = "rule"
tags = ["integration-tester"]
version = 2
+++

### Integration Tester Guidelines

1. **Test multi-module interactions** — verify that modules A → B → C work correctly end-to-end. Follow the data flow across boundaries.
2. **Use real implementations** — minimal mocking. Only mock truly external services (third-party APIs, payment gateways). Internal services must use their real code.
3. **Test the full request lifecycle** — input validation → business logic → data persistence → response. Every layer must be exercised.
4. **Verify data consistency across service boundaries** — what one service writes, another must correctly read. Check serialization/deserialization at every boundary.
5. **Test error propagation** — when an internal service fails, does the system respond with the correct error code, message, and status? Errors must not be swallowed.
6. **Test idempotency** — repeated calls with the same input should produce the same result without side effects. Critical for retry-safe APIs.
7. **Test concurrent access when relevant** — race conditions, deadlocks, and data corruption under parallel requests. Use threading or async test utilities.
8. **Use test containers or in-memory databases** — never test against shared development databases. Each test run must start with a clean, isolated state.
9. **Keep integration tests separate from unit tests** — use a `--integration` flag, marker, or separate directory. Integration tests run in CI but can be skipped locally for speed.
10. **Verify startup and shutdown sequences** — the application must start cleanly (no crash on boot) and shut down gracefully (no orphaned connections, no data loss).
11. **Test configuration variations** — what happens with missing env vars, invalid config values, or partial configuration? The system should fail fast with clear error messages.
12. **Mark integration test tasks ✅ in the todo file** after all tests pass. Append results to the Progress Log.
