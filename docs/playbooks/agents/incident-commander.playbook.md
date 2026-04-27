+++
id = "agents/incident-commander"
title = "Incident Commander Agent Playbook"
agents = ["incident-commander"]
technologies = ["all"]
category = "rule"
tags = ["incident-commander", "incident-response", "sev1"]
version = 1
+++

# Incident Commander Playbook

## Severity Rubric

| Severity | Criteria |
| --- | --- |
| **SEV1** | Service down for all users, data loss possible, or active security breach. Page everyone. |
| **SEV2** | Major feature broken, significant subset of users impacted, or workaround exists but is poor. |
| **SEV3** | Minor feature degraded, single user / non-critical path, no data risk. |

## Mitigation Playbook (try in order)

1. **Rollback** the last deploy if the timeline matches.
2. **Toggle feature flag** off for the suspected feature.
3. **Failover** to the secondary region / replica.
4. **Rate-limit** the offending traffic source.
5. **Restart** affected service (last resort — masks state issues).

## Incident Doc Skeleton

Save to `docs/incidents/{YYYY-MM-DD-HHMM}_{slug}.md`:

```markdown
# Incident: {one-line summary}

- **Severity:** SEV{1|2|3}
- **Started:** {ISO timestamp}
- **Detected:** {ISO timestamp} via {alert / user report / dashboard}
- **Mitigated:** {ISO timestamp}
- **Resolved:** {ISO timestamp}
- **Commander:** Incident Commander Agent (session {id})
- **Impact:** {users affected, data loss, $$, SLO burn}

## Timeline

| Time (UTC) | Actor | Event |
| --- | --- | --- |
| 14:02 | Alert | p99 latency > 2s on /checkout |
| 14:04 | Commander | Declared SEV2, paged team |
| 14:06 | Debug | Started log scan on checkout-service |
| ... | | |

## Hypotheses

- [x] DB connection pool exhaustion — confirmed via metrics
- [ ] Upstream payment provider outage — ruled out
- [ ] Recent deploy regression — ruled out (deploy was 6h prior)

## Mitigations Applied

- Increased pool size from 20 → 50 (temporary)
- Rate-limit on /checkout to 100 rps

## Root Cause

{one paragraph}

## Action Items (handed to Retrospective)

- [ ] Auto-scale connection pool based on queue depth
- [ ] Add alert for pool utilization > 80%
- [ ] Document pool sizing in runbook
```

## Communication Templates

**Initial:** "We're aware of {symptom} affecting {scope}. Investigating. Next update in {N} min."

**Mitigated:** "Mitigation applied: {action}. Service is recovering. Monitoring for {N} min before declaring resolved."

**Resolved:** "Incident resolved. Root cause: {summary}. Postmortem will be shared in {timeframe}."

## Anti-Patterns (forbid)

- Investigating root cause while users are still impacted (mitigate first).
- Multiple commanders giving conflicting orders.
- "Quick fix in prod" without a rollback plan.
- Closing the incident before telemetry confirms stable recovery for the observation window.
- Blaming individuals in the postmortem hand-off.
