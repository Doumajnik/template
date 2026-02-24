# Project setup script (Windows PowerShell)
# Creates standard directory structure, installs git hooks,
# and detects language to set up the environment.
# Usage: .\scripts\setup.ps1

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot

Set-Location $Root

Write-Host "[1/3] Setting up project structure..." -ForegroundColor Cyan

# ── Create standard directories ─────────────────
$dirs = @(
    "src\config", "src\models", "src\services", "src\utils",
    "tests", "scripts", "docs",
    ".ai\sessions", ".ai\plans\impl"
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
}

# ── Install git hooks ───────────────────────────
Write-Host "[2/3] Installing git hooks..." -ForegroundColor Cyan
$hooksSrc = Join-Path $Root "scripts\hooks"
$hooksDst = Join-Path $Root ".git\hooks"
if (Test-Path $hooksSrc) {
    Get-ChildItem $hooksSrc -File | ForEach-Object {
        Copy-Item $_.FullName (Join-Path $hooksDst $_.Name) -Force
        Write-Host "   Installed: $($_.Name)"
    }
}

# ── Detect language and set up environment ──────
Write-Host "[3/3] Detecting project language..." -ForegroundColor Cyan

# Python
if ((Test-Path "requirements.txt") -or (Test-Path "pyproject.toml") -or (Test-Path "setup.py") -or (Test-Path "Pipfile")) {
    Write-Host "  -> Python detected" -ForegroundColor Yellow
    if (-not (Test-Path ".venv")) {
        Write-Host "   Creating virtual environment..."
        python -m venv .venv
    }
    Write-Host "   Activating venv and installing dependencies..."
    & ".venv\Scripts\Activate.ps1"
    python -m pip install --upgrade pip -q
    if (Test-Path "requirements.txt") { pip install -r requirements.txt -q }
    if (Test-Path "requirements-dev.txt") { pip install -r requirements-dev.txt -q }
    if (Test-Path "pyproject.toml") { pip install -e ".[dev]" -q 2>$null; if ($LASTEXITCODE) { pip install -e . -q } }
    Write-Host "   OK: Python environment ready" -ForegroundColor Green
}

# Node.js
if (Test-Path "package.json") {
    Write-Host "  -> Node.js detected" -ForegroundColor Yellow
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install
        Write-Host "   OK: Node dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "   WARN: npm not found -- install Node.js first" -ForegroundColor Red
    }
}

# .NET
if ((Get-ChildItem -Filter "*.sln" -ErrorAction SilentlyContinue) -or (Get-ChildItem -Filter "*.csproj" -ErrorAction SilentlyContinue)) {
    Write-Host "  -> .NET detected" -ForegroundColor Yellow
    if (Get-Command dotnet -ErrorAction SilentlyContinue) {
        dotnet restore
        Write-Host "   OK: .NET packages restored" -ForegroundColor Green
    } else {
        Write-Host "   WARN: dotnet not found -- install .NET SDK first" -ForegroundColor Red
    }
}

# Go
if (Test-Path "go.mod") {
    Write-Host "  -> Go detected" -ForegroundColor Yellow
    if (Get-Command go -ErrorAction SilentlyContinue) {
        go mod download
        Write-Host "   OK: Go modules downloaded" -ForegroundColor Green
    } else {
        Write-Host "   WARN: go not found -- install Go first" -ForegroundColor Red
    }
}

# Rust
if (Test-Path "Cargo.toml") {
    Write-Host "  -> Rust detected" -ForegroundColor Yellow
    if (Get-Command cargo -ErrorAction SilentlyContinue) {
        cargo fetch
        Write-Host "   OK: Rust crates fetched" -ForegroundColor Green
    } else {
        Write-Host "   WARN: cargo not found -- install Rust first" -ForegroundColor Red
    }
}

# Java (Maven)
if (Test-Path "pom.xml") {
    Write-Host "  -> Java (Maven) detected" -ForegroundColor Yellow
    if (Get-Command mvn -ErrorAction SilentlyContinue) {
        mvn dependency:resolve -q
        Write-Host "   OK: Maven dependencies resolved" -ForegroundColor Green
    } else {
        Write-Host "   WARN: mvn not found -- install Maven first" -ForegroundColor Red
    }
}

# Java (Gradle)
if ((Test-Path "build.gradle") -or (Test-Path "build.gradle.kts")) {
    Write-Host "  -> Java (Gradle) detected" -ForegroundColor Yellow
    if (Test-Path "gradlew.bat") {
        .\gradlew.bat dependencies --quiet
        Write-Host "   OK: Gradle dependencies resolved" -ForegroundColor Green
    } elseif (Get-Command gradle -ErrorAction SilentlyContinue) {
        gradle dependencies --quiet
        Write-Host "   OK: Gradle dependencies resolved" -ForegroundColor Green
    } else {
        Write-Host "   WARN: gradle not found -- install Gradle first" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done! Setup complete. Project is ready." -ForegroundColor Green
