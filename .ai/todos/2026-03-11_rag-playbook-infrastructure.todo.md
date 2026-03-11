# Todo: RAG-Powered Playbook Infrastructure

**Date:** 2026-03-11
**Status:** 🟡 In Progress
**Plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`

---

## Tasks

### Phase 0 — Playbook Format, Template & Stubs

- [ ] ⬜ **P0-1:** Create playbook template `docs/playbooks/_TEMPLATE.playbook.md` → *Scaffolder*
- [ ] ⬜ **P0-2:** Create `.gitattributes` entry for `.ai/knowledge-index.json` → *Scaffolder*
- [ ] ⬜ **P0-3:** Create shared playbook stubs (8 files in `docs/playbooks/shared/`) → *Scaffolder*
- [ ] ⬜ **P0-4:** Create agent playbook stubs (32 files in `docs/playbooks/agents/`) → *Scaffolder*
- [ ] ⬜ **P0-5:** Create technology playbook stubs (4 files in `docs/playbooks/technologies/`) → *Scaffolder*

### Phase 1 — Parser & Embedding Client (Layer 1)

**Scaffolding:**

- [ ] ⬜ **P1-S1:** Scaffold `src/utils/playbook_parser.py` (8 functions) → *Scaffolder*
- [ ] ⬜ **P1-S2:** Scaffold `src/utils/embedding_client.py` (7 functions) → *Scaffolder*
- [ ] ⬜ **P1-S3:** Scaffold `tests/utils/test_playbook_parser.py` → *Scaffolder*
- [ ] ⬜ **P1-S4:** Scaffold `tests/utils/test_embedding_client.py` → *Scaffolder*

**Tests (TDD red phase — write BEFORE implementation):**

- [ ] ⬜ **P1-T1:** Write tests for `_extract_frontmatter` → *Test Writer*
- [ ] ⬜ **P1-T2:** Write tests for `_validate_frontmatter` → *Test Writer*
- [ ] ⬜ **P1-T3:** Write tests for `_validate_content` → *Test Writer*
- [ ] ⬜ **P1-T4:** Write tests for `_compute_content_hash` → *Test Writer*
- [ ] ⬜ **P1-T5:** Write tests for `_validate_unique_ids` → *Test Writer*
- [ ] ⬜ **P1-T6:** Write tests for `parse_playbook_file` → *Test Writer*
- [ ] ⬜ **P1-T7:** Write tests for `discover_playbook_files` → *Test Writer*
- [ ] ⬜ **P1-T8:** Write tests for `parse_all_playbooks` → *Test Writer*
- [ ] ⬜ **P1-T9:** Write tests for `_estimate_tokens` → *Test Writer*
- [ ] ⬜ **P1-T10:** Write tests for `_create_batches` → *Test Writer*
- [ ] ⬜ **P1-T11:** Write tests for `_call_embedding_api` → *Test Writer*
- [ ] ⬜ **P1-T12:** Write tests for `_retry_with_backoff` → *Test Writer*
- [ ] ⬜ **P1-T13:** Write tests for `_rate_limit_sleep` → *Test Writer*
- [ ] ⬜ **P1-T14:** Write tests for `embed_single` → *Test Writer*
- [ ] ⬜ **P1-T15:** Write tests for `embed_texts` → *Test Writer*

**Implementation (TDD green phase):**

- [ ] ⬜ **P1-W1:** Implement `_extract_frontmatter` → *Worker*
- [ ] ⬜ **P1-W2:** Implement `_validate_frontmatter` → *Worker*
- [ ] ⬜ **P1-W3:** Implement `_validate_content` → *Worker*
- [ ] ⬜ **P1-W4:** Implement `_compute_content_hash` → *Worker*
- [ ] ⬜ **P1-W5:** Implement `_validate_unique_ids` → *Worker*
- [ ] ⬜ **P1-W6:** Implement `parse_playbook_file` → *Worker*
- [ ] ⬜ **P1-W7:** Implement `discover_playbook_files` → *Worker*
- [ ] ⬜ **P1-W8:** Implement `parse_all_playbooks` → *Worker*
- [ ] ⬜ **P1-W9:** Implement `_estimate_tokens` → *Worker*
- [ ] ⬜ **P1-W10:** Implement `_create_batches` → *Worker*
- [ ] ⬜ **P1-W11:** Implement `_call_embedding_api` → *Worker*
- [ ] ⬜ **P1-W12:** Implement `_retry_with_backoff` → *Worker*
- [ ] ⬜ **P1-W13:** Implement `_rate_limit_sleep` → *Worker*
- [ ] ⬜ **P1-W14:** Implement `embed_single` → *Worker*
- [ ] ⬜ **P1-W15:** Implement `embed_texts` → *Worker*

### Phase 2 — Knowledge Index (Layer 2)

**Scaffolding:**

- [ ] ⬜ **P2-S1:** Scaffold `src/utils/knowledge_index.py` (11 functions) → *Scaffolder*
- [ ] ⬜ **P2-S2:** Scaffold `tests/utils/test_knowledge_index.py` → *Scaffolder*

**Tests (TDD red phase):**

- [ ] ⬜ **P2-T1:** Write tests for `_empty_index` → *Test Writer*
- [ ] ⬜ **P2-T2:** Write tests for `_validate_index` → *Test Writer*
- [ ] ⬜ **P2-T3:** Write tests for `load_index` → *Test Writer*
- [ ] ⬜ **P2-T4:** Write tests for `save_index` → *Test Writer*
- [ ] ⬜ **P2-T5:** Write tests for `_atomic_write` → *Test Writer*
- [ ] ⬜ **P2-T6:** Write tests for `diff_chunks` → *Test Writer*
- [ ] ⬜ **P2-T7:** Write tests for `merge_embeddings` → *Test Writer*
- [ ] ⬜ **P2-T8:** Write tests for `_filter_chunks` → *Test Writer*
- [ ] ⬜ **P2-T9:** Write tests for `_dot_product` → *Test Writer*
- [ ] ⬜ **P2-T10:** Write tests for `_rank_by_similarity` → *Test Writer*
- [ ] ⬜ **P2-T11:** Write tests for `search_chunks` → *Test Writer*

**Implementation (TDD green phase):**

- [ ] ⬜ **P2-W1:** Implement `_empty_index` → *Worker*
- [ ] ⬜ **P2-W2:** Implement `_validate_index` → *Worker*
- [ ] ⬜ **P2-W3:** Implement `load_index` → *Worker*
- [ ] ⬜ **P2-W4:** Implement `save_index` → *Worker*
- [ ] ⬜ **P2-W5:** Implement `_atomic_write` → *Worker*
- [ ] ⬜ **P2-W6:** Implement `diff_chunks` → *Worker*
- [ ] ⬜ **P2-W7:** Implement `merge_embeddings` → *Worker*
- [ ] ⬜ **P2-W8:** Implement `_filter_chunks` → *Worker*
- [ ] ⬜ **P2-W9:** Implement `_dot_product` → *Worker*
- [ ] ⬜ **P2-W10:** Implement `_rank_by_similarity` → *Worker*
- [ ] ⬜ **P2-W11:** Implement `search_chunks` → *Worker*

### Phase 3 — CLI Scripts & CI Workflow (Layer 3)

**Scaffolding:**

- [ ] ⬜ **P3-S1:** Scaffold `scripts/build-knowledge-index.py` (5 functions) → *Scaffolder*
- [ ] ⬜ **P3-S2:** Scaffold `scripts/query-knowledge-index.py` (6 functions) → *Scaffolder*

**Implementation:**

- [ ] ⬜ **P3-W1:** Implement `main` (build script) → *Worker*
- [ ] ⬜ **P3-W2:** Implement `parse_args` (build script) → *Worker*
- [ ] ⬜ **P3-W3:** Implement `validate_environment` (build script) → *Worker*
- [ ] ⬜ **P3-W4:** Implement `run_build` (build script) → *Worker*
- [ ] ⬜ **P3-W5:** Implement `print_summary` (build script) → *Worker*
- [ ] ⬜ **P3-W6:** Implement `main` (query script) → *Worker*
- [ ] ⬜ **P3-W7:** Implement `parse_args` (query script) → *Worker*
- [ ] ⬜ **P3-W8:** Implement `run_query` (query script) → *Worker*
- [ ] ⬜ **P3-W9:** Implement `format_results_markdown` (query script) → *Worker*
- [ ] ⬜ **P3-W10:** Implement `format_results_json` (query script) → *Worker*
- [ ] ⬜ **P3-W11:** Implement `fallback_metadata_retrieval` (query script) → *Worker*
- [ ] ⬜ **P3-W12:** Create `.github/workflows/build-knowledge-index.yml` → *Worker*

**Integration Tests:**

- [ ] ⬜ **P3-IT1:** Write integration tests for build pipeline (end-to-end) → *Integration Tester*
- [ ] ⬜ **P3-IT2:** Write integration tests for query pipeline (end-to-end, including fallback) → *Integration Tester*

### Phase 4 — Librarian Update & Documentation

- [ ] ⬜ **P4-1:** Update Librarian agent with RAG retrieval stage → *Doc Updater*
- [ ] ⬜ **P4-2:** Update `docs/CODE_INVENTORY.md` with all new symbols → *Doc Updater*
- [ ] ⬜ **P4-3:** Update `docs/BUSINESS_LOGIC.md` with RAG data flows → *Doc Updater*
- [ ] ⬜ **P4-4:** Update `docs/PLAYBOOK.md` with RAG architecture decisions → *Doc Updater*
- [ ] ⬜ **P4-5:** Update `README.md` with structure and feature changes → *Doc Updater*
- [ ] ⬜ **P4-6:** Create per-file docs (`docs/files/playbook_parser.md`, `embedding_client.md`, `knowledge_index.md`) → *Doc Updater*

### Post-Implementation

- [ ] ⬜ **POST-1:** Review all implementation for duplication, playbook compliance, preference alignment → *Reviewer*
- [ ] ⬜ **POST-2:** Security audit of all code → *Security*
- [ ] ⬜ **POST-3:** Code quality scan → *Code Quality*
- [ ] ⬜ **POST-4:** Write session summary → *Doc Updater*
- [ ] ⬜ **POST-5:** Retrospective review and PLAYBOOK update → *Retrospective*

---

## Progress Log

| Time | Agent | Update |
| --- | --- | --- |
| 2026-03-11 | Planning Agent | Created plan, impl plans (phases 0-4), and todo file |

---

## Blockers

*None.*

---

## Notes

- **TURBO_MODE ON** — all functions marked `[delegatable]`, mass-spawn enabled.
- **GRANULAR SPAWNING ON** — one Test Writer + one Worker per function.
- **Execution order:** Phase 0 → Phase 1 (parser + client in parallel) → Phase 2 → Phase 3 → Phase 4 → Post-implementation checks.
- **Total sub-agent spawns estimated:** ~5 Scaffolder + 26 Test Writer + 26 Worker + 12 CLI Worker + 2 Integration Tester + 6 Doc Updater + 3 post-impl agents = ~80 spawns.
- **Parallel opportunities:** Within Phase 1, parser and client tracks can be fully parallelized (scaffolding, tests, and implementation). Within Phase 2, all 11 Test Writers can be spawned together, then all 11 Workers. Phase 0 stubs can be batched into a single Scaffolder call.
