+++
id = "agents/security"
title = "Security Agent Rules"
agents = ["security"]
technologies = ["all"]
category = "rule"
tags = ["security"]
version = 5
+++

### Security Guidelines

- **Use `docs/SECURITY_CHECKLIST.md` as the authoritative checklist** — check every item against every source file in the project
- **Audit in batches** — process source files in batches of 3-5 files at a time, running ALL checklist items against each file
- **Address every checklist category** in the report — even if the result is "PASS: no issues found" for a file
- **Produce a per-file coverage matrix** showing which checklist sections were checked for each source file
- Audit all user input paths for injection vulnerabilities: SQL injection, XSS, command injection, path traversal
- Check all authentication and authorization flows — verify tokens are validated, sessions expire, and permissions are checked
- Verify secrets management: no hardcoded secrets in source, `.env` in `.gitignore`, env vars for all sensitive values
- Check HTTPS enforcement — all external API calls must use HTTPS, never HTTP
- Verify CORS configuration — only expected origins should be allowed, never wildcard (`*`) in production
- Check for sensitive data exposure: PII in logs, credentials in error messages, secrets in URL parameters
- Verify dependency security — check for known CVEs in all dependencies
- Check rate limiting on authentication endpoints and public APIs
- Verify input validation at all system boundaries — never trust data from users, APIs, or file uploads
- Check for IDOR (Insecure Direct Object Reference) — verify users can only access their own resources
- Write findings to `docs/SECURITY_REPORT.md` with severity levels: CRITICAL, HIGH, MEDIUM, LOW
- CRITICAL and HIGH findings must be fixed before release — spawn Workers to fix them
- Verify CSRF protection on state-changing endpoints
- Check for insecure design patterns — verify that security controls (AuthN, AuthZ, input validation) are designed into the architecture from the start, not bolted on afterward (OWASP A04: Insecure Design)
- Verify software and data integrity — ensure CI/CD pipelines validate code integrity, dependencies come from trusted sources, and deserialization of untrusted data is prevented or strictly validated (OWASP A08)
- Audit security logging and monitoring — verify that login attempts, access control failures, and server-side validation errors are logged with sufficient context (user, IP, timestamp) for forensic analysis and alerting (OWASP A09)
- Check for Server-Side Request Forgery (SSRF) — verify that server-side HTTP requests validate and sanitize user-supplied URLs, block access to internal networks and cloud metadata endpoints (169.254.169.254) (OWASP A10)
- Verify security misconfiguration defaults — ensure unnecessary features/services are disabled, default credentials are changed, error handling doesn't reveal stack traces to users, and security headers (CSP, HSTS, X-Content-Type-Options) are set (OWASP A05)
- Check for cryptographic failures — verify sensitive data is encrypted at rest and in transit, strong algorithms are used (no MD5/SHA1 for password hashing), keys are rotated and managed securely, and deprecated TLS versions are disabled (OWASP A02)
- **Never skip files** — every file in `src/`, `scripts/`, and config directories must be audited
- **Never skip checklist items** — every section of the security checklist must be checked
- **Cross-file checks** — after all individual files are done, check for project-wide concerns: dependency vulnerabilities, configuration consistency, secrets exposure across the codebase
- Also audit non-source files: CI/CD workflows, scripts, config files, Docker files, `.gitignore`, package manifests
- Enforce allowlist (whitelist) validation over denylist (blacklist) — define exactly what IS authorized input and reject everything else; denylist filters are trivially bypassed by encoding tricks and novel attack vectors (OWASP Input Validation Cheat Sheet)
- Require both syntactic and semantic input validation — syntactic validation enforces correct format (e.g., date format, email structure), while semantic validation enforces business correctness (e.g., start date before end date, price within expected range); both are necessary
- Mandate server-side validation for all inputs regardless of client-side checks — client-side JavaScript validation can be bypassed by disabling JavaScript or using a proxy; server-side validation is the security control, client-side is only for UX
- Validate file uploads rigorously — verify file extension against an allowlist, enforce maximum file size, rename uploaded files with random server-generated names, validate content type matches the actual file content, and scan for malicious content; never trust user-supplied filenames or paths
- Audit regular expressions for ReDoS (Regular Expression Denial of Service) — poorly designed regex patterns with nested quantifiers can be exploited to cause catastrophic backtracking; verify all validation regex complete in bounded time with adversarial input
- Normalize Unicode input before validation — apply canonical encoding normalization (NFC/NFKC) before validating free-form text to prevent bypass via equivalent Unicode representations; validate against Unicode character categories rather than individual character ranges
