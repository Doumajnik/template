+++
id = "agents/load-testing"
title = "Load Testing Agent Playbook"
agents = ["load-testing"]
technologies = ["k6", "locust", "performance"]
category = "rule"
tags = ["load-testing", "performance", "slo", "benchmarking"]
version = 1
+++

### Test Design

- Always define clear SLOs (p50/p95/p99 latency, throughput, error rate, concurrent users) before writing any test script — tests without targets produce meaningless data
- Design test scenarios that model realistic user behavior — include think times, session flows, and varied payloads rather than synthetic request floods
- Cover all five scenario types for critical systems: smoke, load (steady state), stress, spike, and soak — each reveals different failure modes
- Include warm-up and cool-down phases in every test scenario — cold caches, JIT compilation, and connection pool initialization skew early measurements
- Test one variable at a time when diagnosing bottlenecks — changing multiple parameters simultaneously makes root cause attribution impossible
- Prioritize testing critical user flows end-to-end over individual endpoint bombardment — real performance issues emerge from realistic interaction patterns
- Include negative path testing under load — error handling paths often perform worse than happy paths and reveal hidden bottlenecks

### SLO Definition

- Set latency targets per endpoint, not globally — a search endpoint has different acceptable latency than a health check
- Define SLOs at multiple percentiles (p50, p95, p99) — averages hide tail latency problems that affect real users
- Include error rate thresholds as pass/fail criteria — a fast response that's wrong is worse than a slow correct one
- Set resource utilization ceilings (CPU < 70%, memory < 80%) — systems operating near capacity have no headroom for traffic spikes
- Document all SLO assumptions explicitly — test environment specs, data volume, network conditions, and any differences from production
- Revisit SLOs after every major release or infrastructure change — stale targets lead to false confidence

### Script Patterns

- Parameterize all test data using external CSV/JSON files — never hardcode user credentials, IDs, or payloads in test scripts
- Use correlation to extract dynamic values (tokens, IDs, session keys) from responses for subsequent requests — hardcoded values break under concurrent load
- Tag every request with endpoint name, scenario type, and user flow — untagged requests are impossible to analyze at scale
- Handle authentication in setup/teardown phases — token generation should not count toward measured latency
- Keep individual test functions under 40 lines — complex scripts are harder to debug and maintain than composed simple ones
- Use custom metrics (Rate, Trend, Counter) for business-specific measurements beyond built-in HTTP metrics
- Structure scripts as modular, composable scenarios — reuse common flows (login, browse, checkout) across different test types
- Generate test data that reflects production cardinality and distribution — uniform synthetic data misses hotspot and skew issues

### Result Analysis

- Compare every test run against the established baseline — absolute numbers are meaningless without a reference point
- Analyze latency distributions, not just averages — a p50 of 50ms with p99 of 5s indicates a serious tail latency problem
- Correlate error spikes with load ramp events — errors that appear only above a specific concurrency level indicate resource saturation
- Identify the first resource to saturate (CPU, memory, connections, I/O, network) — that resource is the scaling bottleneck
- Run at least 2-3 iterations of each scenario — a single run may reflect transient conditions rather than true system behavior
- Track performance trends across releases — gradual degradation often goes unnoticed without historical comparison
- Check for memory leaks in soak test results — monitor for steadily increasing memory usage or decreasing available connections over time
- Analyze error type distribution, not just error rate — distinguish between 429 rate limits, 503 overload, timeout errors, and application errors

### Anti-Patterns

- Never run load tests against production without explicit approval and safeguards — use staging environments or feature flags to isolate test traffic
- Never use a single virtual user count as "the load test" — real load varies; test multiple levels to understand scaling characteristics
- Never skip the smoke test phase — broken scripts waste hours of load test execution time and produce garbage data
- Never ignore infrastructure monitoring during tests — load test client metrics alone miss server-side resource exhaustion, GC pauses, and network saturation
- Never test from a single geographic location if users are distributed — network latency and CDN behavior vary significantly by region
- Never assume test environment performance matches production — document all environment differences and apply appropriate scaling factors to results
