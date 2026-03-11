+++
id = "agents/security"
title = "Security Agent Rules"
agents = ["security"]
technologies = ["all"]
category = "rule"
tags = ["security"]
version = 2
+++

### Security Guidelines

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
