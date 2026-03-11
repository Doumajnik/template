# Project Feedback

This folder receives automated feedback from projects built with this template.

Each project can send its retrospectives, playbook updates, quality reports, security reports, and lessons learned back here for review.

## Two Feedback Modes

| Mode | Who it's for | Mechanism | PAT scope needed |
| --- | --- | --- | --- |
| **dispatch** | Template owners (your own repos) | `repository_dispatch` event → direct to template | `repo` (full) |
| **issue** | Forks / external contributors | Opens a GitHub Issue on the template repo | `public_repo` |

Both modes trigger Claude Opus 4 (via GitHub Models) to review the feedback and create a PR with proposed improvements.

### Dispatch Mode (own repos)

1. Project workflow sends a `repository_dispatch` event to the template repo.
2. Template's `receive-project-feedback.yml` catches it, runs Claude, and opens a PR.
3. Requires write access to the template repo.

### Issue Mode (forks / external contributors)

1. Project workflow opens a GitHub Issue on the template repo with label `feedback`.
2. Template's `process-feedback-issue.yml` catches it, runs Claude, and opens a PR.
3. The issue gets a comment with the result.
4. Only requires permission to open issues — no write access to the template.
5. Claude applies extra scrutiny to community contributions (conservative, additive-only changes preferred).

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
2. Ask you to choose a mode (**dispatch** or **issue**)
3. Ask for the template repo name (`owner/repo`)
4. Set the `TEMPLATE_REPO`, `TEMPLATE_FEEDBACK_ENABLED`, and `TEMPLATE_FEEDBACK_MODE` variables
5. Prompt for a GitHub PAT and save it as `TEMPLATE_FEEDBACK_TOKEN`

**Prerequisites:** [GitHub CLI](https://cli.github.com) installed and authenticated (`gh auth login`).

## Template-Side Setup

The template repo needs these workflows (already included):

- `.github/workflows/receive-project-feedback.yml` — processes dispatch-mode feedback
- `.github/workflows/process-feedback-issue.yml` — processes issue-mode feedback

And this secret:

- `GH_MODELS_TOKEN` — a GitHub PAT with Models read access (for Claude Opus 4 via GitHub Models API)

To create the label for issue-mode feedback:

```bash
gh label create feedback --description "Automated feedback from projects" --color 0e8a16
```

## Security Model

- **Dispatch mode:** The sender needs a PAT with `repo` scope to the template. This is a high-trust mode — only use it for repos you own.
- **Issue mode:** The sender only needs `public_repo` scope. They can open issues but cannot push code, dispatch events, or modify the template. All proposed changes go through a PR review.
- **Claude review:** Both modes run Claude Opus 4 to review feedback. For issue-mode (community), the prompt instructs Claude to apply extra scrutiny — preferring additive changes and flagging anything that could weaken security or stability.
- **File whitelist:** Only markdown files in `AGENTS.md`, `.github/`, `docs/`, and `.ai/` can be edited. Source code changes are rejected.

## Files

Feedback files are named `{date}_{owner}_{repo}.md` (dispatch) or `{date}_issue_{project}.md` (issue) and contain the latest content from:

- `docs/RETROSPECTIVE_REPORT.md`
- `docs/PLAYBOOK.md`
- `docs/QUALITY_REPORT.md`
- `docs/SECURITY_REPORT.md`
- `.ai/lessons.md`
