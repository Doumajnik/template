# Centralized Agent Orchestration (Multi-Project from One Place)

## The Problem

Currently this template must be copied into EVERY project. That means:
- 53 agent files duplicated per repo
- Updates require syncing across all projects
- Each project carries ~500KB of markdown infrastructure
- Drift between projects is inevitable

## Solution: Global Agent Hub + Project Symlinks

### Architecture

```
~/.claude/                          # Global Claude Code config
├── CLAUDE.md                       # Global instructions (loads AGENTS.md from hub)
├── settings.json                   # Global hooks, model config
└── commands/                       # Global slash commands

~/agent-hub/                        # ONE COPY of the template (this repo)
├── AGENTS.md                       # The single source of truth
├── .github/agents/                 # 53 agent definitions
├── .github/instructions/           # Language-scoped rules
├── .github/skills/                 # Domain skills
├── .ai/LLM_COUNCIL.md             # Council protocol
├── .ai/checklists/                 # Pipeline checklists
├── scripts/tool-guard.py          # Tool enforcement
└── docs/playbooks/                 # Agent playbooks

~/projects/
├── my-app/                         # Actual project
│   ├── .claude/settings.json       # Points hooks to ~/agent-hub/scripts/
│   ├── CLAUDE.md                   # "Read ~/agent-hub/AGENTS.md"
│   ├── .ai/                        # Project-specific memory (plans, todos, sessions)
│   └── docs/                       # Project-specific docs
├── another-app/
│   ├── CLAUDE.md                   # Same pointer
│   ├── .ai/                        # Its own memory
│   └── docs/                       # Its own docs
└── ...
```

### How It Works

1. **Global `~/.claude/CLAUDE.md`** contains the full orchestrator instructions (or a `read` directive pointing to `~/agent-hub/AGENTS.md`). Claude Code loads this for EVERY project automatically.

2. **Per-project `CLAUDE.md`** is minimal — just project-specific context:
   ```markdown
   # Project: My App
   
   Tech stack: Python 3.12, FastAPI, PostgreSQL
   Entry point: src/main.py
   Test command: pytest tests/
   
   ## Project-specific rules
   - Use SQLAlchemy 2.0 async patterns
   - All endpoints must return JSON
   ```

3. **Shared `.ai/` stays in the hub** for agent definitions, checklists, playbooks. Per-project `.ai/` holds only session data (plans, todos, dispatch logs).

4. **`scripts/tool-guard.py`** runs from the hub path — configured once in global settings.

### Implementation Options

#### Option A: Git Submodule (recommended for teams)

```bash
# In each project:
git submodule add https://github.com/Doumajnik/template.git .agent-hub
```

Then `CLAUDE.md` references `.agent-hub/AGENTS.md`. Updates pull in with `git submodule update`.

#### Option B: Symlinks (recommended for solo developers)

```powershell
# Clone the hub once:
git clone https://github.com/Doumajnik/template.git ~/agent-hub

# In each project, create symlinks:
New-Item -ItemType SymbolicLink -Path ".github" -Target "~/agent-hub/.github"
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target "~/agent-hub/AGENTS.md"
```

#### Option C: Global Claude Config (simplest, Claude Code only)

```markdown
# ~/.claude/CLAUDE.md

Read and follow ALL instructions from ~/agent-hub/AGENTS.md.
This applies to every project you work on.

The current project's specific context is in its own CLAUDE.md (if it exists).
Project-specific overrides take precedence over global rules.
```

This requires NO files in the project itself — Claude Code loads `~/.claude/CLAUDE.md` globally.

#### Option D: NPM/pip package (for distribution)

Package the template as an installable CLI tool:
```bash
pip install agent-orchestrator
# or
npm install -g @doumajnik/agent-template

# Then in any project:
agent-init  # Creates minimal CLAUDE.md + .ai/ structure
```

### What Lives Where

| Content | Location | Why |
| --- | --- | --- |
| Agent definitions (53 `.agent.md`) | Hub (global) | Same across all projects |
| Playbooks | Hub (global) | Shared patterns |
| Pipeline checklists | Hub (global) | Same workflow everywhere |
| Language instructions | Hub (global) | Same conventions |
| Skills | Hub (global) | Loaded on-demand |
| `AGENTS.md` | Hub (global) | Single source of truth |
| `tool-guard.py` | Hub (global) | Same enforcement |
| `CLAUDE.md` (project-specific) | Per project | Stack, conventions, overrides |
| `.ai/plans/` | Per project | Project-specific plans |
| `.ai/todos/` | Per project | Project-specific tasks |
| `.ai/sessions/` | Per project | Project-specific dispatch logs |
| `docs/CODE_INVENTORY.md` | Per project | Project-specific symbols |
| `docs/BUSINESS_LOGIC.md` | Per project | Project-specific logic |
| `docs/files/` | Per project | Project-specific file docs |
| `docs/*_REPORT.md` | Per project | Project-specific findings |

### Migration Script

A `scripts/centralize.ps1` / `scripts/centralize.sh` script could:
1. Move hub files to `~/agent-hub/` (or a configured path)
2. Replace per-project files with symlinks or pointers
3. Keep per-project `.ai/` and `docs/` intact
4. Update `.claude/settings.json` to point hooks at the hub

---

## For the Super Greedy Pipeline Specifically

The centralized approach is especially valuable for GREEDY_MODE because:

1. **Model tier assignments** stay consistent across projects (defined once in the hub)
2. **LLM Council protocol** doesn't drift between projects
3. **Quality Scorecard template** is standardized
4. **Mutation testing config** (mutmut/stryker) is shared
5. **Cross-project learnings** (`.ai/lessons.md` in the hub) benefit all projects

### Multi-Project Greedy Orchestration

With a centralized hub, you could even run **cross-project** greedy operations:
- Cross-project coherence review (shared libraries use consistent patterns)
- Unified security posture across all projects
- Shared mock data generators for microservices that talk to each other
- Cross-project integration testing (contract tests between services)

---

## GitHub Repos to Watch (patterns worth adopting)

### For the Council / Multi-Model Approach
- **Aider** (`paul-gauthier/aider`) — repo-map for cross-file awareness, multiple model support
- **Plandex** (`plandex-ai/plandex`) — persistent planning across sessions, multi-file changes
- **OpenHands** (`All-Hands-AI/OpenHands`) — agent sandbox with tool isolation

### For Centralized Config
- **PR-Agent** (`Codium-ai/pr-agent`) — org-level GitHub App, single config for all repos
- **Trunk** (`trunk-io/trunk`) — centralized lint/format config across repos

### For Quality Maximization
- **mutmut** (Python mutation testing) — integrate into the greedy pipeline
- **Stryker** (JS/TS mutation testing) — same for frontend
- **Hypothesis** (property-based testing) — generates adversarial inputs automatically
- **Semgrep** — custom rule-based static analysis, can encode all playbook rules as checks

### Novel Ideas for Super Greedy (not seen elsewhere)
1. **Temporal coherence testing** — re-run the full test suite with the system clock shifted (time zones, DST, leap years, Y2038)
2. **Dependency shadow testing** — run tests with next-major versions of all deps to catch future breakage
3. **LLM self-critique chains** — after Security audits, ask "what did you miss?" with a different temperature
4. **Formal verification snippets** — for critical invariants, generate Z3/TLA+ specs alongside code
5. **Regression oracle** — save all function I/O pairs from tests as golden files, detect behavioral drift on any change
