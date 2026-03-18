# Project Feedback

Automated feedback from projects built with this template. On every push to `main`, the pipeline collects agent reports and opens a GitHub Issue on the template repo. Claude reviews the issue and creates a PR with improvements.

## Pipeline

```
push to main
  → send-feedback-via-issue.yml (project repo)
    → opens issue with "feedback" label on template repo
      → process-feedback-issue.yml (template repo)
        → Claude reviews → PR with improvements
```

Only two workflows:

| Workflow | Runs in | Purpose |
|---|---|---|
| `send-feedback-via-issue.yml` | Project repo | Collects feedback files, opens issue |
| `process-feedback-issue.yml` | Template repo | Claude reviews issue, creates PR |

Forks don't have `TEMPLATE_FEEDBACK_ENABLED` set, so the workflow is skipped automatically.

## What Gets Collected

- `docs/RETROSPECTIVE_REPORT.md` — agent decisions, what worked/didn't
- `docs/PLAYBOOK.md` — architecture rules that evolved
- `docs/QUALITY_REPORT.md` — code quality findings
- `docs/SECURITY_REPORT.md` — security audit results
- `.ai/lessons.md` — lessons captured after corrections
- `feedback/PUSH_NOTE.md` — optional user note (see below)

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

## Deduplication

A SHA-256 hash of the payload is stored in the `LAST_FEEDBACK_SHA` repo variable. If the payload hasn't changed since the last send, the issue is skipped.

## Setup

1. Set repo variable `TEMPLATE_FEEDBACK_ENABLED` to `true`.
2. Set repo variable `TEMPLATE_REPO` to the template's `owner/repo`.
3. Create a PAT with `public_repo` scope → add as secret `TEMPLATE_FEEDBACK_TOKEN`.
4. In the **template repo**, ensure `process-feedback-issue.yml` exists and `GH_MODELS_TOKEN` secret is set.

## Privacy

- No source code is sent — only markdown report files and the optional push note.
- Requires `TEMPLATE_FEEDBACK_ENABLED=true` — off by default.
- Push note is fully opt-in.
