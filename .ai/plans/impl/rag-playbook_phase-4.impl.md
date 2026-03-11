# Impl: Librarian Update & Documentation (Phase 4)

**Parent plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`
**Phase:** 4
**Status:** 🟡 Draft

---

## Overview

Update the Librarian agent to integrate RAG retrieval as Stage 1 of its query workflow. Update all project documentation to reflect the new infrastructure: CODE_INVENTORY with all new symbols, BUSINESS_LOGIC with the RAG data flow, PLAYBOOK with new architectural decisions, README with updated structure, and per-file docs for each new module.

---

## Tasks

### `.github/agents/librarian.agent.md`

**Purpose:** Update the Librarian agent's query workflow to add RAG-based playbook retrieval as a new Stage 1, before the existing documentation search.

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | Add RAG retrieval stage | Insert a new Stage 1 in the query workflow: determine agent/tech from query → shell out to `python3 scripts/query-knowledge-index.py` → capture stdout as RAG chunks | `[delegatable]` |
| 2 | Add context brief format | Add a "### Relevant Playbook Rules (RAG)" section template to the context brief format | `[delegatable]` |
| 3 | Document graceful degradation | Note that if the query script fails or index is missing, the Librarian continues with existing stages only. RAG is additive, never blocking | `[delegatable]` |

**Progress:**

- [ ] #1 Add RAG retrieval stage `[delegatable]`
- [ ] #2 Add context brief format `[delegatable]`
- [ ] #3 Document graceful degradation `[delegatable]`

---

### `docs/CODE_INVENTORY.md`

**Purpose:** Register all new symbols from all 5 modules.

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | Add `playbook_parser.py` symbols | 3 public + 5 private functions | `[delegatable]` |
| 2 | Add `embedding_client.py` symbols | 2 public + 5 private functions | `[delegatable]` |
| 3 | Add `knowledge_index.py` symbols | 5 public + 6 private functions | `[delegatable]` |
| 4 | Add `build-knowledge-index.py` symbols | 5 functions | `[delegatable]` |
| 5 | Add `query-knowledge-index.py` symbols | 6 functions | `[delegatable]` |

**Progress:**

- [ ] #1 `playbook_parser.py` symbols `[delegatable]`
- [ ] #2 `embedding_client.py` symbols `[delegatable]`
- [ ] #3 `knowledge_index.py` symbols `[delegatable]`
- [ ] #4 `build-knowledge-index.py` symbols `[delegatable]`
- [ ] #5 `query-knowledge-index.py` symbols `[delegatable]`

---

### `docs/BUSINESS_LOGIC.md`

**Purpose:** Document the RAG data flow (build-time and query-time), module responsibilities, and the Librarian's updated query workflow.

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | Add RAG infrastructure section | Document the build-time and query-time data flows, module responsibilities, and graceful degradation strategy | `[delegatable]` |

**Progress:**

- [ ] #1 RAG infrastructure section `[delegatable]`

---

### `docs/PLAYBOOK.md`

**Purpose:** Record new architectural decisions from this feature (TOML frontmatter, stdlib-only, incremental builds, committed index).

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | Add RAG architecture decisions | Document: TOML over YAML, `tomllib` stdlib, committed JSON index, incremental builds, graceful degradation, similarity merge | `[delegatable]` |

**Progress:**

- [ ] #1 RAG architecture decisions `[delegatable]`

---

### `README.md`

**Purpose:** Update project structure and features to reflect the new playbook infrastructure.

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | Update structure section | Add `docs/playbooks/`, `src/utils/`, `scripts/build-knowledge-index.py`, `scripts/query-knowledge-index.py` | `[delegatable]` |
| 2 | Add RAG feature description | Brief description of the playbook knowledge retrieval system | `[delegatable]` |

**Progress:**

- [ ] #1 Update structure section `[delegatable]`
- [ ] #2 Add RAG feature description `[delegatable]`

---

### `docs/files/*.md` (per-file documentation)

**Purpose:** Create per-file documentation for each new source module.

| # | Task | Description | Mode |
| --- | --- | --- | --- |
| 1 | `docs/files/playbook_parser.md` | Purpose, API, dependencies, design notes | `[delegatable]` |
| 2 | `docs/files/embedding_client.md` | Purpose, API, dependencies, design notes | `[delegatable]` |
| 3 | `docs/files/knowledge_index.md` | Purpose, API, dependencies, design notes | `[delegatable]` |

**Progress:**

- [ ] #1 `playbook_parser.md` `[delegatable]`
- [ ] #2 `embedding_client.md` `[delegatable]`
- [ ] #3 `knowledge_index.md` `[delegatable]`

---

## Constants & Types

*(None — this phase is documentation only.)*

---

## Dependencies

| Depends on | From | Status |
| --- | --- | --- |
| Phase 1 complete | All parser + client functions implemented and tested | Must be done |
| Phase 2 complete | All knowledge index functions implemented and tested | Must be done |
| Phase 3 complete | CLI scripts and workflow implemented | Must be done |

---

## Notes

- **This phase produces no Python code.** Only documentation and agent instruction files are modified.
- **Doc Updater agent** handles all tasks in this phase.
- **Librarian update is critical** — this is what actually enables the RAG retrieval at query time. Without it, the query script exists but is never called.
- **CODE_INVENTORY update is mandatory** per PLAYBOOK rules — every new symbol must be registered immediately after creation.
- **Retrospective Agent** runs after this phase to review all decisions and update the PLAYBOOK.
