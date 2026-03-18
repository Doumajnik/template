# Integrates the template into an existing project.
# Adds template as a remote, merges infrastructure files, preserves project code.
#
# Usage:
#   .\scripts\integrate.ps1 -TemplateUrl "https://github.com/Doumajnik/template.git"
#   .\scripts\integrate.ps1  # uses default URL
#
# Run from the ROOT of your existing project.

param(
    [string]$TemplateUrl = "https://github.com/Doumajnik/template.git",
    [string]$TemplateBranch = "main",
    [switch]$SkipSetup
)

$ErrorActionPreference = "Stop"

# ── Helpers ──────────────────────────────────────
function Write-Step { param([string]$Num, [string]$Msg) Write-Host "[$Num] $Msg" -ForegroundColor Cyan }
function Write-Ok   { param([string]$Msg) Write-Host "  ✓ $Msg" -ForegroundColor Green }
function Write-Warn { param([string]$Msg) Write-Host "  ⚠ $Msg" -ForegroundColor Yellow }
function Write-Err  { param([string]$Msg) Write-Host "  ✗ $Msg" -ForegroundColor Red }

# ── Preflight checks ────────────────────────────
Write-Host ""
Write-Host "=== Template Integration ===" -ForegroundColor Magenta
Write-Host "Template : $TemplateUrl"
Write-Host "Branch   : $TemplateBranch"
Write-Host ""

# Must be in a git repo
if (-not (Test-Path ".git")) {
    Write-Err "Not a git repository. Run this from your project root."
    exit 1
}

# Must have a clean working tree
$status = git status --porcelain
if ($status) {
    Write-Err "Working tree is dirty. Commit or stash changes first."
    Write-Host $status
    exit 1
}

# ── Step 1: Add template remote ──────────────────
Write-Step "1/6" "Adding template remote..."

$existingRemote = git remote | Where-Object { $_ -eq "template" }
if ($existingRemote) {
    Write-Warn "Remote 'template' already exists — updating URL."
    git remote set-url template $TemplateUrl
} else {
    git remote add template $TemplateUrl
}
Write-Ok "Remote 'template' configured."

# ── Step 2: Fetch template ───────────────────────
Write-Step "2/6" "Fetching template..."
git fetch template
Write-Ok "Template fetched."

# ── Step 3: Create integration branch and merge ──
Write-Step "3/6" "Merging template into integration branch..."

$currentBranch = git branch --show-current
$integrationBranch = "integrate/template-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

git checkout -b $integrationBranch
git merge "template/$TemplateBranch" --allow-unrelated-histories --no-commit --no-ff 2>$null

# ── Step 4: Auto-resolve by ownership ────────────
Write-Step "4/6" "Resolving conflicts by ownership rules..."

# Files the PROJECT owns — keep ours
$projectOwned = @("src", "tests", "README.md", "package.json", "pyproject.toml", "setup.py",
                   "setup.cfg", "Cargo.toml", "go.mod", "go.sum", "pom.xml", "build.gradle",
                   "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml")

foreach ($path in $projectOwned) {
    if (Test-Path $path) {
        git checkout --ours -- $path 2>$null
        if ($LASTEXITCODE -eq 0) { Write-Ok "Kept yours: $path" }
    }
}

# Files the TEMPLATE owns — accept theirs
$templateOwned = @(".github/agents", ".github/prompts", ".github/copilot-instructions.md",
                    ".github/workflows/send-feedback-via-issue.yml",
                    "docs/playbooks", "docs/discoveries", "docs/files",
                    "docs/SECURITY_CHECKLIST.md", "docs/API_DOCUMENTATION.md",
                    "scripts", "AGENTS.md", "feedback", "ideas",
                    ".ai/DEEP_MODE.md", ".ai/DISPATCH_LOG_TEMPLATE.md",
                    ".ai/SESSION_TRANSCRIPT_TEMPLATE.md", ".ai/TRACE_TEMPLATE.md",
                    ".ai/TEMPLATE_SYNC.md", ".ai/TOOL_PATHS.md",
                    ".ai/sessions", ".ai/plans", ".ai/todos", ".ai/specs", ".ai/previews",
                    "TEMPLATE_README.md")

foreach ($path in $templateOwned) {
    git checkout --theirs -- $path 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Ok "Accepted template: $path" }
}

# Stage everything
git add -A

# Check for remaining conflicts
$conflicts = git diff --name-only --diff-filter=U
if ($conflicts) {
    Write-Warn "Some conflicts need manual resolution:"
    $conflicts | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
    Write-Host ""
    Write-Host "  Resolve them, then run:" -ForegroundColor Yellow
    Write-Host "    git add ." -ForegroundColor White
    Write-Host "    git commit -m 'feat: integrate template infrastructure'" -ForegroundColor White
    Write-Host "    git checkout $currentBranch" -ForegroundColor White
    Write-Host "    git merge $integrationBranch" -ForegroundColor White
    Write-Host "    git branch -d $integrationBranch" -ForegroundColor White
    exit 0
}

# ── Step 5: Commit and merge back ────────────────
Write-Step "5/6" "Committing integration..."

git commit -m "feat: integrate template infrastructure"
git checkout $currentBranch
git merge $integrationBranch --no-ff -m "feat: integrate template into project"
git branch -d $integrationBranch

Write-Ok "Template merged into '$currentBranch'."

# ── Step 6: Add .gitattributes merge guards ──────
Write-Step "6/6" "Adding merge guards to .gitattributes..."

$guards = @"

# ── Template merge guards ────────────────────────
# Project code — keep ours during template syncs
src/**            merge=ours
tests/**          merge=ours
README.md         merge=ours

# Template infra — accept theirs during template syncs
.github/agents/** merge=theirs
docs/playbooks/** merge=theirs
AGENTS.md         merge=theirs
scripts/**        merge=theirs
"@

if (Test-Path ".gitattributes") {
    $existing = Get-Content ".gitattributes" -Raw
    if ($existing -notmatch "Template merge guards") {
        Add-Content ".gitattributes" $guards
        Write-Ok "Merge guards appended to .gitattributes"
    } else {
        Write-Ok "Merge guards already present."
    }
} else {
    Set-Content ".gitattributes" $guards.TrimStart()
    Write-Ok "Created .gitattributes with merge guards."
}

git add .gitattributes
git commit -m "chore: add template merge guards to .gitattributes" 2>$null

# ── Run setup ────────────────────────────────────
if (-not $SkipSetup) {
    if (Test-Path "scripts\setup.ps1") {
        Write-Host ""
        Write-Host "Running project setup..." -ForegroundColor Cyan
        & ".\scripts\setup.ps1"
    }
}

# ── Summary ──────────────────────────────────────
Write-Host ""
Write-Host "=== Integration Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "  Remotes:" -ForegroundColor White
git remote -v | ForEach-Object { Write-Host "    $_" }
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor White
Write-Host "    1. Review the changes: git log --oneline -5"
Write-Host "    2. Push to your repo:  git push origin $currentBranch"
Write-Host "    3. Enable feedback:    Set TEMPLATE_FEEDBACK_ENABLED=true in GitHub repo variables"
Write-Host "    4. Pull updates later: git fetch template && git merge template/main"
Write-Host ""
