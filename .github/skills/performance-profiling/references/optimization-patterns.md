# Optimization Patterns

Common optimization patterns with guidance on when to apply them. Ordered by typical ROI — algorithmic and I/O optimizations usually yield the largest gains.

---

## Algorithmic & Data Structure Patterns

### Memoization / Caching

Cache the result of expensive pure functions to avoid redundant computation.

- **When to apply:** A function is called repeatedly with the same arguments and has no side effects.
- **Implementation:** LRU cache (bounded size), dictionary lookup, or decorator-based (`@functools.lru_cache` in Python).
- **Watch out for:** Unbounded caches causing memory growth. Always set a max size. Invalidate when underlying data changes.

### Precomputation

Compute values ahead of time so they can be looked up in O(1) at query time.

- **When to apply:** A value is expensive to compute but is requested frequently with the same inputs. Lookup tables, pre-built indexes, materialized views.
- **Trade-off:** Increased startup time and memory usage for faster runtime queries.

### Lazy Evaluation

Defer computation until the result is actually needed. Avoid computing values that may never be used.

- **When to apply:** Building large data structures where only a subset is consumed. Generators, lazy iterators, virtual scrolling in UIs.
- **Watch out for:** Lazy evaluation can make debugging harder and introduce unexpected timing of side effects.

### Batch Processing

Group many small operations into fewer large operations to amortize overhead.

- **When to apply:** Many individual database inserts (batch into bulk insert), many small HTTP requests (batch API), many small file writes (buffer and flush).
- **Typical improvement:** 10-100x for I/O-bound operations where per-call overhead dominates.

### Pagination

Process or return data in bounded chunks instead of loading everything into memory.

- **When to apply:** Any query or API that could return unbounded results. Cursor-based pagination for real-time data, offset-based for static datasets.
- **Watch out for:** Offset pagination degrades at high offsets — prefer cursor/keyset pagination for large datasets.

---

## I/O & Network Patterns

### Async I/O

Use non-blocking I/O to overlap waiting with useful work. Essential for I/O-bound services.

- **When to apply:** Multiple independent external calls (database, HTTP, file) that currently execute sequentially.
- **Implementation:** `asyncio.gather()` in Python, `Promise.all()` in JavaScript, goroutines in Go.
- **Watch out for:** Async does not help CPU-bound work — it only helps when threads are waiting on I/O.

### Connection Pooling

Reuse established connections instead of creating new ones per request.

- **When to apply:** Any service making repeated connections to databases, HTTP services, or message queues.
- **Configuration:** Set pool size to match expected concurrency. Monitor pool wait time — if requests queue for connections, increase pool size or reduce hold time.

### Request Coalescing

Merge multiple concurrent requests for the same resource into a single request.

- **When to apply:** Cache stampede scenarios where many requests hit the same uncached key simultaneously. Also known as "single-flight" or "request deduplication."
- **Implementation:** Go `singleflight` package, custom in-flight request map with promise/future.

### Circuit Breakers

Fail fast when a dependency is down instead of waiting for timeouts.

- **When to apply:** Any external dependency that can become slow or unavailable. Prevents cascading failures and thread pool exhaustion.
- **Configuration:** Set failure threshold (e.g., 5 failures in 10 seconds), open duration (e.g., 30 seconds), then half-open to probe recovery.

---

## Data & Serialization Patterns

### Serialization Format Choice

Choose the serialization format based on the use case.

| Format | Speed | Size | Schema | Use Case |
|--------|-------|------|--------|----------|
| **JSON** | Moderate | Large | No | Human-readable APIs, config files |
| **MessagePack** | Fast | Compact | No | Internal APIs, caching, binary-safe JSON replacement |
| **Protocol Buffers** | Very fast | Very compact | Yes | High-throughput internal services, strict schema evolution |
| **Avro** | Fast | Compact | Yes | Event streaming, schema registry integration |

- **When to switch:** If profiling shows significant time in serialization/deserialization (common at high throughput), switch internal communication from JSON to a binary format.

### Compression

Reduce data size at the cost of CPU time.

- **When to apply:** Large payloads over the network (enable gzip/brotli), large objects in cache (compress before storing), log files.
- **Trade-off:** Compression uses CPU. For small payloads (<1KB), overhead may exceed savings. For large payloads, the network time saved usually dominates.

### Payload Reduction

Return only the data the consumer needs.

- **When to apply:** APIs returning large objects when clients use only a few fields. GraphQL field selection, sparse fieldsets in REST, database SELECT with specific columns instead of SELECT *.
- **Typical improvement:** 2-10x reduction in payload size, proportional reduction in serialization and network time.

---

## Database Patterns

### Indexing

Add indexes to columns used in WHERE, JOIN, and ORDER BY clauses.

- **When to apply:** Queries doing sequential scans on tables with more than a few thousand rows. Use EXPLAIN to verify.
- **Watch out for:** Over-indexing slows writes. Index only columns that appear in frequent query predicates. Composite indexes must match query column order.

### Denormalization

Duplicate data to avoid expensive joins at query time.

- **When to apply:** Read-heavy workloads where join performance is a bottleneck. Materialized views, precomputed aggregates, embedded documents.
- **Trade-off:** Increased storage, write complexity, and risk of data inconsistency. Only denormalize when read performance justifies it.

### Query Optimization

Restructure queries to use indexes effectively and minimize data scanned.

- **When to apply:** Any slow query. Start with EXPLAIN ANALYZE, look for sequential scans, sort overhead, and excessive row estimates.
- **Common fixes:** Add covering indexes, rewrite subqueries as joins, eliminate OR conditions with UNION, use EXISTS instead of IN for large subqueries.

---

## CDN & Caching Infrastructure

### CDN Offloading

Serve static and semi-static content from edge locations close to users.

- **When to apply:** Static assets (JS, CSS, images), API responses with Cache-Control headers, pre-rendered pages.
- **Configuration:** Set appropriate Cache-Control headers. Use `stale-while-revalidate` for content that can be briefly stale. Purge on deploy for versioned assets.

### Multi-Layer Caching

Design caches in layers, each with different characteristics.

| Layer | Location | Latency | Size | Use Case |
|-------|----------|---------|------|----------|
| **L1** | In-process memory | <1µs | Small (MB) | Hot keys, computed values, config |
| **L2** | Distributed (Redis) | 1-5ms | Medium (GB) | Shared state, session data, query results |
| **L3** | CDN / HTTP cache | 10-50ms | Large | Static assets, public API responses |

- **Invalidation:** L1 with short TTL (seconds), L2 with event-driven invalidation or moderate TTL (minutes), L3 with versioned URLs or purge API.

### Stale-While-Revalidate

Serve a stale cached response immediately while refreshing the cache in the background.

- **When to apply:** Content where brief staleness is acceptable (product listings, dashboards, feed content).
- **Benefit:** Users always get a fast response. Cache is refreshed asynchronously. Eliminates cache stampede.

---

## General Principles

1. **Profile before optimizing.** Intuition about where time is spent is wrong more often than right.
2. **Optimize the bottleneck.** Speeding up a function that accounts for 2% of total time yields at most 2% improvement.
3. **Algorithmic wins beat constant-factor wins.** Reducing O(n²) to O(n log n) matters more than shaving 10% off a loop body.
4. **I/O is almost always the bottleneck.** Network, disk, and database calls dominate in most web applications.
5. **Every cache is a consistency trade-off.** Know what staleness is acceptable before adding a cache.
6. **Measure after every change.** An optimization that doesn't show measurable improvement should be reverted.
