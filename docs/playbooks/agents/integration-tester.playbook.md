+++
id = "agents/integration-tester"
title = "Integration Tester Agent Rules"
agents = ["integration-tester"]
technologies = ["all"]
category = "rule"
tags = ["integration-tester"]
version = 4
+++

### Integration Tester Guidelines

- **Test multi-module interactions** — verify that modules A → B → C work correctly end-to-end. Follow the data flow across boundaries.
- **Use real implementations** — minimal mocking. Only mock truly external services (third-party APIs, payment gateways). Internal services must use their real code.
- **Test the full request lifecycle** — input validation → business logic → data persistence → response. Every layer must be exercised.
- **Verify data consistency across service boundaries** — what one service writes, another must correctly read. Check serialization/deserialization at every boundary.
- **Test error propagation** — when an internal service fails, does the system respond with the correct error code, message, and status? Errors must not be swallowed.
- **Test idempotency** — repeated calls with the same input should produce the same result without side effects. Critical for retry-safe APIs.
- **Test concurrent access when relevant** — race conditions, deadlocks, and data corruption under parallel requests. Use threading or async test utilities.
- **Use test containers or in-memory databases** — never test against shared development databases. Each test run must start with a clean, isolated state.
- **Keep integration tests separate from unit tests** — use a `--integration` flag, marker, or separate directory. Integration tests run in CI but can be skipped locally for speed.
- **Verify startup and shutdown sequences** — the application must start cleanly (no crash on boot) and shut down gracefully (no orphaned connections, no data loss).
- **Test configuration variations** — what happens with missing env vars, invalid config values, or partial configuration? The system should fail fast with clear error messages.
- **Mark integration test tasks ✅ in the todo file** after all tests pass. Append results to the Progress Log.
- **Use consumer-driven contract tests (CDC)** — verify API contracts between services using tools like Pact. Contract tests let consumers define expectations and providers verify compliance, catching breaking changes without full end-to-end tests.
- **Avoid test duplication across pyramid layers** — don't re-test logic already covered by unit tests. Integration tests should focus on boundary behavior, serialization, and cross-service communication — not business logic already verified at lower levels.
- **Test every serialization/deserialization boundary** — write integration tests for every point where data crosses a format boundary: REST APIs, message queues, database reads/writes, and file I/O. Encoding bugs hide at boundaries.
- **Use wire-level stubs for external services** — simulate external service responses at the HTTP level (e.g., WireMock, responses library) rather than mocking at the code level. Wire-level stubs catch request construction and response parsing bugs that code-level mocks miss.
- **Keep integration tests deterministic** — avoid time-dependent, order-dependent, or network-dependent assertions. Use fixed clocks, deterministic ordering, and locally-running services to prevent flaky tests.
- **Place fast integration tests early in the CI pipeline** — narrowly-scoped integration tests that run in seconds belong alongside unit tests in the first pipeline stage. Reserve broad, slow integration tests for later stages to maintain fast feedback loops.
- **Verify backward compatibility on API changes** — when an API evolves, run integration tests against both the old and new contract versions to confirm existing consumers are not broken by the change.
- **Test contract evolution with provider states** — use Pact provider states to define preconditions for each interaction independently. Never chain interactions sequentially; each contract scenario must be self-contained with its own state setup so tests remain independent and parallelizable.
- **Use a Pact Broker to orchestrate contract verification and deployments** — publish consumer pacts to a centralized broker and use `can-i-deploy` to gate deployments. Manual contract sharing via files breaks down at scale and introduces deployment race conditions between consumer and provider pipelines.
- **Test message-based integrations at the payload level** — for event-driven systems using queues (Kafka, SNS, RabbitMQ), verify message contracts at the domain payload level using Message Pact rather than at the transport level. Focus on the event shape, not the queue-specific wrapper or transport envelope.
- **Keep contract tests focused on communication, not business logic** — contract tests validate that services can communicate correctly (request shapes, response structures, status codes). Business logic correctness belongs in unit and functional tests. Mixing concerns produces brittle, slow contract test suites that break for the wrong reasons.
- **Run provider verification in the provider's own CI pipeline** — provider verification replays consumer expectations against the real provider. Run this in the provider's CI, not the consumer's, so providers own their own compliance and can detect breaking changes before merge.
- **Generate API stubs from verified contracts for offline development** — use the Pact file as a source of guaranteed-accurate API stubs so consumers can develop and test offline without standing up the actual provider service. This eliminates environment coupling and enables parallel team development.
