# Installs git hooks from scripts/hooks/ into .git/hooks/
$source = Join-Path $PSScriptRoot "hooks"
$dest = Join-Path (Split-Path $PSScriptRoot) ".git\hooks"

Get-ChildItem $source -File | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $dest $_.Name) -Force
    Write-Host "Installed hook: $($_.Name)"
}
