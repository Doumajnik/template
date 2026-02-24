# Project Name

> Replace this with your project description. Agents will update this file as the project grows.
>
> **This repo was created from the [Agentic Project Template](TEMPLATE_README.md).**
> See that file for template docs (agents, prompts, DEEP_MODE, hooks).

## Setup

1. Run `scripts/setup.ps1` (Windows) or `scripts/setup.sh` (Unix) to install git hooks and create directories.
2. Copy `.env.example` to `.env` and fill in any required values.
3. Install your language's dependencies as usual.

## Usage

*TODO: Add usage instructions as the project develops.*

## Project Structure

```text
src/
├── utils/         → Shared helpers
├── services/      → Business logic
├── models/        → Data models / schemas
└── config/        → Configuration
tests/             → Unit & integration tests
scripts/           → Automation scripts & git hooks
docs/
├── discoveries/   → Structured summaries of analyzed data/codebases
├── files/         → Per-file documentation (one MD per source file)
├── API_DOCUMENTATION.md
├── BUSINESS_LOGIC.md
├── CODE_INVENTORY.md
└── PLAYBOOK.md
.ai/               → Agent memory (preferences, sessions, plans, traces, todos)
.github/           → Copilot instructions, custom agents, prompt files
```

*Agents will keep this structure tree updated.*

## Agent Workflow

This project uses an **Orchestrator** pattern — the main AI agent dispatches specialized sub-agents for each task. See [TEMPLATE_README.md](TEMPLATE_README.md) for full details.

```mermaid
flowchart TD
    U([User Request]) --> O{Orchestrator}
    O -->|new data?| D[Discovery Agent]
    D -->|summary| P
    O -->|no new data| P[Planning Agent]
    P -->|plan + todos| UA{User Approval}
    UA -->|rejected| P
    UA -->|approved| A[Architect Agent]
    A --> IN[Innovator Agent]
    IN -->|creative alternatives| A
    A <-->|adversarial loop| C[Critic Agent]
    C --> S[Scaffolder Agent]
    S -->|file stubs| TW[Test Writer Agent]
    TW -->|failing tests| W[Worker Agent]
    W -->|red-green loop| R[Reviewer Agent]
    R -->|pass| DU[Doc Updater Agent]
    R -->|fail| W
    DU -->|docs + commit| Done([Done])

    style O fill:#4a90d9,color:#fff
    style U fill:#6c757d,color:#fff
    style Done fill:#6c757d,color:#fff
    style UA fill:#e8a838,color:#fff
```

For trivial tasks, the orchestrator skips directly to the needed agent:

```mermaid
flowchart LR
    U([User Request]) --> O{Orchestrator}
    O -->|question| RS[Research Agent]
    O -->|small fix| W[Worker Agent]
    O -->|docs only| DU[Doc Updater Agent]
    O -->|review code| RV[Reviewer Agent]

    style O fill:#4a90d9,color:#fff
    style U fill:#6c757d,color:#fff
```
