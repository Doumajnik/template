# Review Report

> **Persistent review audit trail.** The Reviewer Agent appends findings here after each cycle. This file is append-only — never delete old entries.

---

## Review Log

<!-- Reviewer Agent appends new review entries below this line. -->
<!-- Each entry follows this format:

### Review — {YYYY-MM-DD} — {topic/session}

#### Duplication Check
- [PASS/WARN] {details}

#### Playbook Compliance
- [PASS/WARN] {details}

#### Preference Alignment
- [PASS/WARN] {details}

#### Documentation Completeness
- [PASS/WARN] {details}

#### Security Quick-Check
- [PASS/WARN] {details}

#### Recommendations
- {any suggested improvements}

-->

---

## Review — 2026-03-11 — RAG Playbook Infrastructure

**Verdict: PASS with 1 MEDIUM issue, 2 LOW issues**

### Files Reviewed

- `src/utils/playbook_parser.py` (120 lines, 8 functions)
- `src/utils/embedding_client.py` (166 lines, 7 functions)
- `src/utils/knowledge_index.py` (157 lines, 11 functions)
- `scripts/build-knowledge-index.py` (122 lines, 4 functions)
- `scripts/query-knowledge-index.py` (150 lines, 6 functions)
- `tests/utils/test_playbook_parser.py` (74 tests)
- `tests/utils/test_embedding_client.py` (54 tests)
- `tests/utils/test_knowledge_index.py` (82 tests)

### Correctness

- [PASS] **playbook_parser.py** — All 8 functions have clear, correct implementations. Frontmatter extraction regex handles both Unix and Windows line endings. Validation is thorough and raises descriptive `ValueError` messages with file paths. Content hash normalizes CRLF before hashing.
- [PASS] **embedding_client.py** — Retry logic correctly distinguishes retryable (429, 5xx, URLError) from non-retryable (other 4xx) errors. Exponential backoff with Retry-After header support. Batch ordering is preserved via `(orig_idx, text)` tuples. Lambda default-arg capture (`lambda bt=batch_texts`) avoids the classic closure bug.
- [PASS] **knowledge_index.py** — Incremental diff compares by `content_hash`, correctly identifying new, changed, and removed chunks. `merge_embeddings` handles update-in-place vs. append. `_atomic_write` uses tmp+replace for crash safety. `_filter_chunks` correctly implements the "all" agent wildcard and empty-technologies-matches-any logic.
- [PASS] **build-knowledge-index.py** — Pipeline flow is correct: parse → diff → embed → merge → save. Dry-run mode properly short-circuits before API calls. Full-rebuild mode correctly re-derives the removal list.
- [PASS] **query-knowledge-index.py** — Graceful fallback on missing token or any exception during search. Both markdown and JSON output formats work correctly. JSON output strips embedding vectors.

### Duplication Check

- [WARN] **MEDIUM — Duplicated filter logic** (`scripts/query-knowledge-index.py` lines 68–84)
  - `_filter_by_metadata()` is a near-identical copy of `knowledge_index._filter_chunks()`. The docstring even acknowledges this: *"same logic as _filter_chunks"*.
  - **Violates:** One-Copy Rule in `docs/PLAYBOOK.md`.
  - **Fix:** Make `_filter_chunks` public in `knowledge_index.py` (rename to `filter_chunks`) and import it in the query script. The query script's `fallback_metadata_retrieval` function should call `knowledge_index.filter_chunks()` instead of maintaining its own copy.

- [PASS] **No other meaningful duplication found.** `DIMENSIONS = 1536` is defined in both `embedding_client.py` and `knowledge_index.py`, but these serve different conceptual purposes (API request parameter vs. index schema field). Acceptable — coupling them to a shared constant would create an inappropriate dependency between modules.

### Playbook Compliance

- [PASS] **Functions ≤ 40 lines** — All functions are well within the limit. Longest is `_retry_with_backoff` at ~28 lines. No violations.
- [PASS] **Descriptive names** — Function and variable names are clear and self-documenting: `_extract_frontmatter`, `_validate_unique_ids`, `_create_batches`, `_retry_with_backoff`, `_atomic_write`, `diff_chunks`, `merge_embeddings`.
- [PASS] **Doc comments on exports** — All public functions have docstrings. Module docstrings present on all 3 utility modules.
- [PASS] **No hardcoded secrets** — Token is always passed as a function parameter, never read from env within library code. Only the entry-point scripts read `GH_MODELS_TOKEN` from the environment.
- [PASS] **Structure** — Source in `src/utils/`, tests mirroring in `tests/utils/`, scripts in `scripts/`. Correct.
- [PASS] **Error handling** — Never catches and swallows silently. Config/startup failures in build script exit with clear messages. Runtime failures in query script degrade gracefully to metadata-only fallback.
- [PASS] **One responsibility per file** — Parser handles parsing only, embedding client handles API only, knowledge index handles index CRUD only.
- [PASS] **stdlib preference** — `embedding_client.py` uses only `urllib.request` and `json` (no `requests` dependency). `playbook_parser.py` uses `tomllib` (stdlib since Python 3.11). Good.

### Preference Alignment

- [PASS] **Naming conventions** — `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants. Consistent across all modules.
- [PASS] **Import style** — Standard library imports grouped first, then local imports (with `noqa: E402` for path-manipulated imports in scripts). Consistent.
- [PASS] **Type hints** — Present on all function signatures. Uses `str | None` union syntax (Python 3.10+). Consistent.
- [PASS] **Error messages** — All include context (file paths, field names, error codes). Consistent pattern.

### Documentation Completeness

- [PASS] **CODE_INVENTORY.md** — All public symbols from all 3 utility modules are registered with correct signatures and descriptions.
- [PASS] **BUSINESS_LOGIC.md** — RAG pipeline data flow is documented with both index-build and query flows, plus the fallback behavior.
- [PASS] **PLAYBOOK.md** — No new architecture decisions were needed beyond the existing patterns.
- [LOW] **CODE_INVENTORY.md** — The scripts (`build-knowledge-index.py`, `query-knowledge-index.py`) and their public functions (`parse_args`, `validate_environment`, `run_build`, `run_query`, `format_results_markdown`, `format_results_json`, `fallback_metadata_retrieval`) are not listed in CODE_INVENTORY. These are entry points with stable interfaces and should be documented.

### Security Quick-Check

- [PASS] **No secrets in code** — Token passed explicitly via function parameters. Scripts read from `GH_MODELS_TOKEN` env var only.
- [PASS] **Input validation at boundaries** — CLI args validated (playbook dir exists, token present). Playbook files validated for required fields, valid categories, correct types.
- [PASS] **No injection risk** — No SQL, no shell commands, no template interpolation of user input. HTTP requests use `urllib.request.Request` with explicit headers (no URL injection).
- [PASS] **Atomic file writes** — Index writes use tmp+replace pattern to prevent corruption on crash.

### Elegance Assessment

- [PASS] **Overall quality is high.** The code reads like production-grade utility code. Each module has a single clear responsibility, functions are short and well-named, edge cases are handled, and the design choices (explicit token passing, atomic writes, incremental diffing by content hash) reflect engineering maturity.
- [PASS] **The lambda default-arg pattern** in `embed_texts` (`lambda bt=batch_texts`) is the correct Python idiom for closure capture in loops. Good.
- [PASS] **The sentinel `_UNSET = object()` pattern** in test helpers avoids `None` ambiguity. Clean.
- [LOW] **`_retry_with_backoff` uses a generic `func` callable** — the type signature could be `Callable[[], T]` for better type safety, but this is a minor style point for an internal helper.

### Test Coverage Assessment

- [PASS] **playbook_parser** — 74 tests covering all 8 functions. Edge cases include: Windows line endings, empty frontmatter, malformed TOML, special characters, duplicate IDs, underscore-prefixed files, missing fields (one test per required field).
- [PASS] **embedding_client** — 54 tests covering all 7 functions. HTTP mocking is comprehensive: success, 401, 429, 500, timeout, malformed JSON, Retry-After header, exponential backoff delays. Batch ordering preserved across splits.
- [PASS] **knowledge_index** — 82 tests covering all 11 functions. Mixed scenarios (add + update + remove in one merge), immutability checks (does not mutate original), roundtrip load/save, empty/missing file handling.
- **Total: 210 tests across 3 modules.** Exceeds the 15-per-function minimum for all exported functions.

### Issues Summary

| # | Severity | File | Issue | Recommended Fix |
|---|----------|------|-------|-----------------|
| 1 | **MEDIUM** | `scripts/query-knowledge-index.py` L68–84 | `_filter_by_metadata` duplicates `knowledge_index._filter_chunks` | Make `_filter_chunks` public, import it in the query script |
| 2 | **LOW** | `docs/CODE_INVENTORY.md` | Script entry-point functions not registered | Add sections for `build-knowledge-index.py` and `query-knowledge-index.py` |
| 3 | **LOW** | `src/utils/embedding_client.py` L86 | `_retry_with_backoff` parameter `func` lacks type annotation | Add `Callable[[], T]` signature (optional, internal helper) |

### Verdict

**PASS.** The implementation is correct, well-structured, and thoroughly tested. One duplication issue (MEDIUM) should be addressed by the Worker in a follow-up task. No CRITICAL or HIGH issues. Code quality is high — a staff engineer would approve this.
