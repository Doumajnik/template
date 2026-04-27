+++
id = "agents/cost-finops"
title = "Cost / FinOps Agent Playbook"
agents = ["cost-finops"]
technologies = ["all"]
category = "rule"
tags = ["cost-finops", "finops", "cloud-cost"]
version = 1
+++

# Cost / FinOps Playbook

## Cost Driver Cheat Sheet

| Category | High-cost signals |
| --- | --- |
| Compute | Always-on instances at low utilization; oversized DB instances; serverless on hot paths with high per-invocation cost |
| Storage | Hot-tier storage of cold data; redundant copies; long retention without tiering |
| Network | Cross-AZ chattiness; large egress to internet; unbatched API calls |
| Data warehouse | Full-table scans; SELECT *; missing partitioning; per-query costs on large tables |
| Observability | High-cardinality metrics; verbose logs without sampling; long retention of detailed traces |
| Third-party | Per-request APIs without caching; LLM calls without prompt/response caching; unbatched embeddings |

## Estimation Method

Use order-of-magnitude (OOM) estimates:

```
monthly_cost ≈ unit_price × usage_per_request × requests_per_month
```

State assumptions explicitly. Round generously. Use cloud pricing pages, not memory.

## ROI Threshold

| Saving / month | Worth optimizing if engineering time ≤ |
| --- | --- |
| < $50 | Don't bother unless trivial |
| $50 – $500 | 1–3 days |
| $500 – $5,000 | 1–2 weeks |
| > $5,000 | Up to a month, plus monitor outcome |

## Anti-Patterns to Flag

- "It's only $X/mo" said about something that scales with users.
- Cost optimization that adds significant complexity (premature optimization).
- Manual right-sizing without autoscaling — flips the problem in 6 months.
- Logs/metrics retention longer than the audit requirement allows.
- Per-environment infra duplication where shared infra would be safe (dev/test on production-sized clusters).

## Coordination

- **Architect** — I weigh in during bottleneck-scan and full review.
- **Observability Engineer** — high-cardinality metrics are a shared concern.
- **Data Engineer** — partitioning, clustering, and storage tier choices.
- **Vendor Evaluator** — total cost of ownership for new third-party services.
