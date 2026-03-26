# Agentic Project Template

A repository template that gives AI coding agents **persistent memory**, **anti-duplication checks**, and **plan-driven workflows**. Use this as a starting point for any project where you work with AI assistants (GitHub Copilot, Cursor, Windsurf, Claude Code, etc.).

---

## What This Template Does

| Feature | How |
| --- | --- |
| **Prevents code duplication** | Agents search `docs/CODE_INVENTORY.md` before writing any new code |
| **Learns your preferences** | Agents append to `.ai/PREFERENCES.md` as they learn your style |
| **Plans before coding** | Non-trivial tasks get a `.plan.md` file before any code is written |
| **Delegates to sub-agents** | Plan steps marked `[delegatable]` can be spawned to isolated sub-agents |
| **Maintains a living playbook** | Architecture decisions accumulate in `docs/PLAYBOOK.md` across sessions |
| **Summarizes every session** | A concise summary is written to `.ai/sessions/` after each conversation |
| **Keeps README & .gitignore current** | Agents update these whenever project structure or tooling changes |
| **Security audits every cycle** | Security Agent scans for OWASP Top 10 vulnerabilities, tracks fixes in `docs/SECURITY_REPORT.md` |
| **Code quality checks every cycle** | Code Quality Agent detects duplication, dead code, and smells in `docs/QUALITY_REPORT.md` |
| **Continuous self-improvement** | Retrospective Agent reviews agent decisions after each cycle, updates `docs/PLAYBOOK.md` with lessons learned |

---

## Quick Start

1. **Use this template** — click "Use this template" on GitHub (or clone and remove `.git/`)
2. **Start coding with an AI agent** — the system instructions are loaded automatically
3. The agent will read the playbook, inventory, and preferences before doing anything
4. For new features, use `/plan-feature` to generate a plan before implementation
5. After implementation, use `/review-session` to get a quality check and session summary

---

## Project Structure

```text
.github/
├── copilot-instructions.md           # Master system prompt (auto-loaded by Copilot)
├── agents/
│   ├── accessibility.agent.md        # WCAG compliance and UI accessibility
│   ├── api-design.agent.md           # API contracts, OpenAPI specs, endpoint design
│   ├── architect.agent.md            # System design
│   ├── cleanup.agent.md              # Dead code and stale file removal
│   ├── code-quality.agent.md         # Code quality, duplication, smells audit
│   ├── compliance.agent.md           # License, privacy, regulatory compliance
│   ├── critic.agent.md               # Architecture review
│   ├── database.agent.md             # Schema design, migrations, queries
│   ├── debug.agent.md                # Bug diagnosis and fixing
│   ├── dependency.agent.md           # Dependency audit and license check
│   ├── discovery.agent.md            # Analyzes new data/codebases
│   ├── doc-updater.agent.md          # Updates all documentation
│   ├── error-handling.agent.md       # Error recovery patterns, silent catch audit
│   ├── git-release.agent.md          # Changelogs, semantic versioning, releases
│   ├── innovator.agent.md            # Creative alternatives & outside-the-box ideas
│   ├── integration-tester.agent.md   # E2E and integration tests
│   ├── migration.agent.md            # Framework upgrades, API version bumps
│   ├── monitoring.agent.md           # Audits observability, reports gaps
│   ├── performance.agent.md          # Profiling and optimization
│   ├── planner.agent.md              # Creates plans and todos
│   ├── refactor.agent.md             # Code restructuring without behavior change
│   ├── research.agent.md             # Investigates questions
│   ├── retrospective.agent.md        # Reviews decisions, improves Playbook
│   ├── reviewer.agent.md             # Reviews changes
│   ├── scaffolder.agent.md           # Creates file stubs
│   ├── security.agent.md             # Security vulnerability audit
│   ├── test-writer.agent.md          # Writes thorough tests
│   ├── type-safety.agent.md          # Type coverage, schema validation, strict typing
│   └── worker.agent.md               # Implements functions
├── prompts/
│   ├── plan-feature.prompt.md        # /plan-feature slash command
│   ├── implement-plan.prompt.md      # /implement-plan slash command
│   ├── review-session.prompt.md      # /review-session slash command
│   ├── update-inventory.prompt.md    # /update-inventory slash command
│   └── deep-implement.prompt.md      # /deep-implement slash command (DEEP_MODE)
└── instructions/                     # Path-specific instructions (add as needed)

.ai/
├── PREFERENCES.md                    # Agent-learned user preferences
├── DEEP_MODE.md                      # DEEP_MODE pipeline reference
├── TRACE_TEMPLATE.md                 # Execution trace template
├── sessions/                         # Per-conversation summaries
├── plans/                            # Implementation plan files
└── todos/                            # Persisted task tracking

docs/
├── discoveries/                      # Structured summaries of analyzed data
├── files/                            # Per-file documentation
├── API_DOCUMENTATION.md              # Exposed & consumed API registry
├── BUSINESS_LOGIC.md                 # System logic, data flows, modules
├── CODE_INVENTORY.md                 # Living registry of all code symbols
├── PLAYBOOK.md                       # Architecture decisions & patterns
├── QUALITY_REPORT.md                 # Persistent code quality audit trail
├── RETROSPECTIVE_REPORT.md           # Agent decision audit & improvement log
├── REVIEW_REPORT.md                  # Persistent code review trail
└── SECURITY_REPORT.md                # Persistent security audit trail

src/                                  # Application source code
├── utils/                            # Shared helper functions and utilities
├── services/                         # Business logic and service layer
├── models/                           # Data models, schemas, types
└── config/                           # Configuration and environment setup

tests/                                # Unit and integration tests (mirrors src/)

scripts/
├── hooks/
│   ├── pre-commit                    # Linters, formatters, style checks
│   ├── commit-msg                    # Conventional commit validation
│   └── pre-push                      # Test runner before push
├── setup.ps1                         # Windows setup (dirs, hooks, deps)
└── setup.sh                          # Unix setup (dirs, hooks, deps)

AGENTS.md                             # Cross-tool agent instructions
README.md                             # Project README (agents keep updated)
TEMPLATE_README.md                    # This file — template documentation
.gitignore                            # Broad defaults, agent-maintained
.env.example                          # Placeholder for environment variables
```

---

## How the Agent Workflow Works

The **Orchestrator** (the main AI agent) is a pure dispatcher — it never writes code directly. It reads documentation, decides which sub-agents to spawn, and reports results.

### Full Pipeline (all tasks)

```mermaid
flowchart TD
    U([User Request]) --> O{Orchestrator}
    O -->|new data?| D[Discovery Agent]
    D -->|summary → docs/discoveries/| RE
    O -->|no new data| RE[Research Agent]
    RE -->|research brief + deps| DEP[Install Dependencies]
    DEP --> A[Architect Agent]
    A --> IN[Innovator Agent]
    IN -->|creative alternatives| A
    A <-->|adversarial loop ≤10 rounds| C[Critic Agent]
    C --> P[Planning Agent]
    P -->|plan + todos → .ai/| UA{User Approval}
    UA -->|rejected| RE
    UA -->|approved → suggest new session| S[Scaffolder Agent]
    S -->|file stubs| TW[Test Writer Agent]
    TW -->|failing tests| W[Worker Agent]
    W -->|red → green loop| IT[Integration Tester Agent]
    IT -->|E2E tests pass| R[Reviewer Agent]
    R -->|pass| SEC[Security Agent]
    R -->|fail| W
    SEC -->|audit + report| CQ[Code Quality Agent]
    CQ -->|quality report| DU[Doc Updater Agent]
    DU -->|docs + commit| RT[Retrospective Agent]
    RT -->|review decisions + update Playbook| Done([Done])

    style O fill:#4a90d9,color:#fff
    style U fill:#6c757d,color:#fff
    style Done fill:#6c757d,color:#fff
    style UA fill:#e8a838,color:#fff
```

### Discovery (when new data appears)

```mermaid
sequenceDiagram
    participant U as User
    participant O as Orchestrator
    participant D as Discovery Agent
    participant Docs as docs/discoveries/

    U->>O: Presents new data
    O->>U: "New data detected. Run Discovery?"
    U->>O: Confirms
    O->>D: Spawn with raw data reference
    D->>D: Read & analyze systematically
    D->>Docs: Write structured summary
    D->>O: Report complete
    Note over O,Docs: All other agents read<br/>only the summary — never raw data
```

### Trivial Tasks (shortcut)

Not every request needs the full pipeline. The orchestrator skips to the relevant agent(s).

```mermaid
flowchart LR
    U([User Request]) --> O{Orchestrator}
    O -->|question| RS[Research Agent]
    O -->|small fix| W[Worker Agent]
    O -->|bug| DB[Debug Agent]
    O -->|refactor| RF[Refactor Agent]
    O -->|docs only| DU[Doc Updater Agent]
    O -->|review code| RV[Reviewer Agent]
    O -->|performance| PF[Performance Agent]
    O -->|cleanup| CL[Cleanup Agent]
    O -->|deps audit| DP[Dependency Agent]
    O -->|security audit| SEC[Security Agent]
    O -->|database| DBA[Database Agent]
    O -->|monitoring| MN[Monitoring Agent]
    O -->|accessibility| AC[Accessibility Agent]
    O -->|compliance| CM[Compliance Agent]
    O -->|migration| MG[Migration Agent]
    O -->|API design| AD[API Design Agent]
    O -->|error patterns| EH[Error Handling Agent]
    O -->|type audit| TS[Type Safety Agent]
    O -->|release| GR[Git / Release Agent]

    style O fill:#4a90d9,color:#fff
    style U fill:#6c757d,color:#fff
```

### Architect–Innovator–Critic Loop

Every task goes through adversarial refinement before implementation. The Orchestrator mediates all communication — agents never hand off to each other directly.

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant A as Architect
    participant IN as Innovator
    participant C as Critic

    O->>A: Design architecture
    A-->>O: Architecture plan v1
    O->>IN: Review plan, propose alternatives
    IN-->>O: Innovator report (3+ ideas)
    O->>A: Incorporate Innovator's best ideas
    A-->>O: Architecture plan v2
    loop Up to 10 rounds
        O->>C: Critique the plan
        C-->>O: Verdict + issues
        O->>A: Fix issues from Critic
        A-->>O: Revised plan
    end
    Note over O: Proceed to Planning →<br/>Scaffolder → Test Writer →<br/>Worker → Integration Tester
```

---

## Slash Commands (Prompt Files)

| Command              | What it does                                                                         |
|----------------------|--------------------------------------------------------------------------------------|
| `/plan-feature`      | Full planning pipeline: Research → Architect → Innovator → Critic → Plan → User Approval  |
| `/implement-plan`    | Execute a plan: Scaffolder → Test Writer → Worker → Integration Tester → Reviewer → Quality gates |
| `/review-session`    | Review changes, run Security + Code Quality audits, write session summary               |
| `/update-inventory`  | Re-scan `src/` and regenerate the code inventory + per-file docs                        |
| `/deep-implement`    | Full pipeline: plan + implement + audit + retrospective                         |

---

## Key Files for Agents

| File | Purpose | Updated by |
| --- | --- | --- |
| `docs/CODE_INVENTORY.md` | Registry of every function, class, const | Agent, after every code change |
| `docs/PLAYBOOK.md` | Architecture decisions & patterns | Agent, after design decisions |
| `docs/discoveries/*.md` | Summaries of analyzed data/codebases | Discovery Agent |
| `docs/files/*.md` | Per-file documentation (purpose, API, deps) | Doc Updater Agent |
| `docs/API_DOCUMENTATION.md` | Exposed & consumed API registry | Doc Updater Agent |
| `.ai/PREFERENCES.md` | User's coding style preferences | Agent, when learning new preferences |
| `.ai/sessions/*.md` | Conversation summaries | Doc Updater Agent, at end of session |
| `.ai/plans/*.plan.md` | Implementation plans | Planning Agent, before implementation |
| `.ai/todos/*.todo.md` | Persisted task tracking | Planning Agent / Orchestrator |
| `docs/SECURITY_REPORT.md` | Persistent security audit trail | Security Agent, end of each cycle |
| `docs/QUALITY_REPORT.md` | Persistent code quality audit trail | Code Quality Agent, end of each cycle |
| `docs/REVIEW_REPORT.md` | Persistent code review trail | Reviewer Agent, end of each cycle |
| `docs/RETROSPECTIVE_REPORT.md` | Agent decision audit & improvement log | Retrospective Agent, end of each cycle |

---

## Customizing This Template

- **Language/framework specific rules**: Add files to `.github/instructions/` with `applyTo` globs
- **Custom agents**: Add `.agent.md` files to `.github/agents/` for specialized workflows
- **Prompt templates**: Add `.prompt.md` files to `.github/prompts/` for reusable slash commands
- **Playbook seeding**: Pre-fill `docs/PLAYBOOK.md` with your team's architecture decisions
