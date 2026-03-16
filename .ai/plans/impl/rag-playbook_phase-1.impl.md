# Impl: Parser & Embedding Client (Phase 1)

**Parent plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`
**Phase:** 1
**Status:** 🟡 Draft

---

## Overview

Implement the two Layer-1 utility modules. These have no inter-dependencies and can be built (scaffolded, tested, implemented) in parallel. Both modules depend only on Python stdlib.

---

## Functions

### `src/utils/playbook_parser.py`

**Purpose:** Parse `.playbook.md` files with TOML frontmatter into structured chunk records.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `parse_playbook_file` | `(file_path: str) -> dict` | Parse a single `.playbook.md` file. Returns dict with `id`, `title`, `agents`, `technologies`, `category`, `tags`, `content`, `content_hash`, `source_file` | `[delegatable]` |
| 2 | `discover_playbook_files` | `(base_dir: str) -> list[str]` | Recursively find all `*.playbook.md` files under `base_dir`. Returns sorted list of absolute paths | `[delegatable]` |
| 3 | `parse_all_playbooks` | `(base_dir: str) -> list[dict]` | Discover + parse all playbook files. Validates uniqueness of `id` across all files — raises `ValueError` on collision. Returns list of chunk records | `[delegatable]` |
| 4 | `_extract_frontmatter` | `(raw_text: str) -> tuple[dict, str]` | Split TOML frontmatter from markdown body using `+++` delimiters. Parse TOML with `tomllib.loads()`. Returns `(metadata_dict, body_string)` | `[delegatable]` |
| 5 | `_validate_frontmatter` | `(meta: dict, file_path: str) -> None` | Validate required fields (`id`, `title`, `agents`, `technologies`, `category`, `tags`, `version`), valid category values, non-empty agents list. Raises `ValueError` with file path context | `[delegatable]` |
| 6 | `_compute_content_hash` | `(content: str) -> str` | SHA-256 hex digest of the markdown body (stripped, normalized newlines). Returns `"sha256:{hex}"` | `[delegatable]` |
| 7 | `_validate_unique_ids` | `(chunks: list[dict]) -> None` | Check that all chunk `id` values are unique. Raises `ValueError` listing the duplicate `id` and conflicting source file paths | `[delegatable]` |
| 8 | `_validate_content` | `(body: str, file_path: str) -> None` | Validate that the markdown body is non-empty after stripping whitespace. Raises `ValueError` if the body is blank | `[delegatable]` |

**Progress:**

- [ ] #1 `parse_playbook_file` `[delegatable]`
- [ ] #2 `discover_playbook_files` `[delegatable]`
- [ ] #3 `parse_all_playbooks` `[delegatable]`
- [ ] #4 `_extract_frontmatter` `[delegatable]`
- [ ] #5 `_validate_frontmatter` `[delegatable]`
- [ ] #6 `_compute_content_hash` `[delegatable]`
- [ ] #7 `_validate_unique_ids` `[delegatable]`
- [ ] #8 `_validate_content` `[delegatable]`

---

### `tests/utils/test_playbook_parser.py`

**Purpose:** Unit tests for all `playbook_parser` functions. 15+ tests per function. Written BEFORE implementation (TDD red phase).

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | Tests for `_extract_frontmatter` | N/A | TOML parsing, `+++` delimiters, missing delimiters, malformed TOML, empty frontmatter | `[delegatable]` |
| 2 | Tests for `_validate_frontmatter` | N/A | Required fields, valid category, non-empty agents, invalid category values | `[delegatable]` |
| 3 | Tests for `_validate_content` | N/A | Empty body, whitespace-only body, valid body with heading | `[delegatable]` |
| 4 | Tests for `_compute_content_hash` | N/A | SHA-256 correctness, whitespace normalization, deterministic output | `[delegatable]` |
| 5 | Tests for `_validate_unique_ids` | N/A | Unique IDs pass, duplicate IDs raise ValueError with both file paths | `[delegatable]` |
| 6 | Tests for `parse_playbook_file` | N/A | Full parse of valid file, missing file, malformed file | `[delegatable]` |
| 7 | Tests for `discover_playbook_files` | N/A | Recursive discovery, empty directory, nested subdirs, non-playbook files ignored | `[delegatable]` |
| 8 | Tests for `parse_all_playbooks` | N/A | Multiple files, duplicate ID collision, empty directory | `[delegatable]` |

**Progress:**

- [ ] #1 Tests for `_extract_frontmatter` `[delegatable]`
- [ ] #2 Tests for `_validate_frontmatter` `[delegatable]`
- [ ] #3 Tests for `_validate_content` `[delegatable]`
- [ ] #4 Tests for `_compute_content_hash` `[delegatable]`
- [ ] #5 Tests for `_validate_unique_ids` `[delegatable]`
- [ ] #6 Tests for `parse_playbook_file` `[delegatable]`
- [ ] #7 Tests for `discover_playbook_files` `[delegatable]`
- [ ] #8 Tests for `parse_all_playbooks` `[delegatable]`

---

### `src/utils/embedding_client.py`

**Purpose:** Call the GitHub Models embedding API with batching, retry, and rate-limit logic.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `embed_texts` | `(texts: list[str], token: str) -> list[list[float]]` | Embed a list of texts with batching (54K token limit per batch, 4s sleep between batches). Returns list of 1536-dim vectors in same order as input | `[delegatable]` |
| 2 | `embed_single` | `(text: str, token: str) -> list[float]` | Convenience wrapper — embed one text. Returns single 1536-dim vector | `[delegatable]` |
| 3 | `_estimate_tokens` | `(text: str) -> int` | Rough token estimate: `len(text) // 4` | `[delegatable]` |
| 4 | `_create_batches` | `(texts: list[str], max_tokens: int) -> list[list[tuple[int, str]]]` | Group texts into batches fitting under `max_tokens` (default 54000). Each item is `(original_index, text)` to preserve ordering | `[delegatable]` |
| 5 | `_call_embedding_api` | `(batch_texts: list[str], token: str) -> list[list[float]]` | Single HTTP POST to GitHub Models API. On "too many tokens" error (HTTP 400), halves the batch and retries recursively | `[delegatable]` |
| 6 | `_retry_with_backoff` | `(func: callable, max_retries: int, base_delay: float) -> any` | Retry on HTTP 429/5xx with exponential backoff. Respects `Retry-After` header. Default: 3 retries, 4s base delay | `[delegatable]` |
| 7 | `_rate_limit_sleep` | `(batch_index: int) -> None` | Sleep 4 seconds between batches (skips for batch 0) to stay under 15 req/min | `[delegatable]` |

**Progress:**

- [ ] #1 `embed_texts` `[delegatable]`
- [ ] #2 `embed_single` `[delegatable]`
- [ ] #3 `_estimate_tokens` `[delegatable]`
- [ ] #4 `_create_batches` `[delegatable]`
- [ ] #5 `_call_embedding_api` `[delegatable]`
- [ ] #6 `_retry_with_backoff` `[delegatable]`
- [ ] #7 `_rate_limit_sleep` `[delegatable]`

---

### `tests/utils/test_embedding_client.py`

**Purpose:** Unit tests for all `embedding_client` functions. 15+ tests per function. Written BEFORE implementation (TDD red phase). HTTP calls mocked.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | Tests for `_estimate_tokens` | N/A | Token estimation for short/long/empty text, code-heavy content | `[delegatable]` |
| 2 | Tests for `_create_batches` | N/A | Single batch, multiple batches, oversized single text, batch boundary, empty input | `[delegatable]` |
| 3 | Tests for `_call_embedding_api` | N/A | Success response, 429 error, 5xx error, 4xx error, timeout, batch halving on 400, response parsing | `[delegatable]` |
| 4 | Tests for `_retry_with_backoff` | N/A | Success on first try, success after retry, max retries exceeded, Retry-After header respected | `[delegatable]` |
| 5 | Tests for `_rate_limit_sleep` | N/A | Batch 0 skips sleep, batch >0 sleeps 4s | `[delegatable]` |
| 6 | Tests for `embed_single` | N/A | Single text embedding, error propagation | `[delegatable]` |
| 7 | Tests for `embed_texts` | N/A | Multiple texts batched, ordering preserved, empty list, error propagation | `[delegatable]` |

**Progress:**

- [ ] #1 Tests for `_estimate_tokens` `[delegatable]`
- [ ] #2 Tests for `_create_batches` `[delegatable]`
- [ ] #3 Tests for `_call_embedding_api` `[delegatable]`
- [ ] #4 Tests for `_retry_with_backoff` `[delegatable]`
- [ ] #5 Tests for `_rate_limit_sleep` `[delegatable]`
- [ ] #6 Tests for `embed_single` `[delegatable]`
- [ ] #7 Tests for `embed_texts` `[delegatable]`

---

## Constants & Types

*(No standalone constants/types files in this phase. Constants like API URL, model name, dimensions, max tokens are defined inline as module-level constants within the respective files.)*

---

## Dependencies

| Depends on | From | Status |
| --- | --- | --- |
| Phase 0 playbook stubs | `docs/playbooks/` | Must exist for parser integration tests |
| Python stdlib: `tomllib` | stdlib (3.11+) | Available |
| Python stdlib: `os`, `re`, `hashlib` | stdlib | Available |
| Python stdlib: `urllib.request`, `json`, `time` | stdlib | Available |

---

## Notes

- **Parallel execution:** `playbook_parser.py` and `embedding_client.py` have no inter-dependencies. Their scaffolding, tests, and implementations can all be spawned in parallel.
- **Test-first (TDD):** Test Writer agents are spawned BEFORE Worker agents for each function. Tests must be written and failing before implementation begins.
- **GRANULAR SPAWNING:** Each function gets its own dedicated Test Writer and Worker instance. 8 parser functions + 7 embedding functions = 15 Test Writer spawns, then 15 Worker spawns.
- **Module-level constants** for `embedding_client.py`: `API_URL = "https://models.github.ai/inference/embeddings"`, `MODEL = "openai/text-embedding-3-small"`, `DIMENSIONS = 1536`, `MAX_BATCH_TOKENS = 54000`, `RATE_LIMIT_SLEEP = 4.0`, `MAX_RETRIES = 3`, `BASE_DELAY = 4.0`.
- **Token passed explicitly** — `embedding_client.py` never reads from env. CLI scripts read `GH_MODELS_TOKEN` from env and pass it in.
- **Size watch:** `playbook_parser.py` has 8 functions at ~15-20 lines each = ~120-160 lines. Well within the 200-line PLAYBOOK limit.
- **Size watch:** `embedding_client.py` has 7 functions at ~15-25 lines each = ~105-175 lines. Within the 200-line limit.
