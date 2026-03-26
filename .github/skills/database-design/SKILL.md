---
name: database-design
description: "Full workflow for database schema design, migration planning, query optimization, and SQL security. Use when designing new schemas, writing migrations, optimizing queries, or auditing database code. Triggers on: database, schema, migration, SQL, query optimization, EXPLAIN."
---

# Database Design Skill

Complete workflow for database schema design, migration planning, query optimization, and SQL security auditing.

## When to Use

- Designing a new database schema or extending an existing one
- Writing or reviewing SQL queries for performance
- Planning database migrations (schema changes, data migrations)
- Optimizing slow queries using EXPLAIN plan analysis
- Auditing SQL code for injection vulnerabilities or anti-patterns
- When the user says "database", "schema", "query", "SQL", "migration", or "EXPLAIN"

## Pipeline

### Phase 1 — Requirements & Analysis

1. **Understand the data model** — identify entities, relationships, cardinality, constraints from requirements
2. **Survey existing schema** — read `src/models/`, existing migrations, `docs/CODE_INVENTORY.md`
3. **Identify query patterns** — what queries will run against this schema? Read/write ratio? Expected scale?

### Phase 2 — Schema Design

4. **Spawn Database Agent** — design the schema following normalization rules. Output: DDL, model files, relationship diagram
5. **Review constraints** — every FK has ON DELETE, every column has NOT NULL unless justified, CHECK constraints for domains
6. **Index strategy** — design indexes based on query patterns from Phase 1. Reference: [./references/indexing-strategy.md](./references/indexing-strategy.md)

### Phase 3 — Query Writing & Optimization

7. **Spawn SQL Query Agent** — write queries for all identified patterns. Use parameterized queries, explicit JOINs, CTEs
8. **EXPLAIN analysis** — run EXPLAIN on every query. Flag sequential scans, high-cost nodes, bad cardinality estimates
9. **Optimization pass** — rewrite flagged queries. Add missing indexes. Reference: [./references/query-patterns.md](./references/query-patterns.md)

### Phase 4 — Migration Planning

10. **Write migrations** — reversible up/down migrations. Separate schema from data migrations
11. **Non-blocking changes** — use CONCURRENTLY for index creation, batched updates for large data migrations
12. **Test rollback** — verify down migration restores previous state exactly

### Phase 5 — Security Audit

13. **Spawn Security Agent** — audit all queries for injection, access control, data exposure
14. **Parameterization check** — every user-facing query must use prepared statements
15. **Access control** — verify application uses least-privilege database roles

### Phase 6 — Review & Documentation

16. **Spawn Reviewer** — validate schema design, migration safety, query performance
17. **Update docs** — schema documentation, data flow updates, new model symbols in CODE_INVENTORY

## Reference Files

- [indexing-strategy.md](./references/indexing-strategy.md) — When and how to create indexes
- [query-patterns.md](./references/query-patterns.md) — Common query patterns and their optimized forms

## Playbook References

These playbooks are automatically included by the Librarian when this skill is active:

- `docs/playbooks/shared/database-design.playbook.md` — Schema design rules
- `docs/playbooks/shared/sql-optimization.playbook.md` — Query optimization rules
- `docs/playbooks/shared/sql-security.playbook.md` — SQL security rules
- `docs/playbooks/agents/database.playbook.md` — Database Agent rules
- `docs/playbooks/agents/sql-query.playbook.md` — SQL Query Agent rules
