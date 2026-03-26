+++
id = "technologies/postgresql"
title = "PostgreSQL Best Practices"
agents = ["all"]
technologies = ["postgresql", "sql"]
category = "rule"
tags = ["database", "postgresql", "sql", "relational"]
version = 1
+++

### Connection Management

- Use PgBouncer or pgpool-II for connection pooling — never let application instances open direct connections to PostgreSQL in production.
- Set `max_connections` conservatively (100–200) and rely on the pooler to multiplex; each connection consumes ~10 MB of RAM.
- Configure `idle_in_transaction_session_timeout` (e.g., 30s) to kill sessions that hold transactions open without activity.
- Set `statement_timeout` per role or session to prevent runaway queries from locking resources indefinitely.
- Use `pg_terminate_backend()` to clean up leaked connections rather than restarting the server.

### Schema Design

- Prefer `GENERATED ALWAYS AS IDENTITY` over `SERIAL` for auto-increment columns — IDENTITY follows the SQL standard and prevents accidental manual inserts.
- Use `uuid_generate_v4()` (from uuid-ossp) or `gen_random_uuid()` (PG 13+) for UUID primary keys; pair with a `USING INDEX TABLESPACE` clause on large tables.
- Store semi-structured data in `JSONB` (not `JSON`) — JSONB supports indexing and equality checks; JSON only stores text.
- Create `ENUM` types only for values that rarely change; for frequently changing sets, use a lookup table with a foreign key.
- Partition large tables (>100M rows) using declarative partitioning — prefer range partitioning on timestamp columns for time-series data.
- Add `NOT NULL` constraints by default; make columns nullable only when business logic requires it.

### Performance

- Run `ANALYZE` after bulk inserts or major data changes so the planner has up-to-date statistics.
- Tune autovacuum per-table for high-churn tables: lower `autovacuum_vacuum_scale_factor` (e.g., 0.01) and `autovacuum_analyze_scale_factor` (e.g., 0.005).
- Monitor table bloat with `pgstattuple` or `pg_stat_user_tables.n_dead_tup`; schedule manual `VACUUM FULL` only during maintenance windows when bloat exceeds 50%.
- Enable `pg_stat_statements` in `shared_preload_libraries` and query it regularly to identify the top-10 most time-consuming queries.
- Avoid wrapping read-only SELECT queries in CTEs when inlining would allow predicate pushdown — PG 12+ inlines non-recursive, non-side-effecting CTEs automatically, but `MATERIALIZED` forces the old behavior.
- Set `random_page_cost` to 1.1 (down from 4.0) when running on SSDs to help the planner favor index scans.
- Monitor TOAST table sizes for wide rows; consider splitting frequently accessed columns from large text/JSONB columns into separate tables.

### Indexes

- Create a GIN index on JSONB columns when querying with `@>`, `?`, or `?|` operators — e.g., `CREATE INDEX idx_data ON t USING GIN (data jsonb_path_ops)`.
- Use GiST indexes for range types (`tsrange`, `int4range`) and geometric data; GiST supports containment and overlap operators.
- Use BRIN indexes on naturally ordered large tables (e.g., append-only logs with a timestamp column) — BRIN indexes are 100x smaller than B-tree for sequential data.
- Create expression indexes for case-insensitive lookups: `CREATE INDEX idx_lower_email ON users (lower(email))` instead of using `LOWER()` in every query.
- Use `CREATE INDEX CONCURRENTLY` for production index creation to avoid locking writes; use `REINDEX CONCURRENTLY` (PG 12+) for rebuilding corrupt or bloated indexes.
- Add a partial index with a `WHERE` clause when queries filter on a fixed predicate — e.g., `CREATE INDEX idx_active ON orders (created_at) WHERE status = 'active'`.

### Security

- Enable Row-Level Security (RLS) on multi-tenant tables and define policies per-role — always test with `SET ROLE` to verify policy enforcement.
- Follow least-privilege: grant `CONNECT` on the database, `USAGE` on schemas, and only `SELECT`/`INSERT`/`UPDATE`/`DELETE` as needed — never grant `ALL PRIVILEGES` to application roles.
- Configure `pg_hba.conf` with `scram-sha-256` authentication (not `md5` or `trust`) and restrict `host` entries to specific CIDR ranges.
- Require SSL for all remote connections: set `ssl = on` in `postgresql.conf` and enforce `hostssl` entries in `pg_hba.conf`.
- Never embed credentials in connection strings checked into version control — use environment variables or a secrets manager.

### Reliability

- Set `wal_level = replica` (or `logical` if using logical replication) and configure `archive_mode = on` with `archive_command` for point-in-time recovery.
- Use streaming replication with at least one synchronous standby (`synchronous_commit = on`) for zero-data-loss requirements.
- Use logical replication for cross-version upgrades or selective table replication — be aware it does not replicate DDL.
- Test `pg_dump --format=custom` and `pg_restore --jobs=4` regularly; verify backup integrity by restoring to a staging instance on a schedule.
- Monitor replication lag via `pg_stat_replication.replay_lag` and alert when it exceeds your RPO threshold.

### Extensions

- Use `pg_trgm` with a GIN index for fuzzy text search: `CREATE INDEX idx_trgm ON t USING GIN (name gin_trgm_ops)` enables `LIKE '%term%'` to use the index.
- Use `pgcrypto` for hashing and encryption within the database — prefer `gen_random_bytes()` and `digest()` over application-level crypto when data must never leave the DB unencrypted.
- Install PostGIS for geospatial queries — use `geography` type for lat/lng distance calculations and `geometry` type for planar operations with a known SRID.
- Audit installed extensions with `SELECT * FROM pg_extension` and remove unused ones — each extension increases attack surface and upgrade complexity.
