# Impl: Playbook Format, Template & Stubs (Phase 0)

**Parent plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`
**Phase:** 0
**Status:** 🟡 Draft

---

## Overview

Create the playbook chunk format, directory structure, template file, and all initial playbook stubs. This phase produces no Python code — only markdown content files and a `.gitattributes` entry. All subsequent phases depend on these files existing for testing and integration.

---

## Files

### `docs/playbooks/_TEMPLATE.playbook.md`

**Purpose:** Template for creating new playbook chunks. Contains TOML frontmatter with all required fields and a placeholder body.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | Template file | N/A — markdown content | TOML frontmatter template with `id`, `title`, `agents`, `technologies`, `category`, `tags`, `version` fields plus placeholder body | `[delegatable]` |

**Progress:**

- [ ] #1 Template file `[delegatable]`

---

### `.gitattributes`

**Purpose:** Mark the knowledge index as linguist-generated to suppress diffs in merge requests.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `.gitattributes` entry | N/A — config content | Add `.ai/knowledge-index.json linguist-generated=true diff=json` | `[delegatable]` |

**Progress:**

- [ ] #1 `.gitattributes` entry `[delegatable]`

---

### `docs/playbooks/shared/*.playbook.md` (8 files)

**Purpose:** Shared playbook stubs containing rules that apply to all agents, extracted from existing `docs/PLAYBOOK.md` patterns.

| # | File | Description | Mode |
| --- | --- | --- | --- |
| 1 | `anti-duplication.playbook.md` | Anti-duplication rules (search before creating) | `[delegatable]` |
| 2 | `decomposition.playbook.md` | Function decomposition / size limits | `[delegatable]` |
| 3 | `extraction-rules.playbook.md` | Extraction and refactoring rules | `[delegatable]` |
| 4 | `error-handling.playbook.md` | Error handling patterns | `[delegatable]` |
| 5 | `markdown-formatting.playbook.md` | Markdown formatting conventions | `[delegatable]` |
| 6 | `naming-conventions.playbook.md` | Naming convention rules | `[delegatable]` |
| 7 | `code-style.playbook.md` | Code style preferences | `[delegatable]` |
| 8 | `testing-rules.playbook.md` | Testing requirements (15+ per function) | `[delegatable]` |

**Progress:**

- [ ] #1 `anti-duplication.playbook.md` `[delegatable]`
- [ ] #2 `decomposition.playbook.md` `[delegatable]`
- [ ] #3 `extraction-rules.playbook.md` `[delegatable]`
- [ ] #4 `error-handling.playbook.md` `[delegatable]`
- [ ] #5 `markdown-formatting.playbook.md` `[delegatable]`
- [ ] #6 `naming-conventions.playbook.md` `[delegatable]`
- [ ] #7 `code-style.playbook.md` `[delegatable]`
- [ ] #8 `testing-rules.playbook.md` `[delegatable]`

---

### `docs/playbooks/agents/*.playbook.md` (32 files)

**Purpose:** Agent-specific playbook stubs — one per agent in the roster. Each contains TOML frontmatter with `agents = ["{agent-name}"]` and a placeholder body for agent-specific rules.

| # | File | Agent | Mode |
| --- | --- | --- | --- |
| 1 | `worker.playbook.md` | worker | `[delegatable]` |
| 2 | `architect.playbook.md` | architect | `[delegatable]` |
| 3 | `critic.playbook.md` | critic | `[delegatable]` |
| 4 | `scaffolder.playbook.md` | scaffolder | `[delegatable]` |
| 5 | `test-writer.playbook.md` | test-writer | `[delegatable]` |
| 6 | `reviewer.playbook.md` | reviewer | `[delegatable]` |
| 7 | `debug.playbook.md` | debug | `[delegatable]` |
| 8 | `refactor.playbook.md` | refactor | `[delegatable]` |
| 9 | `security.playbook.md` | security | `[delegatable]` |
| 10 | `code-quality.playbook.md` | code-quality | `[delegatable]` |
| 11 | `performance.playbook.md` | performance | `[delegatable]` |
| 12 | `database.playbook.md` | database | `[delegatable]` |
| 13 | `monitoring.playbook.md` | monitoring | `[delegatable]` |
| 14 | `dependency.playbook.md` | dependency | `[delegatable]` |
| 15 | `cleanup.playbook.md` | cleanup | `[delegatable]` |
| 16 | `accessibility.playbook.md` | accessibility | `[delegatable]` |
| 17 | `compliance.playbook.md` | compliance | `[delegatable]` |
| 18 | `migration.playbook.md` | migration | `[delegatable]` |
| 19 | `api-design.playbook.md` | api-design | `[delegatable]` |
| 20 | `error-handling-agent.playbook.md` | error-handling | `[delegatable]` |
| 21 | `type-safety.playbook.md` | type-safety | `[delegatable]` |
| 22 | `git-release.playbook.md` | git-release | `[delegatable]` |
| 23 | `librarian.playbook.md` | librarian | `[delegatable]` |
| 24 | `prompt-engineer.playbook.md` | prompt-engineer | `[delegatable]` |
| 25 | `ui-preview.playbook.md` | ui-preview | `[delegatable]` |
| 26 | `discovery.playbook.md` | discovery | `[delegatable]` |
| 27 | `planner.playbook.md` | planner | `[delegatable]` |
| 28 | `innovator.playbook.md` | innovator | `[delegatable]` |
| 29 | `research.playbook.md` | research | `[delegatable]` |
| 30 | `integration-tester.playbook.md` | integration-tester | `[delegatable]` |
| 31 | `doc-updater.playbook.md` | doc-updater | `[delegatable]` |
| 32 | `retrospective.playbook.md` | retrospective | `[delegatable]` |

**Progress:**

- [ ] #1–32 Agent playbook stubs (batch `[delegatable]` — all follow identical template pattern)

---

### `docs/playbooks/technologies/*.playbook.md` (4 files)

**Purpose:** Technology-specific playbook stubs for language/framework rules.

| # | File | Technology | Mode |
| --- | --- | --- | --- |
| 1 | `python.playbook.md` | python | `[delegatable]` |
| 2 | `typescript.playbook.md` | typescript | `[delegatable]` |
| 3 | `dotnet.playbook.md` | dotnet | `[delegatable]` |
| 4 | `go.playbook.md` | go | `[delegatable]` |

**Progress:**

- [ ] #1 `python.playbook.md` `[delegatable]`
- [ ] #2 `typescript.playbook.md` `[delegatable]`
- [ ] #3 `dotnet.playbook.md` `[delegatable]`
- [ ] #4 `go.playbook.md` `[delegatable]`

---

## Constants & Types

*(None — this phase is markdown content only.)*

---

## Dependencies

| Depends on | From | Status |
| --- | --- | --- |
| *(none)* | *(Phase 0 has no dependencies)* | N/A |

---

## Notes

- All playbook stubs should follow the exact TOML frontmatter schema defined in the architecture plan: `id`, `title`, `agents`, `technologies`, `category`, `tags`, `version`.
- The `id` field must match the pattern `{category}/{slug}` where slug = filename without `.playbook.md`.
- Agent stubs' `agents` field should be `["{agent-name}"]`. Shared stubs use `["all"]`. Technology stubs use `[]` for agents and `["{tech-name}"]` for technologies.
- Each stub body should contain at least one `###` heading followed by a placeholder paragraph (to pass `_validate_content` checks).
- The 32 agent stubs + 8 shared + 4 technology stubs = 44 playbook files total plus the template.
- The `.gitattributes` entry ensures `linguist-generated=true diff=json` for `.ai/knowledge-index.json`.
