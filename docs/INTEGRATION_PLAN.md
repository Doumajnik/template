# Integration Plan: Template → Existing Project

> **Strategy:** Template-as-Upstream-Remote
> **Audience:** Solo dev / small team (1–5 people)
> **Result:** Full template in every project. Project code pushes to its own repo. Template updates pulled on demand.

---

## Prerequisites

- [ ] An existing project with a git repo (local or on GitHub)
- [ ] The template repo URL (e.g. `https://github.com/Doumajnik/template.git`)
- [ ] Git installed and configured
- [ ] For feedback loop: a GitHub PAT with `public_repo` scope

---

## Phase 1 — Initial Integration (one-time)

### Step 1: Add Template Remote

```bash
cd your-project
git remote add template https://github.com/Doumajnik/template.git
git fetch template
```

### Step 2: Merge Template Into Project

```bash
git checkout -b integrate/template
git merge template/main --allow-unrelated-histories --no-commit
```

### Step 3: Resolve Conflicts by Ownership

| Keep **yours** (project) | Accept **template** | Merge **both** |
|---|---|---|
| `src/**` | `.github/agents/` | `.gitignore` |
| `tests/**` | `.github/prompts/` | `docs/BUSINESS_LOGIC.md` |
| `README.md` | `.github/copilot-instructions.md` | `docs/CODE_INVENTORY.md` |
| `package.json` / `pyproject.toml` | `.github/workflows/send-feedback-via-issue.yml` | `.ai/PREFERENCES.md` |
| `.env` / config files | `docs/playbooks/**` | `.ai/lessons.md` |
| App-specific docs | `scripts/**` | |
| | `AGENTS.md` | |
| | `feedback/` | |
| | `ideas/` | |
| | `.ai/` (templates, sessions structure) | |
| | `docs/discoveries/`, `docs/files/` | |

### Step 4: Commit and Push

```bash
git add .
git commit -m "feat: integrate template infrastructure"
git checkout main
git merge integrate/template
git branch -d integrate/template
git push origin main
```

### Step 5: Add Merge Guard (.gitattributes)

Append to your project's `.gitattributes`:

```gitattributes
# Project code — keep ours during template merges
src/**            merge=ours
tests/**          merge=ours
README.md         merge=ours

# Template infra — accept theirs during template merges
.github/agents/** merge=theirs
docs/playbooks/** merge=theirs
AGENTS.md         merge=theirs
scripts/**        merge=theirs
```

### Step 6: Run Setup

```bash
# Windows
.\scripts\setup.ps1

# Unix/macOS
./scripts/setup.sh
```

This installs git hooks and sets up the project environment.

---

## Phase 2 — Onboard the Codebase (agent-powered audit)

After integration, let the agents discover, document, and audit your existing code. **No code is changed** — this is read-only. Run it by telling copilot:

> "Onboard this project — discover, document, audit, and suggest improvements."

Or use the prompt file directly: `.github/prompts/onboard-project.prompt.md`

### The Onboarding Pipeline

```
Phase 1 — DISCOVER                 Phase 2 — DOCUMENT
┌─────────────────────┐            ┌─────────────────────────┐
│  🔍 Discovery Agent │            │  📝 Doc Updater Agent   │
│                     │            │                         │
│  Reads entire src/  │───────────►│  Fills in:              │
│  Maps structure     │  summary   │  • BUSINESS_LOGIC.md    │
│  Finds entry points │            │  • CODE_INVENTORY.md    │
│  Catalogs models    │            │  • API_DOCUMENTATION.md │
│  Lists integrations │            │  • docs/files/*.md      │
└─────────────────────┘            └────────────┬────────────┘
                                                │
              ┌─────────────────────────────────┘
              │
              ▼
Phase 3 — AUDIT (all run in parallel)
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 🔒 Security  │ │ 📊 Code      │ │ 📦 Dependency│
│   Agent      │ │   Quality    │ │   Agent      │
│              │ │   Agent      │ │              │
│ Vulns        │ │ Duplication  │ │ Outdated     │
│ Secrets      │ │ Dead code    │ │ CVEs         │
│ Injection    │ │ Complexity   │ │ Licenses     │
│ Auth gaps    │ │ Smells       │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ⚠️ Error     │ │ 🔤 Type      │ │ 📡 Monitoring│
│  Handling    │ │  Safety      │ │   Agent      │
│  Agent       │ │  Agent       │              │
│              │ │              │ │ Logging gaps │
│ Silent catch │ │ Missing types│ │ No health    │
│ Swallowed ex │ │ Unsafe casts │ │  checks      │
│ Missing ctx  │ │ Schema drift │ │ No alerting  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
Phase 4 — TEST (safety net before ANY changes)
┌─────────────────────────────────────────┐
│  🧪 Test Writer Agent (per source file) │
│  15+ unit tests per function            │
│  → tests/ (mirrors src/)               │
│                                         │
│  🔗 Integration Tester Agent            │
│  Cross-module flows, API contracts      │
│  → tests/integration/                   │
│                                         │
│  ▶️ Run all → record baseline           │
│  → .ai/plans/{date}_test-baseline.md    │
└─────────────────────────────────────────┘
                        │
                        ▼
Phase 5 — PLAN
┌─────────────────────────────────────────┐
│  📋 Prioritized Improvement Plan        │
│                                         │
│  🔴 Critical — fix now (security, CVEs, │
│     existing bugs found by tests)       │
│  🟠 High — this sprint (quality, errors)│
│  🟡 Medium — next sprint (monitoring)   │
│  🟢 Low — backlog (style, conventions)  │
│                                         │
│  → .ai/plans/{date}_onboarding.md       │
└─────────────────────────────────────────┘
                        │
                        ▼
Phase 6 — PRESENT
┌─────────────────────────────────────────┐
│  "Tests are in place as a safety net.   │
│   Top 5 actions:                        │
│   1. Hardcoded DB password in config.py │
│   2. 3 critical CVEs in dependencies    │
│   3. 5 existing bugs found by tests     │
│   4. 40% of exceptions silently caught  │
│   5. No health check endpoint           │
│                                         │
│   Start fixing? Tests verify each fix." │
└─────────────────────────────────────────┘

After fixes — the verify loop:
┌─────────────────────────────────────────┐
│  Worker fixes issue                     │
│         │                               │
│         ▼                               │
│  Run full test suite                    │
│         │                               │
│   Pass? ├── ✅ Next fix                 │
│         └── 🔴 Fix regression first     │
│                  │                      │
│                  ▼                      │
│             Re-run tests → ✅ Continue  │
└─────────────────────────────────────────┘
```

### What Gets Produced

| Agent | Output File | What It Contains |
|---|---|---|
| Discovery | `docs/discoveries/{date}_existing-codebase.md` | Full codebase map |
| Doc Updater | `docs/BUSINESS_LOGIC.md`, `docs/CODE_INVENTORY.md`, etc. | Project documentation |
| Security | `docs/SECURITY_REPORT.md` | Vulnerabilities, hardcoded secrets, auth gaps |
| Code Quality | `docs/QUALITY_REPORT.md` | Duplication, dead code, complexity |
| Dependency | `docs/DEPENDENCY_REPORT.md` | Outdated packages, CVEs, license issues |
| Error Handling | `docs/ERROR_HANDLING_REPORT.md` | Silent catches, swallowed exceptions |
| Type Safety | `docs/TYPE_SAFETY_REPORT.md` | Missing types, unsafe casts |
| Monitoring | `docs/MONITORING_REPORT.md` | Logging/health check/alerting gaps |
| Test Writer | `tests/**` | 15+ unit tests per function |
| Integration Tester | `tests/integration/` | Cross-module flow tests |
| Baseline | `.ai/plans/{date}_test-baseline.md` | Pass/fail counts, existing bugs |
| Orchestrator | `.ai/plans/{date}_onboarding-improvements.md` | Prioritized fix plan |

---

## Phase 3 — Enable Feedback Loop

### Step 1: Set Repository Variables (GitHub Settings → Variables)

| Variable | Value |
|---|---|
| `TEMPLATE_FEEDBACK_ENABLED` | `true` |
| `TEMPLATE_REPO` | `Doumajnik/template` (or your template repo) |

### Step 2: Set Repository Secret (GitHub Settings → Secrets)

| Secret | Value |
|---|---|
| `TEMPLATE_FEEDBACK_PAT` | PAT with `public_repo` scope |

### Step 3: Verify

Push to main. The `send-feedback-via-issue.yml` workflow should run. If agent reports have content, an issue appears on the template repo.

---

## Phase 4 — Ongoing Sync

### Pull Template Updates

```bash
git fetch template
git checkout -b template-sync
git merge template/main
# Resolve any conflicts per the ownership table above
git checkout main
git merge template-sync
git branch -d template-sync
git push origin main
```

### Recommended Cadence

| Team Size | Sync Frequency |
|---|---|
| Solo | After each template improvement you want |
| 2–3 people | Weekly or bi-weekly |
| 4–5 people | Start of each sprint |

---

## Automated Integration Script

Instead of doing the steps above manually, run:

```bash
# Windows PowerShell
.\scripts\integrate.ps1 -TemplateUrl "https://github.com/Doumajnik/template.git"

# Unix / macOS / Git Bash
./scripts/integrate.sh "https://github.com/Doumajnik/template.git"
```

The script handles:
1. Adding the template remote
2. Fetching and merging with conflict markers
3. Auto-accepting template-owned files
4. Preserving project-owned files
5. Adding `.gitattributes` merge guards
6. Running `setup.ps1` / `setup.sh`

---

## What Gets Integrated

### Files From Template

```
.github/
  ├── agents/          (32 agent instruction files)
  ├── prompts/         (5 prompt templates)
  ├── copilot-instructions.md
  └── workflows/
      └── send-feedback-via-issue.yml

.ai/
  ├── PREFERENCES.md
  ├── DEEP_MODE.md
  ├── DISPATCH_LOG_TEMPLATE.md
  ├── SESSION_TRANSCRIPT_TEMPLATE.md
  ├── TRACE_TEMPLATE.md
  ├── TEMPLATE_SYNC.md
  ├── TOOL_PATHS.md
  ├── sessions/
  ├── plans/
  ├── todos/
  ├── specs/
  └── previews/

docs/
  ├── playbooks/
  │   ├── shared/      (9 shared rules)
  │   ├── agents/      (32 agent playbooks)
  │   └── technologies/ (language-specific rules)
  ├── discoveries/
  ├── files/
  ├── PLAYBOOK.md
  ├── SECURITY_CHECKLIST.md
  └── API_DOCUMENTATION.md

scripts/
  ├── setup.ps1
  ├── setup.sh
  ├── install-hooks.ps1
  └── hooks/

AGENTS.md
feedback/
ideas/
```

### Files That Stay Yours

```
src/           → Your application code
tests/         → Your test suites
README.md      → Your project description
*.toml / *.json → Your dependency configs
.env           → Your environment variables
```

---

## Verification Checklist

After integration, confirm:

- [ ] `git remote -v` shows both `origin` (project) and `template`
- [ ] `.github/agents/` directory exists with 32 `.agent.md` files
- [ ] `docs/playbooks/` directory exists with shared/agent/tech rules
- [ ] `.ai/PREFERENCES.md` exists
- [ ] `AGENTS.md` exists at project root
- [ ] `scripts/setup.ps1` and `setup.sh` exist
- [ ] `feedback/` and `ideas/` directories exist
- [ ] Git hooks are installed (check `.git/hooks/`)
- [ ] `git push origin main` works (code goes to YOUR repo)
- [ ] `git fetch template` works (template updates available)
- [ ] Your `src/` and `tests/` are untouched
