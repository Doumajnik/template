<#
.SYNOPSIS
    Propagates the AGENT_MODEL value from .ai/PREFERENCES.md to all agent and doc files.

.DESCRIPTION
    Reads the AGENT_MODEL setting from .ai/PREFERENCES.md and updates:
    - All .github/agents/*.agent.md frontmatter (model: line)
    - .ai/DEEP_MODE.md (inline model references)
    - AGENTS.md (inline model references)
    - .github/copilot-instructions.md (inline model references)

    Run this script from the repo root after changing the AGENT_MODEL value in .ai/PREFERENCES.md.

.EXAMPLE
    .\scripts\update-agent-model.ps1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path (Join-Path $repoRoot '.ai\PREFERENCES.md'))) {
    $repoRoot = (Get-Location).Path
}
if (-not (Test-Path (Join-Path $repoRoot '.ai\PREFERENCES.md'))) {
    Write-Error "Cannot find .ai/PREFERENCES.md. Run this script from the repo root."
    exit 1
}

# --- 1. Read current AGENT_MODEL from PREFERENCES.md ---
$prefsPath = Join-Path $repoRoot '.ai\PREFERENCES.md'
$prefsContent = Get-Content $prefsPath -Raw -Encoding UTF8
if ($prefsContent -match '\*\*AGENT_MODEL:\s*(.+?)\*\*') {
    $agentModel = $Matches[1].Trim()
} else {
    Write-Error "Could not find **AGENT_MODEL: ...** in .ai/PREFERENCES.md"
    exit 1
}

# Extract short form (e.g., "Opus 4.6" from "Claude Opus 4.6")
$shortModel = $agentModel
if ($agentModel -match '(?:Claude\s+)?(.+)') {
    $shortModel = $Matches[1].Trim()
}

Write-Host "AGENT_MODEL = '$agentModel' (short: '$shortModel')" -ForegroundColor Cyan
Write-Host ""

$updatedFiles = @()

# --- 2. Update all .agent.md frontmatter ---
$agentDir = Join-Path $repoRoot '.github\agents'
if (Test-Path $agentDir) {
    $agentFiles = Get-ChildItem -Path $agentDir -Filter '*.agent.md'
    foreach ($file in $agentFiles) {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $newContent = $content -replace '(?m)^model:\s*.+$', "model: $agentModel"
        if ($newContent -ne $content) {
            [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.UTF8Encoding]::new($false))
            $updatedFiles += ".github/agents/$($file.Name)"
        }
    }
}

# --- 3. Update inline references in narrative docs ---
$narrativeFiles = @(
    'AGENTS.md',
    '.github\copilot-instructions.md',
    '.ai\DEEP_MODE.md'
)

foreach ($relPath in $narrativeFiles) {
    $filePath = Join-Path $repoRoot $relPath
    if (-not (Test-Path $filePath)) { continue }

    $content = Get-Content $filePath -Raw -Encoding UTF8
    $original = $content

    # Replace "(SomeModel X.Y)" pattern in agent descriptions → "(ShortModel)"
    # Matches patterns like "(Opus 4.6)" or "(GPT-5)" etc.
    $content = $content -replace '\((?:Claude\s+)?(?:Opus|GPT|Gemini|Llama|Mistral)[\s\d.]+\)', "($shortModel)"

    # Replace "ALL SomeModel" in headings like "## Sub-Agent Roster (ALL Opus 4.6)"
    $content = $content -replace '\(ALL\s+(?:Claude\s+)?(?:Opus|GPT|Gemini|Llama|Mistral)[\s\d.]+\)', "(ALL $shortModel)"

    # Replace "Opus 4.6 sub-agent" or "SomeModel sub-agent(s)"
    $content = $content -replace '(?:Claude\s+)?(?:Opus|GPT|Gemini|Llama|Mistral)[\s\d.]+ sub-agent', "$shortModel sub-agent"

    # Replace "Sub-agents (Opus 4.6):" pattern
    $content = $content -replace 'Sub-agents \((?:Claude\s+)?(?:Opus|GPT|Gemini|Llama|Mistral)[\s\d.]+\)', "Sub-agents ($shortModel)"

    if ($content -ne $original) {
        [System.IO.File]::WriteAllText($filePath, $content, [System.Text.UTF8Encoding]::new($false))
        $updatedFiles += $relPath
    }
}

# --- 4. Report ---
Write-Host ""
if ($updatedFiles.Count -eq 0) {
    Write-Host "All files already up to date." -ForegroundColor Green
} else {
    Write-Host "Updated $($updatedFiles.Count) files:" -ForegroundColor Green
    foreach ($f in $updatedFiles) {
        Write-Host "  - $f" -ForegroundColor Gray
    }
}
Write-Host ""
Write-Host "Done. All agent model references now set to: $agentModel" -ForegroundColor Cyan
