# Impl: Knowledge Index (Phase 2)

**Parent plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`
**Phase:** 2
**Status:** 🟡 Draft

---

## Overview

Implement the Layer-2 composite module — `knowledge_index.py`. This module handles index CRUD operations, incremental diffing by content hash, and search with integrated similarity math (merged from former `similarity.py`). It has no import-time dependencies on Layer 1 modules — it operates on dicts and lists, not on parser/client objects directly.

**Size risk acknowledged:** 5 public functions + 6 private helpers = 11 functions total. At ~15-25 lines each, this could reach 165-275 lines. If implementation exceeds 200 lines, the pre-planned seam is: split index I/O (`load_index`, `save_index`, `_empty_index`, `_validate_index`, `_atomic_write`) from search logic (`search_chunks`, `diff_chunks`, `merge_embeddings`, `_filter_chunks`, `_dot_product`, `_rank_by_similarity`). The Worker should flag this if it occurs.

---

## Functions

### `src/utils/knowledge_index.py`

**Purpose:** Read, write, search, and diff the knowledge index JSON file. Includes similarity math as private helpers.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `load_index` | `(index_path: str) -> dict` | Load and validate the index JSON. Returns empty index structure if file doesn't exist | `[delegatable]` |
| 2 | `save_index` | `(index: dict, index_path: str) -> None` | Atomically write the index JSON. Updates `built_at` and `chunk_count` before writing | `[delegatable]` |
| 3 | `diff_chunks` | `(current_chunks: list[dict], existing_index: dict) -> tuple[list[dict], list[str]]` | Compare parsed chunks against existing index by `content_hash`. Returns `(chunks_to_embed, ids_to_remove)` | `[delegatable]` |
| 4 | `merge_embeddings` | `(existing_index: dict, new_chunks: list[dict], embeddings: list[list[float]], removed_ids: list[str]) -> dict` | Merge newly embedded chunks into existing index, remove stale IDs. Returns updated index dict | `[delegatable]` |
| 5 | `search_chunks` | `(index: dict, query_embedding: list[float], agent: str or None, tech: str or None, top_k: int) -> list[dict]` | Filter chunks by agent/tech, rank by similarity, return top_k results with scores | `[delegatable]` |
| 6 | `_empty_index` | `() -> dict` | Return a valid empty index structure with `version`, `model`, `dimensions`, `built_at`, `chunk_count`, `chunks` | `[delegatable]` |
| 7 | `_validate_index` | `(index: dict) -> None` | Check schema version, required keys. Raise `ValueError` if invalid or version mismatch | `[delegatable]` |
| 8 | `_filter_chunks` | `(chunks: list[dict], agent: str or None, tech: str or None) -> list[dict]` | Filter by agent name (match if chunk's `agents` contains agent name or `"all"`) and technology (match if chunk's `technologies` contains tech or is empty list) | `[delegatable]` |
| 9 | `_atomic_write` | `(data: str, path: str) -> None` | Write to `{path}.tmp`, then `os.replace()` to atomically swap. Works on both Unix and Windows (NTFS) | `[delegatable]` |
| 10 | `_dot_product` | `(vec_a: list[float], vec_b: list[float]) -> float` | Compute dot product of two equal-length vectors. Pre-normalized embeddings → dot product = cosine similarity | `[delegatable]` |
| 11 | `_rank_by_similarity` | `(query_vec: list[float], candidates: list[dict], top_k: int) -> list[dict]` | Sort candidates by `_dot_product` similarity, return top_k. Each candidate dict must have an `"embedding"` key. Returns candidates enriched with a `"score"` key | `[delegatable]` |

**Progress:**

- [ ] #1 `load_index` `[delegatable]`
- [ ] #2 `save_index` `[delegatable]`
- [ ] #3 `diff_chunks` `[delegatable]`
- [ ] #4 `merge_embeddings` `[delegatable]`
- [ ] #5 `search_chunks` `[delegatable]`
- [ ] #6 `_empty_index` `[delegatable]`
- [ ] #7 `_validate_index` `[delegatable]`
- [ ] #8 `_filter_chunks` `[delegatable]`
- [ ] #9 `_atomic_write` `[delegatable]`
- [ ] #10 `_dot_product` `[delegatable]`
- [ ] #11 `_rank_by_similarity` `[delegatable]`

---

### `tests/utils/test_knowledge_index.py`

**Purpose:** Unit tests for all `knowledge_index` functions. 15+ tests per function. Written BEFORE implementation (TDD red phase).

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | Tests for `_empty_index` | N/A | Correct structure, required keys present, version value | `[delegatable]` |
| 2 | Tests for `_validate_index` | N/A | Valid index passes, missing keys, wrong version, wrong type | `[delegatable]` |
| 3 | Tests for `load_index` | N/A | Valid JSON, missing file returns empty, corrupted JSON raises, schema version mismatch | `[delegatable]` |
| 4 | Tests for `save_index` | N/A | Writes valid JSON, updates built_at and chunk_count, atomic write behavior | `[delegatable]` |
| 5 | Tests for `_atomic_write` | N/A | Writes to tmp then renames, original unchanged on failure | `[delegatable]` |
| 6 | Tests for `diff_chunks` | N/A | New chunks detected, changed chunks detected, removed IDs detected, unchanged chunks skipped, empty index | `[delegatable]` |
| 7 | Tests for `merge_embeddings` | N/A | Adds new chunks, removes stale IDs, preserves unchanged, updates existing | `[delegatable]` |
| 8 | Tests for `_filter_chunks` | N/A | Filter by agent, filter by tech, agent "all" matches any, empty tech list matches any, combined filters, no matches | `[delegatable]` |
| 9 | Tests for `_dot_product` | N/A | Identical vectors, orthogonal vectors, known values, zero vector, equal-length validation | `[delegatable]` |
| 10 | Tests for `_rank_by_similarity` | N/A | Correct ordering, top_k limit, score enrichment, empty candidates, single candidate | `[delegatable]` |
| 11 | Tests for `search_chunks` | N/A | End-to-end: filter + rank, no matches, agent filter, tech filter, combined filters | `[delegatable]` |

**Progress:**

- [ ] #1 Tests for `_empty_index` `[delegatable]`
- [ ] #2 Tests for `_validate_index` `[delegatable]`
- [ ] #3 Tests for `load_index` `[delegatable]`
- [ ] #4 Tests for `save_index` `[delegatable]`
- [ ] #5 Tests for `_atomic_write` `[delegatable]`
- [ ] #6 Tests for `diff_chunks` `[delegatable]`
- [ ] #7 Tests for `merge_embeddings` `[delegatable]`
- [ ] #8 Tests for `_filter_chunks` `[delegatable]`
- [ ] #9 Tests for `_dot_product` `[delegatable]`
- [ ] #10 Tests for `_rank_by_similarity` `[delegatable]`
- [ ] #11 Tests for `search_chunks` `[delegatable]`

---

## Constants & Types

Module-level constants defined inline in `knowledge_index.py`:

- `INDEX_VERSION = 1` — current schema version
- `MODEL_NAME = "openai/text-embedding-3-small"` — model identifier
- `DIMENSIONS = 1536` — embedding vector dimensions

---

## Dependencies

| Depends on | From | Status |
| --- | --- | --- |
| Phase 1 parser types (conceptual) | `src/utils/playbook_parser.py` | No import dependency — operates on dicts |
| Python stdlib: `json`, `os`, `datetime` | stdlib | Available |

---

## Notes

- **No import dependency on Layer 1:** `knowledge_index.py` receives parsed chunks as `list[dict]` — it doesn't import `playbook_parser`. This keeps Layer 2 independently testable.
- **Similarity math is internal:** `_dot_product` and `_rank_by_similarity` are private helpers, not a public API. They were merged from the former standalone `similarity.py` per architecture v2.
- **Atomic writes:** `_atomic_write` uses `os.replace()` which is atomic on both Unix and Windows (NTFS). The `.tmp` file is written first, then atomically swapped. If the process crashes mid-write, the original index is preserved.
- **Schema versioning:** If `INDEX_VERSION` changes, `_validate_index` raises `ValueError`, forcing a full rebuild. This is the intentional migration strategy.
- **GRANULAR SPAWNING:** 11 functions × (1 Test Writer + 1 Worker) = 22 sub-agent spawns for this phase.
