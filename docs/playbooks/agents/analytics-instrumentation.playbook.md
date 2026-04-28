+++
id = "agents/analytics-instrumentation"
title = "Analytics Instrumentation Agent Rules"
agents = ["analytics-instrumentation"]
technologies = ["all"]
category = "rule"
tags = ["analytics", "instrumentation", "kpi"]
version = 1
+++

### Analytics Instrumentation Guidelines

- **Distinct from Observability.** Observability = SLOs, latency, errors. Analytics = funnels, KPIs, cohorts, business metrics. Never duplicate a metric across both planes — pick the right one.
- **Question first, event name last.** Every event answers a documented business question. The name follows the question.
- **`noun_verb` convention.** `signup_completed`, `order_placed`, `subscription_cancelled`. Past tense, not gerund.
- **One trigger, one event.** A single user action never fires two events with overlapping semantics. Consolidate or differentiate explicitly.
- **Properties are typed.** Every property has a documented type and value space. No untyped grab-bags.
- **Identity hygiene.** anonymous_id, user_id, account_id, session_id are distinct. Never collapse at instrumentation time — stitch in the warehouse.
- **PII-by-default suspicion.** Every string property is potentially PII until proven otherwise. Hash or suppress before sending to third-party analytics.
- **Server-side preferred.** When the same event can fire on client or server, prefer server-side — clients block ads / strip params / lose connectivity.
- **KPIs are computations.** Every KPI has a SQL-like definition referencing concrete events. "Engagement" without a definition is not a KPI.
- **Funnels are ordered with windows.** A funnel without a documented allowed window between steps is just a list.
- **Cohorts have membership rules.** Every cohort is defined by a concrete event-based membership rule.
- **Experiment readiness is explicit.** Document weekly volume, expected variance, and the minimum detectable effect at 80% power. If the volume can't detect the MDE in a reasonable window, flag it.
- **Append to `docs/ANALYTICS_EVENTS.md`.** Never overwrite — analytics plans are versioned history. Removing or renaming an event requires a deprecation entry.
- **Re-run on user-flow changes.** Any Change Pipeline that touches a user-facing flow refreshes the analytics plan.
