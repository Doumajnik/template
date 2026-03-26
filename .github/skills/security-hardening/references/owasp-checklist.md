# OWASP Top 10 2021 — Audit Checklist

Systematic checklist for auditing a codebase against every OWASP Top 10 2021 category. For each item, check whether the vulnerability exists, document findings with file/line references, and apply the remediation pattern.

---

## A01: Broken Access Control

**What to check:**

- [ ] Every protected endpoint enforces authentication before processing
- [ ] Authorization checks verify the requesting user has permission for the specific resource (not just "is logged in")
- [ ] No Insecure Direct Object References (IDOR) — users cannot access other users' data by changing IDs in URLs/params
- [ ] Directory listing is disabled on web servers
- [ ] API endpoints enforce access control for CRUD operations consistently
- [ ] CORS policy does not allow unauthorized origins to access protected resources
- [ ] JWT/session tokens cannot be reused after logout (server-side invalidation)
- [ ] Rate limiting is applied to prevent brute-force access attempts
- [ ] Admin functionality is separated and protected with elevated authorization

**Common vulnerabilities:** Missing auth middleware on new endpoints, relying on client-side checks only, IDOR via predictable IDs, elevation of privilege via parameter tampering.

**Remediation:** Deny by default — require explicit authorization on every endpoint. Use framework middleware/decorators. Validate resource ownership server-side. Use UUIDs instead of sequential IDs for external references.

---

## A02: Cryptographic Failures

**What to check:**

- [ ] No sensitive data transmitted in cleartext (HTTP, FTP, SMTP without TLS)
- [ ] Passwords are hashed with bcrypt, argon2, or scrypt — never MD5, SHA1, or plain SHA256
- [ ] Encryption keys are not hardcoded in source — loaded from environment or key management service
- [ ] TLS 1.2+ enforced for all connections — TLS 1.0/1.1 disabled
- [ ] Sensitive data at rest is encrypted (database fields, file storage, backups)
- [ ] No deprecated or weak cryptographic algorithms in use (DES, 3DES, RC4, MD5 for integrity)
- [ ] Random number generation uses cryptographically secure sources (not `Math.random()` or `random.random()`)
- [ ] Sensitive data is not included in URLs, logs, or error messages

**Common vulnerabilities:** Passwords stored as plain hashes, API keys in source code, sensitive data in URL query parameters, using base64 as "encryption."

**Remediation:** Use established crypto libraries — never roll your own. Store secrets in environment variables or a secrets manager. Hash passwords with adaptive algorithms. Encrypt sensitive fields at rest. Enforce TLS everywhere.

---

## A03: Injection

**What to check:**

- [ ] All SQL queries use parameterized statements or ORM — no string concatenation with user input
- [ ] NoSQL queries sanitize user input and avoid operator injection (`$gt`, `$ne`, etc.)
- [ ] OS commands are never constructed from user input — if unavoidable, use allowlists and parameterized APIs
- [ ] LDAP queries sanitize special characters from user input
- [ ] Template engines auto-escape output by default — manual `safe`/`raw` usage is reviewed
- [ ] XSS prevention: user-supplied content is encoded before rendering in HTML, JavaScript, CSS, or URL contexts
- [ ] Email header injection is prevented — CRLF sequences are stripped from user input in email fields
- [ ] XML parsers disable external entity processing (XXE prevention)

**Common vulnerabilities:** String-interpolated SQL, `eval()` with user input, shell exec with unsanitized args, `innerHTML` with user data, XXE in XML parsers.

**Remediation:** Parameterize all queries. Use ORM methods. Escape output contextually. Disable external entities in XML parsers. Never use `eval()`, `exec()`, or `Function()` with user-controlled strings.

---

## A04: Insecure Design

**What to check:**

- [ ] Business logic has abuse-case protections (e.g., can a coupon be applied twice? Can a user skip payment steps?)
- [ ] Rate limiting exists on expensive operations (account creation, password reset, file generation)
- [ ] Multi-step workflows validate state at each step — users cannot skip or reorder steps
- [ ] Trust boundaries are documented — the system does not trust client-side validation alone
- [ ] Sensitive operations require re-authentication (password change, email change, account deletion)
- [ ] Resource limits are enforced (file upload size, API response pagination, batch operation limits)

**Common vulnerabilities:** Unlimited resource consumption, business logic bypass, missing server-side validation that mirrors client-side, no rate limiting on auth endpoints.

**Remediation:** Threat model during design. Implement server-side validation for all business rules. Add rate limiting. Require re-authentication for sensitive operations. Design with abuse cases in mind.

---

## A05: Security Misconfiguration

**What to check:**

- [ ] Default credentials are changed or removed (database, admin panels, API keys)
- [ ] Debug mode is disabled in production (Django `DEBUG=True`, Express `stack traces`, etc.)
- [ ] Unnecessary features, ports, services, and pages are disabled or removed
- [ ] Error messages do not reveal stack traces, database details, or internal paths in production
- [ ] Security headers are set (see [security-headers.md](./security-headers.md))
- [ ] Directory listing is disabled
- [ ] Cloud storage permissions are restrictive — no public S3 buckets or equivalent
- [ ] Framework and server software is up to date with security patches

**Common vulnerabilities:** Debug mode in production, default admin credentials, verbose error pages, open cloud storage, missing security headers, unnecessary HTTP methods enabled.

**Remediation:** Automate configuration hardening. Use environment-specific configs. Disable debug in production. Set all security headers. Review cloud IAM policies. Run periodic configuration scans.

---

## A06: Vulnerable and Outdated Components

**What to check:**

- [ ] All dependencies (direct and transitive) are scanned for known CVEs
- [ ] No dependencies are more than 2 major versions behind the latest release
- [ ] Unused dependencies are removed from the project
- [ ] Dependency lock files exist and are committed (`package-lock.json`, `poetry.lock`, `Cargo.lock`, etc.)
- [ ] A dependency update policy exists — automated or scheduled manual review
- [ ] Components from untrusted or unmaintained sources are flagged for replacement
- [ ] License compliance is verified — no copyleft licenses in proprietary code without legal review

**Common vulnerabilities:** Known CVEs in outdated packages, typosquatting attacks, abandoned libraries with unpatched bugs, dependency confusion.

**Remediation:** Run `npm audit` / `pip audit` / `cargo audit` / equivalent regularly. Pin dependency versions. Remove unused packages. Set up automated dependency update PRs (Dependabot, Renovate). Verify package integrity via checksums.

---

## A07: Identification and Authentication Failures

**What to check:**

- [ ] Passwords require minimum 12 characters with complexity or passphrase support
- [ ] Brute-force protection exists — account lockout or exponential backoff after failed attempts
- [ ] Multi-factor authentication is available for sensitive accounts
- [ ] Session tokens are invalidated on logout (server-side, not just client-side cookie removal)
- [ ] Session IDs are regenerated after login to prevent session fixation
- [ ] Password recovery does not reveal whether an account exists ("If an account exists, we sent an email")
- [ ] Credential stuffing protections exist — rate limiting, CAPTCHA, or breach database checking
- [ ] Default or well-known credentials are not accepted

**Common vulnerabilities:** Weak password policies, no brute-force protection, session fixation, credential stuffing, user enumeration via error messages, missing MFA.

**Remediation:** Enforce strong passwords. Implement account lockout with exponential backoff. Add MFA. Regenerate session IDs on auth state change. Use generic error messages for auth failures. Check passwords against breach databases.

---

## A08: Software and Data Integrity Failures

**What to check:**

- [ ] CI/CD pipeline has integrity checks — signed commits, protected branches, required reviews
- [ ] Dependencies are verified via checksums or signatures — no `--no-verify` flags in install scripts
- [ ] Deserialization of untrusted data is avoided — if required, type-constrained and validated
- [ ] Auto-update mechanisms verify signatures before applying updates
- [ ] Database migrations are reviewed before execution — no auto-migration in production without approval
- [ ] Code signing is used for release artifacts where applicable

**Common vulnerabilities:** Insecure deserialization (pickle, Java serialization, YAML.load), unsigned dependencies, unprotected CI/CD pipelines, auto-migration of unreviewed schemas.

**Remediation:** Verify integrity of all dependencies and artifacts. Avoid native deserialization of untrusted data — use safe alternatives (JSON, protocol buffers). Protect CI/CD pipelines with required reviews and signed commits. Use `yaml.safe_load()` instead of `yaml.load()`.

---

## A09: Security Logging and Monitoring Failures

**What to check:**

- [ ] Failed authentication attempts are logged with timestamp, IP, and username (not password)
- [ ] Access control failures (403s) are logged
- [ ] Input validation failures are logged (potential injection attempts)
- [ ] Logs do NOT contain sensitive data (passwords, tokens, PII, credit card numbers)
- [ ] Log integrity is protected — logs stored in append-only or immutable storage
- [ ] Alerting exists for high-frequency auth failures, unusual access patterns, or error spikes
- [ ] Logs include enough context for incident investigation (request ID, user ID, action, outcome)

**Common vulnerabilities:** No logging of security events, sensitive data in logs, logs easily tampered with, no alerting on suspicious patterns, insufficient log retention.

**Remediation:** Log all security-relevant events. Strip sensitive data from log entries. Use structured logging. Set up alerts for anomalous patterns. Retain logs for incident investigation (minimum 90 days). Centralize logs in tamper-evident storage.

---

## A10: Server-Side Request Forgery (SSRF)

**What to check:**

- [ ] User-supplied URLs are validated against an allowlist of permitted domains/IPs
- [ ] Internal network addresses are blocked (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.169.254)
- [ ] URL redirects do not follow unvalidated user-supplied destinations
- [ ] DNS rebinding protections exist — resolve and validate the IP, not just the hostname
- [ ] Cloud metadata endpoints are blocked (169.254.169.254, metadata.google.internal, etc.)
- [ ] File URL schemes (`file://`, `gopher://`, `dict://`) are blocked in user-supplied URLs

**Common vulnerabilities:** Fetching user-supplied URLs without validation, accessing cloud metadata via SSRF, DNS rebinding to bypass hostname allowlists, open redirects chained with SSRF.

**Remediation:** Allowlist permitted domains and IP ranges. Block all private/reserved IP ranges. Resolve DNS and validate the resulting IP before connecting. Disable unnecessary URL schemes. Use network-level segmentation to limit server outbound access.
