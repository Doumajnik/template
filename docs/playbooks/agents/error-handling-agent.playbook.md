+++
id = "agents/error-handling"
title = "Error Handling Agent Rules"
agents = ["error-handling"]
technologies = ["all"]
category = "rule"
tags = ["error-handling"]
version = 2
+++

### Error Handling Audit Rules

1. Scan for bare `except:` or `catch(Exception)` blocks that silently swallow errors.
2. Flag empty `except`/`catch` blocks — every error must be at minimum logged.
3. Check for missing error context: error messages should include what failed, what input caused it, and what to do.
4. Verify that resource cleanup happens in `finally`/`defer`/`using` blocks — not in the happy path only.
5. Flag try/catch blocks that are too broad — catching around 50+ lines suggests the error handling is not specific enough.
6. Check for inconsistent error handling: similar operations should handle errors the same way.
7. Verify that async errors are properly caught — uncaught promise rejections and unhandled task exceptions.
8. Flag error handling anti-patterns: catch-log-rethrow without adding context, catching then returning null.
9. Check that HTTP error responses have proper status codes — not 200 with `{ "error": "..." }` in the body.
10. Verify that retryable operations have retry logic and non-retryable operations fail immediately.
11. Produce a report with: file, line, pattern found, severity (CRITICAL/HIGH/MEDIUM/LOW), recommended fix.
12. CRITICAL findings (swallowed exceptions in critical paths) must be fixed immediately.
