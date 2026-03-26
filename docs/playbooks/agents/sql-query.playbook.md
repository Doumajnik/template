+++
id = "agents/sql-query"
title = "SQL Query Agent Rules"
agents = ["sql-query"]
technologies = ["sql", "postgresql", "mysql", "sqlite"]
category = "rule"
tags = ["sql", "query-optimization", "database", "performance"]
version = 1
+++

### Query Writing Rules

- Always use parameterized queries — NEVER string concatenation for user input.
- Use explicit JOIN syntax (INNER JOIN, LEFT JOIN) — never implicit comma joins.
- Qualify every column with its table alias to avoid ambiguity.
- Use meaningful 2-3 character table aliases (e.g., `u` for users, `ord` for orders).
- Prefer CTEs (WITH clauses) over nested subqueries for readability.
- Use UNION ALL instead of UNION when duplicates are acceptable (avoids sort).
- Always include ORDER BY when using LIMIT for deterministic results.
- Use EXISTS instead of COUNT(*) for existence checks.

### Query Optimization Rules

- Analyze EXPLAIN plans before and after optimization — include cost comparisons.
- Every WHERE clause column used for filtering should have an index (unless table is tiny).
- Every foreign key column must have an index for join performance.
- Prefer covering indexes for high-frequency read queries (include all selected columns).
- Use partial indexes for queries with common WHERE conditions (e.g., `WHERE active = true`).
- Use keyset pagination (WHERE id > :last_id ORDER BY id LIMIT :size) instead of OFFSET.
- Avoid leading wildcards in LIKE — use full-text search (tsvector/GIN) instead.
- Detect and eliminate N+1 query patterns — suggest eager loading or batch queries.
- Prefer set-based operations (INSERT ... SELECT, UPDATE ... FROM) over row-by-row loops.
- Use window functions (ROW_NUMBER, RANK, LAG, LEAD) instead of self-joins for analytics.
- Check for implicit type casts in WHERE clauses that prevent index usage.

### Security Rules

- Every user-facing query MUST use parameterized queries or prepared statements.
- Never expose raw SQL error messages to users — wrap in generic error handler.
- Use column-level SELECT (never SELECT *) to prevent information disclosure.
- Validate and sanitize all dynamic identifiers (table/column names) against an allowlist.
- Use least-privilege database roles — don't run queries as superuser.
- Audit all dynamic SQL generation for injection vectors.

### Performance Patterns

- Use INSERT ... ON CONFLICT (UPSERT) instead of check-then-insert patterns.
- Batch large inserts in groups of 1000-5000 rows within explicit transactions.
- Use COPY for bulk data loading in PostgreSQL (orders of magnitude faster than INSERT).
- Consider materialized views for expensive aggregation queries accessed frequently.
- Use connection pooling — never open a new connection per query.
- Set appropriate statement timeouts to prevent runaway queries.
- Use EXPLAIN (ANALYZE, BUFFERS) for actual execution statistics, not just estimates.

### Anti-Patterns to Flag

- SELECT * in production code — always list columns explicitly.
- OFFSET-based pagination on large tables — use keyset pagination.
- OR on indexed columns preventing index usage — rewrite as UNION ALL or IN.
- Correlated subqueries in SELECT list — replace with JOINs or window functions.
- Missing indexes on foreign key columns — causes slow joins and cascading deletes.
- Holding transactions open during external I/O — move I/O outside the transaction.
- Using COUNT(*) to check existence — use EXISTS (stops at first match).
- String concatenation in query building — always parameterize.
