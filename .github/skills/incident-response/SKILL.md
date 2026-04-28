---
name: incident-response
description: Full incident-response pipeline — declare → stabilize → investigate in parallel → root-cause → permanent fix → resolve → postmortem. Use when production is broken, degraded, or under attack. Triggers on: incident, down, outage, prod is broken, sev1, sev2.
---

# Incident Response Skill

This skill runs the **Incident Response Pipeline** as defined in [AGENTS.md](../../../AGENTS.md#incident-response-pipeline-live-production-issues).

## When to use

Load this skill when the user reports any of:

- "Incident", "down", "outage", "prod is broken"
- A live customer-facing failure
- A surge of errors / latency in production
- A suspected breach or abuse
- Any "this is on fire" signal

Do **not** use this skill for:

- Bug reports in dev / test → use the **Debug Agent** directly
- Known reproducible bugs → run the **Change Pipeline**
- Performance regressions caught in CI → run the **Performance Agent**

## Workflow

Follow the canonical 7-phase pipeline:

1. **Declare** — spawn Incident Commander → severity → open `docs/incidents/{YYYY-MM-DD-HHMM}_{slug}.md` → initial comms.
2. **Stabilize** — rollback / flag-off / failover / shed / restart, in that priority order. Telemetry must confirm recovery.
3. **Investigate (parallel)** — Debug, Performance, Security, Database, SQL Query, Observability — spawned in parallel based on symptom.
4. **Root cause** — first hypothesis confirmed by evidence wins.
5. **Permanent fix** — run Change Pipeline from step 2 onward (the incident doc is the spec).
6. **Resolution** — only when telemetry is stable for the SEV's observation window (SEV1: 30 min, SEV2: 1 h, SEV3: 4 h).
7. **Postmortem** — Retrospective writes a blameless postmortem; Doc Updater updates runbooks; action items go to the next session's todo.

## Severity matrix

| Severity | Definition | Update cadence | Observation window |
| --- | --- | --- | --- |
| **SEV1** | Customer-facing outage, data loss, revenue impact | 15 min | 30 min |
| **SEV2** | Major degradation, partial outage, critical path slow | 30 min | 1 h |
| **SEV3** | Minor degradation, single-tenant, cosmetic | 1 h | 4 h |

## Librarian-first under pressure

Even in a SEV1, query the Librarian **first** — but in **fast mode**: cached briefs are acceptable, index refresh is deferred to post-incident. Do NOT skip the Librarian — investigators need an up-to-date code/infrastructure brief, not raw source.

## Consistency Check

A **single** gate runs after Phase 7 (postmortem). This is a deliberate SEV1 speed exception to the standard 3-gate pattern; mitigation correctness is verified by telemetry in real time, not by a static gate. SEV2 / SEV3 may opt into 3 gates at the Commander's discretion.

## See also

- [.github/prompts/incident-response.prompt.md](../../prompts/incident-response.prompt.md) — slash-command form of this pipeline
- `.github/agents/incident-commander.agent.md` — the Commander's responsibilities
- `docs/incidents/` — historical postmortems and runbooks
