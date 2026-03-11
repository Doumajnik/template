# Feedback Pipeline Setup (Windows PowerShell)
# Configures the GitHub secret and variables needed by the feedback workflows.
# Supports two modes:
#   dispatch — for repos you own (uses repository_dispatch, needs repo write access)
#   issue    — for forks/external users (opens a GitHub Issue, needs public_repo scope)
#
# Prerequisites: gh CLI installed and authenticated (gh auth login).
# Usage: .\scripts\setup-feedback.ps1

$ErrorActionPreference = "Stop"

Write-Host "=== Feedback Pipeline Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check gh CLI
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: GitHub CLI (gh) is required. Install it: https://cli.github.com" -ForegroundColor Red
    exit 1
}

# Check auth
try { gh auth status 2>&1 | Out-Null } catch {
    Write-Host "ERROR: Not authenticated. Run: gh auth login" -ForegroundColor Red
    exit 1
}

# Get current repo
$Repo = gh repo view --json nameWithOwner -q '.nameWithOwner' 2>$null
if ([string]::IsNullOrWhiteSpace($Repo)) {
    Write-Host "ERROR: Not inside a GitHub repo, or repo has no remote." -ForegroundColor Red
    exit 1
}

Write-Host "Project repo: $Repo"
Write-Host ""

# Choose feedback mode
Write-Host "How do you send feedback to the template?" -ForegroundColor Yellow
Write-Host "  [1] dispatch — You own the template repo (direct push via repository_dispatch)"
Write-Host "  [2] issue    — You forked the template or are an external contributor (opens a GitHub Issue)"
Write-Host ""
$ModeChoice = Read-Host "Choose mode (1 or 2)"

switch ($ModeChoice) {
    "1" { $Mode = "dispatch" }
    "2" { $Mode = "issue" }
    default {
        Write-Host "ERROR: Invalid choice. Enter 1 or 2." -ForegroundColor Red
        exit 1
    }
}

Write-Host "  -> Mode: $Mode" -ForegroundColor Green
Write-Host ""

# Ask for template repo
$TemplateRepo = Read-Host "Enter the template repo (owner/repo)"
if ([string]::IsNullOrWhiteSpace($TemplateRepo)) {
    Write-Host "ERROR: Template repo is required." -ForegroundColor Red
    exit 1
}

# Validate template repo exists
try { gh repo view $TemplateRepo 2>&1 | Out-Null } catch {
    Write-Host "ERROR: Cannot access $TemplateRepo. Check the name and your permissions." -ForegroundColor Red
    exit 1
}

# Set variables
$Step = 1
$TotalSteps = if ($Mode -eq "dispatch") { 4 } else { 4 }

Write-Host ""
Write-Host "[$Step/$TotalSteps] Setting TEMPLATE_REPO variable..." -ForegroundColor Yellow
gh variable set TEMPLATE_REPO --body $TemplateRepo --repo $Repo
Write-Host "  -> TEMPLATE_REPO=$TemplateRepo" -ForegroundColor Green
$Step++

Write-Host ""
Write-Host "[$Step/$TotalSteps] Setting TEMPLATE_FEEDBACK_ENABLED variable..." -ForegroundColor Yellow
gh variable set TEMPLATE_FEEDBACK_ENABLED --body "true" --repo $Repo
Write-Host "  -> TEMPLATE_FEEDBACK_ENABLED=true" -ForegroundColor Green
$Step++

Write-Host ""
Write-Host "[$Step/$TotalSteps] Setting TEMPLATE_FEEDBACK_MODE variable..." -ForegroundColor Yellow
gh variable set TEMPLATE_FEEDBACK_MODE --body $Mode --repo $Repo
Write-Host "  -> TEMPLATE_FEEDBACK_MODE=$Mode" -ForegroundColor Green
$Step++

Write-Host ""
Write-Host "[$Step/$TotalSteps] Setting TEMPLATE_FEEDBACK_TOKEN secret..." -ForegroundColor Yellow
Write-Host ""

if ($Mode -eq "dispatch") {
    Write-Host "You need a GitHub PAT (classic) with 'repo' scope (write access to template repo)."
    Write-Host "Create one at: https://github.com/settings/tokens/new"
    Write-Host "  - Note: template-feedback-$Repo"
    Write-Host "  - Scopes: repo (full)"
} else {
    Write-Host "You need a GitHub PAT (classic) with 'public_repo' scope (to open issues on the template)."
    Write-Host "Create one at: https://github.com/settings/tokens/new"
    Write-Host "  - Note: template-feedback-$Repo"
    Write-Host "  - Scopes: public_repo"
}

Write-Host ""

$SecureToken = Read-Host "Paste your PAT" -AsSecureString
$Token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
)

if ([string]::IsNullOrWhiteSpace($Token)) {
    Write-Host "ERROR: Token is required." -ForegroundColor Red
    exit 1
}

$Token | gh secret set TEMPLATE_FEEDBACK_TOKEN --repo $Repo
Write-Host "  -> Secret TEMPLATE_FEEDBACK_TOKEN saved." -ForegroundColor Green

Write-Host ""
Write-Host "=== Setup complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mode: $Mode"
Write-Host ""
Write-Host "The feedback pipeline is now active. When these files change on main,"
Write-Host "updates will be sent to $TemplateRepo automatically:"
Write-Host "  - docs/RETROSPECTIVE_REPORT.md"
Write-Host "  - docs/PLAYBOOK.md"
Write-Host "  - docs/QUALITY_REPORT.md"
Write-Host "  - docs/SECURITY_REPORT.md"
Write-Host "  - .ai/lessons.md"
Write-Host ""

if ($Mode -eq "dispatch") {
    Write-Host "Feedback is sent via repository_dispatch (direct to template)."
} else {
    Write-Host "Feedback is sent as a GitHub Issue on $TemplateRepo."
    Write-Host "The template maintainer reviews and merges improvements via PR."
}

Write-Host ""
Write-Host "You can also trigger it manually: Actions > Send Feedback to Template > Run workflow"
