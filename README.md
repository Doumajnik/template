# Project Name

> Replace this with your project description.

## Setup

1. Run `scripts/setup.ps1` (Windows) or `scripts/setup.sh` (Unix) to install git hooks and create directories.
2. Copy `.env.example` to `.env` and fill in any required values.
3. Install your language's dependencies as usual.

## Playbook System

The project includes a knowledge system that delivers relevant coding rules and patterns to AI agents.

### Playbook Rules

Playbook rules live in `docs/playbooks/` organized by scope:

- `shared/` — cross-cutting rules (anti-duplication, naming, error handling)
- `agents/` — agent-specific instructions
- `technologies/` — language/framework conventions

Each `.playbook.md` file has `+++` TOML frontmatter (id, title, agents, technologies, category, tags, version) followed by markdown body.

### Adding a New Rule

1. Create a new `.playbook.md` file in the appropriate subdirectory
2. Fill in the TOML frontmatter fields
3. Write the rule content in markdown below the closing `+++`

### How It Works

The Librarian Agent queries the index before assembling context briefs for other agents. Relevant playbook rules are retrieved via semantic similarity search and included in the brief. If the index or token is unavailable, the Librarian falls back to documentation-only search.

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
docs/              → Project documentation
```
