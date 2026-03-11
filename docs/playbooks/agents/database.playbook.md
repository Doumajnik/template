+++
id = "agents/database"
title = "Database Agent Rules"
agents = ["database"]
technologies = ["all"]
category = "rule"
tags = ["database"]
version = 2
+++

### Database Guidelines

1. **Design schemas in 3NF by default** — denormalize only with measured performance justification. Premature denormalization is premature optimization.
2. **Every table must have a primary key** — prefer UUIDs over auto-increment for distributed systems. Auto-increment is acceptable for single-node databases.
3. **Add indexes on columns used in WHERE, JOIN, and ORDER BY** — but don't over-index. Every index slows writes. Measure before adding.
4. **Foreign keys must have explicit ON DELETE behavior** — CASCADE, SET NULL, or RESTRICT. Never leave it unspecified.
5. **Write migrations as up/down pairs** — every migration must be reversible. Test the down migration before deploying the up.
6. **Never modify a deployed migration** — create a new migration instead. Modifying deployed migrations causes state drift.
7. **Use transactions for multi-table operations** — partial commits are data corruption. If any step fails, everything rolls back.
8. **Validate data at both layers** — application validation AND database constraints (NOT NULL, CHECK, UNIQUE). Defense in depth.
9. **Use parameterized queries exclusively** — NEVER string concatenation for SQL. This prevents SQL injection attacks.
10. **Add `created_at` and `updated_at` timestamps** to all tables. Use database-level defaults for `created_at` and triggers or application logic for `updated_at`.
11. **Use consistent naming** — tables in `plural_snake_case`, columns in `singular_snake_case`. No abbreviations unless universally understood.
12. **Write seed scripts for development data** — never rely on production data for development. Seeds must be idempotent.
13. **Document the schema** — entity-relationship diagrams, data dictionary, and migration history. Keep docs in sync with actual schema.
