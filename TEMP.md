# 🧬 Using This Template in Your Projects

> **Audience:** Solo developer or small team (1–5 people)
> **Goal:** Full template power in every project — project code stays separate from template code

---

## The Big Picture

You have **two repos**. The template is infrastructure. Your project is product. They merge locally but push separately.

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR MACHINE                         │
│                                                         │
│   ┌─────────────────────────────────────────────────┐   │
│   │           your-project/  (one directory)        │   │
│   │                                                 │   │
│   │   🧬 Template files     📦 Your code           │   │
│   │   ├── .github/agents/   ├── src/                │   │
│   │   ├── .ai/              ├── tests/              │   │
│   │   ├── docs/playbooks/   ├── README.md           │   │
│   │   ├── scripts/          ├── pyproject.toml      │   │
│   │   ├── AGENTS.md         └── .env                │   │
│   │   ├── feedback/                                 │   │
│   │   └── ideas/                                    │   │
│   └─────────────────────────────────────────────────┘   │
│          │                          │                   │
│     git pull template          git push origin          │
│          │                          │                   │
└──────────┼──────────────────────────┼───────────────────┘
           │                          │
           ▼                          ▼
   ┌───────────────┐         ┌────────────────┐
   │  🧬 Template  │         │  📦 Project   │
   │  Repo         │         │  Repo          │
   │  (upstream)   │         │  (origin)      │
   └───────────────┘         └────────────────┘
```

**Key insight:** Your project repo contains *everything* — template infra + your code. But you only push to your project repo. The template repo is read-only from your project's perspective.

---

## Who Owns What

| Owned by Template 🧬 | Owned by Project 📦 | Shared (merge both) |
|---|---|---|
| `.github/agents/` | `src/` | `.gitignore` |
| `.github/prompts/` | `tests/` | `docs/BUSINESS_LOGIC.md` |
| `.github/copilot-instructions.md` | `README.md` | `docs/CODE_INVENTORY.md` |
| `docs/playbooks/` | `pyproject.toml` / `package.json` | `docs/SECURITY_REPORT.md` |
| `scripts/` | `.env` / config | `docs/QUALITY_REPORT.md` |
| `AGENTS.md` | App-specific docs | `.ai/PREFERENCES.md` |
| `feedback/` structure | — | `.ai/lessons.md` |
| `ideas/` structure | — | — |

> **Rule of thumb:** If it's about *how to work*, the template owns it. If it's about *what you're building*, the project owns it.

---

## Setup (Do Once)

```
  ① Clone your project
         │
         ▼
  ② Add template as remote ──────────── git remote add template <url>
         │
         ▼
  ③ Fetch template ──────────────────── git fetch template
         │
         ▼
  ④ Merge with --allow-unrelated-histories
         │
         ▼
  ⑤ Resolve conflicts ──────────────── Template infra → accept template
         │                               Project code  → keep yours
         │                               Shared files  → merge both
         ▼
  ⑥ Add .gitattributes ─────────────── Protects against future overwrites
         │
         ▼
  ⑦ Push to project repo ───────────── git push origin main
         │
         ▼
       ✅ Done — template is live in your project
```

### Commands

```bash
# ① Already have your project cloned
cd your-project

# ② + ③ Add template remote
git remote add template https://github.com/Doumajnik/template.git
git fetch template

# ④ First-time merge
git merge template/main --allow-unrelated-histories --no-commit

# ⑤ Resolve conflicts — see "Who Owns What" table above
# Then:
git add .
git commit -m "feat: integrate template infrastructure"

# ⑥ Add merge guard (see below)

# ⑦ Push
git push origin main
```

### Merge Guard (`.gitattributes`)

Add this to your project root to make future template pulls safer:

```gitattributes
# YOUR CODE — always keep yours during template merges
src/**            merge=ours
tests/**          merge=ours
README.md         merge=ours

# TEMPLATE FILES — always accept template updates
.github/agents/** merge=theirs
docs/playbooks/** merge=theirs
AGENTS.md         merge=theirs
scripts/**        merge=theirs
```

---

## Onboarding: Discover, Document, Audit 🔍

Right after integration, let the agents map, audit, and test-harness your existing codebase.

Tell copilot: *"Onboard this project"* — or use `.github/prompts/onboard-project.prompt.md`

```
┌──────────────────────────────────────────────────────────────┐
│                    ONBOARDING PIPELINE                        │
│                                                              │
│  Phase 1 ─ DISCOVER                                          │
│  ┌──────────────────────────────────────────────┐            │
│  │  🔍 Discovery Agent                          │            │
│  │  Reads all src/, tests/, configs             │            │
│  │  → docs/discoveries/{date}_codebase.md       │            │
│  └──────────────────────┬───────────────────────┘            │
│                         │                                    │
│  Phase 2 ─ DOCUMENT     ▼                                    │
│  ┌──────────────────────────────────────────────┐            │
│  │  📝 Doc Updater Agent                        │            │
│  │  → BUSINESS_LOGIC.md  → CODE_INVENTORY.md    │            │
│  │  → API_DOCUMENTATION.md  → docs/files/*.md   │            │
│  └──────────────────────┬───────────────────────┘            │
│                         │                                    │
│  Phase 3 ─ AUDIT        ▼  (6 agents in parallel)           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │🔒 Security │ │📊 Quality  │ │📦 Deps     │               │
│  │ vulns      │ │ duplication│ │ CVEs       │               │
│  │ secrets    │ │ dead code  │ │ outdated   │               │
│  │ injection  │ │ complexity │ │ licenses   │               │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘               │
│  ┌─────┴──────┐ ┌─────┴──────┐ ┌─────┴──────┐               │
│  │⚠️ Errors   │ │🔤 Types    │ │📡 Monitor  │               │
│  │ silent     │ │ missing    │ │ logging    │               │
│  │ catches    │ │ unsafe cast│ │ health chk │               │
│  │ swallowed  │ │ schema     │ │ alerting   │               │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘               │
│        └───────────────┼───────────────┘                     │
│                        │                                     │
│  Phase 4 ─ TEST        ▼  (safety net before ANY changes)   │
│  ┌──────────────────────────────────────────────┐            │
│  │  🧪 Test Writer Agent (one per source file)  │            │
│  │  15+ unit tests per function:                │            │
│  │  • happy path • edge cases • error handling  │            │
│  │  • boundary values • types • side effects    │            │
│  │  → tests/ (mirrors src/ structure)           │            │
│  ├──────────────────────────────────────────────┤            │
│  │  🔗 Integration Tester Agent                 │            │
│  │  • cross-module flows • API contracts        │            │
│  │  • data transforms • error propagation       │            │
│  │  → tests/integration/                        │            │
│  ├──────────────────────────────────────────────┤            │
│  │  ▶️ Run all tests → record baseline          │            │
│  │  → .ai/plans/{date}_test-baseline.md         │            │
│  └──────────────────────┬───────────────────────┘            │
│                         │                                    │
│  Phase 5 ─ PLAN         ▼                                    │
│  ┌──────────────────────────────────────────────┐            │
│  │  📋 Prioritized Improvement Plan             │            │
│  │  🔴 Critical — fix now (vulns + test bugs)   │            │
│  │  🟠 High — this sprint                       │            │
│  │  🟡 Medium — next sprint                     │            │
│  │  🟢 Low — backlog                            │            │
│  └──────────────────────┬───────────────────────┘            │
│                         │                                    │
│  Phase 6 ─ PRESENT      ▼                                    │
│  ┌──────────────────────────────────────────────┐            │
│  │  "Tests are in place. Top 5 things to fix.   │            │
│  │   Start the criticals?"                      │            │
│  └──────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────┘

After fixes: Worker fixes → run tests → all pass? → next fix
             If regression → fix regression first → re-run → continue
```

### Reports & Tests Produced

| Agent | Output | What |
|---|---|---|
| 🔍 Discovery | `docs/discoveries/` | Codebase structure & map |
| 📝 Doc Updater | `docs/*.md` | Fills project documentation |
| 🔒 Security | `SECURITY_REPORT.md` | Vulnerabilities, secrets, auth |
| 📊 Code Quality | `QUALITY_REPORT.md` | Duplication, dead code, smells |
| 📦 Dependency | `DEPENDENCY_REPORT.md` | Outdated packages, CVEs |
| ⚠️ Error Handling | `ERROR_HANDLING_REPORT.md` | Silent catches, missing context |
| 🔤 Type Safety | `TYPE_SAFETY_REPORT.md` | Missing types, unsafe casts |
| 📡 Monitoring | `MONITORING_REPORT.md` | Logging, health check, alerting gaps |
| 🧪 Test Writer | `tests/**` | 15+ unit tests per function |
| 🔗 Integration Tester | `tests/integration/` | Cross-module flow tests |
| ▶️ Baseline | `test-baseline.md` | Pass/fail counts, existing bugs found |

---

## Pulling Template Updates

When the template improves (new playbook rules, better agent instructions, new scripts):

```
  git fetch template
         │
         ▼
  git checkout -b template-sync
         │
         ▼
  git merge template/main
         │
         ├── No conflicts? ──────── Skip to push
         │
         └── Conflicts? ─────────── Resolve per ownership table
                                         │
                                         ▼
                                    Run tests
                                         │
                                         ▼
  git checkout main
  git merge template-sync
  git branch -d template-sync
  git push origin main
         │
         ▼
       ✅ Project has latest template
```

---

## The Feedback Loop 🔄

This is the magic. Your project doesn't just *use* the template — it **improves it automatically**.

```
┌──────────────────────────────────────────────────────────────┐
│                     FEEDBACK LOOP                            │
│                                                              │
│   📦 Your Project                    🧬 Template Repo       │
│                                                              │
│   You work normally                                          │
│   Agents generate reports:                                   │
│   • docs/RETROSPECTIVE_REPORT.md                             │
│   • docs/PLAYBOOK.md                                         │
│   • docs/QUALITY_REPORT.md                                   │
│   • docs/SECURITY_REPORT.md                                  │
│   • .ai/lessons.md                                           │
│   • feedback/PUSH_NOTE.md  ← optional personal note          │
│          │                                                   │
│          ▼                                                   │
│   push to main triggers                                      │
│   send-feedback-via-issue.yml                                │
│          │                                                   │
│          │  Opens GitHub Issue                               │
│          │  with label "feedback"                            │
│          │                                                   │
│          └─────────────────────────►  Issue lands here       │
│                                       │                      │
│                                       ▼                      │
│                                 process-feedback-issue.yml   │
│                                       │                      │
│                                       ▼                      │
│                                 Claude reviews feedback      │
│                                       │                      │
│                                       ▼                      │
│                                 Opens PR with improvements   │
│                                       │                      │
│          ◄────────────────────────────┘                      │
│          │                                                   │
│   Next template-sync pull                                    │
│   brings improvements into                                   │
│   your project automatically                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### What Gets Sent Back

| File | Content | Sent automatically? |
|---|---|---|
| `docs/RETROSPECTIVE_REPORT.md` | What agents did well/poorly | ✅ Yes |
| `docs/PLAYBOOK.md` | Rules that evolved during development | ✅ Yes |
| `docs/QUALITY_REPORT.md` | Code quality findings | ✅ Yes |
| `docs/SECURITY_REPORT.md` | Security audit results | ✅ Yes |
| `.ai/lessons.md` | Lessons learned from corrections | ✅ Yes |
| `feedback/PUSH_NOTE.md` | Your personal note to the template | 📝 Opt-in |

> Each file is truncated to 500 lines. If none have content, the workflow skips entirely — no noise.

### Push Notes

Before any push, drop a personal note to improve the template:

```markdown
# feedback/PUSH_NOTE.md

The scaffold agent assumed src/ but my project uses lib/.
Suggestion: ask about the source directory before scaffolding.
```

The note ships with the next push and is **auto-cleared** after sending. Prefix with `DRAFT` to hold without sending.

### The Virtuous Cycle

```
  You use the template in Project A
         │
         ▼
  Agents find friction, generate reports
         │
         ▼
  Push triggers feedback → Template repo issue
         │
         ▼
  Claude reviews → Opens improvement PR
         │
         ▼
  You merge the PR in the template repo
         │
         ▼
  Next template-sync in Project A (and B, C...) pulls the fix
         │
         ▼
  The same friction never happens again
         │
         ▼
       🔄 Template gets smarter over time
```

---

## Multiple Projects

The pattern scales naturally. Each project feeds back independently, and all benefit from collective improvements:

```
                    ┌──────────────────┐
              ┌────►│   🧬 Template    │◄────┐
              │     │   Repo           │     │
              │     └───────┬──────────┘     │
              │             │                │
              │    ┌────────┼────────┐       │
              │    │ pull   │ pull   │ pull  │
              │    ▼        ▼        ▼       │
              │  ┌────┐  ┌────┐  ┌────┐      │
              │  │ 📦 │  │ 📦│  │ 📦 │      │
              │  │ A  │  │ B  │  │ C  │      │
              │  └──┬─┘  └──┬─┘  └──┬─┘      │
              │     │       │       │        │
              │     │push   │push   │push    │
              │     ▼       ▼       ▼        │
              │  ┌────┐  ┌────┐  ┌────┐      │
              │  │ GH │  │ GH │  │ GH │      │
              │  │ A  │  │ B  │  │ C  │      │
              │  └──┬─┘  └──┬─┘  └──┬─┘      │
              │     │       │       │        │
              │     └───────┼───────┘        │
              │      feedback (issues)       │
              └──────────────────────────────┘

  App A finds a playbook gap     → Template fixes it
  App B and C get the fix next sync  → Everyone benefits
```

---

## Enabling Feedback in Your Project

For the feedback loop to work, set up three things in your project's GitHub Settings:

| What | Where | Value |
|---|---|---|
| Enable flag | Settings → Variables → `TEMPLATE_FEEDBACK_ENABLED` | `true` |
| PAT token | Settings → Secrets → `TEMPLATE_FEEDBACK_PAT` | PAT with `public_repo` scope |
| Workflow | `.github/workflows/send-feedback-via-issue.yml` | Comes with the template merge |

That's it. Every push to main auto-collects agent reports and (if they have content) opens an issue on the template repo.

---

## Daily Workflow (What You Actually Do)

```
┌─────────────────────────────────────────────────────────────┐
│  MORNING                                                     │
│  Open your project — template infra is just there            │
│  Agents use playbooks, AGENTS.md, .ai/ — everything works   │
├─────────────────────────────────────────────────────────────┤
│  CODING                                                      │
│  Write code in src/, tests in tests/                         │
│  Agents generate retrospectives, quality, security reports   │
│  Optionally write feedback/PUSH_NOTE.md                      │
├─────────────────────────────────────────────────────────────┤
│  PUSH                                                        │
│  git push origin main                                        │
│    → Code goes to your project repo                          │
│    → Feedback workflow fires automatically                   │
│    → Template repo gets an issue with your agent reports     │
├─────────────────────────────────────────────────────────────┤
│  WEEKLY / MONTHLY                                            │
│  git fetch template && git merge template/main               │
│    → Pull in template improvements                           │
│    → Including improvements triggered by YOUR feedback       │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Reference

| Action | Command |
|---|---|
| **Automated setup** | `.\scripts\integrate.ps1` (Win) or `./scripts/integrate.sh` (Unix) |
| **First-time manual** | `git remote add template <url>` → `git fetch template` → `git merge template/main --allow-unrelated-histories` |
| **Pull updates** | `git fetch template` → `git merge template/main` |
| **Push your code** | `git push origin main` (feedback auto-sends) |
| **Leave a note** | Edit `feedback/PUSH_NOTE.md` before pushing |
| **Draft a note** | Start with `DRAFT` — won't send until removed |
| **Check remotes** | `git remote -v` (should show `origin` + `template`) |

---

## Automated Integration Script

Instead of doing all the steps manually, the template ships with integration scripts:

```bash
# From your existing project root:

# Windows PowerShell
.\scripts\integrate.ps1 -TemplateUrl "https://github.com/Doumajnik/template.git"

# Unix / macOS / Git Bash
./scripts/integrate.sh "https://github.com/Doumajnik/template.git"
```

The script handles everything:

```
┌──────────────────────────────────────────────────────────┐
│  integrate.ps1 / integrate.sh                            │
│                                                          │
│  [1/6] Add template remote                               │
│        └─ git remote add template <url>                  │
│                                                          │
│  [2/6] Fetch template                                    │
│        └─ git fetch template                             │
│                                                          │
│  [3/6] Merge on integration branch                       │
│        └─ git merge --allow-unrelated-histories          │
│                                                          │
│  [4/6] Auto-resolve conflicts                            │
│        ├─ Project files (src/, tests/) → keep yours      │
│        └─ Template files (.github/, docs/) → accept new  │
│                                                          │
│  [5/6] Commit and merge to main                          │
│        └─ Clean merge commit                             │
│                                                          │
│  [6/6] Add .gitattributes merge guards                   │
│        └─ Future syncs are safer                         │
│                                                          │
│  Then runs scripts/setup.ps1 automatically               │
└──────────────────────────────────────────────────────────┘
```

---

## Full Documentation

- **Detailed plan:** `docs/INTEGRATION_PLAN.md` — phases, ownership table, verification checklist
- **Ideas & alternatives:** `ideas/integrate-template-into-existing-project.md` — 3 strategies with tradeoffs

---

> 📌 **This file is temporary.** Delete when done, or move to `ideas/` for reference.
