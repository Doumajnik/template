# Ideas

Brainstorm space for in-flight design notes that aren't ready to be a plan yet.

## Purpose

This folder holds **pre-planning design notes** — proposals, sketches, and "what if we did X" documents that the Architect or Planning Agent may turn into formal plans later. It's a staging area, NOT a decision log.

## What goes here

- Early-stage proposals not yet ready for the Planning Agent
- Alternative approaches the Innovator generated but the Architect didn't adopt (kept for future reference)
- Sketches for features under discussion with the user

## What does NOT go here

| Content | Goes in |
| --- | --- |
| Approved architecture | `.ai/plans/` |
| Active todo list | `.ai/todos/` |
| Decisions and rationale | `docs/PLAYBOOK.md` |
| Lessons from corrections | `.ai/lessons.md` |
| Session summary | `.ai/sessions/` |

## Lifecycle

1. **Draft** — created here as a free-form Markdown file.
2. **Promoted** — when the user approves an idea, the Planning Agent moves the relevant content into a formal plan in `.ai/plans/` and the original file in `ideas/` is left as a historical reference (or removed during the next Cleanup pass).
3. **Discarded** — superseded ideas should be deleted by the Cleanup Agent.

## Current files

See the directory listing — each file is self-describing.
