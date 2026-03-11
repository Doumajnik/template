+++
id = "shared/error-handling"
title = "Error Handling Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["error-handling", "exceptions", "logging"]
version = 3
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
