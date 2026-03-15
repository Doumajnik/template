+++
id = "agents/performance"
title = "Performance Agent Rules"
agents = ["performance"]
technologies = ["all"]
category = "rule"
tags = ["performance"]
version = 4
+++

### Performance Guidelines

- Measure before optimizing — never optimize without profiling data showing an actual bottleneck
- Focus on algorithmic complexity first: O(n²) algorithms with large datasets are the most impactful optimization targets
- Check for N+1 query problems in database access patterns
- Verify caching strategy: are expensive computations cached? Are caches invalidated correctly?
- Check for unnecessary I/O: redundant file reads, repeated API calls, unbatched database queries
- Verify pagination on large collections — never load all records into memory at once
- Check for memory leaks: unclosed resources, growing caches without eviction, circular references
- Profile hot paths — optimize the code that runs most frequently, not the code that looks slow
- Verify async operations are truly concurrent — check for accidental serialization of parallel work
- Check string concatenation in loops — use builders or join patterns for O(n) instead of O(n²)
- Report findings with metrics: before/after measurements, complexity analysis, memory usage
- CRITICAL findings (exponential algorithms, memory leaks) must be fixed — spawn Workers
- Establish performance baselines before making changes — record current metrics (response time, throughput, memory usage, P50/P95/P99 latencies) so improvements can be measured objectively against a known reference point
- Use distributed tracing to identify latency across service boundaries — single-service profiling misses network, serialization, and queue delays in distributed systems; correlate traces end-to-end
- Check for thread pool starvation and deadlocks — verify that async operations are truly non-blocking and not accidentally synchronizing on shared resources or starving the thread pool with blocking calls
- Profile memory allocation patterns, not just total memory usage — excessive short-lived allocations cause GC pressure and latency spikes even when peak memory usage looks acceptable
- Test performance under realistic production-like load — synthetic benchmarks with trivial data often miss real-world bottlenecks like lock contention, cache misses, connection pool exhaustion, and data skew
- Prefer lazy initialization and on-demand loading for expensive resources — avoid paying startup costs for data, connections, or computations that may never be used in a given request path
- Optimize for Core Web Vitals when profiling web applications — measure Largest Contentful Paint (LCP) for perceived load speed, Cumulative Layout Shift (CLS) for visual stability, and Interaction to Next Paint (INP) for responsiveness; these are the metrics that directly correlate with user experience (ref: web.dev)
- Apply lazy loading for below-the-fold images, iframes, and non-critical resources — defer loading of content not visible in the initial viewport to reduce initial page load time and bandwidth consumption
- Use code splitting and tree shaking to minimize bundle sizes — split application code into smaller chunks loaded on demand, and configure the build tool to eliminate dead (unreachable) code from production bundles; analyze bundle composition with source map explorers
- Use modern, efficient asset formats — prefer AVIF/WebP over JPEG/PNG for images, use WOFF2 for fonts, and enable Brotli/gzip compression for text assets; format selection alone can reduce payload sizes by 30-50%
- Monitor and prevent layout shifts — reserve explicit dimensions for images, ads, and dynamically injected content; unexpected layout shifts degrade user experience and indicate missing size attributes or late-loading elements that push content around
- Use connection pooling and keep-alive for backend services — creating a new TCP/TLS connection per request adds significant latency; reuse connections to databases, HTTP APIs, and caches via connection pools with appropriate sizing and idle timeout configuration
