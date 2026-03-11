+++
id = "agents/monitoring"
title = "Monitoring Agent Rules"
agents = ["monitoring"]
technologies = ["all"]
category = "rule"
tags = ["monitoring"]
version = 2
+++

### Monitoring Guidelines

1. **Audit logging coverage** — every significant business operation must be logged with sufficient context (who, what, when, result).
2. **Verify correct log levels** — DEBUG for development detail, INFO for normal operations, WARNING for unexpected but handled situations, ERROR for failures requiring attention.
3. **Check for structured logging** — JSON format with consistent field names: `timestamp`, `level`, `message`, `request_id`, `service`. No free-form strings.
4. **Verify health check endpoints** — liveness (is the process running?) and readiness (can it serve traffic?) must both exist and return meaningful status.
5. **Check for metrics collection** — request rate, error rate, latency percentiles (p50, p95, p99), and resource utilization (CPU, memory, connections).
6. **Verify alerting rules for critical paths** — if the error rate spikes or latency degrades, someone must be notified. No silent failures.
7. **Check that sensitive data is NOT logged** — passwords, tokens, PII, credit card numbers, API keys must never appear in logs. Audit existing log statements.
8. **Verify request tracing** — distributed trace IDs should propagate across service boundaries. Every log line in a request should share the same trace ID.
9. **Check for graceful degradation monitoring** — when a dependency is down, is the fallback behavior logged and tracked? Silent degradation is invisible degradation.
10. **Report gaps to the Orchestrator** — the Monitoring Agent identifies what's missing, Workers implement the fixes. Do not implement fixes directly.
11. **Produce findings in a structured format** — for each area, report: what exists, what's missing, severity of each gap (CRITICAL/HIGH/MEDIUM/LOW).
