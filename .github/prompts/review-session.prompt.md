---
description: Review recent changes and write a session summary
agent: Reviewer
---

# Review Session

Review all changes made in the current session and produce a quality report.

## Instructions

1. Read `docs/CODE_INVENTORY.md`, `docs/PLAYBOOK.md`, and `.ai/PREFERENCES.md`.
2. Identify all files created or modified in this session.
3. Check for:
   - **Duplication** — any new symbols that overlap with existing ones in the inventory
   - **Playbook violations** — patterns that contradict documented decisions
   - **Preference mismatches** — code style deviations from the user's preferences
   - **Missing docs** — functions without doc comments, inventory not updated
4. Present the review summary.
5. Write a session summary to `.ai/sessions/` using the template at `.ai/sessions/_TEMPLATE.md`.
6. If you learned any user preferences during this session, append them to `.ai/PREFERENCES.md`.
