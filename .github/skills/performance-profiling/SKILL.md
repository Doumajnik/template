---
name: performance-profiling
description: "Full performance profiling and optimization workflow. Covers CPU profiling, memory analysis, algorithmic complexity, database query optimization, and caching strategies. Use when optimizing slow code, investigating memory leaks, or establishing performance baselines. Triggers on: performance, profiling, slow, optimize, memory leak, latency, throughput, benchmark."
---

# Performance Profiling Skill

Systematic workflow for identifying and resolving performance bottlenecks. Every optimization must be measurement-driven — never optimize without profiling first.

## Core Principle

**Measure → Identify → Fix → Verify.** No speculative optimization. Every change must show measurable improvement against the baseline.

---

## Pipeline Phases

### Phase 1: Baseline Measurement

Establish current performance metrics before any optimization. Without a baseline, you cannot prove improvement.

1. Define the performance scenario (which endpoint, function, or workflow is slow)
2. Identify the metric that matters: latency (p50/p95/p99), throughput (req/s), memory usage, CPU time
3. Run the scenario under realistic load (not just one request — use representative data volumes)
4. Record baseline metrics in a structured format:
   - **Latency**: p50, p95, p99, max
   - **Throughput**: requests/second or operations/second
   - **Memory**: peak RSS, heap usage, allocation rate
   - **CPU**: user time, system time, utilization percentage
5. Save the baseline to the performance report — all future measurements compare against this
6. Set a target: "reduce p95 latency from 800ms to under 200ms" — concrete and measurable

**Output:** Baseline metrics document with scenario description, measurement methodology, and improvement target.

### Phase 2: Hotspot Identification

CPU profiling to find the functions consuming the most time. Start broad, then narrow.

1. Select the appropriate profiler for the language/runtime (see `./references/profiling-tools.md`)
2. Run the profiler under the same scenario as the baseline — same data, same load
3. Generate a flame graph for visual inspection — wide bars are your hotspots
4. Identify the top 5 functions by cumulative CPU time
5. Distinguish between self-time (time in the function itself) and total-time (including callees)
6. Check for unexpected hotspots: serialization, logging, regex compilation, repeated parsing
7. Flag any function where self-time exceeds 10% of total execution time

**Output:** Ranked list of hotspot functions with file paths, self-time, total-time, and call counts.

### Phase 3: Memory Analysis

Heap snapshots, allocation tracking, and leak detection.

1. Take heap snapshots at: startup, after warmup, under load, and after load stops
2. Compare snapshots to identify growing allocations (potential leaks)
3. Track allocation rate — high allocation rate causes GC pressure even without leaks
4. Look for: large retained objects, duplicate strings, unbounded caches, event listener accumulation
5. Check for common leak patterns:
   - Closures capturing large scopes
   - Global collections that grow but never shrink
   - Circular references preventing GC (in reference-counted runtimes)
   - Unclosed resources (file handles, database connections, HTTP connections)
6. Profile GC behavior — frequency, pause duration, promotion rate

**Output:** Memory profile report with leak suspects, allocation hotspots, and GC analysis.

### Phase 4: Algorithmic Review

Spawn the Performance Agent to analyze computational complexity.

1. Review hotspot functions from Phase 2 for algorithmic complexity
2. Identify any O(n²) or worse algorithms — nested loops over collections, repeated linear searches
3. Check data structure choices: using lists where sets/maps would be O(1) lookup
4. Look for accidental quadratic behavior: string concatenation in loops, repeated array filtering
5. Analyze sort operations — are they necessary? Can data arrive pre-sorted?
6. Check for redundant computation — same value calculated multiple times in a loop
7. Propose algorithmic improvements with expected complexity reduction

**Output:** Complexity analysis with specific functions, current Big-O, proposed Big-O, and implementation approach.

### Phase 5: Database Profiling

Slow query analysis, connection pool monitoring, and N+1 detection. Uses the SQL Query Agent for query optimization.

1. Enable slow query logging (threshold: 100ms for OLTP, 1s for reporting)
2. Capture query execution plans (EXPLAIN ANALYZE) for slow queries
3. Detect N+1 query patterns — look for repeated identical queries with different parameters in a single request
4. Check index usage — sequential scans on large tables, missing composite indexes
5. Monitor connection pool: utilization, wait time, checkout duration, pool exhaustion events
6. Check for lock contention — long-held transactions, deadlock frequency
7. Review ORM-generated queries — ORMs often generate suboptimal SQL
8. Spawn the SQL Query Agent for complex query optimization

**Output:** Slow query report with execution plans, N+1 instances, missing indexes, and connection pool metrics.

### Phase 6: I/O Analysis

Network calls, file I/O, serialization overhead, and unnecessary blocking operations.

1. Trace all external calls (HTTP, gRPC, database, cache, message queue) with timing
2. Identify sequential external calls that could be parallelized
3. Measure serialization/deserialization time — often a hidden cost at scale
4. Check for synchronous I/O in async contexts (blocking the event loop or thread pool)
5. Look for unnecessary I/O: reading files that could be cached, redundant API calls
6. Measure DNS resolution, TLS handshake, and connection establishment overhead
7. Check payload sizes — over-fetching from APIs, returning unused fields

**Output:** I/O trace showing all external calls, their latency, and parallelization opportunities.

### Phase 7: Caching Strategy

Identify cacheable computations and design appropriate cache layers.

1. Identify computations or queries whose results are reused — candidates for caching
2. Classify cache candidates by volatility:
   - **Static**: configuration, feature flags — cache at startup, refresh on signal
   - **Slow-changing**: user profiles, product catalog — TTL-based (minutes to hours)
   - **Request-scoped**: computed values used multiple times in one request — per-request memoization
3. Design cache layers:
   - **L1 (in-process)**: LRU cache for hot data, zero network overhead
   - **L2 (distributed)**: Redis/Memcached for shared state across instances
   - **HTTP cache**: Cache-Control headers, ETags, CDN offloading for static assets
4. Define cache invalidation strategy — TTL, event-driven, or write-through
5. Estimate memory cost of each cache — set max sizes to prevent unbounded growth
6. Plan for cache stampede prevention: lock-based refresh, stale-while-revalidate

**Output:** Caching design document with cache layers, TTLs, invalidation strategy, and memory budget.

### Phase 8: Optimization Implementation

Spawn Workers to implement targeted fixes — one optimization at a time, measure after each.

1. Prioritize optimizations by expected impact (Phase 2-7 findings) and implementation effort
2. Implement one optimization at a time — never batch multiple changes
3. After each optimization:
   - Run the same profiling scenario as the baseline
   - Record the new metrics
   - Calculate improvement: `(baseline - new) / baseline * 100%`
   - If improvement is less than 5%, consider reverting — the complexity may not be worth it
4. Common optimization order (highest ROI first):
   - Fix N+1 queries and add missing indexes
   - Add caching for expensive repeated computations
   - Replace O(n²) algorithms with O(n log n) or O(n)
   - Parallelize independent I/O operations
   - Reduce payload sizes and serialization overhead
5. After all optimizations, run the full scenario and compare against the original baseline

**Output:** Optimization log showing each change, its measured impact, and cumulative improvement.

### Phase 9: Regression Testing

Run load tests to verify improvements hold under realistic load and detect regressions.

1. Run the load test scenario that matches production traffic patterns
2. Verify latency targets are met at expected concurrency levels
3. Check for latency degradation under sustained load (resource leaks, GC pressure)
4. Monitor error rates — optimization must not increase failures
5. Test edge cases: cold start performance, cache-miss storms, connection pool exhaustion
6. Compare final metrics against the baseline and the target:
   - ✅ Target met: proceed to documentation
   - ⚠️ Improved but below target: document what was achieved, plan next iteration
   - ❌ Regression detected: revert the offending change, investigate

**Output:** Load test results with comparison against baseline and target metrics.

### Phase 10: Documentation

Update performance baselines and document optimization decisions for future reference.

1. Update the performance baseline document with new metrics
2. Document each optimization decision:
   - What was slow and why (root cause)
   - What was changed (the fix)
   - Measured improvement (before/after numbers)
   - Trade-offs accepted (memory for speed, complexity for performance)
3. Record any optimizations considered but rejected — and why
4. Update monitoring dashboards and alert thresholds if latency baselines changed
5. Add performance-related findings to the project playbook for future reference

**Output:** Updated performance baseline, optimization decision log, and playbook entries.

---

## Key Rules

- **Never optimize without measuring first.** Gut-feel optimization wastes time and often makes things worse.
- **One change at a time.** Multiple simultaneous changes make it impossible to attribute improvement.
- **Profile in production-like conditions.** Profiling with toy data gives misleading results.
- **Prefer algorithmic improvements over micro-optimizations.** Reducing O(n²) to O(n) beats shaving cycles.
- **Cache invalidation is harder than caching.** Design the invalidation strategy before implementing the cache.
- **Set concrete targets.** "Make it faster" is not a goal. "Reduce p95 from 800ms to 200ms" is.
- **Document trade-offs.** Every optimization has a cost — make it explicit.

## Reference Files

- [Profiling Tools by Language](./references/profiling-tools.md)
- [Optimization Patterns](./references/optimization-patterns.md)
