+++
id = "agents/error-handling"
title = "Error Handling Agent Rules"
agents = ["error-handling"]
technologies = ["all"]
category = "rule"
tags = ["error-handling"]
version = 5
+++

> General error handling rules are in `shared/error-handling.playbook.md`. This playbook covers **audit-specific** patterns unique to the Error Handling Agent.

### Error Handling Audit Rules

- Check for inconsistent error handling: similar operations should handle errors the same way.
- Verify that async errors are properly caught — uncaught promise rejections and unhandled task exceptions.
- Flag error handling anti-patterns: catch-log-rethrow without adding context, catching then returning null.
- Produce a report with: file, line, pattern found, severity (CRITICAL/HIGH/MEDIUM/LOW), recommended fix.
- CRITICAL findings (swallowed exceptions in critical paths) must be fixed immediately.
- Check that custom exceptions are named after the problem, not the thrower — e.g., `InsufficientFundsError` not `AccountServiceError`.
- Verify exceptions are converted at layer boundaries — low-level exceptions (I/O, SQL) must be translated to domain-appropriate exceptions before crossing module boundaries.
- Verify error messages and responses do not leak sensitive information — no stack traces, internal file paths, database queries, or credentials in user-facing errors.
- Flag error handling that violates the single responsibility principle — methods should not handle errors for data or operations they don't own (feature-envy error handling).
- Implement a global error handler (middleware or filter) that intercepts all unhandled exceptions and returns a generic, safe response to clients — never let framework default error pages reach production (OWASP Error Handling Cheat Sheet).
- Use RFC 7807 Problem Details format (`application/problem+json`) for all API error responses — include `type`, `title`, `status`, and `detail` fields for machine-readable, standardized error communication.
- Differentiate error detail levels by environment: development mode may show stack traces and debug info; production mode must return only generic messages with a correlation ID for server-side log lookup.
- Verify error responses use correct 4xx vs 5xx status codes — 4xx for client mistakes (bad input, unauthorized), 5xx for server failures (unhandled bugs, downstream outages); never return 200 with an error body.
- Flag error messages that reveal technology stack details — framework names, versions, library paths, SQL dialects, or internal IP addresses in error responses are information disclosure vulnerabilities (OWASP reconnaissance risk).
