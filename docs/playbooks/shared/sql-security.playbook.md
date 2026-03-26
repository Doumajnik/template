+++
id = "shared/sql-security"
title = "SQL Security Rules"
agents = ["all"]
technologies = ["sql", "postgresql", "mysql", "sqlite", "mssql"]
category = "rule"
tags = ["sql", "security", "injection", "authentication", "authorization"]
version = 1
+++

### SQL Injection Prevention

- ALWAYS use parameterized queries or prepared statements — no exceptions.
- NEVER concatenate user input into SQL strings, even for "safe" inputs like integers.
- Dynamic table/column names MUST be validated against a strict allowlist — never interpolated from user input.
- ORM-generated queries are safe by default — but raw SQL within ORMs MUST still be parameterized.
- Stored procedures reduce injection surface but don't eliminate it — parameterize inside procedures too.
- Log and alert on any SQL syntax errors from user-facing endpoints — they may be injection probes.

### Access Control

- Use database roles with minimum required privileges — NEVER run application queries as superuser.
- Separate read-only and read-write connection strings — route read queries to replicas.
- Row-level security (RLS) for multi-tenant applications — never rely solely on WHERE clauses in app code.
- Revoke PUBLIC schema permissions — explicitly grant only what's needed.
- Use schema-level isolation for multi-tenant databases when row-level security is insufficient.
- Application service accounts should NEVER have DROP, TRUNCATE, or ALTER privileges.

### Data Protection

- Encrypt sensitive columns at rest (PII, financial data, health records) using pgcrypto or equivalent.
- Hash passwords with bcrypt/argon2 — NEVER store plaintext or reversible encryption.
- Mask sensitive data in non-production environments — don't copy production PII to staging.
- Audit trails: log all INSERT/UPDATE/DELETE on sensitive tables using triggers or CDC.
- Use column-level SELECT to prevent accidental exposure of sensitive fields.
- Implement data retention policies — automatically purge data beyond retention period.

### Connection Security

- Use TLS/SSL for all database connections — even within private networks.
- Rotate database credentials on a regular schedule (minimum quarterly).
- Use short-lived tokens or IAM authentication instead of long-lived passwords where supported.
- Connection strings MUST be stored in environment variables or secrets managers — NEVER in code or config files.
- Limit connection sources: database firewall rules should allow only application servers.

### Error Handling

- NEVER expose raw SQL errors to end users — they reveal schema, table names, and query structure.
- Map database errors to generic application errors with correlation IDs for server-side lookup.
- Log full SQL errors server-side (including the offending query with parameters redacted).
- Constraint violation errors should be caught and mapped to user-friendly messages.
- Timeout errors should trigger circuit breakers — don't retry indefinitely.

### Monitoring and Alerting

- Monitor failed login attempts — alert on unusual patterns (brute force).
- Log all privilege escalation and DDL operations (CREATE, ALTER, DROP).
- Alert on queries accessing tables they shouldn't (application role accessing admin tables).
- Track connection pool exhaustion — potential DoS vector.
- Audit slow queries for timing-based injection attempts (e.g., `SLEEP()`, `pg_sleep()`).
