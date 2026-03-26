+++
id = "shared/sql-optimization"
title = "SQL Optimization Rules"
agents = ["all"]
technologies = ["sql", "postgresql", "mysql", "sqlite", "mssql"]
category = "rule"
tags = ["sql", "performance", "optimization", "database", "indexing"]
version = 1
+++

### Index Strategy

- Every foreign key column MUST have an index — prevents slow joins and cascading deletes.
- Create composite indexes in selectivity order (most selective column first).
- Use covering indexes for high-frequency read queries — include all columns in the SELECT.
- Use partial indexes for queries with common filters (e.g., `CREATE INDEX idx_active ON users(email) WHERE active = true`).
- Don't over-index: each index adds write overhead and storage cost. Justify every index with a query pattern.
- Review indexes quarterly — drop unused indexes using `pg_stat_user_indexes` (PostgreSQL) or equivalent.
- Use INCLUDE columns (PostgreSQL 11+) instead of making all columns part of the index key.

### EXPLAIN Plan Analysis

- Always check EXPLAIN before deploying a new or modified query to production.
- Use `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` for real execution stats, not just estimates.
- Red flags in EXPLAIN output: Seq Scan on large tables, Nested Loop with high row estimates, Sort with large external merge.
- Target: every production query should show Index Scan or Index Only Scan on the primary filter.
- If a Seq Scan appears on a table >10K rows, investigate missing indexes.
- Watch for `rows=1 (actual rows=50000)` — bad cardinality estimates cause bad plans. Run ANALYZE.

### Join Optimization

- Prefer EXISTS over IN for correlated subqueries with large result sets (stops at first match).
- Use LATERAL joins for row-dependent subqueries instead of correlated subqueries in SELECT.
- Ensure join columns have matching types — implicit casts prevent index usage.
- For self-joins on large tables, consider window functions (ROW_NUMBER, LAG/LEAD) instead.
- Join order matters for the planner — put the most selective table first in complex queries.
- Use INNER JOIN when NULLs are never expected; reserve LEFT JOIN for optional relationships.

### N+1 Query Detection and Prevention

- Symptom: a loop that executes one query per iteration (`for user in users: user.orders`).
- Fix: use eager loading (`SELECT_RELATED`, `prefetch_related` in Django; `Include()` in EF Core; `joinedload` in SQLAlchemy).
- Alternative: batch the IDs and use `WHERE id IN (:ids)` with a single query.
- In GraphQL: use DataLoader pattern to batch and cache per-request.
- In REST APIs: support `?include=orders` expand parameters to avoid downstream N+1s.

### Pagination

- NEVER use OFFSET for deep pagination — it scans and discards N rows.
- Use keyset pagination: `WHERE id > :last_id ORDER BY id LIMIT :page_size`.
- For user-facing tables: cursor-based pagination with encoded cursors (base64 of last row key).
- For admin/internal tools: OFFSET is acceptable for small datasets (<10K rows).
- Always include a deterministic ORDER BY — without it, pagination results are non-deterministic.

### Bulk Operations

- Batch INSERT in groups of 1000-5000 rows for optimal throughput.
- Use COPY (PostgreSQL) or LOAD DATA (MySQL) for millions of rows — 10-100x faster than INSERT.
- Use INSERT ... ON CONFLICT (upsert) instead of check-then-insert patterns.
- Wrap bulk operations in explicit transactions — auto-commit per row is catastrophically slow.
- For large UPDATEs, batch by range (`WHERE id BETWEEN :start AND :end`) to avoid lock escalation.

### Query Security

- ALWAYS use parameterized queries — no string concatenation or interpolation for user input.
- Sanitize dynamic identifiers (table/column names) against a strict allowlist — never pass user input as identifiers.
- Use column-level SELECT instead of SELECT * to prevent information disclosure.
- Set statement timeouts to prevent resource exhaustion from runaway queries.
- Log slow queries (>100ms) for monitoring; alert on queries >1s.
- Never expose raw database errors to end users — wrap in generic error handlers.

### Common Anti-Patterns

- `SELECT *` — wastes bandwidth, breaks on schema changes, leaks sensitive columns.
- `LIKE '%term%'` — no index usage with leading wildcard. Use full-text search instead.
- `COUNT(*) WHERE ...` for existence — use `EXISTS` (stops at first match).
- `OR` on different indexed columns — prevents index usage. Rewrite as UNION ALL.
- `DISTINCT` to mask duplicate joins — fix the join instead.
- `ORDER BY RANDOM()` — scans entire table. Use `TABLESAMPLE` or pre-selected random IDs.
- Nested subqueries 3+ levels deep — refactor to CTEs for readability and optimizer hints.
