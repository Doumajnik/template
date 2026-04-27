+++
id = "shared/cost-aware-design"
title = "Cost-Aware Design (shared)"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["cost", "finops", "shared"]
version = 1
+++

# Cost-Aware Design (shared)

Every code-writing and architecture agent should weigh cost in design decisions. The Cost/FinOps Agent owns the explicit analysis; this playbook is the baseline awareness everyone applies.

## Core Principle

Cost is a constraint to be made visible — not a veto. Make trade-offs explicit so the user can choose.

## Cost-Driver Awareness

When designing or implementing, ask:

1. Does this scale with users, requests, or data? (Linear / superlinear costs are dangerous.)
2. Does this run when nothing is happening? (Idle cost.)
3. Does this cross an AZ, region, or cloud boundary? (Network egress.)
4. Does this store data in the hot tier indefinitely? (Storage tier + retention.)
5. Does this call a paid third-party API per request? (Per-call costs.)

## Defaults That Save Money

- Cache aggressively when stale-while-revalidate is acceptable.
- Batch external calls when latency budget allows.
- Stream large datasets, don't load into memory.
- Compress payloads for cross-region traffic.
- Use spot/preemptible compute for fault-tolerant workloads.
- Tier storage by access pattern (hot → warm → cold → archive).
- Pre-aggregate analytical queries; don't scan raw events on the read path.

## Anti-Patterns (flag immediately)

- Polling loops where webhooks/streaming would work.
- Unbounded fan-out (one user request → N parallel external calls).
- High-cardinality observability labels (raw user/URL/IP in metrics).
- Per-environment full-size infra duplication (dev sized like prod).
- Logs/metrics retention exceeding the audit requirement.
- "Just use the LLM for everything" without prompt/response caching.

## When to Engage Cost/FinOps Explicitly

- New service or region.
- New high-volume table or topic.
- New paid third-party dependency.
- Any design where back-of-envelope math suggests > $500/month at expected load.

Below the threshold, cost-awareness is just background practice — no formal Cost/FinOps spawn needed.
