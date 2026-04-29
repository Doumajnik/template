# 🚨 Orchestrator Checklist — Incident Response Pipeline

> Copy this block into the session todo file at the very top. Tick: `[ ]` not started · `[~]` in progress · `[x]` done · `[!]` blocked.

**Pipeline:** Incident Response (Phases 1–7, single Consistency Check gate at the end).
**Use when:** "incident", "down", "outage", "prod is broken", live impact reported.
**Distinct from Autonomous Bug Fixing** — that's for known bugs in dev/test. This is for live, ambiguous, high-pressure situations.
**Source of truth:** [AGENTS.md → Incident Response Pipeline](../../AGENTS.md#incident-response-pipeline-live-production-issues) and [.github/prompts/incident-response.prompt.md](../../.github/prompts/incident-response.prompt.md).

> **Speed exception:** the Librarian still runs first, but in **fast mode** (cached briefs OK; index refresh deferred to post-incident). No 3-gate Consistency Check during the response — telemetry verifies mitigation in real time.

---

## Phase 0 — Session bootstrap (fast)

- [ ] Read `.ai/PREFERENCES.md` (skip if already in working memory)
- [ ] Create incident dispatch log `.ai/sessions/{date}_incident-{slug}.dispatch.md`
- [ ] Spawn **Librarian** (fast mode — cached briefs allowed)

## Phase 1 — Declare

- [ ] Spawn **Incident Commander**
- [ ] Commander assigns severity (SEV1 / SEV2 / SEV3)
- [ ] Open incident doc `docs/incidents/{YYYY-MM-DD-HHMM}_{slug}.md`
- [ ] Issue **initial communication** (acknowledge)

## Phase 2 — Stabilise first, fix second

- [ ] Commander recommends mitigation: rollback / feature flag off / rate-limit / failover / shed load
- [ ] Spawn **Worker** to apply mitigation
- [ ] **Wait for telemetry to confirm recovery** before moving on (do NOT skip)
- [ ] Issue **mitigated communication** when recovery confirmed

## Phase 3 — Investigate (parallel arms)

- [ ] Spawn **Debug** on suspected modules (logs, stack traces) — always
- [ ] Spawn **Performance** if latency / throughput is the symptom
- [ ] Spawn **Security** if attack / breach suspected
- [ ] Spawn **Database / SQL Query** if data corruption / lock contention suspected
- [ ] Spawn **Observability Engineer** if telemetry gaps block diagnosis (designs new instrumentation; Worker implements after the incident)
- [ ] Each arm reports hypotheses + evidence back to Commander

## Phase 4 — Root cause

- [ ] Commander consolidates hypotheses in incident timeline
- [ ] First hypothesis confirmed by evidence wins; disproven hypotheses also stay in the timeline (audit trail)

## Phase 5 — Permanent fix

- [ ] Run **Change Pipeline** for the permanent fix (skip Step 1 — incident doc IS the spec)
- [ ] Mitigation can stay in place until permanent fix ships

## Phase 6 — Resolution

- [ ] Telemetry stable for the agreed observation window?
  - SEV1: 30 minutes minimum
  - SEV2: 1 hour minimum
- [ ] If yes → Commander declares resolution
- [ ] Issue **resolved communication** (root cause + next steps)

## Phase 7 — Postmortem (blameless)

- [ ] Spawn **Retrospective** → blameless postmortem; append action items to next session's todo
- [ ] Spawn **Doc Updater** → write postmortem summary, update `docs/incidents/`, update runbooks
- [ ] **🛑 Single Consistency Check gate** → incident doc ↔ timeline ↔ action items ↔ runbook updates; no stale references to rolled-back mitigations
- [ ] Mark incident 🟢 Closed
