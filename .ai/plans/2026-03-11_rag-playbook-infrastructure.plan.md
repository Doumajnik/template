# Plan: RAG-Powered Playbook Infrastructure

**Date:** 2026-03-11
**Status:** 🟡 Draft
**Architecture:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.architecture.md`

## Objective

Build a retrieval-augmented generation (RAG) infrastructure that enables the Librarian agent to serve semantically relevant playbook knowledge to all agents at query time. Playbook rules are decomposed into individually addressable markdown chunks with TOML frontmatter, embedded via the GitHub Models API, and stored in a committed JSON index. A CI workflow rebuilds the index on playbook changes; the Librarian queries it at runtime for top-K results by cosine similarity.

## Existing Code to Reuse

| Symbol | File | Reuse how |
| --- | --- | --- |
| *(none)* | *(greenfield — CODE_INVENTORY is empty)* | N/A |
| `GH_MODELS_TOKEN` | GitHub Secrets | Reuse existing secret from feedback pipeline |

**Deduplication report:** No duplication risk. All modules are net-new. No existing Python source in `src/`. No existing utilities overlap.

---

## Phases

- [ ] **Phase 0: Playbook Format, Template & Stubs** `[delegatable]`
  - Scope: Create the playbook chunk template, directory structure (`docs/playbooks/shared/`, `agents/`, `technologies/`), and all initial playbook stub files (32 agent stubs + shared + technology stubs). Add `.gitattributes` entry for the knowledge index.
  - Files: `docs/playbooks/_TEMPLATE.playbook.md`, `docs/playbooks/shared/*.playbook.md`, `docs/playbooks/agents/*.playbook.md`, `docs/playbooks/technologies/*.playbook.md`, `.gitattributes`
  - Impl plan: `.ai/plans/impl/rag-playbook_phase-0.impl.md`

- [ ] **Phase 1: Parser & Embedding Client** `[delegatable]`
  - Scope: Implement the two Layer-1 utility modules — `playbook_parser.py` (TOML frontmatter parsing, file discovery, validation) and `embedding_client.py` (GitHub Models API, batching, retry). These have no inter-dependencies and can be built in parallel. Includes test files for both.
  - Files: `src/utils/playbook_parser.py`, `src/utils/embedding_client.py`, `tests/utils/test_playbook_parser.py`, `tests/utils/test_embedding_client.py`
  - Impl plan: `.ai/plans/impl/rag-playbook_phase-1.impl.md`

- [ ] **Phase 2: Knowledge Index** `[delegatable]`
  - Scope: Implement the Layer-2 composite module — `knowledge_index.py` (index CRUD, incremental diff, search with integrated similarity math). Depends on playbook_parser types conceptually but no import-time dependency. Includes test file.
  - Files: `src/utils/knowledge_index.py`, `tests/utils/test_knowledge_index.py`
  - Impl plan: `.ai/plans/impl/rag-playbook_phase-2.impl.md`

- [ ] **Phase 3: CLI Scripts & CI Workflow** `[delegatable]`
  - Scope: Implement the Layer-3 CLI entry points — `build-knowledge-index.py` (CI build pipeline) and `query-knowledge-index.py` (Librarian query with graceful degradation). Create the GitHub Actions workflow for automated index rebuilds.
  - Files: `scripts/build-knowledge-index.py`, `scripts/query-knowledge-index.py`, `.github/workflows/build-knowledge-index.yml`
  - Impl plan: `.ai/plans/impl/rag-playbook_phase-3.impl.md`

- [ ] **Phase 4: Librarian Update & Documentation** `[delegatable]`
  - Scope: Update the Librarian agent instructions (`.github/agents/librarian.agent.md`) to add RAG retrieval as Stage 1. Update all project documentation: CODE_INVENTORY, PLAYBOOK, BUSINESS_LOGIC, README, and per-file docs.
  - Files: `.github/agents/librarian.agent.md`, `docs/CODE_INVENTORY.md`, `docs/BUSINESS_LOGIC.md`, `docs/PLAYBOOK.md`, `README.md`, `docs/files/playbook_parser.md`, `docs/files/embedding_client.md`, `docs/files/knowledge_index.md`
  - Impl plan: `.ai/plans/impl/rag-playbook_phase-4.impl.md`

---

## Post-Implementation Checklist

- [ ] `docs/CODE_INVENTORY.md` updated with all new symbols
- [ ] `docs/API_DOCUMENTATION.md` updated with any API usage found
- [ ] `docs/PLAYBOOK.md` updated with any new decisions
- [ ] `README.md` updated if structure/setup/features changed
- [ ] `.gitignore` updated if new tooling/dirs introduced
- [ ] `.ai/todos/2026-03-11_rag-playbook-infrastructure.todo.md` marked ✅ Complete
- [ ] `.ai/sessions/2026-03-11_rag-playbook-infrastructure.md` summary written
- [ ] Git commit with conventional message

## Critique Log

<!-- Architecture plan: .ai/plans/2026-03-11_rag-playbook-infrastructure.architecture.md -->

| Round | Issues Found | Resolution | Verdict |
| --- | --- | --- | --- |
| 1 | C1: `handle_missing_index` contradictory; C2: Missing token crashes; C3: No test files; C4: No duplicate id validation; C5: Fallback triggers not consolidated; C6: sys.path fragile; C7: Token overflow risk; C8: CI push race; C9: Empty body not validated | All fixed in architecture v3. See architecture plan critique log. | All resolved |
| 2 | All 9 Round 1 issues verified resolved. No new critical/important issues. 3 minor notes carried. | APPROVED | ✅ Approved |

---

## Acceptance Criteria

- [ ] All `.playbook.md` files parse correctly with TOML frontmatter via `tomllib`
- [ ] `playbook_parser` discovers, parses, and validates all playbook chunks
- [ ] `embedding_client` batches texts, calls GitHub Models API with retry/backoff
- [ ] `knowledge_index` supports load/save/diff/merge/search with atomic writes
- [ ] `build-knowledge-index.py` performs incremental builds with `--dry-run` support
- [ ] `query-knowledge-index.py` returns ranked results and degrades gracefully when index/token unavailable
- [ ] CI workflow triggers on `docs/playbooks/**` changes and commits updated index
- [ ] Librarian agent updated with RAG retrieval as Stage 1
- [ ] All functions have 15+ unit tests (TDD — tests written before implementation)
- [ ] No duplication with existing inventory
- [ ] All functions ≤40 lines, doc comments on all public functions
- [ ] Zero errors, zero warnings
