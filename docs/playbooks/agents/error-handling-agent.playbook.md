+++
id = "agents/error-handling"
title = "Error Handling Agent Rules"
agents = ["error-handling"]
technologies = ["all"]
category = "rule"
tags = ["error-handling"]
version = 4
+++

### Error Handling Audit Rules

- Scan for bare `except:` or `catch(Exception)` blocks that silently swallow errors.
- Flag empty `except`/`catch` blocks — every error must be at minimum logged.
- Check for missing error context: error messages should include what failed, what input caused it, and what to do.
- Verify that resource cleanup happens in `finally`/`defer`/`using` blocks — not in the happy path only.
- Flag try/catch blocks that are too broad — catching around 50+ lines suggests the error handling is not specific enough.
- Check for inconsistent error handling: similar operations should handle errors the same way.
- Verify that async errors are properly caught — uncaught promise rejections and unhandled task exceptions.
- Flag error handling anti-patterns: catch-log-rethrow without adding context, catching then returning null.
- Check that HTTP error responses have proper status codes — not 200 with `{ "error": "..." }` in the body.
- Verify that retryable operations have retry logic and non-retryable operations fail immediately.
- Produce a report with: file, line, pattern found, severity (CRITICAL/HIGH/MEDIUM/LOW), recommended fix.
- CRITICAL findings (swallowed exceptions in critical paths) must be fixed immediately.
- Flag exceptions used for flow control — exceptions are for exceptional conditions, not normal branching logic (e.g., don't use `StopIteration`-style patterns for regular loops).
- Check that custom exceptions are named after the problem, not the thrower — e.g., `InsufficientFundsError` not `AccountServiceError`.
- Verify exceptions are converted at layer boundaries — low-level exceptions (I/O, SQL) must be translated to domain-appropriate exceptions before crossing module boundaries.
- Flag catch-and-rethrow without added context — if no meaningful recovery or context enrichment happens, let the exception propagate naturally.
- Check for missing circuit breaker patterns on external service calls — repeated failures should trip a breaker to prevent cascading failures and resource exhaustion.
- Verify error messages and responses do not leak sensitive information — no stack traces, internal file paths, database queries, or credentials in user-facing errors.
- Flag error handling that violates the single responsibility principle — methods should not handle errors for data or operations they don't own (feature-envy error handling).
- Implement a global error handler (middleware or filter) that intercepts all unhandled exceptions and returns a generic, safe response to clients — never let framework default error pages reach production (OWASP Error Handling Cheat Sheet).
- Use RFC 7807 Problem Details format (`application/problem+json`) for all API error responses — include `type`, `title`, `status`, and `detail` fields for machine-readable, standardized error communication.
- Differentiate error detail levels by environment: development mode may show stack traces and debug info; production mode must return only generic messages with a correlation ID for server-side log lookup.
- Verify error responses use correct 4xx vs 5xx status codes — 4xx for client mistakes (bad input, unauthorized), 5xx for server failures (unhandled bugs, downstream outages); never return 200 with an error body.
- Flag error messages that reveal technology stack details — framework names, versions, library paths, SQL dialects, or internal IP addresses in error responses are information disclosure vulnerabilities (OWASP reconnaissance risk).
- Ensure all error handlers include centralized logging that captures full exception details (stack trace, request context, user ID, timestamp) server-side while returning only a safe correlation ID to the client.
