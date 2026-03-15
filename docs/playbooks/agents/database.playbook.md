+++
id = "agents/database"
title = "Database Agent Rules"
agents = ["database"]
technologies = ["all"]
category = "rule"
tags = ["database"]
version = 4
+++

### Database Guidelines

- **Design schemas in 3NF by default** — denormalize only with measured performance justification. Premature denormalization is premature optimization.
- **Every table must have a primary key** — prefer UUIDs over auto-increment for distributed systems. Auto-increment is acceptable for single-node databases.
- **Add indexes on columns used in WHERE, JOIN, and ORDER BY** — but don't over-index. Every index slows writes. Measure before adding.
- **Foreign keys must have explicit ON DELETE behavior** — CASCADE, SET NULL, or RESTRICT. Never leave it unspecified.
- **Write migrations as up/down pairs** — every migration must be reversible. Test the down migration before deploying the up.
- **Never modify a deployed migration** — create a new migration instead. Modifying deployed migrations causes state drift.
- **Use transactions for multi-table operations** — partial commits are data corruption. If any step fails, everything rolls back.
- **Validate data at both layers** — application validation AND database constraints (NOT NULL, CHECK, UNIQUE). Defense in depth.
- **Use parameterized queries exclusively** — NEVER string concatenation for SQL. This prevents SQL injection attacks.
- **Add `created_at` and `updated_at` timestamps** to all tables. Use database-level defaults for `created_at` and triggers or application logic for `updated_at`.
- **Use consistent naming** — tables in `plural_snake_case`, columns in `singular_snake_case`. No abbreviations unless universally understood.
- **Write seed scripts for development data** — never rely on production data for development. Seeds must be idempotent.
- **Document the schema** — entity-relationship diagrams, data dictionary, and migration history. Keep docs in sync with actual schema.
- **Design multi-column indexes with column order in mind** — place the most selective column first in composite indexes. The column order determines which queries the index can optimize; a `(status, created_at)` index cannot serve a query that filters only on `created_at`.
- **Use covering indexes to avoid table lookups** — include frequently selected columns in the index (via INCLUDE clause or appending to the key) to enable index-only scans and eliminate expensive random table access.
- **Avoid function calls on indexed columns in WHERE clauses** — wrapping an indexed column in a function (e.g., `UPPER(name)`, `YEAR(created_at)`) prevents the optimizer from using the index. Use functional indexes or rewrite the query to compare against pre-computed values.
- **Implement pagination with the keyset (seek) method** — use `WHERE id > :last_seen ORDER BY id LIMIT N` instead of `OFFSET`. Offset-based pagination degrades linearly as the offset grows because the database must scan and discard all skipped rows.
- **Plan for schema evolution from day one** — design tables with future extension in mind: use nullable columns for optional fields, avoid rigid ENUMs that require migrations to extend, and prefer additive-only changes over destructive ones.
- **Benchmark migrations against production-size data** — a migration that runs in milliseconds on a dev database may lock a production table for minutes. Always test migrations against realistic data volumes before deploying.
- **Configure connection pooling explicitly** — never let the application open unlimited database connections. Set connection pool min/max sizes, idle timeouts, and connection validation queries. Runaway connections are the most common cause of production database outages.
- **Use pipelined Top-N queries instead of unbounded sorts** — always use FETCH FIRST / LIMIT / TOP to inform the optimizer that only a subset of rows is needed. Without top-N syntax, the database cannot choose a pipelined order-by execution that delivers rows directly from an index, resulting in full table scans and expensive materialized sorts.
- **Prefer window functions over self-joins for analytical queries** — use ROW_NUMBER(), RANK(), LAG(), LEAD() and other window functions for row numbering, running totals, and peer comparisons. Window functions express intent clearly and allow the optimizer to use pipelined execution plans, while equivalent self-joins produce redundant table scans.
- **Prefer CTEs over deeply nested subqueries for readability** — use Common Table Expressions (WITH clauses) to name and decompose complex queries into logical steps. CTEs improve maintainability and make query intent explicit, but verify that the optimizer materializes or inlines them appropriately for your specific database engine.
- **Use materialized views for expensive repeated aggregations** — pre-compute costly aggregate queries as materialized views with defined refresh strategies (on-commit, on-demand, or periodic). Verify that the refresh cost is less than the cumulative query cost it replaces, and monitor for data staleness.
- **Always analyze query execution plans before and after index changes** — use EXPLAIN ANALYZE (PostgreSQL), EXPLAIN (MySQL), or SET STATISTICS IO ON (SQL Server) to verify that the optimizer uses the intended execution plan. Never assume an index will be used — the optimizer may choose a full scan if table statistics suggest it is cheaper.
- **Monitor and update table statistics regularly** — stale statistics cause the query optimizer to choose suboptimal execution plans. Schedule regular ANALYZE / UPDATE STATISTICS runs, especially after bulk data loads, large DELETE operations, or schema changes that affect data distribution.
