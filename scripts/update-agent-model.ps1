# Thin PowerShell wrapper around scripts/update-agent-model.py.
# Propagates sub-agent model assignments from AGENTS.md into the
# frontmatter of each .github/agents/{name}.agent.md file.
#
# Usage:
#   .\scripts\update-agent-model.ps1            # apply changes
#   .\scripts\update-agent-model.ps1 -Check     # exit 1 on drift, no writes
#   .\scripts\update-agent-model.ps1 -DryRun    # show diffs, no writes

[CmdletBinding()]
param(
    [switch]$Check,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "python not found on PATH. Activate your venv first."
    exit 2
}

$args = @()
if ($Check)  { $args += "--check" }
if ($DryRun) { $args += "--dry-run" }

& $python.Source (Join-Path $PSScriptRoot "update-agent-model.py") @args
exit $LASTEXITCODE
