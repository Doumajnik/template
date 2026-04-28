# Deep Implement Pipeline Checklist

## Pre-Implementation Gates

- [ ] Librarian queried before every agent spawn (Context Gateway Protocol)
- [ ] Prompt Engineer produced enriched spec in `.ai/specs/`
- [ ] Context files read (PREFERENCES, PLAYBOOK, CODE_INVENTORY)
- [ ] Discovery completed (if new data involved)
- [ ] Research brief produced with dependency list
- [ ] All dependencies installed
- [ ] Architecture designed by Architect
- [ ] Innovator reviewed and proposed alternatives
- [ ] Architect incorporated best ideas
- [ ] Critic approved (≤10 rounds)
- [ ] Planning Agent created function-level plan + todo file
- [ ] UI Preview generated (if UI/frontend task) or explicitly skipped
- [ ] User explicitly approved the plan

## Implementation Deliverables

- [ ] File stubs created by Scaffolder
- [ ] ≥10 tests per function across the 12-category taxonomy by Test Writer (red phase), edge cases first
- [ ] ≥50 tests per functionality summed across unit + integration + E2E + contract layers
- [ ] All functions implemented by Worker (green phase)
- [ ] Integration/E2E tests written and passing

## Post-Implementation Quality

- [ ] Reviewer approved
- [ ] Security audit completed — no CRITICAL/HIGH unresolved
- [ ] Code Quality scan completed — no CRITICAL/HIGH unresolved
- [ ] All documentation updated
- [ ] Session summary written
- [ ] Retrospective completed (chunked) and Playbook updated
- [ ] Cleanup Agent dedup pass completed (reports consolidated)
- [ ] Todo file marked ✅ Complete

## Output Files

| File | Purpose |
| --- | --- |
| `.ai/specs/{date}_{topic}.md` | Enriched spec from Prompt Engineer |
| `.ai/todos/{date}_{topic}.todo.md` | Living task tracker |
| `.ai/sessions/{date}_{topic}.dispatch.md` | Dispatch log |
| `.ai/sessions/{date}_{topic}.transcript.md` | Session transcript |
| `docs/SECURITY_REPORT.md` | Security findings (appended) |
| `docs/QUALITY_REPORT.md` | Quality findings (appended) |
| `docs/RETROSPECTIVE_REPORT.md` | Session retrospective (appended) |
