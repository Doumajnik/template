+++
id = "shared/telemetry-conventions"
title = "Telemetry Conventions (shared)"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["telemetry", "observability", "metrics", "traces", "logs", "shared"]
version = 1
+++

# Telemetry Conventions (shared)

Universal rules for emitting metrics, traces, and logs. Applies to every code-writing agent (Worker, Frontend Component, Refactor, Migration). The Observability Engineer designs the telemetry plan; this playbook defines the conventions everyone follows when implementing it.

## Three Pillars

- **Metrics** — aggregate signals (rates, durations, gauges). Cheap to query at scale.
- **Traces** — per-request causal chains. Most useful for cross-service flows.
- **Logs** — discrete events with context. Most useful for debugging individual requests.

## Metric Conventions

- Snake_case, prefixed with service: `checkout_request_duration_seconds`.
- Suffix with unit: `_seconds`, `_bytes`, `_total`, `_ratio`.
- Histograms for durations; counters for events; gauges for current state.
- Cardinality budget: any label that could exceed 10k unique values is forbidden (no raw user IDs, full URLs with IDs, free-text input).

## Trace Conventions

- One span per cross-service hop and per external API / DB call.
- Span name = operation, not URL: `db.users.select_by_email`, not `/users/123`.
- Always propagate trace context through queues, async tasks, and background jobs.
- Span attributes for cardinality-safe metadata only — never PII.

## Log Conventions

- Structured JSON (no free-text logs).
- Mandatory fields: `timestamp` (ISO 8601, UTC), `level`, `service`, `event`. When in a request context: `trace_id`, `span_id`.
- Levels:
  - `DEBUG` — verbose, off in prod by default.
  - `INFO` — significant business events (request received, job completed).
  - `WARN` — handled abnormality (retry succeeded, deprecated path hit).
  - `ERROR` — unhandled or returned-to-user errors.
  - `FATAL` — process exit imminent (use sparingly).
- **Forbidden in logs:** PII, secrets, full request/response bodies of user data, tokens.

## Sampling

- Logs: keep all WARN/ERROR; sample DEBUG/INFO on hot paths.
- Traces: head-based sampling at the edge (e.g., 1% of OK, 100% of errors).
- Metrics: never sample — they're already aggregated.

## Anti-Patterns (forbid)

- `console.log` / `print` in production code.
- Free-text logs that require regex to parse later.
- Catching and logging without re-throwing or returning a proper error.
- Metrics with unbounded label cardinality.
- Tracing only inside one service (breaks the cross-service chain).
- Alert thresholds on raw metric values instead of SLO burn.
