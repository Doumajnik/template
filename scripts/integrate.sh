#!/bin/sh
# Integrates the template into an existing project.
# Adds template as a remote, merges infrastructure files, preserves project code.
#
# Usage:
#   ./scripts/integrate.sh "https://github.com/Doumajnik/template.git"
#   ./scripts/integrate.sh   # uses default URL
#
# Run from the ROOT of your existing project.

set -e

TEMPLATE_URL="${1:-https://github.com/Doumajnik/template.git}"
TEMPLATE_BRANCH="${2:-main}"
SKIP_SETUP="${SKIP_SETUP:-false}"

# ── Helpers ──────────────────────────────────────
step()  { printf "\033[36m[%s] %s\033[0m\n" "$1" "$2"; }
ok()    { printf "\033[32m  ✓ %s\033[0m\n" "$1"; }
warn()  { printf "\033[33m  ⚠ %s\033[0m\n" "$1"; }
err()   { printf "\033[31m  ✗ %s\033[0m\n" "$1"; }

# ── Preflight checks ────────────────────────────
echo ""
printf "\033[35m=== Template Integration ===\033[0m\n"
echo "Template : $TEMPLATE_URL"
echo "Branch   : $TEMPLATE_BRANCH"
echo ""

# Must be in a git repo
if [ ! -d ".git" ]; then
    err "Not a git repository. Run this from your project root."
    exit 1
fi

# Must have a clean working tree
if [ -n "$(git status --porcelain)" ]; then
    err "Working tree is dirty. Commit or stash changes first."
    git status --short
    exit 1
fi

# ── Step 1: Add template remote ──────────────────
step "1/6" "Adding template remote..."

if git remote | grep -q "^template$"; then
    warn "Remote 'template' already exists — updating URL."
    git remote set-url template "$TEMPLATE_URL"
else
    git remote add template "$TEMPLATE_URL"
fi
ok "Remote 'template' configured."

# ── Step 2: Fetch template ───────────────────────
step "2/6" "Fetching template..."
git fetch template
ok "Template fetched."

# ── Step 3: Create integration branch and merge ──
step "3/6" "Merging template into integration branch..."

current_branch=$(git branch --show-current)
integration_branch="integrate/template-$(date +%Y%m%d-%H%M%S)"

git checkout -b "$integration_branch"
git merge "template/$TEMPLATE_BRANCH" --allow-unrelated-histories --no-commit --no-ff 2>/dev/null || true

# ── Step 4: Auto-resolve by ownership ────────────
step "4/6" "Resolving conflicts by ownership rules..."

# Files the PROJECT owns — keep ours
for path in src tests README.md package.json pyproject.toml setup.py \
            setup.cfg Cargo.toml go.mod go.sum pom.xml build.gradle \
            Makefile Dockerfile docker-compose.yml docker-compose.yaml; do
    if [ -e "$path" ]; then
        git checkout --ours -- "$path" 2>/dev/null && ok "Kept yours: $path" || true
    fi
done

# Files the TEMPLATE owns — accept theirs
for path in .github/agents .github/prompts .github/copilot-instructions.md \
            .github/workflows/send-feedback-via-issue.yml \
            docs/playbooks docs/discoveries docs/files \
            docs/SECURITY_CHECKLIST.md docs/API_DOCUMENTATION.md \
            scripts AGENTS.md feedback ideas \
            .ai/DEEP_MODE.md .ai/DISPATCH_LOG_TEMPLATE.md \
            .ai/SESSION_TRANSCRIPT_TEMPLATE.md .ai/TRACE_TEMPLATE.md \
            .ai/TEMPLATE_SYNC.md .ai/TOOL_PATHS.md \
            .ai/sessions .ai/plans .ai/todos .ai/specs .ai/previews \
            TEMPLATE_README.md; do
    git checkout --theirs -- "$path" 2>/dev/null && ok "Accepted template: $path" || true
done

# Stage everything
git add -A

# Check for remaining conflicts
conflicts=$(git diff --name-only --diff-filter=U 2>/dev/null || true)
if [ -n "$conflicts" ]; then
    warn "Some conflicts need manual resolution:"
    echo "$conflicts" | while read -r f; do echo "    $f"; done
    echo ""
    echo "  Resolve them, then run:"
    echo "    git add ."
    echo "    git commit -m 'feat: integrate template infrastructure'"
    echo "    git checkout $current_branch"
    echo "    git merge $integration_branch"
    echo "    git branch -d $integration_branch"
    exit 0
fi

# ── Step 5: Commit and merge back ────────────────
step "5/6" "Committing integration..."

git commit -m "feat: integrate template infrastructure"
git checkout "$current_branch"
git merge "$integration_branch" --no-ff -m "feat: integrate template into project"
git branch -d "$integration_branch"

ok "Template merged into '$current_branch'."

# ── Step 6: Add .gitattributes merge guards ──────
step "6/6" "Adding merge guards to .gitattributes..."

guards='
# ── Template merge guards ────────────────────────
# Project code — keep ours during template syncs
src/**            merge=ours
tests/**          merge=ours
README.md         merge=ours

# Template infra — accept theirs during template syncs
.github/agents/** merge=theirs
docs/playbooks/** merge=theirs
AGENTS.md         merge=theirs
scripts/**        merge=theirs'

if [ -f ".gitattributes" ]; then
    if ! grep -q "Template merge guards" .gitattributes; then
        echo "$guards" >> .gitattributes
        ok "Merge guards appended to .gitattributes"
    else
        ok "Merge guards already present."
    fi
else
    echo "$guards" | sed '1d' > .gitattributes
    ok "Created .gitattributes with merge guards."
fi

git add .gitattributes
git commit -m "chore: add template merge guards to .gitattributes" 2>/dev/null || true

# ── Run setup ────────────────────────────────────
if [ "$SKIP_SETUP" != "true" ]; then
    if [ -f "scripts/setup.sh" ]; then
        echo ""
        step "" "Running project setup..."
        chmod +x scripts/setup.sh
        ./scripts/setup.sh
    fi
fi

# ── Summary ──────────────────────────────────────
echo ""
printf "\033[32m=== Integration Complete ===\033[0m\n"
echo ""
echo "  Remotes:"
git remote -v | while read -r line; do echo "    $line"; done
echo ""
echo "  Next steps:"
echo "    1. Review the changes: git log --oneline -5"
echo "    2. Push to your repo:  git push origin $current_branch"
echo "    3. Enable feedback:    Set TEMPLATE_FEEDBACK_ENABLED=true in GitHub repo variables"
echo "    4. Pull updates later: git fetch template && git merge template/main"
echo ""
