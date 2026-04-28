---
mode: agent
description: Triage and respond to a live production incident — declare → stabilize → investigate → root-cause → permanent fix → resolve → postmortem.
---

# Incident Response

You are the **Orchestrator**. The user has reported a live production issue. You are now running the **Incident Response Pipeline** as defined in [AGENTS.md](../../AGENTS.md#incident-response-pipeline-live-production-issues).

**Triggers:** "incident", "down", "outage", "prod is broken", or any user message describing live production impact.

> **Librarian-first still applies.** Even under SEV1 pressure, query the Librarian in **fast mode** (cached briefs OK; index refresh deferred to post-incident) before spawning Debug / Performance / Security / Database / Observability investigators.

---

## Phase 1 — Declare

1. Spawn the **Incident Commander** with: the user's report, recent deploys, recent alerts (if known), affected surface.
2. The Commander assigns a severity:

   | Severity | Definition | Observation window before declaring resolved |
   | --- | --- | --- |
   | **SEV1** | Customer-facing outage, data loss risk, or revenue impact | 30 min stable telemetry |
   | **SEV2** | Major degradation, partial outage, or critical-path slowness | 1 h stable telemetry |
   | **SEV3** | Minor degradation, single-tenant issue, or cosmetic | 4 h stable telemetry |

3. The Commander opens `docs/incidents/{YYYY-MM-DD-HHMM}_{slug}.md` and produces the **initial communication template** (acknowledge to stakeholders).

## Phase 2 — Stabilize first, fix second

The Commander's first recommendation is **mitigation**, not root-cause. Options in priority order:

1. **Rollback** the most recent deploy.
2. **Feature-flag off** the suspected feature.
3. **Failover** to a healthy replica / region.
4. **Rate-limit / shed load** on the suspected entry point.
5. **Restart** the suspected component (last resort — destroys debug state).

Spawn a **Worker** to apply the chosen mitigation. Telemetry must confirm recovery before moving on.

## Phase 3 — Investigate in parallel

Spawn **in parallel** as many of the following as the symptom warrants — all report back to the Commander via the Orchestrator:

- **Debug Agent** — logs, stack traces, recent code changes
- **Performance Agent** — if latency / throughput is the symptom
- **Security Agent** — if breach / abuse / DDoS is suspected
- **Database Agent** — if data corruption / lock contention / replication lag is suspected
- **SQL Query Agent** — if a slow query is the symptom
- **Observability Engineer** — if telemetry gaps are blocking diagnosis (designs new instrumentation; Worker implements after the incident)

Each investigator produces a hypothesis + evidence. The Commander consolidates hypotheses in the incident timeline. Disproven hypotheses stay in the timeline.

## Phase 4 — Root cause

The first hypothesis confirmed by **evidence** (not just plausibility) wins. The Commander writes the root-cause section of the incident doc.

## Phase 5 — Permanent fix

Run the **Change Pipeline** for the permanent fix — but **skip step 1 (Prompt Engineer)**: the incident doc is the spec. Resume from step 2 (Impact Analysis) onward.

## Phase 6 — Resolution

The Commander declares resolution **only when** telemetry confirms stable recovery for the SEV's observation window. Send the **resolved** communication.

## Phase 7 — Postmortem hand-off

1. Spawn the **Retrospective Agent** for a blameless postmortem.
2. Spawn the **Doc Updater** to write the postmortem summary into `docs/incidents/` and update affected runbooks.
3. The Retrospective appends action items to the next session's todo file.

## Consistency Check Gate

A single Consistency Check runs **after Phase 7**: incident doc ↔ timeline ↔ action items ↔ runbook updates. No stale references to mitigations that were rolled back.

> **Why one gate, not three:** SEV1 speed exception. The mitigation phase happens under the gun and is verified by telemetry in real time, not by a static gate. SEV2 / SEV3 may opt into the standard 3-gate pattern at the Commander's discretion.

---

## Communication templates

The Commander produces three updates — surface them to the user to forward to stakeholders.

**Initial:**
> We are investigating a {SEV} incident affecting {surface}. Symptoms: {symptoms}. Started: {time}. Next update: {time + 15 min for SEV1, 30 min SEV2, 1 h SEV3}.

**Mitigated:**
> The {SEV} incident affecting {surface} has been mitigated by {mitigation}. We are continuing root-cause analysis. Expect resolution within {observation window}.

**Resolved:**
> The {SEV} incident affecting {surface} is resolved. Root cause: {one-sentence cause}. Permanent fix: {summary}. Full postmortem: `docs/incidents/{file}`.
