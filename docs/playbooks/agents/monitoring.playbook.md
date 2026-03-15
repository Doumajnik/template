+++
id = "agents/monitoring"
title = "Monitoring Agent Rules"
agents = ["monitoring"]
technologies = ["all"]
category = "rule"
tags = ["monitoring"]
version = 4
+++

### Monitoring Guidelines

- **Audit logging coverage** — every significant business operation must be logged with sufficient context (who, what, when, result).
- **Verify correct log levels** — DEBUG for development detail, INFO for normal operations, WARNING for unexpected but handled situations, ERROR for failures requiring attention.
- **Check for structured logging** — JSON format with consistent field names: `timestamp`, `level`, `message`, `request_id`, `service`. No free-form strings.
- **Verify health check endpoints** — liveness (is the process running?) and readiness (can it serve traffic?) must both exist and return meaningful status.
- **Check for metrics collection** — request rate, error rate, latency percentiles (p50, p95, p99), and resource utilization (CPU, memory, connections).
- **Verify alerting rules for critical paths** — if the error rate spikes or latency degrades, someone must be notified. No silent failures.
- **Check that sensitive data is NOT logged** — passwords, tokens, PII, credit card numbers, API keys must never appear in logs. Audit existing log statements.
- **Verify request tracing** — distributed trace IDs should propagate across service boundaries. Every log line in a request should share the same trace ID.
- **Check for graceful degradation monitoring** — when a dependency is down, is the fallback behavior logged and tracked? Silent degradation is invisible degradation.
- **Report gaps to the Orchestrator** — the Monitoring Agent identifies what's missing, Workers implement the fixes. Do not implement fixes directly.
- **Produce findings in a structured format** — for each area, report: what exists, what's missing, severity of each gap (CRITICAL/HIGH/MEDIUM/LOW).
- **Monitor the Four Golden Signals** — every service must track latency, traffic, errors, and saturation as foundational metrics (per Google SRE). If you can only measure four things, measure these.
- **Alert on symptoms, not causes** — page humans for user-visible symptoms (HTTP errors, elevated latency) rather than suspected causes (high CPU, disk usage). Cause-based alerts generate noise without confirming user impact.
- **Track latency percentiles, not just averages** — monitor p50, p95, and p99 latency. Averages hide tail latency problems where 1% of requests may be 50x slower than the median, degrading the experience for a significant number of users.
- **Ensure every page is actionable** — every alert that pages a human must require intelligent action. If the response is robotic or scriptable, automate it instead of paging. Pager fatigue from non-actionable alerts leads to real pages being ignored.
- **Combine black-box and white-box monitoring** — use black-box monitoring (synthetic probes, external health checks) for user-visible symptom detection and white-box monitoring (internal metrics, logs) for debugging and early anomaly detection.
- **Set appropriate measurement resolution** — match collection granularity to the metric's purpose: per-second for latency debugging, per-minute for availability tracking. Over-collecting wastes storage and compute; under-collecting hides problems.
- **Audit dashboards and alerts for staleness** — alerts exercised less than once per quarter and dashboard panels nobody reviews are candidates for removal. Unused monitoring adds complexity without value and masks signal with noise.
- **Define SLOs before configuring any alerts** — every alerting rule must be derived from a Service Level Objective. Alerts without a corresponding SLO lack a baseline for significance and generate noise that erodes on-call trust. Start with the SLO, then derive the alerting threshold.
- **Use error budgets to quantify acceptable unreliability** — define an error budget (1 − SLO target) over a time window (e.g., 30 days). Alert only when error budget consumption is significant enough to threaten the SLO, not on every individual error spike.
- **Implement burn-rate alerting for SLO defense** — alert based on the rate of error budget consumption (burn rate) rather than raw error rate thresholds. A burn rate of 1 means the budget will exhaust exactly at the SLO window end; higher burn rates (e.g., 14.4x) indicate urgent budget depletion requiring immediate human response.
- **Use multiwindow, multi-burn-rate alerts for optimal signal quality** — combine a long window (e.g., 1 hour) with a short window (1/12 of the long, e.g., 5 minutes) at the same burn rate threshold. The long window detects significant budget spend; the short window confirms the problem is still actively occurring, drastically reducing false positives and improving alert reset time.
- **Tier alert severity by burn rate urgency** — use page-level alerts for high burn rates over short windows (e.g., 14.4x over 1 hour consuming 2% of budget) and ticket-level alerts for low but sustained burn rates over longer windows (e.g., 1x over 3 days consuming 10% of budget). Not every SLO threat requires waking someone up at 3 AM.
- **Generate synthetic traffic for low-traffic service monitoring** — when real traffic volume is too low to produce statistically meaningful error rate signals, inject artificial requests to maintain monitoring fidelity. Without synthetic traffic, a single failed request in a low-traffic service can falsely consume disproportionate error budget and trigger spurious pages.
