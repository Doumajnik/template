# Security Checklist

> This is the authoritative security checklist for the project. The Security Agent MUST check every item in this list against every source file in the project. Items are organized by category with specific, testable checks.
>
> **Usage:** The Security Agent processes this checklist in batches, auditing all source files against each section. Every item must be addressed in the security report — either as a finding or as "PASS" for the file.
>
> **Sources:** OWASP Top 10 (2021), OWASP Cheat Sheet Series, OWASP Web Security Testing Guide (WSTG v4.2), CWE database.

## How to Use This Checklist

- `[ ]` means not yet checked
- `[x]` means checked and passing
- Each item should be checked against EVERY source file in `src/`
- Findings go in `docs/SECURITY_REPORT.md` with severity (CRITICAL / HIGH / MEDIUM / LOW / INFO) and file/line references
- Items marked with regex patterns should be searched using those patterns across all source files
- When an item is not applicable to a file, mark it PASS with note "N/A"

---

## 1. OWASP A01 — Broken Access Control

> CWEs: CWE-200, CWE-201, CWE-352, CWE-22, CWE-284, CWE-285, CWE-639, CWE-862, CWE-863, CWE-913

- [ ] **A01-01** Verify all endpoints enforce access control checks — no endpoint is accessible without authorization unless explicitly public
- [ ] **A01-02** Verify deny-by-default policy — access is denied unless explicitly granted for a specific role/capability
- [ ] **A01-03** Check for Insecure Direct Object References (IDOR) — verify user-supplied IDs (e.g., `?id=123`, `?acct=456`) are validated against the authenticated user's permissions before use
- [ ] **A01-04** Verify access control checks cannot be bypassed by modifying URL parameters, request body, or HTTP headers
- [ ] **A01-05** Verify API endpoints enforce access controls for POST, PUT, PATCH, and DELETE methods — not just GET
- [ ] **A01-06** Check for missing function-level access control — verify admin/privileged endpoints require appropriate roles
- [ ] **A01-07** Verify no elevation of privilege — users cannot act as admins, and unauthenticated users cannot act as authenticated users
- [ ] **A01-08** Check for CORS misconfiguration — verify `Access-Control-Allow-Origin` is not set to `*` or reflects arbitrary origins for authenticated endpoints
- [ ] **A01-09** Verify JWT tokens are validated (signature, expiration, issuer, audience) before granting access
- [ ] **A01-10** Check that stateful session identifiers are invalidated server-side on logout
- [ ] **A01-11** Verify JWT tokens are short-lived (< 15 minutes recommended) and refresh tokens are properly managed
- [ ] **A01-12** Check for forced browsing — verify unauthenticated users cannot access authenticated pages by direct URL
- [ ] **A01-13** Verify metadata/token tampering is prevented — JWTs, cookies, hidden fields cannot be modified to escalate privileges
- [ ] **A01-14** Check for path traversal vulnerabilities — search for `../`, `..\\`, `%2e%2e%2f`, `%2e%2e/` in file path handling
- [ ] **A01-15** Verify web server directory listing is disabled
- [ ] **A01-16** Verify `.git`, `.env`, backup files, and metadata files are not accessible from web roots
- [ ] **A01-17** Verify access control failures are logged with sufficient detail for forensics
- [ ] **A01-18** Verify rate limiting is applied to API and controller endpoints
- [ ] **A01-19** Check for Cross-Site Request Forgery (CSRF) — verify anti-CSRF tokens are present on state-changing operations
- [ ] **A01-20** Verify record-level ownership — access control enforces that users can only access their own records unless authorized

---

## 2. OWASP A02 — Cryptographic Failures

> CWEs: CWE-259, CWE-327, CWE-331, CWE-321, CWE-319, CWE-326, CWE-328, CWE-330, CWE-338, CWE-916

- [ ] **A02-01** Scan for hardcoded passwords — regex: `password\s*=\s*['"][^'"]+['"]`, `passwd\s*=`, `pwd\s*=\s*['"]`
- [ ] **A02-02** Scan for hardcoded API keys — regex: `api_key\s*=\s*['"]`, `apikey\s*=`, `api[-_]?secret`
- [ ] **A02-03** Scan for hardcoded tokens — regex: `token\s*=\s*['"][A-Za-z0-9+/=]+['"]`, `bearer\s+[A-Za-z0-9._-]+`
- [ ] **A02-04** Scan for hardcoded connection strings — regex: `(mongodb|postgres|mysql|redis|amqp):\/\/[^@]+@`
- [ ] **A02-05** Scan for hardcoded cryptographic keys — regex: `(secret|private)[-_]?key\s*=\s*['"]`, `-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----`
- [ ] **A02-06** Scan for hardcoded AWS credentials — regex: `AKIA[0-9A-Z]{16}`, `aws[-_]?(secret[-_]?access[-_]?key|access[-_]?key[-_]?id)\s*=`
- [ ] **A02-07** Verify no data is transmitted in cleartext — check for `http://` URLs (not `https://`) in API calls and configuration
- [ ] **A02-08** Verify deprecated hash functions are not used — scan for: `md5(`, `hashlib.md5`, `SHA1(`, `hashlib.sha1`, `Digest::MD5`, `createHash('md5')`, `createHash('sha1')`
- [ ] **A02-09** Verify passwords are hashed with strong adaptive algorithms — check for: `bcrypt`, `argon2`, `scrypt`, `pbkdf2` usage (not plain SHA-256/SHA-512)
- [ ] **A02-10** Verify password hashes use salts — check that password hashing includes per-user salts
- [ ] **A02-11** Verify no use of deprecated cryptographic algorithms — scan for: `DES`, `3DES`, `RC4`, `RC2`, `Blowfish` (for encryption), `ECB` mode
- [ ] **A02-12** Verify cryptographic randomness uses CSPRNG — scan for insecure random: `Math.random()`, `random.random()`, `random.randint()`, `rand()` used for security-sensitive operations (tokens, keys, nonces)
- [ ] **A02-13** Verify `secrets` module (Python) or `crypto.randomBytes` (Node.js) is used for security-sensitive random values
- [ ] **A02-14** Check that encryption uses authenticated encryption modes (GCM, CCM) instead of unauthenticated modes (CBC without HMAC, ECB)
- [ ] **A02-15** Verify initialization vectors (IVs) are not reused and are generated with CSPRNG
- [ ] **A02-16** Verify TLS 1.2+ is enforced — no SSLv2, SSLv3, TLS 1.0, or TLS 1.1
- [ ] **A02-17** Verify certificate validation is not disabled — scan for: `verify=False`, `rejectUnauthorized: false`, `InsecureSkipVerify`, `CURLOPT_SSL_VERIFYPEER.*false`
- [ ] **A02-18** Verify encryption keys are not checked into source code repositories
- [ ] **A02-19** Verify sensitive data at rest is encrypted (database fields, files, backups)
- [ ] **A02-20** Verify caching is disabled for responses containing sensitive data — check for `Cache-Control: no-store` headers

---

## 3. OWASP A03 — Injection

> CWEs: CWE-79, CWE-89, CWE-78, CWE-77, CWE-94, CWE-95, CWE-74, CWE-90, CWE-643, CWE-917

### 3.1 SQL Injection

- [ ] **A03-01** Scan for SQL injection via string concatenation — regex: `(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE).*['"]\s*\+\s*`, `f".*SELECT.*{`, `f".*WHERE.*{`
- [ ] **A03-02** Verify all database queries use parameterized queries or prepared statements — no string formatting/concatenation with user input
- [ ] **A03-03** Verify ORM queries do not use raw SQL with user input — scan for `.raw(`, `.execute(` with string formatting
- [ ] **A03-04** Check for SQL injection in stored procedures — verify no dynamic SQL with user input
- [ ] **A03-05** Verify database query input is validated and typed (integers for IDs, etc.)

### 3.2 OS Command Injection

- [ ] **A03-06** Scan for dangerous command execution functions — regex: `os\.system\(`, `os\.popen\(`, `subprocess\.call\(.*shell\s*=\s*True`, `subprocess\.Popen\(.*shell\s*=\s*True`, `exec\(`, `eval\(`
- [ ] **A03-07** Scan for Node.js command injection — regex: `child_process\.exec\(`, `child_process\.execSync\(`, `child_process\.spawn\(.*shell:\s*true`
- [ ] **A03-08** Verify user input is never passed directly to shell commands
- [ ] **A03-09** Verify `subprocess` calls use argument lists (not strings with `shell=True`)
- [ ] **A03-10** Verify command arguments are properly escaped/sanitized if shell execution is unavoidable

### 3.3 Cross-Site Scripting (XSS)

- [ ] **A03-11** Scan for reflected/stored XSS — verify all user input is HTML-encoded before rendering in HTML context
- [ ] **A03-12** Scan for DOM-based XSS — regex: `\.innerHTML\s*=`, `\.outerHTML\s*=`, `document\.write\(`, `document\.writeln\(`
- [ ] **A03-13** Scan for React XSS — regex: `dangerouslySetInnerHTML`
- [ ] **A03-14** Scan for template injection — verify template engines auto-escape by default; check for `| safe`, `{% autoescape false %}`, `{!! !!}`
- [ ] **A03-15** Verify Content Security Policy (CSP) header is set to prevent inline scripts

### 3.4 Other Injection Types

- [ ] **A03-16** Scan for LDAP injection — verify LDAP queries use parameterized/escaped input
- [ ] **A03-17** Scan for XPath injection — verify XPath queries are parameterized
- [ ] **A03-18** Scan for Expression Language injection — verify EL expressions do not include user input
- [ ] **A03-19** Scan for Server-Side Template Injection (SSTI) — verify user input is not passed as template content
- [ ] **A03-20** Scan for CRLF injection — verify headers do not include unsanitized user input containing `\r\n`
- [ ] **A03-21** Scan for code injection via `eval()` / `exec()` — regex: `eval\(`, `exec\(`, `compile\(`, `new\s+Function\(`
- [ ] **A03-22** Scan for NoSQL injection — regex: `\$where`, `\$gt`, `\$ne`, `\$regex` used with unsanitized user input in MongoDB queries
- [ ] **A03-23** Scan for XML injection / XXE — regex: `<!DOCTYPE`, `<!ENTITY`, `SYSTEM\s+"`, and verify XML parsers disable external entities
- [ ] **A03-24** Scan for log injection — verify user input written to logs is sanitized (no newlines, control characters)

---

## 4. OWASP A04 — Insecure Design

> CWEs: CWE-209, CWE-256, CWE-501, CWE-522, CWE-434, CWE-840, CWE-841

- [ ] **A04-01** Verify threat modeling has been performed for critical flows (authentication, authorization, payment, data access)
- [ ] **A04-02** Verify error messages do not contain sensitive information — regex: `traceback`, `stack\s*trace`, `Exception`, `Error` messages should not expose internal paths, database details, or credentials
- [ ] **A04-03** Verify credentials are not stored in recoverable format — no plaintext or reversibly encrypted passwords
- [ ] **A04-04** Verify trust boundary violations — data crossing trust boundaries is validated and sanitized
- [ ] **A04-05** Verify file upload restrictions — type validation, size limits, name sanitization, storage outside web root
- [ ] **A04-06** Verify business logic controls are enforced server-side — not just client-side validation
- [ ] **A04-07** Verify rate limiting on resource-intensive operations (login, registration, password reset, API calls)
- [ ] **A04-08** Verify application enforces behavioral workflows — actions must follow expected sequence
- [ ] **A04-09** Verify secure design patterns are used — separation of concerns, defense in depth, principle of least privilege
- [ ] **A04-10** Verify user stories include abuse cases and security acceptance criteria
- [ ] **A04-11** Verify security controls exist at each tier (frontend, backend, database)
- [ ] **A04-12** Verify tenant isolation in multi-tenant applications
- [ ] **A04-13** Verify resource consumption limits per user/service (memory, CPU, file descriptors, connections)
- [ ] **A04-14** Verify GET requests do not trigger state changes — use POST/PUT/PATCH/DELETE for mutations
- [ ] **A04-15** Verify sensitive data is not passed via GET query parameters — check for `?password=`, `?token=`, `?secret=`

---

## 5. OWASP A05 — Security Misconfiguration

> CWEs: CWE-16, CWE-611, CWE-614, CWE-756, CWE-1004, CWE-942, CWE-315

- [ ] **A05-01** Verify debug mode is disabled in production — scan for: `DEBUG\s*=\s*True`, `debug:\s*true`, `NODE_ENV\s*!==?\s*['"]production['"]` used insecurely
- [ ] **A05-02** Verify stack traces are not returned to users in production error responses
- [ ] **A05-03** Verify default credentials are not used — scan for: `admin/admin`, `root/root`, `password`, `123456`, `default`
- [ ] **A05-04** Verify unnecessary features, services, ports, endpoints, and sample/test pages are disabled/removed in production
- [ ] **A05-05** Verify security headers are configured — check for: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`
- [ ] **A05-06** Verify `X-Content-Type-Options: nosniff` header is set
- [ ] **A05-07** Verify `X-Frame-Options: DENY` or `SAMEORIGIN` header is set (clickjacking prevention)
- [ ] **A05-08** Verify `Strict-Transport-Security` (HSTS) header is set with `max-age >= 31536000` and `includeSubDomains`
- [ ] **A05-09** Verify `Content-Security-Policy` header restricts `script-src`, `style-src`, `object-src`, and `default-src`
- [ ] **A05-10** Verify `Referrer-Policy` header is set (e.g., `strict-origin-when-cross-origin` or `no-referrer`)
- [ ] **A05-11** Verify `Permissions-Policy` header restricts browser features (camera, microphone, geolocation)
- [ ] **A05-12** Verify XML parsers disable external entity processing (XXE prevention) — check for `defusedxml` (Python), `libxml_disable_entity_loader` (PHP), `FEATURE_SECURE_PROCESSING` (Java)
- [ ] **A05-13** Verify cloud storage permissions are not overly permissive (e.g., S3 bucket not public)
- [ ] **A05-14** Verify application framework security features are enabled — auto-escaping, CSRF protection, etc.
- [ ] **A05-15** Verify no sensitive information in configuration comments or documentation committed to the repository
- [ ] **A05-16** Verify environment-specific configurations use different credentials per environment (dev, staging, production)
- [ ] **A05-17** Verify CORS is configured with a specific allowlist of origins — not `Access-Control-Allow-Origin: *` with credentials
- [ ] **A05-18** Verify `Server` and `X-Powered-By` headers are removed or genericized to prevent information disclosure
- [ ] **A05-19** Verify cookies use `Secure`, `HttpOnly`, and `SameSite` attributes appropriately
- [ ] **A05-20** Verify no sensitive data is stored in cookies in cleartext

---

## 6. OWASP A06 — Vulnerable and Outdated Components

> CWE: components with known vulnerabilities

- [ ] **A06-01** Verify all dependencies are up to date — run `npm audit`, `pip-audit`, `dotnet list package --vulnerable`, `cargo audit`
- [ ] **A06-02** Verify no dependencies have known CRITICAL or HIGH vulnerabilities
- [ ] **A06-03** Verify dependency lock files exist and are committed — `package-lock.json`, `Pipfile.lock`, `poetry.lock`, `requirements.txt` with pinned versions
- [ ] **A06-04** Verify lock file integrity — hashes match expected values
- [ ] **A06-05** Verify no deprecated or end-of-life frameworks/libraries are used
- [ ] **A06-06** Verify dependencies are from trusted sources — official registries, not typosquatted packages
- [ ] **A06-07** Verify third-party JavaScript is loaded with Subresource Integrity (SRI) hashes
- [ ] **A06-08** Verify unused dependencies are removed from the project
- [ ] **A06-09** Verify a process exists for monitoring dependency vulnerabilities (Dependabot, Snyk, Renovate)
- [ ] **A06-10** Verify components are obtained from official sources over secure links (HTTPS)
- [ ] **A06-11** Verify signed packages are preferred when available
- [ ] **A06-12** Verify components do not contain known backdoors or malicious code

---

## 7. OWASP A07 — Identification and Authentication Failures

> CWEs: CWE-287, CWE-384, CWE-256, CWE-522, CWE-307, CWE-798

- [ ] **A07-01** Verify passwords are hashed with bcrypt (cost factor ≥ 10), Argon2id, scrypt, or PBKDF2 (≥ 600,000 iterations for SHA-256)
- [ ] **A07-02** Verify passwords are never stored in plaintext, reversible encryption, or weak hashes (MD5, SHA1, SHA256 without stretching)
- [ ] **A07-03** Verify password complexity requirements — minimum 8 characters, check against breached password lists
- [ ] **A07-04** Verify account lockout or progressive delays after failed login attempts (e.g., lockout after 5–10 failures)
- [ ] **A07-05** Verify rate limiting on authentication endpoints (login, register, password reset)
- [ ] **A07-06** Verify session IDs are cryptographically random (minimum 128-bit entropy)
- [ ] **A07-07** Verify session IDs are regenerated after successful authentication (session fixation prevention)
- [ ] **A07-08** Verify sessions expire after inactivity timeout (e.g., 15–30 minutes for sensitive apps)
- [ ] **A07-09** Verify sessions are invalidated server-side on logout
- [ ] **A07-10** Verify multi-factor authentication (MFA) is available for sensitive operations
- [ ] **A07-11** Verify credential recovery does not reveal whether an account exists (generic error messages)
- [ ] **A07-12** Verify password reset tokens are single-use, time-limited (< 1 hour), and cryptographically random
- [ ] **A07-13** Verify authentication is not bypassable by parameter manipulation or forced browsing
- [ ] **A07-14** Verify hardcoded credentials do not exist — scan for: `username\s*=\s*['"]admin['"]`, `password\s*=\s*['"]`, default credentials patterns
- [ ] **A07-15** Verify JWT signing uses strong algorithms (RS256/ES256) — scan for `alg.*none`, `HS256` with weak secrets
- [ ] **A07-16** Verify JWT secrets are not hardcoded — scan for `jwt.encode.*secret`, `jwt_secret\s*=`
- [ ] **A07-17** Verify JWT expiration (`exp` claim) is set and validated
- [ ] **A07-18** Verify OAuth 2.0 / OIDC implementation follows best practices — PKCE for public clients, state parameter for CSRF
- [ ] **A07-19** Verify passwords are not logged in application logs
- [ ] **A07-20** Verify authentication credentials are transmitted only over encrypted channels (HTTPS)

---

## 8. OWASP A08 — Software and Data Integrity Failures

> CWE: CWE-502 (Deserialization of Untrusted Data)

- [ ] **A08-01** Scan for unsafe deserialization (Python) — regex: `pickle\.loads?\(`, `pickle\.Unpickler\(`, `shelve\.open\(`, `marshal\.loads?\(`
- [ ] **A08-02** Scan for unsafe deserialization (Python YAML) — regex: `yaml\.load\(` without `Loader=yaml.SafeLoader` or `yaml\.unsafe_load\(`
- [ ] **A08-03** Scan for unsafe deserialization (Java) — regex: `ObjectInputStream`, `readObject\(`, `XMLDecoder`
- [ ] **A08-04** Scan for unsafe deserialization (Node.js) — regex: `node-serialize`, `serialize-javascript` with user input, `JSON\.parse\(` of untrusted data fed to constructors
- [ ] **A08-05** Scan for unsafe deserialization (.NET) — regex: `BinaryFormatter`, `NetDataContractSerializer`, `ObjectStateFormatter`
- [ ] **A08-06** Verify CI/CD pipelines have integrity checks — code review required, signed commits, protected branches
- [ ] **A08-07** Verify auto-update mechanisms validate signatures before applying updates
- [ ] **A08-08** Verify serialized data from untrusted sources is validated with digital signatures or integrity checks
- [ ] **A08-09** Verify `npm install` / `pip install` uses lock files to prevent dependency substitution attacks
- [ ] **A08-10** Verify no use of `eval()` or `exec()` to process serialized/structured data
- [ ] **A08-11** Verify data integrity checks (checksums, HMACs) on data crossing trust boundaries
- [ ] **A08-12** Verify code signing for releases and deployment artifacts

---

## 9. OWASP A09 — Security Logging and Monitoring Failures

> CWEs: CWE-778 (Insufficient Logging), CWE-223 (Omission of Security-relevant Information)

- [ ] **A09-01** Verify login attempts (success and failure) are logged with username, timestamp, IP, and user-agent
- [ ] **A09-02** Verify access control failures are logged (unauthorized access attempts)
- [ ] **A09-03** Verify input validation failures are logged
- [ ] **A09-04** Verify high-privilege actions (admin operations, role changes, permission changes) are logged
- [ ] **A09-05** Verify data access to sensitive records is logged (audit trail)
- [ ] **A09-06** Verify logs do NOT contain sensitive data — passwords, tokens, API keys, credit card numbers, PII
- [ ] **A09-07** Verify log injection is prevented — user input in logs is sanitized (no newlines `\n`, `\r`, control characters)
- [ ] **A09-08** Verify logs include sufficient context — timestamp, source IP, user ID, action, resource, result
- [ ] **A09-09** Verify logs are protected from tampering and unauthorized access
- [ ] **A09-10** Verify alerting is configured for suspicious activity (brute force, multiple access control failures)
- [ ] **A09-11** Verify security events are forwarded to a centralized logging/SIEM system
- [ ] **A09-12** Verify log retention meets compliance requirements
- [ ] **A09-13** Verify application errors are logged with stack traces (server-side only — never exposed to clients)
- [ ] **A09-14** Verify log format is consistent and machine-parseable (structured logging — JSON, key-value)
- [ ] **A09-15** Verify security-relevant configuration changes are logged

---

## 10. OWASP A10 — Server-Side Request Forgery (SSRF)

> CWE: CWE-918

- [ ] **A10-01** Verify user-supplied URLs are validated against an allowlist of permitted domains/IP ranges
- [ ] **A10-02** Verify user-supplied URLs cannot target internal/private IP ranges — block `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1`, `fc00::/7`
- [ ] **A10-03** Verify URL schemes are restricted to `https` (and `http` only if necessary) — block `file://`, `ftp://`, `gopher://`, `dict://`, `ldap://`
- [ ] **A10-04** Verify DNS rebinding protection — re-resolve DNS after validation or pin resolved IP
- [ ] **A10-05** Verify HTTP redirects from user-supplied URLs are not followed blindly — limit redirect count or disable redirects
- [ ] **A10-06** Scan for SSRF-vulnerable patterns — regex: `requests\.get\(.*user`, `urllib\.open\(`, `fetch\(.*user`, `http\.get\(.*user` where URL comes from user input
- [ ] **A10-07** Verify cloud metadata endpoints are blocked — `169.254.169.254`, `metadata.google.internal`
- [ ] **A10-08** Verify webhook URLs are validated before use
- [ ] **A10-09** Verify import/export URLs (image URLs, RSS feeds, file URLs) are validated
- [ ] **A10-10** Verify server-side HTTP clients have timeouts configured to prevent resource exhaustion

---

## 11. Code-Level Security Patterns

> Language-agnostic code scanning for dangerous patterns

### 11.1 Dangerous Function Calls

- [ ] **CL-01** Scan for `eval()` usage — regex: `\beval\s*\(` — verify it does not process user-controlled input
- [ ] **CL-02** Scan for `exec()` usage — regex: `\bexec\s*\(` — verify it does not process user-controlled input
- [ ] **CL-03** Scan for `compile()` usage in Python — regex: `\bcompile\s*\(` with user input
- [ ] **CL-04** Scan for `Function()` constructor in JavaScript — regex: `new\s+Function\s*\(`
- [ ] **CL-05** Scan for `setTimeout`/`setInterval` with string arguments — regex: `setTimeout\s*\(\s*['"]`, `setInterval\s*\(\s*['"]`
- [ ] **CL-06** Scan for `__import__()` with user input in Python — regex: `__import__\s*\(`
- [ ] **CL-07** Scan for `importlib.import_module()` with user input — regex: `import_module\s*\(`
- [ ] **CL-08** Scan for `globals()` / `locals()` manipulation — regex: `globals\s*\(\s*\)\s*\[`, `locals\s*\(\s*\)\s*\[`

### 11.2 Path Traversal

- [ ] **CL-09** Scan for path traversal patterns — regex: `\.\.\/`, `\.\.\\\\`, `\.\./`, path concatenation with user input
- [ ] **CL-10** Verify file paths are canonicalized before use — `os.path.realpath()`, `os.path.abspath()`, `Path.resolve()`
- [ ] **CL-11** Verify file operations validate the resolved path is within an expected base directory
- [ ] **CL-12** Scan for unsanitized file names in file operations — regex: `open\(.*request`, `open\(.*user`, `open\(.*param`

### 11.3 Prototype Pollution (JavaScript)

- [ ] **CL-13** Scan for unsafe object merge/clone — regex: `Object\.assign\(.*req\.`, `\.\.\.req\.body`, deep merge of user input without sanitization
- [ ] **CL-14** Verify `__proto__`, `constructor`, and `prototype` properties are filtered from user input before merging
- [ ] **CL-15** Verify `Object.create(null)` is used for dictionary-like objects that receive user input

### 11.4 Regex Denial of Service (ReDoS)

- [ ] **CL-16** Scan for catastrophic backtracking patterns — regex groups with nested quantifiers: `(a+)+`, `(a|a)+`, `(a*)*`, `(.*a){x}` where x > 10
- [ ] **CL-17** Verify regex input length is bounded before matching
- [ ] **CL-18** Verify regex timeout/complexity limits are configured where available

### 11.5 Race Conditions

- [ ] **CL-19** Scan for Time-of-Check-Time-of-Use (TOCTOU) — file existence checks followed by file operations without locks
- [ ] **CL-20** Verify shared mutable state is protected with proper synchronization (locks, mutexes, semaphores)
- [ ] **CL-21** Verify database operations that depend on prior reads use transactions or optimistic locking
- [ ] **CL-22** Verify file operations use atomic operations where available (`os.rename()`, `tempfile` + rename)

### 11.6 Integer and Type Safety

- [ ] **CL-23** Verify numeric input bounds are checked — no integer overflow in array indices, buffer sizes, or loop counters
- [ ] **CL-24** Verify null/undefined/None values are checked before dereferencing — scan for unguarded `.` access on nullable values
- [ ] **CL-25** Verify type coercion is explicit — no implicit type conversion that could lead to unexpected behavior

### 11.7 Timing Attacks

- [ ] **CL-26** Verify secret comparison uses constant-time comparison — scan for `==` or `!=` on tokens, passwords, HMAC values; should use `hmac.compare_digest()` (Python), `crypto.timingSafeEqual()` (Node.js)
- [ ] **CL-27** Verify authentication responses take the same time regardless of whether the account exists

### 11.8 Log Injection

- [ ] **CL-28** Verify user input written to logs is sanitized — no newlines, carriage returns, or ANSI escape codes
- [ ] **CL-29** Verify log messages do not include passwords, tokens, session IDs, or other secrets
- [ ] **CL-30** Verify structured logging is used to separate message templates from user data

---

## 12. Authentication & Session Management

- [ ] **AUTH-01** Verify password hashing uses bcrypt (cost ≥ 10), Argon2id (memory ≥ 19 MiB, iterations ≥ 2, parallelism ≥ 1), scrypt (N=2^17, r=8, p=1), or PBKDF2 (≥ 600,000 iterations SHA-256)
- [ ] **AUTH-02** Verify passwords are never stored in plaintext or logged
- [ ] **AUTH-03** Verify session cookies have `Secure` flag (HTTPS only)
- [ ] **AUTH-04** Verify session cookies have `HttpOnly` flag (no JavaScript access)
- [ ] **AUTH-05** Verify session cookies have `SameSite=Lax` or `SameSite=Strict` attribute
- [ ] **AUTH-06** Verify session IDs are regenerated after any privilege level change (login, role change)
- [ ] **AUTH-07** Verify session tokens have sufficient entropy (≥ 128 bits of randomness)
- [ ] **AUTH-08** Verify absolute session timeout exists (force re-authentication after max lifetime)
- [ ] **AUTH-09** Verify idle session timeout exists (configurable, e.g., 15 minutes for sensitive apps)
- [ ] **AUTH-10** Verify concurrent session control — limit active sessions per user or notify on new session
- [ ] **AUTH-11** Verify "remember me" functionality uses a separate long-lived token (not the session token) and is revocable
- [ ] **AUTH-12** Verify password change requires the current password
- [ ] **AUTH-13** Verify password reset flow validates token, expires quickly, and is single-use
- [ ] **AUTH-14** Verify MFA/2FA is supported and enforced for admin accounts at minimum
- [ ] **AUTH-15** Verify OAuth/OIDC implementations use PKCE for authorization code flow, validate `state` parameter, and validate `id_token` claims

---

## 13. Authorization

- [ ] **AUTHZ-01** Verify role-based access control (RBAC) is implemented with roles defined server-side
- [ ] **AUTHZ-02** Verify function-level access control — every API endpoint/function checks the caller's role/permissions
- [ ] **AUTHZ-03** Verify object-level access control — every data access verifies the authenticated user has permission for the specific record
- [ ] **AUTHZ-04** Check for horizontal privilege escalation — user A cannot access user B's data by changing IDs
- [ ] **AUTHZ-05** Check for vertical privilege escalation — regular users cannot access admin functions by manipulating requests
- [ ] **AUTHZ-06** Verify authorization checks are centralized (single authorization module, reused everywhere) — not duplicated/inconsistent
- [ ] **AUTHZ-07** Verify authorization is enforced server-side — client-side checks are for UX only
- [ ] **AUTHZ-08** Verify API endpoints require authentication unless explicitly public
- [ ] **AUTHZ-09** Verify authorization is checked on every request (not just once at login)
- [ ] **AUTHZ-10** Verify administrative endpoints are segregated and require elevated authentication

---

## 14. Input Validation & Output Encoding

- [ ] **IV-01** Verify all input is validated at trust boundaries — API endpoints, form submissions, file uploads, URL parameters, headers, cookies
- [ ] **IV-02** Verify input validation uses an allowlist approach (what is permitted) rather than a denylist (what is blocked)
- [ ] **IV-03** Verify input validation is enforced server-side (client-side validation is supplemental only)
- [ ] **IV-04** Verify Content-Type header is validated — reject unexpected content types
- [ ] **IV-05** Verify file uploads validate: file type (magic bytes, not just extension), file size (maximum limit), file name (sanitize special characters, path separators)
- [ ] **IV-06** Verify uploaded files are stored outside the web root with randomized names
- [ ] **IV-07** Verify uploaded files are scanned for malware/viruses when feasible
- [ ] **IV-08** Verify URL redirect targets are validated against an allowlist — prevent open redirects
- [ ] **IV-09** Verify output encoding is context-specific: HTML encoding for HTML context, JavaScript encoding for JS context, URL encoding for URL context, CSS encoding for CSS context, SQL parameterization for SQL context
- [ ] **IV-10** Verify JSON output uses `Content-Type: application/json` and JSON serializer (not string concatenation)
- [ ] **IV-11** Verify email addresses, phone numbers, and other structured input are validated against expected format
- [ ] **IV-12** Verify request size limits are enforced to prevent denial of service
- [ ] **IV-13** Verify XML input is validated and external entity processing is disabled
- [ ] **IV-14** Verify GraphQL queries have depth limiting and query complexity analysis to prevent abuse
- [ ] **IV-15** Verify mass assignment protection — only expected fields are accepted from user input (allowlisting fields)

---

## 15. Cryptography

- [ ] **CRYPTO-01** Verify TLS 1.2 or higher is used for all communications — no SSL 2.0/3.0, TLS 1.0/1.1
- [ ] **CRYPTO-02** Verify strong cipher suites — prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305); no NULL, export, DES, RC4, or 3DES ciphers
- [ ] **CRYPTO-03** Verify forward secrecy is enabled — prefer ECDHE key exchange
- [ ] **CRYPTO-04** Verify cryptographic key length meets minimum requirements — RSA ≥ 2048, ECDSA ≥ 256 (P-256), AES ≥ 128
- [ ] **CRYPTO-05** Verify key rotation policy exists and is implemented
- [ ] **CRYPTO-06** Verify keys are not stored alongside encrypted data
- [ ] **CRYPTO-07** Verify no use of custom/homegrown cryptographic algorithms — use established libraries only (OpenSSL, libsodium, Bouncy Castle, etc.)
- [ ] **CRYPTO-08** Verify password-based key derivation uses PBKDF2, scrypt, or Argon2 — never raw passwords as keys
- [ ] **CRYPTO-09** Verify encryption at rest for sensitive data (PII, credentials, financial data)
- [ ] **CRYPTO-10** Verify encryption in transit for all external communications
- [ ] **CRYPTO-11** Verify certificate validation is enforced — no disabled validation, self-signed certificates in production
- [ ] **CRYPTO-12** Verify certificate pinning for mobile applications and high-security APIs (when applicable)

---

## 16. API Security

- [ ] **API-01** Verify rate limiting is implemented on all API endpoints — per-user and per-IP
- [ ] **API-02** Verify all API endpoints validate input (type, length, range, format)
- [ ] **API-03** Verify CORS is configured with specific allowed origins — not wildcard (`*`) for authenticated endpoints
- [ ] **API-04** Verify `Content-Type` is enforced on requests — reject requests with unexpected content types
- [ ] **API-05** Verify API responses include appropriate security headers
- [ ] **API-06** Verify API versioning strategy does not expose deprecated/insecure versions
- [ ] **API-07** Verify GraphQL introspection is disabled in production — regex: `introspection.*true`, `__schema`, `__type`
- [ ] **API-08** Verify GraphQL depth limiting is configured — prevent deeply nested queries (max depth 7–10)
- [ ] **API-09** Verify GraphQL query complexity limits are set — prevent expensive queries
- [ ] **API-10** Verify API error responses do not leak internal information (stack traces, database errors, internal paths)
- [ ] **API-11** Verify API authentication tokens are transmitted via `Authorization` header (not URL query parameters)
- [ ] **API-12** Verify API pagination has maximum page size limits — prevent data dumping
- [ ] **API-13** Verify batch/bulk endpoints have limits on the number of operations per request
- [ ] **API-14** Verify WebSocket connections are authenticated and authorized
- [ ] **API-15** Verify API documentation does not expose sensitive endpoints or credentials

---

## 17. Infrastructure & Configuration

- [ ] **INFRA-01** Verify HTTPS is enforced for all public endpoints — HTTP requests redirect to HTTPS or are blocked
- [ ] **INFRA-02** Verify security headers are set (see A05 section for full list)
- [ ] **INFRA-03** Verify error pages do not reveal stack traces, framework versions, or internal paths
- [ ] **INFRA-04** Verify debug endpoints, profiler, and admin tools are disabled/removed in production
- [ ] **INFRA-05** Verify database ports are not exposed to the public internet
- [ ] **INFRA-06** Verify only necessary ports are open — run port scan review
- [ ] **INFRA-07** Verify container images are based on minimal base images (Alpine, distroless) and regularly updated
- [ ] **INFRA-08** Verify containers run as non-root users
- [ ] **INFRA-09** Verify environment variables for secrets are not logged or exposed via process inspection
- [ ] **INFRA-10** Verify health check endpoints do not reveal sensitive internal state
- [ ] **INFRA-11** Verify admin interfaces are restricted by IP allowlist or VPN
- [ ] **INFRA-12** Verify production infrastructure uses immutable deployments when possible
- [ ] **INFRA-13** Verify no test/development data exists in production databases
- [ ] **INFRA-14** Verify network segmentation between application tiers (web, app, database)
- [ ] **INFRA-15** Verify DNS configuration is secure — no dangling CNAME records (subdomain takeover prevention)

---

## 18. Supply Chain Security

- [ ] **SC-01** Verify all dependencies are pinned to exact versions in lock files
- [ ] **SC-02** Verify dependency lock file integrity — hashes present and verified
- [ ] **SC-03** Verify automated dependency vulnerability scanning is configured (Dependabot, Snyk, pip-audit, npm audit)
- [ ] **SC-04** Verify no dependency confusion risk — private package names do not collide with public registry names
- [ ] **SC-05** Verify package sources are explicitly configured — use official registries only
- [ ] **SC-06** Verify CI/CD pipeline is secured — secrets are not exposed in build logs, build environments are ephemeral
- [ ] **SC-07** Verify CI/CD pipeline uses pinned action/tool versions (not `latest` or `main` branch references)
- [ ] **SC-08** Verify pull request reviews are required before merging to protected branches
- [ ] **SC-09** Verify build artifacts are signed or have integrity checks
- [ ] **SC-10** Verify Software Bill of Materials (SBOM) is generated and maintained
- [ ] **SC-11** Verify no malicious or abandoned packages are in the dependency tree
- [ ] **SC-12** Verify pre-commit hooks / CI checks include security scanning (SAST, secret detection)
- [ ] **SC-13** Verify third-party code (CDN-loaded scripts, external APIs) uses SRI hashes or pinned versions
- [ ] **SC-14** Verify `.npmrc` / `pip.conf` / `NuGet.Config` do not contain embedded credentials

---

## 19. Data Protection

- [ ] **DATA-01** Verify PII is identified and classified — document what PII the application handles
- [ ] **DATA-02** Verify sensitive data is encrypted at rest using AES-256 or equivalent
- [ ] **DATA-03** Verify data minimization — only collect and store data that is necessary for the business purpose
- [ ] **DATA-04** Verify data retention policies — data is deleted/anonymized after the retention period
- [ ] **DATA-05** Verify PII is not logged — scan logs for email addresses, phone numbers, social security numbers, credit card numbers
- [ ] **DATA-06** Verify sensitive data is not exposed in URLs — no PII or tokens in query parameters (logged by web servers, proxies, browsers)
- [ ] **DATA-07** Verify sensitive data is not stored in browser localStorage/sessionStorage — scan for: `localStorage.setItem.*token`, `sessionStorage.setItem.*password`
- [ ] **DATA-08** Verify database backups are encrypted
- [ ] **DATA-09** Verify data masking for sensitive fields in non-production environments
- [ ] **DATA-10** Verify GDPR/privacy compliance — right to erasure, data portability, consent management (if applicable)
- [ ] **DATA-11** Verify credit card data handling complies with PCI DSS (if applicable) — no full card numbers stored
- [ ] **DATA-12** Verify sensitive data is not cached — appropriate `Cache-Control` and `Pragma` headers
- [ ] **DATA-13** Verify data in transit between services is encrypted (mTLS for service-to-service communication)
- [ ] **DATA-14** Verify PII is not included in error messages returned to users

---

## 20. Secrets Management

- [ ] **SEC-01** Verify no secrets exist in source code — scan for: API keys, passwords, tokens, private keys, connection strings (see A02 regex patterns)
- [ ] **SEC-02** Verify `.env` files are listed in `.gitignore` — scan `.gitignore` for `.env` entry
- [ ] **SEC-03** Verify `.env.example` / `.env.sample` files do not contain real secrets — only placeholder values
- [ ] **SEC-04** Verify no secrets in Docker build arguments, Dockerfiles, or docker-compose files — scan for `ARG.*PASSWORD`, `ENV.*SECRET`, hardcoded values
- [ ] **SEC-05** Verify no secrets in CI/CD configuration files committed to the repository — scan `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- [ ] **SEC-06** Verify secret rotation is implemented — API keys, passwords, tokens have expiration and are periodically rotated
- [ ] **SEC-07** Verify secrets are loaded from environment variables, secret manager (Vault, AWS Secrets Manager, Azure Key Vault), or encrypted configuration — not from files in the repository
- [ ] **SEC-08** Verify secrets are not passed as command-line arguments (visible in process listings via `ps`)
- [ ] **SEC-09** Verify secrets are not displayed in application logs — scan for: `print.*key`, `log.*password`, `console.log.*token`, `logger.*secret`
- [ ] **SEC-10** Verify secrets are not exposed in error messages or stack traces
- [ ] **SEC-11** Verify git history does not contain previously committed secrets — consider tools like `git-secrets`, `trufflehog`, `gitleaks`
- [ ] **SEC-12** Verify environment variable names follow conventions that indicate sensitivity — `*_SECRET`, `*_KEY`, `*_PASSWORD`, `*_TOKEN`

---

## 21. Frontend-Specific Security

- [ ] **FE-01** Verify Content Security Policy (CSP) is deployed and restrictive — no `unsafe-inline`, `unsafe-eval`, or `*` in `script-src`
- [ ] **FE-02** Verify Subresource Integrity (SRI) is used for all externally loaded scripts and stylesheets — `integrity` attribute with SHA-384/SHA-512 hash
- [ ] **FE-03** Verify clickjacking protection — `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'`
- [ ] **FE-04** Verify open redirect prevention — all redirect URLs are validated against an allowlist
- [ ] **FE-05** Verify `postMessage` origin validation — regex: `addEventListener\s*\(\s*['"]message['"]` without origin check (`event.origin`)
- [ ] **FE-06** Verify `innerHTML` is not used with unsanitized user input — use `textContent` or DOM API instead
- [ ] **FE-07** Verify `document.write()` is not used with user-controlled content
- [ ] **FE-08** Verify sensitive data is not stored in `localStorage` or `sessionStorage` — tokens, passwords, PII
- [ ] **FE-09** Verify form auto-complete is disabled for sensitive fields — `autocomplete="off"` for passwords in admin forms, credit card fields
- [ ] **FE-10** Verify client-side validation is supplemented by server-side validation — never relied upon solely
- [ ] **FE-11** Verify third-party scripts are reviewed and loaded from trusted CDNs with SRI
- [ ] **FE-12** Verify no sensitive data leaks through `Referer` header — `Referrer-Policy` configured
- [ ] **FE-13** Verify Web Workers and Service Workers do not process untrusted data without validation
- [ ] **FE-14** Verify DOM Clobbering prevention — IDs and names in HTML do not collide with global JavaScript variables used in security-sensitive logic
- [ ] **FE-15** Verify `target="_blank"` links include `rel="noopener noreferrer"`

---

## 22. Database Security

- [ ] **DB-01** Verify all queries use parameterized statements — no string concatenation for SQL construction
- [ ] **DB-02** Verify database accounts use least-privilege access — application account cannot DROP tables, ALTER schema, or access other databases
- [ ] **DB-03** Verify connection strings do not contain credentials in source code — use environment variables or secret managers
- [ ] **DB-04** Verify database connections use TLS/SSL encryption
- [ ] **DB-05** Verify database error messages are not returned to users — catch and log internally, return generic errors
- [ ] **DB-06** Verify NoSQL query injection prevention — validate and sanitize operators like `$gt`, `$ne`, `$where`, `$regex` in MongoDB queries
- [ ] **DB-07** Verify database connection pooling has maximum limits to prevent resource exhaustion
- [ ] **DB-08** Verify database backups are encrypted and access-controlled
- [ ] **DB-09** Verify database migration scripts do not contain secrets or test data
- [ ] **DB-10** Verify database audit logging is enabled for sensitive table access
- [ ] **DB-11** Verify row-level security or application-level filters prevent unauthorized data access
- [ ] **DB-12** Verify stored procedures do not use dynamic SQL with unsanitized input

---

## 23. File System Security

- [ ] **FS-01** Verify path traversal prevention — all file paths are validated and canonicalized
- [ ] **FS-02** Verify file uploads restrict allowed extensions — allowlist approach (e.g., only `.jpg`, `.png`, `.pdf`)
- [ ] **FS-03** Verify file uploads validate content type via magic bytes (file header) — not just MIME type or extension
- [ ] **FS-04** Verify file upload size limits are enforced server-side
- [ ] **FS-05** Verify uploaded files are stored outside the web root with non-guessable names
- [ ] **FS-06** Verify uploaded files are not executable on the server
- [ ] **FS-07** Verify temporary files are cleaned up after use — `tempfile.NamedTemporaryFile(delete=True)` or explicit cleanup in `finally` blocks
- [ ] **FS-08** Verify file permissions follow principle of least privilege — no world-writable files (0666/0777)
- [ ] **FS-09** Verify symlink attacks are prevented — use `os.open()` with `O_NOFOLLOW` or validate canonical path
- [ ] **FS-10** Verify directory traversal sequences (`..`, `%2e%2e`) are blocked in file path inputs
- [ ] **FS-11** Verify no sensitive files are accessible via web server — `.env`, `.git/`, `.svn/`, `*.bak`, `*.swp`
- [ ] **FS-12** Verify file download endpoints validate the requested file path is within an allowed directory

---

## 24. Error Handling & Logging

- [ ] **EH-01** Verify no stack traces are returned in production API/page responses — scan for: `traceback.format_exc()` in response, `res.send(err.stack)`, `@app.errorhandler` returning full exception
- [ ] **EH-02** Verify generic error messages are returned to users — "An error occurred" not "NullPointerException at com.example.UserService.findById(UserService.java:42)"
- [ ] **EH-03** Verify error handlers exist for all unhandled exceptions — global exception handlers that log and return safe responses
- [ ] **EH-04** Verify sensitive data is not present in error messages — no database connection strings, credentials, internal IP addresses
- [ ] **EH-05** Verify errors are logged with sufficient detail for debugging (server-side) but redacted for client responses
- [ ] **EH-06** Verify fail-secure behavior — when an error occurs, the system denies access rather than granting it
- [ ] **EH-07** Verify no bare `except:` or `catch(Exception)` that silently swallow errors without logging
- [ ] **EH-08** Verify timeout errors are handled gracefully — external service calls have timeouts and circuit breakers
- [ ] **EH-09** Verify resource cleanup in error paths — connections, file handles, and locks are released in `finally`/`with`/`using` blocks
- [ ] **EH-10** Verify custom error pages are configured — no default framework error pages in production (e.g., Django yellow page, Express default error)
- [ ] **EH-11** Verify HTTP status codes are used correctly — 401 for unauthenticated, 403 for unauthorized, 404 for not found (not 200 with error in body)
- [ ] **EH-12** Verify error responses have consistent format (JSON API error schema) to prevent information leakage through response structure differences

---

## 25. Python-Specific Security

> Applicable when the project uses Python

- [ ] **PY-01** Verify `pickle` is not used with untrusted data — regex: `pickle\.(loads?|Unpickler)\s*\(` — use JSON or MessagePack instead
- [ ] **PY-02** Verify `yaml.safe_load()` or `yaml.load(Loader=yaml.SafeLoader)` is used instead of `yaml.load()` — regex: `yaml\.load\s*\((?!.*Loader\s*=\s*yaml\.SafeLoader)`
- [ ] **PY-03** Verify `subprocess` uses argument lists, not `shell=True` — regex: `subprocess\.\w+\(.*shell\s*=\s*True`
- [ ] **PY-04** Verify `os.system()` is not used — use `subprocess.run()` with argument list
- [ ] **PY-05** Verify `eval()` and `exec()` are not used with user input
- [ ] **PY-06** Verify `assert` is not used for security checks — assertions are disabled with `-O` flag
- [ ] **PY-07** Verify `secrets` module is used for security-sensitive random values (not `random` module)
- [ ] **PY-08** Verify `hashlib` operations for passwords use `hashlib.pbkdf2_hmac()` or dedicated libraries (bcrypt, argon2-cffi)
- [ ] **PY-09** Verify `xml.etree.ElementTree` or `lxml` is configured to prevent XXE — use `defusedxml` for untrusted XML
- [ ] **PY-10** Verify Django/Flask `SECRET_KEY` is not hardcoded — loaded from environment variable
- [ ] **PY-11** Verify Django `ALLOWED_HOSTS` is set (not `['*']` in production)
- [ ] **PY-12** Verify Django `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY` are `True` in production
- [ ] **PY-13** Verify Flask `app.secret_key` is cryptographically random and not hardcoded
- [ ] **PY-14** Verify SQL queries use parameterized queries — `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))` not f-strings
- [ ] **PY-15** Verify `hmac.compare_digest()` is used for constant-time comparison of tokens/secrets
- [ ] **PY-16** Verify `tempfile.mkstemp()` or `tempfile.NamedTemporaryFile()` is used for temp files (not predictable names)
- [ ] **PY-17** Verify `os.path.join()` does not accept absolute paths from user input that could override the base directory
- [ ] **PY-18** Verify `requests` library calls use `verify=True` (default) for TLS certificate validation
- [ ] **PY-19** Verify `DEBUG = False` in Django production settings
- [ ] **PY-20** Verify no `# nosec` or `# noqa: S` annotations that suppress security warnings without justification

---

## 26. Node.js/JavaScript-Specific Security

> Applicable when the project uses Node.js or JavaScript

- [ ] **JS-01** Verify `eval()`, `Function()`, and `vm.runInContext()` are not used with user input
- [ ] **JS-02** Verify `child_process.exec()` is not used with user input — use `child_process.execFile()` or `spawn()` with argument arrays
- [ ] **JS-03** Verify `JSON.parse()` results are validated before use as constructors or in prototype-sensitive operations
- [ ] **JS-04** Verify Express.js uses `helmet` middleware for security headers
- [ ] **JS-05** Verify Express.js uses `express-rate-limit` or equivalent for rate limiting
- [ ] **JS-06** Verify `cors()` middleware is configured with specific origins — not default (allow all)
- [ ] **JS-07** Verify `cookie-parser` sets `httpOnly`, `secure`, and `sameSite` options
- [ ] **JS-08** Verify `crypto.randomBytes()` or `crypto.randomUUID()` is used for security-sensitive random values (not `Math.random()`)
- [ ] **JS-09** Verify `===` is used for comparisons (not `==`) to prevent type coercion vulnerabilities
- [ ] **JS-10** Verify `Object.freeze()` is applied to configuration objects to prevent modification
- [ ] **JS-11** Verify no `node-serialize`, `js-yaml` (with unsafe options), or other known-vulnerable deserialization packages
- [ ] **JS-12** Verify `npm audit` reports no critical or high vulnerabilities
- [ ] **JS-13** Verify `.env` is not committed — present in `.gitignore`
- [ ] **JS-14** Verify `process.env` is used for secrets — not hardcoded values in source
- [ ] **JS-15** Verify `crypto.timingSafeEqual()` is used for comparing secrets/tokens

---

## 27. .NET-Specific Security

> Applicable when the project uses C# / .NET

- [ ] **NET-01** Verify `BinaryFormatter` is not used — it is deprecated and unsafe for deserialization
- [ ] **NET-02** Verify parameterized queries are used — `SqlCommand` with `SqlParameter`, not string concatenation
- [ ] **NET-03** Verify `Antiforgery` tokens are used on all POST/PUT/DELETE endpoints
- [ ] **NET-04** Verify `OutputCache` does not cache sensitive data
- [ ] **NET-05** Verify `[Authorize]` attribute is applied to controllers/actions requiring authentication
- [ ] **NET-06** Verify `Data Protection API` is used for encryption — not custom implementations
- [ ] **NET-07** Verify `SecureString` or `byte[]` is used for in-memory secret handling where feasible
- [ ] **NET-08** Verify `HTTPS Redirection` middleware is enabled in production
- [ ] **NET-09** Verify `HSTS` middleware is enabled
- [ ] **NET-10** Verify `ValidateAntiForgeryToken` is used on form submissions

---

## 28. Go-Specific Security

> Applicable when the project uses Go

- [ ] **GO-01** Verify `sql.DB.Query()` uses parameterized queries — `db.Query("SELECT * FROM users WHERE id = $1", id)` not string formatting
- [ ] **GO-02** Verify `template/html` package is used (not `text/template`) for HTML output — auto-escaping
- [ ] **GO-03** Verify `crypto/rand` is used for security-sensitive random values (not `math/rand`)
- [ ] **GO-04** Verify HTTP client has timeouts set — `http.Client{Timeout: ...}`
- [ ] **GO-05** Verify `TLS.Config.MinVersion` is set to `tls.VersionTLS12` or higher
- [ ] **GO-06** Verify error handling checks every return value — `if err != nil` pattern consistently applied
- [ ] **GO-07** Verify `defer` is used for resource cleanup (file handles, connections)
- [ ] **GO-08** Verify `filepath.Clean()` is used to sanitize file paths
- [ ] **GO-09** Verify race conditions are prevented — `go vet -race` passes
- [ ] **GO-10** Verify `gosec` linter reports no high-severity findings

---

## 29. Docker & Container Security

> Applicable when the project uses containers

- [ ] **DOCK-01** Verify Dockerfile does not run as root — `USER` instruction specifies non-root user
- [ ] **DOCK-02** Verify base images are from trusted registries and use specific version tags (not `latest`)
- [ ] **DOCK-03** Verify no secrets are embedded in Docker images — no `COPY .env`, no hardcoded credentials in `ENV`
- [ ] **DOCK-04** Verify multi-stage builds are used to minimize final image size (no build tools in production image)
- [ ] **DOCK-05** Verify `.dockerignore` excludes sensitive files (`.env`, `.git/`, `node_modules/`, test data)
- [ ] **DOCK-06** Verify container images are scanned for vulnerabilities (Trivy, Snyk Container, Grype)
- [ ] **DOCK-07** Verify `HEALTHCHECK` instruction is defined
- [ ] **DOCK-08** Verify read-only filesystem is used where possible — `--read-only` flag
- [ ] **DOCK-09** Verify container resource limits are set (memory, CPU)
- [ ] **DOCK-10** Verify no `--privileged` flag is used in production deployments

---

## 30. CI/CD Pipeline Security

- [ ] **CICD-01** Verify secrets in CI/CD are stored as encrypted secrets (GitHub Secrets, GitLab CI variables) — not in pipeline files
- [ ] **CICD-02** Verify build logs do not contain secrets — secrets are masked in output
- [ ] **CICD-03** Verify CI/CD actions/plugins are pinned to specific commit SHA (not branch or tag)
- [ ] **CICD-04** Verify branch protection rules are enabled — require PR reviews, status checks, no force-push to main
- [ ] **CICD-05** Verify SAST (Static Application Security Testing) runs in CI pipeline
- [ ] **CICD-06** Verify SCA (Software Composition Analysis) runs in CI pipeline — `npm audit`, `pip-audit`, `safety`
- [ ] **CICD-07** Verify secret scanning is enabled in CI — tools like `gitleaks`, `trufflehog`, `git-secrets`
- [ ] **CICD-08** Verify deploy tokens/keys have minimal permissions and are rotated regularly
- [ ] **CICD-09** Verify CI/CD environments are ephemeral — build environments are destroyed after use
- [ ] **CICD-10** Verify deployment requires approval for production environments

---

## 31. Denial of Service Prevention

- [ ] **DOS-01** Verify request size limits are enforced — max body size, max header size, max URL length
- [ ] **DOS-02** Verify rate limiting is applied per-IP and per-user on resource-intensive endpoints
- [ ] **DOS-03** Verify pagination limits — maximum results per page to prevent data dumping
- [ ] **DOS-04** Verify file upload size limits are enforced
- [ ] **DOS-05** Verify regex patterns do not have catastrophic backtracking (see CL-16)
- [ ] **DOS-06** Verify connection timeouts are configured for external service calls
- [ ] **DOS-07** Verify database query timeouts are configured
- [ ] **DOS-08** Verify resource cleanup on error — connections, file handles, memory are released even on exceptions
- [ ] **DOS-09** Verify batch operations have limits — maximum items per batch request
- [ ] **DOS-10** Verify recursive data structures have depth limits — JSON parsing depth, XML nesting depth

---

## Checklist Summary

| Section | Items | Category |
| --- | --- | --- |
| 1. A01 — Broken Access Control | 20 | OWASP Top 10 |
| 2. A02 — Cryptographic Failures | 20 | OWASP Top 10 |
| 3. A03 — Injection | 24 | OWASP Top 10 |
| 4. A04 — Insecure Design | 15 | OWASP Top 10 |
| 5. A05 — Security Misconfiguration | 20 | OWASP Top 10 |
| 6. A06 — Vulnerable Components | 12 | OWASP Top 10 |
| 7. A07 — Auth Failures | 20 | OWASP Top 10 |
| 8. A08 — Integrity Failures | 12 | OWASP Top 10 |
| 9. A09 — Logging Failures | 15 | OWASP Top 10 |
| 10. A10 — SSRF | 10 | OWASP Top 10 |
| 11. Code-Level Security | 30 | Code Patterns |
| 12. Auth & Session | 15 | Auth |
| 13. Authorization | 10 | AuthZ |
| 14. Input/Output | 15 | Validation |
| 15. Cryptography | 12 | Crypto |
| 16. API Security | 15 | API |
| 17. Infrastructure | 15 | Infra |
| 18. Supply Chain | 14 | Supply Chain |
| 19. Data Protection | 14 | Data |
| 20. Secrets Management | 12 | Secrets |
| 21. Frontend Security | 15 | Frontend |
| 22. Database Security | 12 | Database |
| 23. File System Security | 12 | Filesystem |
| 24. Error Handling | 12 | Error Handling |
| 25. Python-Specific | 20 | Language |
| 26. Node.js-Specific | 15 | Language |
| 27. .NET-Specific | 10 | Language |
| 28. Go-Specific | 10 | Language |
| 29. Docker Security | 10 | Container |
| 30. CI/CD Security | 10 | Pipeline |
| 31. DoS Prevention | 10 | Availability |
| **TOTAL** | ****472**** | |

---

## References

- [OWASP Top 10 (2021)](https://owasp.org/Top10/2021/)
- [OWASP Top 10 (2025)](https://owasp.org/Top10/2025/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE/SANS Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
- [NIST SP 800-53 Security Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [OWASP Proactive Controls](https://owasp.org/www-project-proactive-controls/)
