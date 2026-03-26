---
name: security-hardening
description: "Full security audit and hardening workflow covering OWASP Top 10, dependency scanning, secrets management, and infrastructure security. Use when auditing security, hardening an application, or responding to vulnerability reports. Triggers on: security, harden, vulnerability, OWASP, audit, CVE, penetration."
---

# Security Hardening Skill

Full security audit and hardening pipeline. Covers threat modeling, OWASP Top 10 compliance, dependency scanning, secrets management, auth review, input validation, infrastructure hardening, and verified remediation.

## References

- [OWASP Top 10 Checklist](./references/owasp-checklist.md) — all OWASP Top 10 2021 items with check procedures
- [Security Headers Reference](./references/security-headers.md) — HTTP security header recommendations and common mistakes

## Pipeline

### Phase 1: Threat Modeling

Identify the application's attack surface before auditing code.

1. Map all **entry points** — HTTP endpoints, WebSocket handlers, CLI commands, message consumers, file upload paths
2. Identify **trust boundaries** — where untrusted data crosses into trusted zones (user input → server, server → database, service → service)
3. Document **data flows** — trace sensitive data (credentials, PII, tokens, payment info) from ingress to storage to egress
4. Enumerate **threat actors** — anonymous users, authenticated users, internal services, supply chain (dependencies), infrastructure operators
5. Classify assets by sensitivity — public, internal, confidential, restricted
6. Produce a **threat model summary**: entry points, trust boundaries, data classification, and identified risks ranked by likelihood × impact

### Phase 2: OWASP Top 10 Audit

Systematically check every OWASP Top 10 2021 category against the codebase. Use the full checklist in [references/owasp-checklist.md](./references/owasp-checklist.md).

1. For each of the 10 categories (A01–A10), check every item in the checklist
2. For each finding, record: category, file, line, severity (CRITICAL/HIGH/MEDIUM/LOW), description, and recommended fix
3. Cross-reference with the threat model — findings on high-sensitivity data flows escalate one severity level
4. Flag any category with zero findings as "reviewed — no issues found" (not "skipped")
5. Append all findings to `docs/SECURITY_REPORT.md`

### Phase 3: Dependency Scanning

Audit all direct and transitive dependencies for known vulnerabilities.

1. Identify the package manager(s) in use (npm, pip, cargo, go modules, NuGet, Maven, etc.)
2. Run or simulate a dependency audit — check for known CVEs in all dependencies
3. Flag **outdated packages** — any dependency more than 2 major versions behind or with known CVEs
4. Check **license compliance** — flag copyleft licenses (GPL, AGPL) in proprietary projects, flag unknown licenses
5. Identify **unused dependencies** — installed but never imported
6. Record findings with: package name, current version, latest version, CVE IDs (if any), severity, and recommended action (update/replace/remove)

### Phase 4: Secrets Audit

Scan for hardcoded secrets and verify secrets management practices.

1. Search the entire codebase for **hardcoded secrets** — API keys, passwords, tokens, connection strings, private keys, JWTs
2. Check patterns: `password=`, `secret=`, `api_key=`, `token=`, `-----BEGIN`, base64-encoded strings in source, `.env` files committed to git
3. Verify `.gitignore` includes: `.env`, `.env.*`, `*.pem`, `*.key`, secrets directories
4. Check git history for previously committed secrets (even if currently removed)
5. Verify secrets are loaded from environment variables or a secrets manager — never from source code
6. Check secret rotation policies — are there expiration dates, rotation mechanisms, or revocation procedures?
7. Flag any finding as **CRITICAL** — hardcoded secrets are always critical severity

### Phase 5: Authentication & Authorization

Audit auth flows, session management, and access control.

1. Review **authentication mechanisms** — password hashing algorithm (bcrypt/argon2/scrypt, NOT MD5/SHA1), multi-factor auth support, account lockout after failed attempts
2. Check **session management** — secure cookie flags (HttpOnly, Secure, SameSite), session expiration, session invalidation on logout, token rotation
3. Audit **authorization** — verify access control checks on every protected endpoint, check for IDOR vulnerabilities, verify RBAC/ABAC implementation
4. Check **password policies** — minimum length (≥12), complexity requirements, breach database checking
5. Review **JWT handling** (if applicable) — algorithm validation (reject `none`), expiration enforcement, audience/issuer validation, key management
6. Verify **OAuth/OIDC flows** (if applicable) — state parameter usage, PKCE for public clients, redirect URI validation

### Phase 6: Input Validation

Check all user input paths for proper sanitization and injection prevention.

1. Trace every path where user input enters the system (request params, headers, body, file uploads, URL paths)
2. Check for **SQL injection** — verify parameterized queries or ORM usage everywhere, no string concatenation in queries
3. Check for **XSS** — verify output encoding in templates, CSP headers, no `innerHTML`/`dangerouslySetInnerHTML` with user data
4. Check for **command injection** — verify no shell command construction with user input, use parameterized APIs
5. Check for **path traversal** — verify file path inputs are sanitized, no `../` sequences reach the filesystem
6. Check for **SSRF** — verify URL inputs are validated against allowlists, no internal network access from user-supplied URLs
7. Verify **file upload** security — type validation (not just extension), size limits, storage outside webroot, filename sanitization
8. Check for **mass assignment** — verify request body fields are explicitly allowlisted, not blindly bound to models

### Phase 7: Infrastructure Security

Audit HTTP headers, TLS configuration, CORS policy, and rate limiting.

1. Check all **security headers** per [references/security-headers.md](./references/security-headers.md) — CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, COEP, COOP, CORP
2. Verify **TLS configuration** — TLS 1.2+ only, strong cipher suites, HSTS with `includeSubDomains` and `preload`
3. Audit **CORS policy** — no wildcard (`*`) origins in production, credentials mode properly configured, allowed methods/headers restricted
4. Check **rate limiting** — authentication endpoints, API endpoints, file upload endpoints, password reset
5. Verify **error handling** — no stack traces or internal details in production error responses, generic error messages for auth failures
6. Check **logging** — security events logged (failed auth, access denied, input validation failures), no sensitive data in logs (passwords, tokens, PII)
7. Verify **cookie security** — Secure flag, HttpOnly flag, SameSite attribute, appropriate domain/path scope

### Phase 8: Remediation Plan

Prioritize all findings and create an actionable fix list.

1. Aggregate all findings from Phases 2–7
2. Deduplicate — merge findings that share the same root cause
3. Assign final severity: **CRITICAL** (actively exploitable, data breach risk), **HIGH** (exploitable with effort), **MEDIUM** (defense-in-depth gap), **LOW** (best practice improvement)
4. Sort by severity, then by blast radius (number of affected endpoints/files)
5. For each finding, provide:
   - One-line description
   - Affected file(s) and line(s)
   - Specific remediation steps (code-level, not generic advice)
   - Estimated effort (trivial/small/medium/large)
6. Group into implementation batches: Batch 1 = all CRITICAL, Batch 2 = all HIGH, Batch 3 = MEDIUM + LOW
7. Write the plan to `docs/SECURITY_REPORT.md` under a `## Remediation Plan` section

### Phase 9: Verification

Re-scan after fixes to confirm resolution.

1. After Workers implement fixes from the remediation plan, re-run the relevant audit phases
2. For each fixed finding, verify:
   - The specific vulnerability is no longer present
   - The fix did not introduce new vulnerabilities
   - Existing tests still pass (no regressions)
3. Update `docs/SECURITY_REPORT.md` — mark resolved findings as ✅, note verification date
4. Any finding that persists after a fix attempt escalates one severity level
5. Produce a **verification summary**: total findings, resolved, remaining, new (if any)

## Severity Definitions

| Severity | Definition | SLA |
|----------|-----------|-----|
| **CRITICAL** | Actively exploitable, immediate data breach or system compromise risk | Fix before merge |
| **HIGH** | Exploitable with moderate effort or insider knowledge | Fix within current sprint |
| **MEDIUM** | Defense-in-depth gap, requires chained vulnerabilities to exploit | Fix within next sprint |
| **LOW** | Best practice improvement, minimal direct risk | Track in backlog |

## Output

All findings are appended to `docs/SECURITY_REPORT.md` using the project's report template format. The Security Agent owns this file. Each audit session adds a dated section with findings, remediation plan, and verification status.
