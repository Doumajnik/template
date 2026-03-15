# Plan A: Push-Triggered Feedback Collection Pipeline

## Goal

Automatically collect two types of feedback every time a user pushes to a project that was built from this template:

1. **Agent-generated feedback** — structured data produced by AI agents during the session (retrospectives, lessons learned, quality reports, security findings, playbook updates).
2. **User feedback** — opt-in human input about the template experience (friction points, missing features, confusing docs).

Both streams are routed back to the template repo where they are reviewed by Claude and turned into concrete improvement PRs.

---

## What to Collect

### Agent-Generated

These files are already produced by the AI agent pipeline and change frequently on `main`:

| File | What it contains |
| --- | --- |
| `docs/RETROSPECTIVE_REPORT.md` | Agent decisions, what worked, what didn't |
| `docs/PLAYBOOK.md` | Architecture rules that evolved during the project |
| `docs/QUALITY_REPORT.md` | Code quality findings |
| `docs/SECURITY_REPORT.md` | Security audit results |
| `.ai/lessons.md` | Actionable lessons captured after corrections |

### User-Supplied

Opt-in text collected once per push (only if the user chooses to add it):

- A free-text comment in a dedicated file: `feedback/PUSH_NOTE.md`
- GitHub repository variables set by the project owner (e.g. `TEMPLATE_FEEDBACK_NOTE`)

---

## How It Works (Step by Step)

### 1 — Push Event Fires

The project's CI workflow listens for any push to `main` (not just when specific files change).

```yaml
on:
  push:
    branches: [main]
```

### 2 — Collect Agent Output

The workflow reads the agent-produced files listed above (up to 500 lines each to stay within API limits) and concatenates them into a single feedback payload.

### 3 — Collect Optional User Note

If `feedback/PUSH_NOTE.md` exists in the repo, its content is appended to the payload under a `## User Note` heading. The file is cleared after each push so notes are per-push, not accumulated.

If the variable `TEMPLATE_FEEDBACK_NOTE` is set (via `gh variable set`), its value is appended instead.

### 4 — Route to Template Repo

Two routing modes (chosen at setup time via `scripts/setup-feedback.sh`):

| Mode | Mechanism | PAT scope needed |
| --- | --- | --- |
| `dispatch` | `repository_dispatch` → `receive-project-feedback.yml` | `repo` (full) |
| `issue` | Opens a GitHub Issue with label `feedback` → `process-feedback-issue.yml` | `public_repo` |

### 5 — Claude Reviews and Opens a PR

The template repo's existing workflows pick up the feedback, run Claude Opus 4 via GitHub Models, and create a PR with proposed improvements to template files.

---

## GitHub Actions Workflow (Revised `send-feedback-to-template.yml`)

The existing workflow in `.github/workflows/send-feedback-to-template.yml` needs one key change: remove the `paths` filter so it fires on **every push to main**, not just when report files change.

```yaml
# Before (only fires when specific files change)
on:
  push:
    branches: [main]
    paths:
      - 'docs/RETROSPECTIVE_REPORT.md'
      - ...

# After (fires on every push — agent output or not)
on:
  workflow_dispatch:
  push:
    branches: [main]
```

To avoid spamming the template repo with empty feedback, add a guard step that skips the dispatch if none of the tracked files exist or have meaningful content:

```yaml
- name: Check if feedback files exist
  id: check
  run: |
    has_content=false
    for file in docs/RETROSPECTIVE_REPORT.md docs/PLAYBOOK.md docs/QUALITY_REPORT.md docs/SECURITY_REPORT.md .ai/lessons.md feedback/PUSH_NOTE.md; do
      if [ -f "$file" ] && [ -s "$file" ]; then
        has_content=true
        break
      fi
    done
    echo "has_content=${has_content}" >> "$GITHUB_OUTPUT"

- name: Send feedback
  if: steps.check.outputs.has_content == 'true'
  ...
```

---

## User Note Workflow

### Writing a Push Note

A user who wants to attach a comment to a push creates or edits `feedback/PUSH_NOTE.md` before committing:

```markdown
# Push Note

The scaffold agent took 3 attempts before it got the file structure right.
The issue was that my project uses a non-standard `lib/` directory instead of `src/`.
Suggestion: add a step that asks about the top-level source directory before scaffolding.
```

After the feedback workflow fires and sends the note, the workflow automatically resets the file:

```yaml
- name: Clear push note after sending
  run: |
    printf '# Push Note\n\n<!-- Add your feedback here before pushing. This file is cleared after each send. -->\n' \
      > feedback/PUSH_NOTE.md
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add feedback/PUSH_NOTE.md
    git commit -m "chore: clear push note after feedback send [skip ci]" || true
    git push || true
```

### Skipping the Reset (for drafts)

If the user includes the word `DRAFT` at the top of `PUSH_NOTE.md`, the workflow detects it and does not send or clear the note:

```yaml
- name: Check for draft note
  run: |
    if head -1 feedback/PUSH_NOTE.md | grep -qi 'draft'; then
      echo "Note is a draft — skipping send."
      exit 0
    fi
```

---

## Deduplication

To avoid sending the same feedback twice (e.g. multiple pushes in quick succession), the workflow records a SHA hash of the last-sent payload in a GitHub variable `LAST_FEEDBACK_SHA`. Before sending, it computes the current payload hash and skips if identical.

---

## Privacy Considerations

- No source code is ever sent — only markdown report files and the optional user note.
- Users opt in by running `setup-feedback.sh`. The `TEMPLATE_FEEDBACK_ENABLED` variable must be `true` for any dispatch to happen.
- The `feedback/PUSH_NOTE.md` file is opt-in — it only affects the payload if the user creates and edits it.
- Dispatch mode requires a PAT the user created themselves — no implicit data sharing.

---

## Implementation Checklist

- [ ] Remove `paths` filter from `send-feedback-to-template.yml` and `send-feedback-via-issue.yml`
- [ ] Add the `check if feedback files exist` guard step
- [ ] Add `feedback/PUSH_NOTE.md` template file (with DRAFT placeholder)
- [ ] Add push-note collection step to the send workflows
- [ ] Add push-note auto-clear step with `[skip ci]` commit
- [ ] Add deduplication via `LAST_FEEDBACK_SHA` variable
- [ ] Update `scripts/setup-feedback.sh` to explain the push-note feature
- [ ] Update `feedback/README.md` with push-note documentation

---

## Success Metrics

- Feedback arrives in the template repo after every meaningful push (not just report updates).
- User notes are readable, isolated per push, and not accidentally duplicated.
- The template receives at least one actionable improvement PR per 10 feedback submissions.
- Zero source code leaks in feedback payloads.
