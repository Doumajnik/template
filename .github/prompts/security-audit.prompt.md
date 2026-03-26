---
description: Run a comprehensive security audit of the project
agent: Security
---

# Security Audit

Run a comprehensive security audit of the entire project.

## Instructions

1. **Read the security checklist:**
   - `docs/SECURITY_CHECKLIST.md` — every item must be checked against every source file
   - `docs/SECURITY_REPORT.md` — review previous findings for resolved/recurring issues

2. **Read project context:**
   - `.ai/PREFERENCES.md` — coding style and project settings
   - `docs/PLAYBOOK.md` — architecture decisions and patterns
   - `docs/CODE_INVENTORY.md` — all source files and symbols to audit

3. **Scan for OWASP Top 10 vulnerabilities:**
   - **Injection:** SQL injection, XSS, command injection, template injection
   - **Broken access control:** missing auth checks, privilege escalation paths
   - **Cryptographic failures:** weak algorithms, hardcoded keys, plaintext secrets
   - **Insecure design:** missing rate limiting, unsafe defaults, trust boundaries
   - **Security misconfiguration:** debug mode enabled, permissive CORS, default credentials

4. **Check secrets management:**
   - Scan all files for hardcoded secrets, API keys, tokens, and passwords
   - Verify `.env` files are in `.gitignore`
   - Check git history for accidentally committed secrets
   - Verify environment variables are used for all sensitive configuration

5. **Audit dependencies:**
   - Check for known vulnerabilities in installed packages
   - Flag outdated dependencies with published CVEs
   - Review dependency permissions and scope

6. **Review authentication and authorization:**
   - Verify input validation at all system boundaries
   - Check session management and token handling
   - Audit role-based access control implementation

7. **Generate the security report:**
   - Append findings to `docs/SECURITY_REPORT.md`
   - Classify each finding: CRITICAL / HIGH / MEDIUM / LOW / INFO
   - Include: location, description, risk, and recommended fix
   - CRITICAL and HIGH findings must be fixed before release

8. **Summary:**
   - Total findings by severity
   - Top 3 risks requiring immediate attention
   - Comparison with previous audit (new, resolved, recurring)
