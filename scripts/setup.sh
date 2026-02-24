#!/bin/sh
# Project setup script (Unix/macOS/WSL/Git Bash)
# Creates standard directory structure, installs git hooks,
# and detects language to set up the environment.
# Usage: ./scripts/setup.sh

set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

echo "[1/3] Setting up project structure..."

# ── Create standard directories ─────────────────
for dir in src/config src/models src/services src/utils tests scripts docs .ai/sessions .ai/plans/impl; do
    mkdir -p "$dir"
done

# ── Install git hooks ───────────────────────────
echo "[2/3] Installing git hooks..."
HOOKS_SRC="$ROOT/scripts/hooks"
HOOKS_DST="$ROOT/.git/hooks"
if [ -d "$HOOKS_SRC" ]; then
    for hook in "$HOOKS_SRC"/*; do
        cp "$hook" "$HOOKS_DST/$(basename "$hook")"
        chmod +x "$HOOKS_DST/$(basename "$hook")"
    done
    echo "   Installed: $(ls "$HOOKS_SRC" | tr '\n' ' ')"
fi

# ── Detect language and set up environment ──────
echo "[3/3] Detecting project language..."

# Python
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "Pipfile" ]; then
    echo "  -> Python detected"
    if [ ! -d ".venv" ]; then
        echo "   Creating virtual environment..."
        python -m venv .venv
    fi
    echo "   Activating venv and installing dependencies..."
    . .venv/bin/activate
    pip install --upgrade pip -q
    [ -f "requirements.txt" ] && pip install -r requirements.txt -q
    [ -f "requirements-dev.txt" ] && pip install -r requirements-dev.txt -q
    [ -f "pyproject.toml" ] && pip install -e ".[dev]" -q 2>/dev/null || true
    echo "   OK: Python environment ready"
fi

# Node.js
if [ -f "package.json" ]; then
    echo "  -> Node.js detected"
    if command -v npm >/dev/null 2>&1; then
        npm install
        echo "   OK: Node dependencies installed"
    else
        echo "   WARN: npm not found -- install Node.js first"
    fi
fi

# .NET
if ls *.sln *.csproj 2>/dev/null | head -1 >/dev/null 2>&1; then
    echo "  -> .NET detected"
    if command -v dotnet >/dev/null 2>&1; then
        dotnet restore
        echo "   OK: .NET packages restored"
    else
        echo "   WARN: dotnet not found -- install .NET SDK first"
    fi
fi

# Go
if [ -f "go.mod" ]; then
    echo "  -> Go detected"
    if command -v go >/dev/null 2>&1; then
        go mod download
        echo "   OK: Go modules downloaded"
    else
        echo "   WARN: go not found -- install Go first"
    fi
fi

# Rust
if [ -f "Cargo.toml" ]; then
    echo "  -> Rust detected"
    if command -v cargo >/dev/null 2>&1; then
        cargo fetch
        echo "   OK: Rust crates fetched"
    else
        echo "   WARN: cargo not found -- install Rust first"
    fi
fi

# Java (Maven)
if [ -f "pom.xml" ]; then
    echo "  -> Java (Maven) detected"
    if command -v mvn >/dev/null 2>&1; then
        mvn dependency:resolve -q
        echo "   OK: Maven dependencies resolved"
    else
        echo "   WARN: mvn not found -- install Maven first"
    fi
fi

# Java (Gradle)
if [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    echo "  -> Java (Gradle) detected"
    if [ -f "gradlew" ]; then
        ./gradlew dependencies --quiet
        echo "   OK: Gradle dependencies resolved"
    elif command -v gradle >/dev/null 2>&1; then
        gradle dependencies --quiet
        echo "   OK: Gradle dependencies resolved"
    else
        echo "   WARN: gradle not found -- install Gradle first"
    fi
fi

echo ""
echo "Done! Setup complete. Project is ready."
