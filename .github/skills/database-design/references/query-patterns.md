# Query Patterns Reference

## Pagination

### Offset-Based (Simple, Not for Large Datasets)

```sql
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100;
```

**Problem:** Database still scans and discards `OFFSET` rows. Degrades with large offsets.

### Keyset (Cursor) Pagination (Preferred)

```sql
-- Page 1
SELECT * FROM orders ORDER BY id LIMIT 20;

-- Next pages: use last seen id
SELECT * FROM orders WHERE id > :last_id ORDER BY id LIMIT 20;
```

**Always use keyset pagination for APIs and large datasets.**

## Bulk Operations

### Bulk Insert

```sql
-- Single multi-row INSERT (not one INSERT per row)
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com'),
  ('Charlie', 'charlie@example.com');
```

### Bulk Update (Batched)

```sql
-- Update in batches to avoid long locks
UPDATE orders SET status = 'archived'
WHERE id IN (SELECT id FROM orders WHERE created_at < '2023-01-01' LIMIT 1000);
```

### Bulk Delete (Batched)

```sql
-- Delete in batches to avoid table-level locks
DELETE FROM logs WHERE id IN (
  SELECT id FROM logs WHERE created_at < NOW() - INTERVAL '90 days' LIMIT 5000
);
```

## JOIN Patterns

### Always Use Explicit JOINs

```sql
-- GOOD: explicit JOIN
SELECT o.id, u.name
FROM orders o
INNER JOIN users u ON u.id = o.user_id;

-- BAD: implicit join (comma syntax)
SELECT o.id, u.name FROM orders o, users u WHERE u.id = o.user_id;
```

### JOIN Order

Put the smaller table (or the table with more selective WHERE conditions) first. Most query planners handle this, but explicit ordering helps readability.

### Avoiding N+1

```sql
-- BAD: N+1 (one query per order to get user)
-- Application code: for each order, SELECT * FROM users WHERE id = order.user_id

-- GOOD: single JOIN
SELECT o.*, u.name FROM orders o JOIN users u ON u.id = o.user_id;

-- GOOD: batch IN query
SELECT * FROM users WHERE id IN (:user_id_1, :user_id_2, ...);
```

## Aggregation Patterns

### Conditional Aggregation (Avoid Multiple Queries)

```sql
-- GOOD: single query with FILTER
SELECT
  COUNT(*) FILTER (WHERE status = 'active') AS active_count,
  COUNT(*) FILTER (WHERE status = 'inactive') AS inactive_count,
  AVG(amount) FILTER (WHERE status = 'completed') AS avg_completed
FROM orders;

-- Alternative: CASE WHEN (works on all databases)
SELECT
  COUNT(CASE WHEN status = 'active' THEN 1 END) AS active_count,
  COUNT(CASE WHEN status = 'inactive' THEN 1 END) AS inactive_count
FROM orders;
```

### Window Functions (Running Totals, Rankings)

```sql
SELECT
  id,
  amount,
  SUM(amount) OVER (ORDER BY created_at) AS running_total,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
FROM orders;
```

## CTE Patterns

### Readable Multi-Step Queries

```sql
WITH active_users AS (
  SELECT id, name FROM users WHERE active = true
),
recent_orders AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE created_at > NOW() - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT u.name, COALESCE(o.order_count, 0) AS recent_orders
FROM active_users u
LEFT JOIN recent_orders o ON o.user_id = u.id;
```

**Note:** Some databases materialize CTEs (PostgreSQL < 12). Use subqueries if CTE forces materialization of a large result set.

## Anti-Patterns and Rewrites

| Anti-Pattern | Problem | Rewrite |
|---|---|---|
| `SELECT *` | Fetches unnecessary columns | List specific columns |
| `WHERE col LIKE '%value%'` | Cannot use index (leading wildcard) | Full-text search or `col LIKE 'value%'` |
| `WHERE UPPER(col) = 'VALUE'` | Function prevents index use | Create functional index or use `ILIKE` |
| `OR` across different columns | Hard to index | Use `UNION ALL` of two indexed queries |
| Correlated subquery in SELECT | Executes once per row | Rewrite as JOIN or window function |
| `COUNT(*)` on huge table | Full table scan | Use approximate count or materialized view |
| `NOT IN (subquery)` | Fails with NULLs | Use `NOT EXISTS` instead |
| `DISTINCT` to fix duplicates | Masks a bad JOIN | Fix the JOIN logic |
