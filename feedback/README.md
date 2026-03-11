# Project Feedback

This folder receives automated feedback from projects built with this template.

Each project can send its retrospectives, playbook updates, quality reports, security reports, and lessons learned back here for review.

## How it works

1. **Project repos** have a workflow (`.github/workflows/send-feedback-to-template.yml`) that triggers when retrospective/playbook files change on `main`.
2. That workflow sends the data to this template repo via GitHub's `repository_dispatch` API.
3. **This repo** has a workflow (`.github/workflows/receive-project-feedback.yml`) that receives the dispatch, saves the feedback here, and opens a PR.
4. You review the PR, extract useful patterns, and update the template accordingly.

## Setup (per project)

Run the setup script — it handles everything interactively:

```powershell
# Windows
.\scripts\setup-feedback.ps1

# Unix / macOS / WSL
./scripts/setup-feedback.sh
```

The script will:
1. Detect the current GitHub repo
2. Ask for your template repo name (`owner/repo`)
3. Set the `TEMPLATE_REPO` and `TEMPLATE_FEEDBACK_ENABLED` variables
4. Prompt for a GitHub PAT and save it as `TEMPLATE_FEEDBACK_TOKEN`

**Prerequisites:** [GitHub CLI](https://cli.github.com) installed and authenticated (`gh auth login`).

## Files

Feedback files are named `{date}_{owner}_{repo}.md` and contain the latest content from:

- `docs/RETROSPECTIVE_REPORT.md`
- `docs/PLAYBOOK.md`
- `docs/QUALITY_REPORT.md`
- `docs/SECURITY_REPORT.md`
- `.ai/lessons.md`
