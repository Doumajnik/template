---
description: Review recent changes and write a session summary
agent: Reviewer
---

# Review Session

Review all changes made in the current session and produce a quality report.

## Instructions

1. **Read context files:**
   - `docs/CODE_INVENTORY.md` — the living registry of all code symbols
   - `docs/PLAYBOOK.md` — current architecture decisions and patterns
   - `.ai/PREFERENCES.md` — user's coding style preferences

2. **Read the todo file** in `.ai/todos/` for the current session (if one exists):
   - Check which tasks are marked ✅ done and which are still ⬜ or 🔵
   - Use this to understand what was planned vs what was actually completed

3. **Identify all files** created or modified in this session.

4. **Review for quality issues:**
   - **Duplication** — new symbols that overlap with existing ones in the inventory
   - **Playbook violations** — patterns that contradict documented decisions
   - **Preference mismatches** — code style deviations from the user's preferences
   - **Missing docs** — functions without doc comments, inventory not updated
   - **Todo adherence** — verify implemented code matches what was planned in the todo file

5. **Verify documentation was updated:**
   - Was `docs/CODE_INVENTORY.md` updated with all new symbols?
   - Was `docs/PLAYBOOK.md` updated with any new decisions?
   - Was `README.md` updated if structure changed?

6. **Write review report** — append findings to `docs/REVIEW_REPORT.md` (do NOT overwrite previous reviews).

7. **Update the todo file** — mark the review task as ✅ done and append to the Progress Log.

8. **Flag preference updates** — if user feedback revealed new preferences, include them in your report. The Retrospective Agent will update `.ai/PREFERENCES.md`.
