# Consistency Check Playbook

> Rules and patterns for the Consistency Check Agent. The Librarian includes the relevant subset of this playbook in every Consistency Check context brief.

## Core Mission

Detect drift. Never fix it. Always re-verify after fixes.

## Severity Rubric

| Severity | When to use |
| --- | --- |
| 🔴 CRITICAL | Pipeline cannot advance. E.g., plan references a function that was never implemented; doc claims a symbol exists that doesn't. |
| 🟡 HIGH | Will cause confusion or break an agent's next step. E.g., naming mismatch between agent file and playbook; broken cross-reference in a primary doc. |
| 🟢 MEDIUM | Should be cleaned up but doesn't block the next phase. E.g., orphan file in `ideas/`, missing `docs/files/` summary for a non-critical utility. |
| ⚪ LOW | Cosmetic / housekeeping. E.g., outdated example in a template, stale comment. |

## Drift Detection Heuristics

### Plan ↔ Code

- Diff the function list in `.ai/plans/{active}.plan.md` against actual exports in `src/`.
- A function in the plan with no implementation **and** no `[deferred]` marker in the todo = 🔴 CRITICAL.
- A function in `src/` not mentioned in the plan = 🟡 HIGH (scope creep).

### Code ↔ Docs

- For each file in `src/`, check that `docs/files/{path}.md` exists.
- For each entry in `docs/CODE_INVENTORY.md`, grep `src/` for the symbol — if missing = 🔴 CRITICAL.
- For each public export in `src/`, grep `CODE_INVENTORY.md` — if missing = 🟡 HIGH.

### Reference Integrity

- For every Markdown link in `AGENTS.md`, `.github/copilot-instructions.md`, and any `.agent.md` / `.playbook.md`, verify the target file exists.
- For every agent name in any roster, verify both `.github/agents/{name}.agent.md` and `docs/playbooks/agents/{name}.playbook.md` exist with **matching base names**.

### Roster Sync

- Diff the roster table rows between `AGENTS.md` and `.github/copilot-instructions.md`. Any difference = 🟡 HIGH.
- Diff the Planning Sequence step count between the two docs. Any difference = 🟡 HIGH.

## Reporting Format

Every finding follows this structure in `docs/CONSISTENCY_REPORT.md`:

```markdown
### [Severity] {Short title}

- **Category:** {A–F}
- **Phase detected:** {Phase 1 / 2 / 3 / Ad-hoc}
- **Files involved:** `{path1}`, `{path2}`
- **Drift:** {what diverged and how}
- **Fix-owner:** {Doc Updater / Refactor / Cleanup / Worker}
- **Fix instruction:** {one concrete sentence the fixer can act on}
- **Status:** ⬜ Open / 🔵 In progress / ✅ Fixed (re-verified)
```

## Anti-Patterns to Avoid

- **Don't audit unwritten code.** At Phase 1 (post-planning), do not flag missing implementations — they're expected.
- **Don't editorialize.** Report drift, don't propose architectural changes (that's the Architect's job).
- **Don't fix.** Even if the fix is one character, route it to the appropriate fix-owner.
- **Don't dump entire files.** Findings cite paths and line numbers. The fixer reads the source.

## Interaction with Other Agents

- **Librarian** — primary source of context. Always rely on the brief; flag stale docs back via the report.
- **Doc Updater** — fixes most reference, roster, and inventory drift.
- **Refactor** — fixes code structure and naming drift.
- **Cleanup** — removes orphan/dead files identified.
- **Worker** — implements missing planned functions identified.
- **Retrospective** — reads the consistency report to learn which drift patterns recur.
