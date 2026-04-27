+++
id = "agents/observability"
title = "Observability Engineer Agent Playbook"
agents = ["observability"]
technologies = ["all"]
category = "rule"
tags = ["observability", "telemetry", "slo", "metrics", "traces", "logs"]
version = 1
+++

# Observability Engineer Playbook

## SLO Defaults

| Service tier | Availability SLO | Latency SLO (p99) | Window |
| --- | --- | --- | --- |
| User-facing critical | 99.9% | 300 ms | 30 days rolling |
| User-facing standard | 99.5% | 1 s | 30 days rolling |
| Internal API | 99.0% | 2 s | 30 days rolling |
| Async / batch | 99.0% freshness | N/A — use lag SLO | 7 days rolling |

Adjust per business need; document the rationale in the report.

## Metric Naming

- Snake_case, prefixed with service: `checkout_request_duration_seconds`.
- Histograms for durations; counters for events; gauges for current state.
- Labels: keep cardinality under control. Never use raw user IDs, URLs with IDs, free-text input.

## Mandatory Log Fields

Every log line must include:

- `timestamp` (ISO 8601, UTC)
- `level` (DEBUG / INFO / WARN / ERROR)
- `service`
- `trace_id` (when in a request context)
- `span_id` (when in a span)
- `event` (machine-readable event name)

Optional but encouraged: `user_id` (hashed), `tenant_id`, `request_id`, `duration_ms`.

Forbidden: PII, secrets, full request/response bodies of user data.

## Trace Span Rules

- One span per cross-service call.
- One span per external API / DB query.
- Span name = operation, not URL: `db.users.select_by_email`, not `/users/123`.
- Attach attributes for cardinality-safe metadata; never attach PII.

## Alert Rules

- Symptom-based: alert on SLO burn rate, not raw error count.
- Multi-window multi-burn-rate: short window (5m) for fast burn, long window (1h) for slow burn.
- Every alert has: severity, owner, runbook URL, mitigation hint.
- Forbidden: alerts that fire more than once per week without action — they cause alert fatigue.

## Dashboard Defaults

- **Overview dashboard** per service: RED metrics, top errors, recent deploys, SLO status.
- **CUJ dashboard** per critical journey: end-to-end latency, success rate, conversion at each step.
- **Resource dashboard** per stateful component: USE metrics.

## Coordination

- **Architect** — I review the architecture before Critic full review.
- **Monitoring Agent** — runs gap audits on existing instrumentation; my plan is its baseline.
- **Incident Commander** — uses my dashboards and runbooks during incidents.
- **Cost/FinOps** — high-cardinality metrics drive cost; coordinate.
