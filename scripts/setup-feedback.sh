#!/bin/sh
# Sets up the feedback pipeline for this project repo.
# Configures the GitHub secret and variables needed by send-feedback-to-template.yml.
#
# Prerequisites: gh CLI installed and authenticated (gh auth login).
# Usage: ./scripts/setup-feedback.sh

set -e

echo "=== Feedback Pipeline Setup ==="
echo ""

# Check gh CLI
if ! command -v gh >/dev/null 2>&1; then
    echo "ERROR: GitHub CLI (gh) is required. Install it: https://cli.github.com"
    exit 1
fi

# Check auth
if ! gh auth status >/dev/null 2>&1; then
    echo "ERROR: Not authenticated. Run: gh auth login"
    exit 1
fi

# Get current repo
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null)
if [ -z "$REPO" ]; then
    echo "ERROR: Not inside a GitHub repo, or repo has no remote."
    exit 1
fi

echo "Project repo: $REPO"
echo ""

# Ask for template repo
printf "Enter your template repo (owner/repo): "
read TEMPLATE_REPO

if [ -z "$TEMPLATE_REPO" ]; then
    echo "ERROR: Template repo is required."
    exit 1
fi

# Validate template repo exists
if ! gh repo view "$TEMPLATE_REPO" >/dev/null 2>&1; then
    echo "ERROR: Cannot access $TEMPLATE_REPO. Check the name and your permissions."
    exit 1
fi

echo ""
echo "[1/3] Setting TEMPLATE_REPO variable..."
gh variable set TEMPLATE_REPO --body "$TEMPLATE_REPO" --repo "$REPO"
echo "  -> Set TEMPLATE_REPO=$TEMPLATE_REPO"

echo ""
echo "[2/3] Setting TEMPLATE_FEEDBACK_ENABLED variable..."
gh variable set TEMPLATE_FEEDBACK_ENABLED --body "true" --repo "$REPO"
echo "  -> Set TEMPLATE_FEEDBACK_ENABLED=true"

echo ""
echo "[3/3] Setting TEMPLATE_FEEDBACK_TOKEN secret..."
echo ""
echo "You need a GitHub PAT (classic) with 'repo' scope."
echo "Create one at: https://github.com/settings/tokens/new"
echo "  - Note: template-feedback-$REPO"
echo "  - Scopes: repo (full)"
echo ""
printf "Paste your PAT (input is hidden): "
stty -echo 2>/dev/null || true
read TOKEN
stty echo 2>/dev/null || true
echo ""

if [ -z "$TOKEN" ]; then
    echo "ERROR: Token is required."
    exit 1
fi

echo "$TOKEN" | gh secret set TEMPLATE_FEEDBACK_TOKEN --repo "$REPO"
echo "  -> Secret TEMPLATE_FEEDBACK_TOKEN saved."

echo ""
echo "=== Setup complete! ==="
echo ""
echo "The feedback pipeline is now active. When these files change on main,"
echo "updates will be sent to $TEMPLATE_REPO automatically:"
echo "  - docs/RETROSPECTIVE_REPORT.md"
echo "  - docs/PLAYBOOK.md"
echo "  - docs/QUALITY_REPORT.md"
echo "  - docs/SECURITY_REPORT.md"
echo "  - .ai/lessons.md"
echo ""
echo "You can also trigger it manually: Actions > Send Feedback to Template > Run workflow"
