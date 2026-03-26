# Change Pipeline Checklist

## Pre-Implementation Gates

- [ ] Librarian queried before every agent spawn (Context Gateway Protocol)
- [ ] Context files read (PREFERENCES, PLAYBOOK, CODE_INVENTORY)
- [ ] Prompt Engineer produced enriched spec (what exists, what changes, what must NOT change)
- [ ] Impact Analysis completed — blast radius mapped (affected files, deps, tests, risks)
- [ ] Research brief produced with best practices for this type of change
- [ ] Dependencies installed/uninstalled (if applicable)
- [ ] Architecture designed by Architect — preserves existing behavior where intended
- [ ] Innovator reviewed and proposed alternatives
- [ ] Architect incorporated best ideas
- [ ] Critic approved (≤10 rounds) — explicitly verified "nothing currently working breaks"
- [ ] Planning Agent created change plan + regression checklist + todo file
- [ ] User explicitly approved the change plan, impact analysis, and regression checklist

## Implementation Deliverables

- [ ] Tests updated/written for changed behavior (15+ per changed function)
- [ ] Regression tests written for unchanged behavior at risk
- [ ] All changed functions implemented by Worker (green phase)
- [ ] ALL existing tests still pass (not just new/changed tests)
- [ ] Integration/E2E tests written and passing — boundary between changed and unchanged code covered

## Post-Implementation Quality

- [ ] Reviewer approved — regression checklist fully verified
- [ ] No unintended side effects detected
- [ ] All affected callers/consumers updated
- [ ] Security audit completed — no CRITICAL/HIGH unresolved
- [ ] Code Quality scan completed — no CRITICAL/HIGH unresolved
- [ ] All affected documentation updated (API, business logic, file docs, inventory)
- [ ] Session summary written
- [ ] Retrospective completed (chunked) and Playbook updated
- [ ] Reports consolidated (Cleanup Agent dedup pass)
- [ ] Todo file marked ✅ Complete

## Output Files

| File | Purpose |
| --- | --- |
| `.ai/specs/{date}_{topic}.md` | Enriched change spec (what exists, changes, must NOT change) |
| `.ai/todos/{date}_{topic}.todo.md` | Living task tracker with regression checklist |
| `.ai/sessions/{date}_{topic}.dispatch.md` | Dispatch log |
| `.ai/sessions/{date}_{topic}.transcript.md` | Session transcript |
| `docs/SECURITY_REPORT.md` | Security findings (appended) |
| `docs/QUALITY_REPORT.md` | Quality findings (appended) |
| `docs/RETROSPECTIVE_REPORT.md` | Session retrospective (appended) |

## Change-Specific Verification

These items are unique to the Change Pipeline and MUST be verified:

- [ ] **Blast radius documented** — every affected file, function, test, and module listed
- [ ] **Regression checklist complete** — every existing behavior that must survive is listed
- [ ] **Regression checklist verified** — Reviewer confirmed each item still works
- [ ] **No orphaned code** — old behavior's dead code removed or flagged
- [ ] **Callers migrated** — every consumer of the changed API/function updated
- [ ] **Backward compatibility addressed** — breaking changes documented or avoided
