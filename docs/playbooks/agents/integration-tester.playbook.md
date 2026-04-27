+++
id = "agents/integration-tester"
title = "Integration Tester Agent Rules"
agents = ["integration-tester"]
technologies = ["all"]
category = "rule"
tags = ["integration-tester"]
version = 5
+++

### Integration Tester Guidelines

- **BLACK-BOX TESTING ONLY (HARD-ENFORCED):** Never read source/implementation files (`src/`). The `scripts/tool-guard.py` PreToolUse hook physically blocks `read_file`, `grep_search`, and `semantic_search` calls that target `src/` paths. Work exclusively from `docs/API_DOCUMENTATION.md`, `docs/BUSINESS_LOGIC.md`, the Librarian's context brief, the existing `tests/` directory, and the running system as a black box.
- **Three test layers, separate directories:** integration tests in `tests/integration/`, E2E tests in `tests/e2e/`, contract tests in `tests/contracts/`. Don't mix — they have different runtime / dependency profiles.
- **Minimum counts per cycle:** 15 integration tests per feature, 5 E2E tests per user-facing feature, 1 contract test per consumer↔provider pair. Below = the category was skipped, not "sufficient".
- **Run a 60-second adversarial brainstorm before writing.** Imagine flaky network, slow DB, duplicate webhook, partial outage of one downstream, malformed queue message, clock skew, retried request arriving twice, mid-deployment with old + new versions running side-by-side. Write tests for what each of those would break.
- **Integration test categories** (cover all): data flow across boundaries (3+), error propagation (3+), schema/contract correctness (2+), idempotency at boundaries (2+), failure modes — timeout / 5xx / malformed / unavailable (3+), configuration variations — missing/invalid/partial (2+).
- **E2E test categories** (cover all): critical happy path, critical error path, critical recovery path with transient failure, cross-feature interaction, data integrity across restart.
- **Contract tests are Consumer-Driven** (Pact or equivalent): consumer defines expectation, provider verifies in provider's CI. Use wire-level stubs (WireMock, MSW, `responses`) — never code-level mocks. Each scenario self-contained with its own provider state.
- **Test multi-module interactions** — verify that modules A → B → C work correctly end-to-end. Follow the data flow across boundaries.
- **Use real implementations** — minimal mocking. Only mock truly external services. Internal services must use their real code.
- **Test the full request lifecycle** — input validation → business logic → data persistence → response. Every layer must be exercised.
- **Verify data consistency across service boundaries** — what one service writes, another must correctly read. Check serialization/deserialization at every boundary.
- **Test error propagation** — when an internal service fails, the system responds with correct error code, message, and status. Errors must not be swallowed and must not leak internal stack traces.
- **Test idempotency** — repeated calls with the same input produce the same result without side effects. Critical for retry-safe APIs.
- **Test concurrent access when relevant** — race conditions, deadlocks, data corruption under parallel requests.
- **Use test containers or in-memory databases** — never test against shared development databases. Each test run starts with clean isolated state.
- **Verify startup and shutdown sequences** — application starts cleanly, shuts down gracefully, no orphaned connections, no data loss.
- **Test configuration variations** — missing env vars, invalid values, partial configuration. System should fail fast with clear error messages.
- **Keep integration tests deterministic** — frozen clocks, seeded RNG, locally-running services, no order dependence.
- **Place fast integration tests early in the CI pipeline** — narrowly-scoped tests run alongside unit tests. Reserve broad slow tests for later stages.
- **Verify backward compatibility on API changes** — run integration tests against both old and new contract versions.
- **Test contract evolution with provider states** — each contract scenario self-contained with own state setup; never chain interactions sequentially.
- **Use a Pact Broker to orchestrate contract verification and deployments** — publish consumer pacts to a centralized broker; use `can-i-deploy` to gate deployments.
- **Test message-based integrations at the payload level** — for queue-based systems (Kafka, SNS, RabbitMQ), verify domain payload shape via Message Pact, not transport envelope.
- **Keep contract tests focused on communication, not business logic** — contract tests validate request/response shapes; business logic correctness belongs in unit tests.
- **Run provider verification in the provider's own CI pipeline** — providers own their own compliance and detect breaking changes before merge.
- **Generate API stubs from verified contracts for offline development** — use Pact files as guaranteed-accurate stubs.
- **Report Contract Gaps explicitly.** Every Integration Tester report includes a `## Contract Gaps Found` section listing places where docs were too vague to test thoroughly. Do NOT silently skip a test because the contract was unclear; do NOT peek at source.
- **Mark integration test tasks ✅ in the todo file** after all tests pass. Append results to the Progress Log.
