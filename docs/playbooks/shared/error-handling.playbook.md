+++
id = "shared/error-handling"
title = "Error Handling Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["error-handling", "exceptions", "logging"]
version = 5
+++

### Error Handling

- Never use bare `except:` — always catch specific exception types
- Never silently swallow exceptions. At minimum, log the error with context
- Raise early, catch late — validate inputs at function boundaries, handle errors at the outermost level
- Use custom exception classes when built-in types are insufficient (inherit from Exception, name ends in Error)
- Include context in error messages: what failed, what value caused it, what was expected
- Never catch Exception to suppress errors — only to log-and-reraise or to add context
- Use `finally` or context managers (`with`) for resource cleanup — never rely on garbage collection
- Don't use exceptions for control flow — exceptions are for exceptional cases only
- When retrying operations, use exponential backoff and set a maximum retry count
- Log stack traces at ERROR level. Log expected/handled errors at WARNING or INFO
- In scripts, distinguish between user errors (clear message, exit code 1) and bugs (full traceback)
- Never use `assert` for input validation — asserts can be stripped in production
- Use structured logging (JSON) in production — include request ID, user ID, and operation name in error context
- Define error codes for API errors — clients should never parse error message strings to determine error type
- Transient errors (network, timeout, 503) should be retryable. Permanent errors (400, 404, validation) should not
- Circuit breakers: after N consecutive failures to an external service, fail fast for a cooldown period
- Validate all external input at system boundaries — never trust data from users, APIs, or files
- When wrapping errors, preserve the original error as the cause — don't discard the root cause
- HTTP error responses must include: error code, human-readable message, and request ID for debugging
- Log enough context to reproduce the error: input parameters, state, and the full exception chain
- Use dead-letter queues for failed async operations — never silently drop messages
- Timeout all external calls — never make a network request without a timeout
- Application startup must validate all required configuration and fail fast with a clear message if anything is missing
- Always clean up partial state on error — if step 3 of 5 fails, undo steps 1-2 or use transactions
- Apply the Bulkhead pattern: isolate critical resources (thread pools, connection pools, memory) into separate pools so one failing component cannot exhaust resources for others (Azure Architecture Patterns, Bulkhead)
- Implement Compensating Transactions: for multi-step distributed operations that cannot use ACID transactions, define explicit undo/compensation logic for each step to maintain consistency on failure (Azure Architecture Patterns, Compensating Transaction)
- Expose health check endpoints that verify connectivity to all dependencies (database, cache, external APIs) — return degraded status if any dependency is unhealthy (Azure Architecture Patterns, Health Endpoint Monitoring)
- For distributed workflows spanning multiple services, use the Saga pattern with per-step compensation instead of distributed locks or two-phase commit (Azure Architecture Patterns, Saga)
- Implement rate limiting on outbound calls to downstream services — prevent your application from overwhelming dependencies during traffic spikes (Azure Architecture Patterns, Rate Limiting)
- Use an Anti-Corruption Layer when integrating with legacy or third-party systems — wrap external calls in an adapter that translates between your domain model and the external model (Azure Architecture Patterns, Anti-Corruption Layer)
- Distinguish between retriable and non-retriable errors at the call site — never retry on 400/401/403/422 (client errors), only on 408/429/500/502/503/504 (transient/server errors)
- Use idempotency keys for retried write operations: assign a unique ID to each request so the server can detect and deduplicate retried calls — this prevents double-charging, duplicate record creation, or repeated side effects (Azure Architecture Patterns, Retry — Idempotency)
- Implement poison message handling: if an async message fails processing after the maximum retry count, move it to a dead-letter queue with full context (original message, error details, retry count, timestamps) — never silently discard or endlessly retry a failing message
- Avoid nested retry policies: if a high-level task wraps a low-level task that also has retry logic, the total wait time multiplies unpredictably — configure the inner task to fail fast and let the outer task manage retries with its own policy (Azure Architecture Patterns, Retry — General Guidance)
- Propagate correlation IDs through the entire request chain: assign a unique request ID at the entry point and include it in every log entry, error response, and inter-service call — this enables end-to-end tracing of failures across distributed systems
- Implement graceful degradation: when a non-critical dependency fails, return a degraded response rather than failing the entire request — use fallback values, cached data, or feature flags to maintain partial functionality
- Aggregate related errors before reporting: when processing a batch of items and multiple items fail, collect all errors and return them in a single structured response rather than failing on the first error — this gives callers actionable information to fix all issues at once
- Log early retry failures at INFO level, only the final failure at ERROR: this prevents flooding alerting systems with transient errors that self-resolve, while still capturing the ultimate failure for investigation (Azure Architecture Patterns, Retry — Logging)
