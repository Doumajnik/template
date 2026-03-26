# Project Feedback

Automated feedback from projects built with this template. The Retrospective Agent appends template-relevant observations to a single file (`FEEDBACK.md`) after every session. On push to `main`, the pipeline collects this file and opens a GitHub Issue on the template repo. Claude reviews the issue and creates a PR with improvements.

## How It Works

```
Retrospective Agent → appends to feedback/FEEDBACK.md
  → push to main
    → send-feedback-via-issue.yml (project repo)
      → opens issue with "feedback" label on template repo
        → process-feedback-issue.yml (template repo)
          → Claude reviews → PR with improvements
```

## Files

| File | Purpose | Tracked in git? |
|---|---|---|
| `README.md` | This documentation | Yes |
| `PUSH_NOTE.md` | Optional user note attached to a push | Yes (template only) |
| `FEEDBACK.md` | Append-only log written by Retrospective Agent | **No** (gitignored) |

All other files in this folder are gitignored. The Retrospective Agent is the only writer — it appends a `## Template Feedback` entry after every session with observations about the template itself (confusing instructions, missing patterns, conflicting rules).

## What Gets Collected

On push to `main`, the feedback workflow collects:

- `feedback/FEEDBACK.md` — template observations from the Retrospective Agent
- `feedback/PUSH_NOTE.md` — optional user note (see below)
- `docs/RETROSPECTIVE_REPORT.md` — agent decisions, what worked/didn't
- `docs/PLAYBOOK.md` — architecture rules that evolved
- `docs/QUALITY_REPORT.md` — code quality findings
- `docs/SECURITY_REPORT.md` — security audit results
- `.ai/lessons.md` — lessons captured after corrections

Each file is truncated to 500 lines. A guard step skips the entire job if none of these have content.

## Push Notes

Edit `feedback/PUSH_NOTE.md` before committing to attach a personal comment:

```markdown
# Push Note

The scaffold agent assumed src/ but my project uses lib/.
Suggestion: ask about the source directory before scaffolding.
```

The note is included as a `## User Note` section in the issue and auto-cleared after send.

### Drafts

Prefix the first line with **DRAFT** to hold the note without sending:

```markdown
DRAFT
# Push Note
Still thinking about this...
```

## Setup

1. Set repo variable `TEMPLATE_FEEDBACK_ENABLED` to `true`.
2. Set repo variable `TEMPLATE_REPO` to the template's `owner/repo`.
3. Create a PAT with `public_repo` scope → add as secret `TEMPLATE_FEEDBACK_TOKEN`.
4. In the **template repo**, ensure `process-feedback-issue.yml` exists and `GH_MODELS_TOKEN` secret is set.

Forks don't have `TEMPLATE_FEEDBACK_ENABLED` set, so the workflow is skipped automatically.

## Privacy

- No source code is sent — only markdown report files and the optional push note.
- Requires `TEMPLATE_FEEDBACK_ENABLED=true` — off by default.
- Push note is fully opt-in.
