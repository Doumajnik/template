+++
id = "shared/database-design"
title = "Database Design Rules"
agents = ["all"]
technologies = ["sql", "postgresql", "mysql", "sqlite", "mongodb"]
category = "rule"
tags = ["database", "schema", "normalization", "design", "migration"]
version = 1
+++

### Schema Design

- Start with 3NF (Third Normal Form) — denormalize only when profiling proves a bottleneck.
- Every table MUST have a primary key. Prefer surrogate keys (UUID or BIGSERIAL) for independence from business logic.
- Add `created_at` and `updated_at` timestamps to every table — essential for debugging and auditing.
- Use soft deletes (`deleted_at` timestamp) instead of hard deletes for business-critical data.
- Name tables as plural nouns (e.g., `users`, `orders`, `line_items`). Name columns as singular (e.g., `user_id`, `email`).
- Use snake_case for all identifiers — never camelCase or PascalCase in SQL.
- Avoid reserved words as table/column names — use `status_code` not `status`, `user_type` not `type`.

### Constraints

- Every foreign key MUST reference a primary key or unique column with an explicit ON DELETE action.
- Use NOT NULL by default — only allow NULL when the absence of a value has business meaning.
- Use CHECK constraints for domain validation (e.g., `CHECK (price >= 0)`, `CHECK (status IN ('active', 'inactive'))`).
- Use UNIQUE constraints for natural keys (email, username, SKU) in addition to the surrogate PK.
- Prefer database-level constraints over application-level validation — the database is the last line of defense.

### Relationships

- One-to-many: FK on the "many" side pointing to the "one" side's PK.
- Many-to-many: junction table with composite PK (both FKs) plus optional metadata columns.
- One-to-one: FK with UNIQUE constraint, or merge into a single table if accessed together.
- Self-referential: FK pointing to the same table's PK (e.g., `parent_id` in categories).
- Avoid circular dependencies between tables — they complicate migrations and seeding.

### Data Types

- Use the most specific type: `BOOLEAN` not `INTEGER`, `DATE` not `VARCHAR`, `INET` not `TEXT`.
- Store monetary values as `NUMERIC(precision, scale)` or integer cents — NEVER floating point.
- Store timestamps as `TIMESTAMPTZ` (PostgreSQL) — always timezone-aware.
- Use `UUID` for distributed systems; `BIGSERIAL` for single-database applications.
- Use `JSONB` (PostgreSQL) for semi-structured data that varies per row — but don't use it as an escape hatch from proper normalization.
- Text columns: use `TEXT` with CHECK constraints on length, not `VARCHAR(N)` — PostgreSQL treats them identically but TEXT is more flexible.

### Migration Rules

- Every migration MUST be reversible — include both `up` and `down` operations.
- Name migrations descriptively: `{timestamp}_{action}_{entity}` (e.g., `20260326_add_email_index_to_users`).
- Never modify a deployed migration — create a new migration instead.
- Separate schema changes from data migrations — run them in different deployment steps.
- Test migrations in both directions (up AND down) before deploying.
- For large tables: use non-blocking index creation (`CREATE INDEX CONCURRENTLY` in PostgreSQL).
- Add indexes in separate migrations from table alterations — keeps lock time minimal.

### Partitioning Strategy

- Consider partitioning when a table exceeds 100M rows or 100GB.
- Range partitioning by date is the most common and useful pattern (e.g., monthly partitions for logs).
- List partitioning for status-based queries (e.g., `active` vs `archived`).
- Hash partitioning for even distribution across nodes in distributed systems.
- Always include the partition key in queries — otherwise the planner scans all partitions.

### Monitoring

- Track slow queries: log anything >100ms, alert on >1s.
- Monitor table bloat: schedule regular VACUUM on high-churn tables (PostgreSQL).
- Monitor connection count: alert when approaching pool limits.
- Track index usage: drop indexes that haven't been used in 30 days.
- Monitor replication lag: alert if replica falls behind by >1s.
- Use pg_stat_statements (PostgreSQL) or Performance Schema (MySQL) for query analytics.
