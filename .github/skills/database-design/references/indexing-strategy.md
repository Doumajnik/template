# Indexing Strategy Reference

## When to Create an Index

- Column appears in WHERE, JOIN, or ORDER BY for frequent queries
- Foreign key columns (always index these)
- Columns used in GROUP BY or DISTINCT
- Columns with high selectivity (many distinct values relative to row count)

## When NOT to Create an Index

- Small tables (< 1000 rows) — sequential scan is usually faster
- Columns rarely used in queries
- Columns with very low cardinality (e.g., boolean) unless used with other columns
- Write-heavy tables where insert performance matters more than read

## Index Types

### B-Tree (Default)

Best for: equality, range queries, ORDER BY, BETWEEN.

```sql
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_orders_date ON orders (created_at DESC);
```

### Composite (Multi-Column)

Best for: queries that filter on multiple columns together. Column order matters — put the most selective column first.

```sql
-- For: WHERE status = 'active' AND created_at > '2024-01-01'
CREATE INDEX idx_orders_status_date ON orders (status, created_at);
```

**Rule:** A composite index on (A, B, C) supports queries on (A), (A, B), and (A, B, C) but NOT (B) or (C) alone.

### Covering Index (INCLUDE)

Best for: queries that only read indexed columns — avoids heap lookup entirely.

```sql
-- For: SELECT email, name FROM users WHERE email = ?
CREATE INDEX idx_users_email_cover ON users (email) INCLUDE (name);
```

### Partial Index

Best for: queries that always filter on a specific condition (e.g., only active records).

```sql
CREATE INDEX idx_users_active ON users (email) WHERE active = true;
```

### GIN (Generalized Inverted Index) — PostgreSQL

Best for: JSONB containment, full-text search, array operations.

```sql
CREATE INDEX idx_data_gin ON events USING GIN (metadata);
CREATE INDEX idx_search_gin ON articles USING GIN (to_tsvector('english', title || ' ' || body));
```

### GiST (Generalized Search Tree) — PostgreSQL

Best for: geometric data, range types, nearest-neighbor queries.

```sql
CREATE INDEX idx_location ON places USING GIST (coordinates);
```

## Sizing and Maintenance

- Monitor index usage: `pg_stat_user_indexes` (PostgreSQL)
- Remove unused indexes — they slow writes with no read benefit
- REINDEX periodically for heavily-updated tables
- Use CONCURRENTLY for creating indexes on live tables:

```sql
CREATE INDEX CONCURRENTLY idx_large_table_col ON large_table (col);
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Index every column | Slows writes, wastes storage | Index based on query patterns only |
| Redundant indexes | (A, B) makes (A) redundant | Drop the single-column index |
| Wrong column order | Composite index not used | Put most selective column first |
| Missing FK indexes | Slow JOINs, slow cascading deletes | Always index foreign keys |
| Never reviewing usage | Unused indexes accumulate | Audit `pg_stat_user_indexes` quarterly |
