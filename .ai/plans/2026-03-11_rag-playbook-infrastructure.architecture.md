# Architecture Plan: RAG-Powered Playbook Infrastructure

**Status:** ✅ Approved (Critic Round 2 — 2026-03-11)
**Date:** 2026-03-11
**Author:** Architect Agent

---

## Objective

Design a retrieval-augmented generation (RAG) infrastructure that enables the Librarian agent to serve semantically relevant playbook knowledge to all agents at query time. Playbook rules are decomposed into individually addressable markdown chunks with **TOML frontmatter** (parsed via `tomllib`, stdlib since Python 3.11), embedded via the GitHub Models API (`openai/text-embedding-3-small`, 1536 dimensions), and stored in a committed JSON index. A CI workflow rebuilds the index on playbook changes; the Librarian shells out to a query script at runtime to retrieve top-K chunks by cosine similarity (dot product on pre-normalized vectors), filtered by agent and technology tags. When the index is unavailable or the API is unreachable, the system **degrades gracefully** to metadata-only filtering — the Librarian reads playbook files directly and filters by `agents`/`technologies` fields without embeddings.

---

## Entities & Data Flow

### Core Entities

| Entity | Description | Location |
| --- | --- | --- |
| Playbook Chunk | A single rule/pattern unit — TOML frontmatter + markdown body | `docs/playbooks/{category}/{slug}.playbook.md` |
| Knowledge Index | JSON file mapping chunk IDs → metadata + embedding vectors | `.ai/knowledge-index.json` |
| Embedding Vector | 1536-dim float array from `text-embedding-3-small` | Stored inside the index |
| Context Brief | Markdown output returned to the Librarian with top-K chunk content | stdout of query script |

### Data Flow: Build Time (CI)

```text
docs/playbooks/**/*.playbook.md
        │
        ▼
  playbook_parser.py          ── parse TOML frontmatter + markdown body
        │
        ▼
  List[ChunkRecord]           ── id, title, agents, technologies, category, tags, content
        │
        ▼
  knowledge_index.py          ── load existing index, diff by content_hash
        │
        ▼
  embedding_client.py         ── batch-embed only NEW/CHANGED chunks via GitHub Models API
        │
        ▼
  knowledge_index.py          ── merge new embeddings, atomic write to .ai/knowledge-index.json
```

### Data Flow: Query Time (Librarian)

```text
Librarian agent spawned in query mode
        │
        ▼
  shells out: python3 scripts/query-knowledge-index.py \
    --query "anti-duplication rules for Python" \
    --agent worker --tech python --top-k 10
        │
        ▼
  query-knowledge-index.py
    ├── load .ai/knowledge-index.json        (knowledge_index.py)
    ├── embed query string                   (embedding_client.py)
    ├── filter chunks by --agent / --tech    (knowledge_index.py)
    ├── rank by dot product similarity       (similarity.py)
    └── output top-K chunks as markdown      (stdout)
        │
        ▼
  Librarian incorporates chunks into context brief
```

---

## Decomposition Strategy

### Build Order (bottom-up, shared pieces first)

```text
Layer 1 (I/O utilities, independent of each other):
  ├── src/utils/playbook_parser.py    (filesystem + tomllib)
  └── src/utils/embedding_client.py   (HTTP + retry)

Layer 2 (composes Layer 1, includes similarity math):
  └── src/utils/knowledge_index.py    (index CRUD + search + similarity)

Layer 3 (CLI entry points, compose everything):
  ├── scripts/build-knowledge-index.py
  └── scripts/query-knowledge-index.py
```

> **v2 change:** Merged `similarity.py` (2 functions, ~20 lines) into `knowledge_index.py`. Two pure math functions (`_dot_product`, `_rank_by_similarity`) are implementation details of search, not a public API warranting their own module. This reduces from 4 layers to 3 and eliminates one cross-module dependency.

### Dependency Graph

```text
build-knowledge-index.py ──► playbook_parser
                         ──► embedding_client
                         ──► knowledge_index

query-knowledge-index.py ──► playbook_parser  (v3: for metadata-only fallback)
                         ──► embedding_client
                         ──► knowledge_index
```

No circular dependencies. Each layer depends only on layers below it.

### Test File Decomposition (v3 addition)

Test files mirror `src/utils/` in `tests/utils/`, per PLAYBOOK rules.

| Test File | Mirrors | Key Coverage Areas |
| --- | --- | --- |
| `tests/utils/test_playbook_parser.py` | `src/utils/playbook_parser.py` | TOML frontmatter parsing, `+++` delimiter extraction, missing/malformed frontmatter, required field validation, empty body detection (C9), content hash computation, file discovery, duplicate `id` collision detection (C4), category validation |
| `tests/utils/test_embedding_client.py` | `src/utils/embedding_client.py` | Token estimation, batch creation with 54K limit, API call mocking (success/429/5xx/4xx/timeout), retry with backoff, rate limit sleep, batch halving on token overflow (C7), response parsing, error propagation |
| `tests/utils/test_knowledge_index.py` | `src/utils/knowledge_index.py` | Load/save/diff/merge/search operations, atomic write safety, empty index creation, schema version validation, chunk filtering by agent/tech, dot product math, similarity ranking, content hash diffing for incremental builds |

**Note:** The Test Writer agent will generate 15+ tests per function within these files. The table above defines the structural placement and coverage scope — not the individual test cases.

---

## Deduplication Report

| Check | Result |
| --- | --- |
| Existing Python files in `src/` | None — greenfield |
| Existing utilities in `scripts/` | `setup.sh`/`setup.ps1` — infrastructure only, no reusable logic |
| `CODE_INVENTORY.md` symbols | Empty — no source code exists |
| PLAYBOOK.md conflicts | None — the new chunked playbooks are a **parallel system**; old `docs/PLAYBOOK.md` stays as-is |
| Existing embedding/similarity code | None |
| `GH_MODELS_TOKEN` secret | Already configured for feedback pipeline — reuse the same secret |

**Conclusion:** No duplication risk. All modules are net-new. The only shared asset is `GH_MODELS_TOKEN`.

---

## Playbook Chunk Format

Each chunk is a standalone `.playbook.md` file with **TOML frontmatter** (delimited by `+++`):

```toml
+++
id = "shared/anti-duplication"
title = "Anti-Duplication Rules"
agents = ["all"]
technologies = []
category = "shared"
tags = ["duplication", "extraction", "reuse"]
version = 1
+++
```

```markdown
### Anti-Duplication Rules

Before creating anything new:

1. Search `docs/CODE_INVENTORY.md` for similar functionality.
2. Search across `src/` with grep/semantic search.
3. Reuse or extend existing code if possible.

...
```

> **v2 change:** Switched from YAML (`---` delimiters) to TOML (`+++` delimiters). Python 3.11+ includes `tomllib` in stdlib — a battle-tested, spec-compliant parser that eliminates the fragility of hand-rolled regex-based YAML parsing. The frontmatter schema is flat (strings, lists of strings, int) — a perfect fit for TOML. No external dependencies needed.

### Frontmatter Schema

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | string | yes | Unique identifier, format: `{category}/{slug}` |
| `title` | string | yes | Human-readable title |
| `agents` | list[string] | yes | Which agents this applies to. `["all"]` = universal |
| `technologies` | list[string] | yes | Technology filter. `[]` = technology-agnostic |
| `category` | string | yes | One of: `shared`, `agents`, `technologies` |
| `tags` | list[string] | yes | Free-form tags for additional filtering |
| `version` | int | yes | Chunk version — increment on meaningful content change |

### Validation Rules

- `id` must match the file path pattern: `{category}/{slug}` where slug = filename without `.playbook.md`
- `agents` values must be valid agent names or `"all"`
- `category` must be one of `shared`, `agents`, `technologies`
- Body must contain at least one `###` heading

---

## Knowledge Index JSON Schema

```json
{
  "version": 1,
  "model": "openai/text-embedding-3-small",
  "dimensions": 1536,
  "built_at": "2026-03-11T12:00:00Z",
  "chunk_count": 42,
  "chunks": [
    {
      "id": "shared/anti-duplication",
      "source_file": "docs/playbooks/shared/anti-duplication.playbook.md",
      "title": "Anti-Duplication Rules",
      "agents": ["all"],
      "technologies": [],
      "category": "shared",
      "tags": ["duplication", "extraction", "reuse"],
      "content_hash": "sha256:a1b2c3d4...",
      "embedding": [0.0123, -0.0456, 0.0789]
    }
  ]
}
```

### Schema Notes

- `content_hash`: SHA-256 of the raw markdown body (excluding frontmatter). Used for incremental builds — only re-embed chunks whose content changed.
- `embedding`: Array of exactly 1536 floats. Pre-normalized by OpenAI — dot product = cosine similarity.

### Git Considerations

> **v2 addition:** The index file (~1-2MB) is committed to git so the Librarian works immediately on clone without a build step. To mitigate git bloat from repeated rebuilds:
>
> - Add `.ai/knowledge-index.json` to `.gitattributes` with `linguist-generated=true` — hides diffs in merge requests and excludes from language stats.
> - Incremental builds minimize changes — only re-embedded chunks produce new float arrays.
> - If bloat becomes problematic (>50MB pack growth), migrate to Git LFS or treat as a CI artifact. This is a **documented upgrade path**, not a current requirement.
> - Add to `.gitattributes`: `.ai/knowledge-index.json linguist-generated=true diff=json`
- `chunk_count`: Redundant count for quick validation without iterating.
- `version`: Schema version. Increment if the JSON structure changes (forces full rebuild).

---

## Directory Structure

```text
docs/playbooks/
├── shared/                           ← Rules that apply to all agents
│   ├── anti-duplication.playbook.md
│   ├── decomposition.playbook.md
│   ├── extraction-rules.playbook.md
│   ├── error-handling.playbook.md
│   ├── markdown-formatting.playbook.md
│   ├── naming-conventions.playbook.md
│   ├── code-style.playbook.md
│   └── testing-rules.playbook.md
├── agents/                           ← Agent-specific instructions
│   ├── worker.playbook.md
│   ├── architect.playbook.md
│   ├── critic.playbook.md
│   ├── scaffolder.playbook.md
│   ├── test-writer.playbook.md
│   ├── reviewer.playbook.md
│   ├── debug.playbook.md
│   ├── refactor.playbook.md
│   ├── security.playbook.md
│   ├── code-quality.playbook.md
│   ├── performance.playbook.md
│   ├── database.playbook.md
│   ├── monitoring.playbook.md
│   ├── dependency.playbook.md
│   ├── cleanup.playbook.md
│   ├── accessibility.playbook.md
│   ├── compliance.playbook.md
│   ├── migration.playbook.md
│   ├── api-design.playbook.md
│   ├── error-handling-agent.playbook.md
│   ├── type-safety.playbook.md
│   ├── git-release.playbook.md
│   ├── librarian.playbook.md
│   ├── prompt-engineer.playbook.md
│   ├── ui-preview.playbook.md
│   ├── discovery.playbook.md
│   ├── planner.playbook.md
│   ├── innovator.playbook.md
│   ├── research.playbook.md
│   ├── integration-tester.playbook.md
│   ├── doc-updater.playbook.md
│   └── retrospective.playbook.md
└── technologies/                     ← Language/framework-specific rules
    ├── python.playbook.md
    ├── typescript.playbook.md
    ├── dotnet.playbook.md
    └── go.playbook.md
```

All 32 agent stubs are listed above. Shared and technology playbooks cover the initial PLAYBOOK.md rules decomposed into semantic units.

---

## Module Breakdown

> **v2 change:** Reduced from 6 modules (4 layers) to 5 modules (3 layers). `similarity.py` merged into `knowledge_index.py` — its 2 functions (~20 lines) are now private helpers within the search module.

### Module 1: `src/utils/playbook_parser.py`

**Purpose:** Parse `.playbook.md` files with TOML frontmatter into structured chunk records.

**Public API:**

| Symbol | Type | Signature | Description |
| --- | --- | --- | --- |
| `parse_playbook_file` | function | `(file_path: str) -> dict` | Parse a single `.playbook.md` file. Returns dict with `id`, `title`, `agents`, `technologies`, `category`, `tags`, `content`, `source_file` |
| `discover_playbook_files` | function | `(base_dir: str) -> list[str]` | Recursively find all `*.playbook.md` files under `base_dir`. Returns sorted list of absolute paths |
| `parse_all_playbooks` | function | `(base_dir: str) -> list[dict]` | Discover + parse all playbook files. Validates uniqueness of `id` across all files — raises `ValueError` on collision. Returns list of chunk records. Raises on any parse errors |

**Internal helpers:**

- `_extract_frontmatter(raw_text: str) -> tuple[dict, str]` — split TOML frontmatter from markdown body using `+++` delimiters. Regex: `^\+\+\+\n(.*?)\n\+\+\+\n(.*)` (dotall). Parse the TOML block with `tomllib.loads()` (stdlib since Python 3.11)
- `_validate_frontmatter(meta: dict, file_path: str) -> None` — validate required fields, valid category, non-empty agents list. Raises `ValueError` with file path context
- `_validate_content(body: str, file_path: str) -> None` — validate that the markdown body is non-empty after stripping whitespace. Raises `ValueError` if the body is blank (frontmatter-only file would produce an empty embedding)
- `_validate_unique_ids(chunks: list[dict]) -> None` — check that all chunk `id` values are unique across parsed files. Raises `ValueError` listing the duplicate `id` and the conflicting source file paths
- `_compute_content_hash(content: str) -> str` — SHA-256 hex digest of the markdown body (stripped, normalized newlines)

**Dependencies:** `os`, `re`, `hashlib`, `tomllib` (stdlib since Python 3.11)

**Design notes:**

> **v2 change:** Replaced hand-rolled regex YAML parsing with `tomllib` (stdlib). The `+++` delimiters are split via a simple regex, then the extracted TOML string is parsed by `tomllib.loads()`. This is robust, spec-compliant, handles edge cases (multiline strings, special characters, quoting) correctly, and requires zero custom parsing logic. The fragile `_parse_simple_yaml()` helper is eliminated entirely.

- Content hash uses the body only (not frontmatter) — so metadata-only changes don't trigger re-embedding.
- `tomllib` is read-only (parse only, no write). This is exactly what we need — we never programmatically generate frontmatter, only read it.

---

### Module 2: `src/utils/embedding_client.py`

**Purpose:** Call the GitHub Models embedding API with batching and retry logic.

**Public API:**

| Symbol | Type | Signature | Description |
| --- | --- | --- | --- |
| `embed_texts` | function | `(texts: list[str], token: str) -> list[list[float]]` | Embed a list of texts. Handles batching internally (respects 64K token limit per request, 15 req/min rate limit). Returns list of 1536-dim vectors in same order as input |
| `embed_single` | function | `(text: str, token: str) -> list[float]` | Convenience wrapper — embed one text. Used by query script for the query string |

**Internal helpers:**

- `_estimate_tokens(text: str) -> int` — rough token estimate: `len(text) // 4` (standard heuristic for English text)
- `_create_batches(texts: list[str], max_tokens: int) -> list[list[tuple[int, str]]]` — group texts into batches that fit under `max_tokens` (default 54000 — leave 10K headroom below the 64K limit to absorb token estimation variance for code-heavy or non-English text). Each item is `(original_index, text)` to preserve ordering
- `_call_embedding_api(batch_texts: list[str], token: str) -> list[list[float]]` — single HTTP POST to `https://models.github.ai/inference/embeddings` with headers `Authorization: Bearer {token}`, `Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2022-11-28`. Body: `{"input": batch_texts, "model": "openai/text-embedding-3-small", "dimensions": 1536}`. Returns list of embedding vectors. On "too many tokens" error (HTTP 400 with token limit message), halves the batch and retries recursively
- `_retry_with_backoff(func, max_retries: int, base_delay: float) -> any` — retry on HTTP 429/5xx with exponential backoff. Default: 3 retries, 4s base delay (doubles each retry). Respects `Retry-After` header if present
- `_rate_limit_sleep(batch_index: int) -> None` — sleep 4 seconds between batches to stay under 15 req/min

**Dependencies:** `urllib.request`, `json`, `time`, `os`, `sys`

**Design notes:**

- Token is passed explicitly — never read from env inside this module. The CLI entry points read `GH_MODELS_TOKEN` from env and pass it in.
- Batching strategy: estimate tokens per chunk (~500 tokens for a typical playbook chunk), pack up to ~54K tokens per request (conservative 10K headroom). With ~50-80 chunks total, expect 1-2 API calls for a full build. If a batch exceeds the actual token limit, the API call handler halves the batch and retries.
- Incremental builds only embed changed chunks — usually 1-5 chunks, fitting in a single request.
- On HTTP 429, parse `Retry-After` header and sleep. On 5xx, exponential backoff.
- On HTTP 4xx (other than 429), fail immediately with a descriptive error — don't retry.

---

### Module 3: `src/utils/knowledge_index.py`

**Purpose:** Read, write, search, and diff the knowledge index JSON file.

**Public API:**

| Symbol | Type | Signature | Description |
| --- | --- | --- | --- |
| `load_index` | function | `(index_path: str) -> dict` | Load and validate the index JSON. Returns empty index structure if file doesn't exist |
| `save_index` | function | `(index: dict, index_path: str) -> None` | Atomically write the index JSON (write to `.tmp`, then rename). Updates `built_at` and `chunk_count` |
| `diff_chunks` | function | `(current_chunks: list[dict], existing_index: dict) -> tuple[list[dict], list[str]]` | Compare parsed chunks against existing index by `content_hash`. Returns `(chunks_to_embed, ids_to_remove)` — only chunks that are new or changed, plus IDs no longer present in source |
| `merge_embeddings` | function | `(existing_index: dict, new_chunks: list[dict], embeddings: list[list[float]], removed_ids: list[str]) -> dict` | Merge newly embedded chunks into the existing index. Remove stale IDs. Returns updated index dict |
| `search_chunks` | function | `(index: dict, query_embedding: list[float], agent: str or None, tech: str or None, top_k: int) -> list[dict]` | Filter chunks by agent/tech, rank by similarity, return top_k results with scores |

**Internal helpers:**

- `_empty_index() -> dict` — return a valid empty index structure with version, model, dimensions
- `_validate_index(index: dict) -> None` — check schema version, required keys. Raise `ValueError` if invalid or version mismatch (forces rebuild)
- `_filter_chunks(chunks: list[dict], agent: str or None, tech: str or None) -> list[dict]` — filter by agent name (match if chunk's `agents` contains agent name or `"all"`) and technology (match if chunk's `technologies` contains tech or is empty list)
- `_atomic_write(data: str, path: str) -> None` — write to `{path}.tmp`, then `os.replace()` to atomically swap

**Internal helpers (similarity — merged from former `similarity.py`):**

- `_dot_product(vec_a: list[float], vec_b: list[float]) -> float` — compute dot product of two equal-length vectors. OpenAI embeddings are pre-normalized, so dot product = cosine similarity. Uses `sum()` + `zip()` — no numpy needed
- `_rank_by_similarity(query_vec: list[float], candidates: list[dict], top_k: int) -> list[dict]` — sort candidates by `_dot_product` similarity, return top_k. Each candidate dict must have an `"embedding"` key. Returns candidates enriched with a `"score"` key

> **v2 change:** These two functions (~20 lines total) were previously in a standalone `similarity.py` module. They are pure implementation details of `search_chunks` and don't warrant their own file. Now private helpers prefixed with `_`.

**Dependencies:** `json`, `os`, `datetime` (for `built_at`)

**Design notes:**

- `diff_chunks` enables incremental builds: only re-embed what changed. The `content_hash` in each chunk record is compared against the stored hash. If hash matches, skip embedding — reuse the existing vector.
- `merge_embeddings` preserves existing embeddings for unchanged chunks, adds new ones, removes deleted IDs.
- `_atomic_write` uses `os.replace()` which is atomic on both Unix and Windows (NTFS). This prevents index corruption if the process is killed mid-write.
- `search_chunks` composes filtering → `_rank_by_similarity`. All similarity math is internal to this module.
- Agent/tech filter is applied **before** similarity ranking to reduce the candidate set.

---

### Module 4: `scripts/build-knowledge-index.py`

**Purpose:** CLI entry point for CI. Parses all playbooks, computes incremental diff, embeds new/changed chunks, writes updated index.

**Public API (CLI):**

```text
Usage: python3 scripts/build-knowledge-index.py [OPTIONS]

Options:
  --playbooks-dir PATH   Base directory for playbook files (default: docs/playbooks)
  --index-path PATH      Output index file path (default: .ai/knowledge-index.json)
  --full-rebuild         Force re-embedding all chunks (ignore content hashes)
  --dry-run              Parse and diff only — don't call API or write index
  --verbose              Print detailed progress

Environment:
  GH_MODELS_TOKEN        Required. GitHub Models API token for embeddings
```

**Internal structure (functions):**

| Function | Signature | Description |
| --- | --- | --- |
| `main` | `() -> None` | Parse args, orchestrate the build pipeline, exit with appropriate code |
| `parse_args` | `() -> argparse.Namespace` | Define and parse CLI arguments |
| `validate_environment` | `(args: Namespace) -> str` | Check `GH_MODELS_TOKEN` is set, playbooks dir exists. Returns token. Exits with error if validation fails |
| `run_build` | `(args: Namespace, token: str) -> None` | Core pipeline: discover → parse → diff → embed → merge → save. Prints summary |
| `print_summary` | `(total: int, embedded: int, removed: int, skipped: int) -> None` | Print build statistics |

**Dependencies:** `argparse`, `sys`, `os`, `playbook_parser`, `embedding_client`, `knowledge_index`

**Design notes:**

- `sys.path` manipulation at top to import from `src/utils/` — uses `pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"` to compute the path relative to the script file, not the CWD. This ensures correct imports regardless of the working directory
- Exit code 0 on success, 1 on error
- `--dry-run` is valuable for CI validation without consuming API quota
- `--full-rebuild` ignores content hashes — used when model version changes or index schema changes

---

### Module 5: `scripts/query-knowledge-index.py`

**Purpose:** CLI entry point for Librarian agent. Loads index, embeds query, filters, ranks, outputs markdown.

**Public API (CLI):**

```text
Usage: python3 scripts/query-knowledge-index.py [OPTIONS]

Options:
  --query TEXT           Required. The search query
  --agent NAME           Filter to chunks relevant to this agent (e.g. "worker")
  --tech NAME            Filter to chunks for this technology (e.g. "python")
  --top-k INT            Number of results to return (default: 10)
  --index-path PATH      Index file path (default: .ai/knowledge-index.json)
  --format TEXT          Output format: "markdown" (default) or "json"

Environment:
  GH_MODELS_TOKEN        Optional. GitHub Models API token for embedding the query.
                         If unset, falls back to metadata-only retrieval.
```

**Internal structure (functions):**

| Function | Signature | Description |
| --- | --- | --- |
| `main` | `() -> None` | Parse args, run query, output results |
| `parse_args` | `() -> argparse.Namespace` | Define and parse CLI arguments |
| `run_query` | `(args: Namespace, token: str or None) -> list[dict]` | Attempt embedding-based search (load index → embed query → search). On any failure, call `fallback_metadata_retrieval`. Token may be `None` (triggers immediate fallback) |
| `format_results_markdown` | `(results: list[dict]) -> str` | Format results as markdown with title, score, source, and content for each chunk |
| `format_results_json` | `(results: list[dict]) -> str` | Format results as JSON array |
| `fallback_metadata_retrieval` | `(playbooks_dir: str, agent: str or None, tech: str or None) -> list[dict]` | Graceful degradation: discover and parse all playbook files, filter by agent/tech metadata, return matching chunks (unranked). Prints fallback warning to stderr |

**Dependencies:** `argparse`, `sys`, `os`, `json`, `playbook_parser`, `embedding_client`, `knowledge_index`

**Design notes:**

- `sys.path` manipulation at top uses `pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"` — same approach as the build script, ensuring correct imports regardless of CWD.
- Output goes to stdout (for piping/capture by the Librarian). Diagnostics go to stderr.
- If the index file is missing, token is unavailable, or the embedding API fails, fall back to `fallback_metadata_retrieval` — parse all playbook files from disk, filter by agent/tech metadata, and return matching chunks unranked. The Librarian always gets results.
- `--format json` is useful for programmatic consumption; `--format markdown` is the default for Librarian context briefs.
- The query string is embedded via `embed_single()` — exactly one API call per query.

---

### Graceful Degradation: Metadata-Only Fallback

> **v3 update:** When the knowledge index is missing (first clone, deleted, corrupted) or the embedding API is unreachable (no token, rate limited, offline), the query script falls back to **metadata-only retrieval** via `fallback_metadata_retrieval`:
>
> 1. Read all `.playbook.md` files directly from `docs/playbooks/`
> 2. Parse TOML frontmatter (no API call needed)
> 3. Filter by `agents` and `technologies` metadata
> 4. Return all matching chunks (unranked, or sorted by tag overlap with query keywords)
> 5. Print a warning to stderr: `"⚠️ Knowledge index unavailable — falling back to metadata-only retrieval"`
>
> This ensures the Librarian **always** returns playbook knowledge, even without embeddings. The embedding-based path is the primary and preferred approach (per user's explicit choice of Option C), but the system never hard-fails on API unavailability.
>
> **Implementation:** `fallback_metadata_retrieval` in the query script imports `playbook_parser` to discover and parse playbook files, filters by agent/tech metadata, and returns their content as results.

#### Consolidated Fallback Trigger List (C5)

The query script uses a **try/except** structure: attempt embedding-based search → on any failure → fall back to metadata-only → on metadata failure → return empty results. The following conditions trigger `fallback_metadata_retrieval`:

| # | Trigger Condition | Detection Point |
| --- | --- | --- |
| F1 | `GH_MODELS_TOKEN` not set | `main()` — `os.environ.get()` returns `None` |
| F2 | Index file does not exist | `load_index()` — `FileNotFoundError` |
| F3 | Index file is corrupted (invalid JSON) | `load_index()` — `json.JSONDecodeError` |
| F4 | Index schema version mismatch | `_validate_index()` — `ValueError` |
| F5 | Embedding API call fails after retries | `embed_single()` — any exception after max retries |
| F6 | Embedding API returns invalid response | `embed_single()` — `KeyError` / unexpected response shape |

If `fallback_metadata_retrieval` itself fails (e.g., `docs/playbooks/` directory missing), the query script outputs empty results to stdout and logs the error to stderr. This is the **last resort** — the Librarian continues with its other documentation-search stages.

---

## GitHub Actions Workflow

**File:** `.github/workflows/build-knowledge-index.yml`

```yaml
name: Build Knowledge Index

on:
  push:
    paths:
      - 'docs/playbooks/**'
    branches:
      - main
  workflow_dispatch:

concurrency:
  group: knowledge-index
  cancel-in-progress: true

jobs:
  build-index:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Build knowledge index
        env:
          GH_MODELS_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
        run: python3 scripts/build-knowledge-index.py --verbose

      - name: Commit updated index
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .ai/knowledge-index.json
          git diff --cached --quiet || git commit -m "chore: rebuild knowledge index"
          git pull --rebase || true
          git push
```

**Design notes:**

- Triggers only on changes to `docs/playbooks/` on `main` — avoids unnecessary builds.
- `workflow_dispatch` allows manual trigger for full rebuilds.
- `concurrency` group prevents race conditions if multiple playbook changes are pushed rapidly.
- Commits the updated index back to the repo — keeps it in git as specified.
- Uses `git diff --cached --quiet` to skip commit if nothing changed (incremental build found no changes).

---

## Librarian Agent Updates

The Librarian's query workflow gains a new **two-stage retrieval**:

### Updated Query Workflow

```text
Stage 1: RAG Retrieval (NEW)
  ├── Determine agent type and technology from the query
  ├── Shell out: python3 scripts/query-knowledge-index.py \
  │     --query "{parsed query}" --agent {agent} --tech {tech} --top-k 10
  └── Capture stdout → RAG chunks (ranked playbook knowledge)

Stage 2: Documentation Search (EXISTING — unchanged)
  ├── Search docs/CODE_INVENTORY.md
  ├── Search docs/files/
  ├── Search docs/BUSINESS_LOGIC.md
  └── Search docs/API_DOCUMENTATION.md

Stage 3: Assemble Context Brief
  ├── Merge RAG chunks into a "### Relevant Playbook Rules" section
  ├── Merge documentation search results (existing sections)
  └── Return combined brief to Orchestrator
```

### New Section in Librarian's Context Brief Format

```markdown
### Relevant Playbook Rules (RAG)

<!-- Top-K chunks from the knowledge index, ranked by relevance -->

**[Score: 0.89]** Anti-Duplication Rules (`shared/anti-duplication`)
> Before creating anything new:
> 1. Search CODE_INVENTORY.md for similar functionality...

**[Score: 0.85]** Python Testing Conventions (`technologies/python`)
> Use pytest. Minimum 15 tests per function...
```

### Graceful Degradation

If the query script fails or the index is missing, the Librarian continues with Stage 2 only (existing behavior). The RAG stage is additive — never blocking.

---

## Error Handling Strategy

### By Component

| Component | Error Scenario | Handling |
| --- | --- | --- |
| `playbook_parser` | Malformed TOML frontmatter | Raise `ValueError` wrapping `tomllib.TOMLDecodeError` with file path context. Build script fails loudly — malformed playbooks must be fixed |
| `playbook_parser` | Missing `+++` delimiters | Raise `ValueError` — file is not a valid playbook chunk. Include file path |
| `playbook_parser` | Missing required frontmatter field | Raise `ValueError` naming the missing field and file. Fail the build |
| `playbook_parser` | No `.playbook.md` files found | Return empty list. Build script prints warning, writes empty index |
| `embedding_client` | HTTP 429 (rate limited) | Parse `Retry-After` header, sleep, retry. Max 3 retries |
| `embedding_client` | HTTP 5xx (server error) | Exponential backoff: 4s, 8s, 16s. Max 3 retries |
| `embedding_client` | HTTP 4xx (client error, not 429) | Fail immediately with status code and response body. Likely auth or payload issue |
| `embedding_client` | Network error / timeout | Retry with backoff (same as 5xx). `urllib` default timeout overridden to 30s |
| `embedding_client` | `GH_MODELS_TOKEN` invalid | API returns 401. Fail with clear message: "Invalid GH_MODELS_TOKEN" |
| `knowledge_index` | Index file missing (query time) | Trigger metadata-only fallback. Print warning to stderr |
| `knowledge_index` | Index file corrupted JSON | Trigger metadata-only fallback at query time. Build script does full rebuild |
| `knowledge_index` | Index schema version mismatch | Trigger metadata-only fallback at query time. Build script triggers full rebuild |
| `knowledge_index` | Atomic write fails | `.tmp` file remains, original index unchanged. Build fails with error. Next run retries |
| `build-knowledge-index.py` | `GH_MODELS_TOKEN` not set | Exit with code 1 and message: "Error: GH_MODELS_TOKEN environment variable is required" |
| `build-knowledge-index.py` | Playbooks dir doesn't exist | Exit with code 1 and message naming the missing directory |
| `query-knowledge-index.py` | `GH_MODELS_TOKEN` not set | Fall back to `fallback_metadata_retrieval`. Print warning to stderr: "GH_MODELS_TOKEN not set — using metadata-only retrieval". Return metadata-filtered results to stdout |
| `query-knowledge-index.py` | Embedding API fails | Print error to stderr. Fall back to `fallback_metadata_retrieval`. Return metadata-filtered results to stdout |

### Error Propagation Pattern

```text
Utility functions → raise exceptions with context (file path, HTTP status, etc.)
Build script   → catch at top level, print to stderr, exit with code 1
Query script   → cascading fallback:
                   1. Try embedding-based search (primary path)
                   2. On any failure → fallback_metadata_retrieval (parse files, filter by metadata)
                   3. On metadata failure → output empty results to stdout, log error to stderr
                   Never exit with code 1. Always return valid output to stdout.
```

**Principle:** Build-time errors are **loud** (fail CI). Query-time errors are **silent** (don't break the Librarian — degrade gracefully through the cascading fallback chain).

---

## Optimization Notes

### Incremental Builds (Critical for Rate Limits)

- Each chunk stores a `content_hash` (SHA-256 of markdown body)
- On rebuild, compare hashes against existing index
- Only embed chunks with new/changed hashes
- With 150 req/day free tier, this is essential — a full rebuild of ~50 chunks uses ~1 request, but we should still be incremental by default

### Token Budget Optimization

- Typical playbook chunk: 200-800 tokens (~800-3200 chars)
- At 60K tokens per batch (conservative vs 64K limit): ~75-300 chunks per batch
- Expected total chunks: ~50-80 → fits in a single API request
- For query time: single text → single API call, minimal latency

### Query-Time Performance

- Index is loaded from disk (JSON parse) — for ~80 chunks with 1536-dim vectors, the file is ~1-2MB. Parse time: <100ms
- Dot product of 1536 floats in pure Python: ~0.5ms per chunk. 80 chunks: ~40ms
- Total query time dominated by the embedding API call (~200-500ms)
- No optimization needed at this scale (sub-second total)

### Memory Considerations

- 80 chunks × 1536 floats × 8 bytes = ~1MB in memory. Negligible
- JSON file with embeddings: ~1-2MB on disk. Committed to git for immediate availability; marked `linguist-generated` in `.gitattributes` to suppress diffs in merge requests

### Future Scale Considerations (documented but NOT implemented)

- If chunks exceed ~500: consider binary index format (msgpack or custom) instead of JSON
- If query latency matters: pre-compute filtered sub-indices per agent
- If rate limits are hit frequently: cache embeddings locally per-query with TTL
- None of these are needed now. Current scale (~80 chunks) is well within bounds

---

## Critique Log

| Round | Issues Raised | Resolution |
| --- | --- | --- |
| 1 | C1: `handle_missing_index` contradictory behavior; C2: Missing token crashes instead of degrading; C3: No test files; C4: No duplicate id detection; C5: Fallback triggers not consolidated; C6: sys.path fragile; C7: Token overflow risk; C8: CI push race; C9: Empty body not validated | **All fixed in v3.** C1: Renamed to `fallback_metadata_retrieval` with correct signature/deps/behavior. C2: Query script now degrades to metadata-only when token missing (never exits 1). C3: Added test file decomposition section with 3 test files. C4: Added `_validate_unique_ids` to parser. C5: Added consolidated fallback trigger table (F1-F6). C6: Specified `pathlib.Path(__file__).resolve()` approach for both scripts. C7: Increased headroom to 10K + batch-halving on overflow. C8: Added `git pull --rebase` before push. C9: Added `_validate_content` for empty body detection. |
| 2 | All 9 Round 1 issues verified resolved. No new critical or important issues. Two carried-over minor notes (M1, M2) and one new minor note (M3). | **APPROVED.** See Round 2 Critique below. |

---

### Round 1 Critique

**Reviewed by:** Critic Agent
**Date:** 2026-03-11

---

#### Innovator Log Check

- ✅ **Pass.** The Innovator provided 7 assumption challenges and 5 alternatives. The Architect responded to every one with clear decisions and rationale in the **Architect Response** section. Several ideas were adopted (TOML frontmatter, similarity merge, graceful degradation, git bloat mitigation). Rejected ideas have well-justified reasoning. No dismissiveness detected.

---

#### Duplication Check — ✅ Pass

- CODE_INVENTORY is empty — greenfield project, no existing symbols to collide with.
- Plan correctly identifies `GH_MODELS_TOKEN` as the only shared asset (reused from feedback pipeline).
- All 5 modules and 2 scripts are net-new with no overlap.
- No duplicated logic between modules — `playbook_parser` handles parsing, `embedding_client` handles API, `knowledge_index` handles index CRUD + search.
- No issues found.

---

#### Decomposition Check — ⚠️ Minor

1. **`knowledge_index.py` function count after similarity merge.** The module now has 5 public functions + 6 private helpers = 11 functions total. At ~15-25 lines each, this could reach 165-275 lines, approaching or exceeding the PLAYBOOK's 200-line decomposition threshold. The Architect's rationale for keeping `embedding_client.py` separate ("would push past 200 lines") applies equally here. **Verdict:** Acknowledge the size risk in the plan. If the module exceeds 200 lines during implementation, pre-plan the seam along which to split (e.g., index I/O vs. search logic).

2. **Dependency order is correct.** Layer 1 → Layer 2 → Layer 3 with no cycles. Shared utilities (parser, client) are built before the composite module (knowledge_index), which is built before the CLI scripts. Clean.

3. **No missing extractions detected.** The `_atomic_write` helper is correctly scoped to `knowledge_index.py` since only that module writes JSON.

---

#### Over-Engineering Check — ⚠️ Minor

1. **`--format json` in query script:** No concrete consumer is identified. The Librarian uses markdown format. JSON output is a speculative feature with no stated requirement. **Suggest:** Remove from v1 scope or document which consumer needs it. Adding it later is trivial.

2. **`chunk_count` field in JSON schema:** The plan itself calls it "redundant count for quick validation without iterating." A simple `len(index["chunks"])` achieves the same. This isn't harmful but adds a field that can go stale if manually edited. **Suggest:** Keep (it's cheap), but don't over-invest in validating it — treat it as advisory.

3. **Overall complexity is justified.** The user explicitly chose Option C (live embeddings), so the embedding pipeline is not over-engineering — it's a stated requirement. The graceful degradation adds complexity but provides genuine resilience.

---

#### Completeness Check — ❌ Fail (3 issues must be fixed)

**Issue C1 — CRITICAL: `handle_missing_index` is contradictory.**

Module 5 defines `handle_missing_index` as: *"print warning to stderr, output empty results to stdout."*

The Graceful Degradation section says: *"`handle_missing_index` in the query script is extended to do metadata-only retrieval instead of just returning empty results."*

These are mutually exclusive behaviors. The Module 5 function table must be updated to match the degradation specification. Specifically:

- Rename to `fallback_metadata_retrieval` (or similar) to reflect its actual behavior.
- Update the signature: it needs `playbooks_dir` and the filter args (`agent`, `tech`), not just `index_path` and `query`.
- Import `playbook_parser` in the query script (currently not listed as a dependency of Module 5).
- Document the output: unranked matching chunks formatted as markdown.

**Issue C2 — CRITICAL: Missing token should trigger fallback, not exit code 1.**

The Error Handling table states:

> `query-knowledge-index.py` | `GH_MODELS_TOKEN` not set | Exit with code 1 and message to stderr. Empty results to stdout

This directly contradicts the graceful degradation promise. If the token is unavailable, the query script should fall through to metadata-only retrieval — not crash. The build script should correctly exit with code 1 (it can't embed without a token), but the query script must degrade gracefully. Fix the error handling table to specify:

> `query-knowledge-index.py` | `GH_MODELS_TOKEN` not set | Fall back to metadata-only retrieval. Print warning to stderr. Return metadata-filtered results to stdout.

**Issue C3 — CRITICAL: No test files in the decomposition.**

The PLAYBOOK mandates "test files planned to mirror `src/` in `tests/`." The plan lists no test files. At minimum, the decomposition should include:

- `tests/utils/test_playbook_parser.py`
- `tests/utils/test_embedding_client.py`
- `tests/utils/test_knowledge_index.py`

Even if the Test Writer agent will generate the tests later, the plan's decomposition section should show where they go and what they cover. This is a structural planning gap.

**Issue C4 — IMPORTANT: No duplicate `id` validation across playbook files.**

The plan enforces that `id` must match the file path pattern, but does not detect or handle the case where two different files produce the same `id`. `parse_all_playbooks` should validate uniqueness and raise `ValueError` on collision. Without this, the index will silently overwrite one chunk with another.

**Issue C5 — IMPORTANT: Metadata-only fallback triggers not fully enumerated.**

The fallback should trigger on any of these conditions:

1. Index file missing
2. Index file corrupted (invalid JSON)
3. Index schema version mismatch
4. `GH_MODELS_TOKEN` not set (can't embed query)
5. Embedding API call fails after retries

The plan partially addresses these in the error handling table but doesn't consolidate them into a single fallback trigger list. The query script design should have a clear try/except structure: attempt embedding-based search → on any failure → fall back to metadata-only → on metadata failure → return empty results.

**Issue C6 — IMPORTANT: `sys.path` manipulation is fragile.**

The plan says "sys.path manipulation at top to import from `src/utils/`" but doesn't specify how. If the scripts use `sys.path.insert(0, "../src/utils")`, they break when run from a different working directory. **Specify:** use `pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"` to compute the path relative to the script file, not the CWD.

**Issue C7 — MINOR: Token estimation `len/4` has no overflow guard.**

`_estimate_tokens` uses `len(text) // 4`. For code-heavy chunks or non-English text, actual tokens can be 2-3x more. If a batch is packed to 60K estimated tokens but the real count exceeds 64K, the API call fails. **Suggest:** Add a try/except around the API call in `_call_embedding_api` that, on a "too many tokens" error, halves the batch size and retries. Or reduce the headroom from 4K to 10K (use 54K limit instead of 60K).

**Issue C8 — MINOR: CI workflow push race condition.**

If another commit arrives between `actions/checkout` and `git push`, the push will fail. The workflow should either:

- Use `git pull --rebase` before push, or
- Retry the push once

This is low probability but worth noting for robustness.

**Issue C9 — MINOR: Empty chunk body not validated.**

No validation ensures a playbook chunk's markdown body is non-empty. A file with only frontmatter and no body would produce an empty `content` field and an embedding of an empty string. `_validate_frontmatter` (or a new `_validate_content`) should check for minimum content length.

---

#### Structure Check — ⚠️ Minor

1. **Test files not planned.** See Issue C3 above. ❌

2. **All 3 modules in `src/utils/`.** `embedding_client.py` is an HTTP client (service concern) and `knowledge_index.py` manages state (service/data concern). Both could arguably belong in `src/services/`. However, with no existing `src/services/` directory and no precedent set, keeping everything in `src/utils/` is pragmatic for a greenfield project. **Verdict:** Acceptable for v1. If `src/` grows significantly, consider migrating the stateful modules to `src/services/`.

3. **`docs/playbooks/` directory is new.** The PLAYBOOK rules say "No new top-level dirs without updating README." `docs/playbooks/` is a subdirectory of existing `docs/`, so this is fine — but the README should still be updated to mention the playbooks system.

4. **Naming is consistent.** `snake_case` throughout, `*.playbook.md` suffix is descriptive, CLI scripts use `kebab-case` (matching existing `scripts/` patterns).

---

#### Optimization Check — ✅ Pass

1. **Incremental builds** — well-designed with `content_hash` diffing. Essential for rate limits.
2. **Pre-filtering before similarity ranking** — correct approach, reduces candidate set before expensive computation.
3. **Index size analysis** (~1-2MB, <100ms parse) — reasonable at current scale.
4. **Single API call per query** — good, minimizes latency.
5. **No premature optimization needed** — the plan correctly identifies future scale considerations without implementing them.
6. **Token estimation risk** — noted in C7 but not a blocking optimization issue.

---

### Overall Verdict: REVISE

**Three critical issues must be addressed before approval:**

| # | Issue | Severity | Fix Required |
| --- | --- | --- | --- |
| C1 | `handle_missing_index` contradicts graceful degradation spec | ❌ Critical | Reconcile Module 5 function with degradation section. Update signature, dependencies, behavior. |
| C2 | Missing token exits with code 1 instead of degrading gracefully | ❌ Critical | Update error handling table: query script degrades to metadata-only when token is missing. |
| C3 | No test files in decomposition | ❌ Critical | Add test file listing to decomposition. Minimum: 3 test files mirroring `src/utils/`. |

**Important issues that should be fixed:**

| # | Issue | Severity | Suggested Fix |
| --- | --- | --- | --- |
| C4 | No duplicate `id` detection | ⚠️ Important | Add uniqueness check to `parse_all_playbooks`. |
| C5 | Fallback triggers not consolidated | ⚠️ Important | Add explicit fallback trigger list to query script design. |
| C6 | `sys.path` manipulation unspecified | ⚠️ Important | Specify `pathlib.Path(__file__).resolve()` approach. |

**Minor issues (non-blocking, fix if convenient):**

| # | Issue | Severity | Note |
| --- | --- | --- | --- |
| C7 | Token estimation overflow risk | Minor | Add overflow guard or increase headroom. |
| C8 | CI push race condition | Minor | Add rebase-before-push or retry. |
| C9 | Empty chunk body not validated | Minor | Add minimum content length check. |
| OE1 | `--format json` has no stated consumer | Minor | Consider deferring to v2. |
| D1 | `knowledge_index.py` may exceed 200 lines | Minor | Acknowledge and pre-plan split seam. |

---

### Round 2 Critique

**Reviewed by:** Critic Agent
**Date:** 2026-03-11

---

#### Round 1 Issue Verification

All 9 issues from Round 1 have been verified as resolved:

| # | Issue | Status | Verification |
| --- | --- | --- | --- |
| C1 | `handle_missing_index` contradicts graceful degradation | ✅ Resolved | Renamed to `fallback_metadata_retrieval` with correct signature `(playbooks_dir, agent, tech) -> list[dict]`. Module 5 dependency list now includes `playbook_parser`. Behavior matches the degradation section exactly. |
| C2 | Missing token exits with code 1 | ✅ Resolved | `GH_MODELS_TOKEN` is now marked "Optional" in CLI docs. `run_query` accepts `token: str or None`. Error handling table corrected: query script degrades to metadata-only. Fallback trigger F1 explicitly covers this case. |
| C3 | No test files in decomposition | ✅ Resolved | Test File Decomposition section added with 3 test files in `tests/utils/` mirroring `src/utils/`. Coverage areas documented per file. Note correctly defers individual test case design to the Test Writer agent. |
| C4 | No duplicate `id` detection | ✅ Resolved | `_validate_unique_ids` added as internal helper to `playbook_parser.py`. `parse_all_playbooks` docstring confirms it raises `ValueError` on collision with conflicting file paths. |
| C5 | Fallback triggers not consolidated | ✅ Resolved | Consolidated Fallback Trigger List (F1-F6) added with detection point for each trigger. Try/except cascade structure clearly documented: embedding → metadata-only → empty results. |
| C6 | `sys.path` fragility | ✅ Resolved | Both Module 4 and Module 5 design notes now specify `pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"`. Path is relative to script file, not CWD. |
| C7 | Token overflow risk | ✅ Resolved | Headroom increased from 4K to 10K (54K limit). `_call_embedding_api` now halves the batch and retries recursively on "too many tokens" errors. |
| C8 | CI push race condition | ✅ Resolved | Workflow now includes `git pull --rebase \|\| true` before `git push`. |
| C9 | Empty body not validated | ✅ Resolved | `_validate_content` added to `playbook_parser.py`. Validates non-empty body after stripping whitespace. Raises `ValueError` for frontmatter-only files. |

---

#### Duplication Check — ✅ Pass

- CODE_INVENTORY remains empty — still a greenfield project.
- No new duplications introduced by the fixes.
- `fallback_metadata_retrieval` correctly reuses `playbook_parser` rather than reimplementing parsing logic — good.
- All 5 modules remain net-new with no inter-module overlap.

---

#### Decomposition Check — ✅ Pass (with carried-over note)

- 3 layers, 5 modules, correct bottom-up build order. No cycles.
- `query-knowledge-index.py` now depends on `playbook_parser` (for fallback) — this is correct (Layer 3 uses Layer 1).
- `knowledge_index.py` now has 5 public + 6 private helpers = 11 functions total. This was flagged in Round 1 as a size risk (~200 lines). The plan acknowledged it but didn't pre-plan a split seam. **Carried forward as M1** (see below) — non-blocking.
- No new decomposition issues introduced by the fixes.

---

#### Over-Engineering Check — ✅ Pass (with carried-over note)

- `_validate_unique_ids` — simple uniqueness check, appropriately scoped. Not over-engineered.
- `_validate_content` — simple empty-body check, appropriately scoped. Not over-engineered.
- Batch-halving retry — standard pattern for token estimation errors. Not over-engineered.
- Fallback trigger table (F1-F6) — documents existing behavior, doesn't add code complexity.
- `--format json` still has no stated consumer. **Carried forward as M2** (see below) — non-blocking.

---

#### Completeness Check — ✅ Pass

- All 3 former critical issues fully resolved.
- Edge cases now comprehensively covered: empty body, duplicate IDs, missing token, corrupted index, schema mismatch, API failures, batch overflow.
- Fallback chain is well-defined and exhaustive: embedding search → metadata-only → empty results.
- Error handling table is internally consistent — build script fails loudly, query script degrades gracefully. No more contradictions.
- `pathlib` is used in both scripts' `sys.path` setup but not listed in their Dependencies sections. **Noted as M3** (see below) — non-blocking since it's stdlib and usage is clearly documented in design notes.

---

#### Structure Check — ✅ Pass

- Test files properly mirror `src/utils/` in `tests/utils/`. 3 test files for 3 source modules.
- All modules in correct directories per project structure rules.
- Naming remains consistent throughout.
- No structural issues introduced by the fixes.

---

#### Optimization Check — ✅ Pass

- Batch-halving retry is a sensible fallback for token estimation errors — handles the edge case without premature optimization.
- 10K headroom (54K limit) is conservative but reasonable given that code-heavy chunks can have higher token-to-character ratios.
- No new optimization concerns.

---

#### Minor Notes (non-blocking, for Worker awareness)

| # | Note | Severity | Recommendation |
| --- | --- | --- | --- |
| M1 | `knowledge_index.py` has 11 functions — may approach 200-line decomposition threshold | Minor (carried from R1) | Workers should monitor during implementation. If it exceeds 200 lines, split along the index I/O vs. search seam. |
| M2 | `--format json` in query script has no stated consumer | Minor (carried from R1) | Consider deferring to v2, or document which consumer needs it. Trivial to add later. |
| M3 | `pathlib` not listed in Dependencies for Modules 4 and 5 | Minor (new) | Add `pathlib` to both scripts' dependency lists for completeness. |

---

### Overall Verdict: APPROVED

All 3 critical issues, 3 important issues, and 3 minor issues from Round 1 are fully resolved. The fixes are clean and proportionate — no over-engineering or unnecessary complexity was introduced. The plan is internally consistent: the graceful degradation design, error handling table, module APIs, and fallback trigger list all align.

Three minor non-blocking notes (M1-M3) are carried forward for Worker awareness during implementation. None affect the architecture.

**The plan is ready for function-level breakdown by the Planning Agent.**

---

## Innovator Log

**Reviewed by:** Innovator Agent
**Date:** 2026-03-11

---

### Assumptions Challenged

| # | Assumption in Current Plan | Challenge | Lens Used |
| --- | --- | --- | --- |
| 1 | **Semantic embeddings are necessary** for retrieval over ~80 playbook chunks | At ~80 chunks, metadata filtering (agent + tech) reduces candidates to ~5-15. That's small enough to include inline or rank via keyword matching — no embedding API needed at this scale. Embeddings solve a scale problem we don't have. | Simplification, Elimination |
| 2 | **Stdlib-only YAML parsing via regex is acceptable** because the schema is flat | Regex YAML parsing is a known source of subtle bugs (multiline strings, special characters, quoting). Python 3.11+ includes `tomllib` in stdlib — a full-featured, battle-tested parser. Switching to TOML frontmatter eliminates fragility while staying stdlib-only. | Analogy (frontmatter in other ecosystems), Inversion |
| 3 | **6 modules across 4 layers is appropriate** for this scope | The entire system has 2 use cases: build an index and query it. 6 modules + 4 layers + `sys.path` manipulation for a ~80-chunk system is over-engineered. The decomposition rules in PLAYBOOK say "one responsibility per file" — but also "files > ~200 lines → decompose," implying small files shouldn't be split further. A 2-function `similarity.py` is a file that shouldn't exist yet. | Simplification, Elimination |
| 4 | **One file per chunk** is the right granularity | ~45 separate tiny files creates directory sprawl. Related rules (e.g., all "shared" patterns) lose context when split into individual files. The original spec proposed multi-chunk files with `<!-- chunk -->` separators — the Architect overrode this without strong justification. | User-first, Combination |
| 5 | **Committing a 1-2MB JSON file with float arrays to git** is fine | Embedding vectors change format on every rebuild (float precision). Git stores full snapshots of text, so every rebuild creates a ~1-2MB diff. Over 100 rebuilds = ~100-200MB of git bloat with no meaningful diffability. The index is a build artifact, not source. | Future-back |
| 6 | **Shelling out to Python** is the right Librarian interface | The Librarian agent already has file-read tools. If retrieval were metadata-based, the Librarian could read playbook files directly with its existing tools — no subprocess, no Python runtime dependency, no token requirement for queries. | Elimination, User-first |
| 7 | **Rate limits (15 req/min, 150/day) are manageable** | The plan hand-waves this with "usually fits in 1-2 requests." But a full rebuild of the template for a new user consumes quota. If the index is corrupted or deleted, rebuilding costs API calls. Are we over-depending on an external API for what could be a local-only operation? | Future-back, Inversion |

---

### Alternative Approaches

#### Alternative 1: "Direct File Retrieval" — No Embeddings, No Index

**Core insight:** At ~80 chunks, metadata filtering alone reduces candidates to ~5-15 files. That's small enough to read and include directly. Embeddings solve a scale problem that doesn't exist here.

**How it works:**

- Keep the playbook chunk format (`.playbook.md` files with YAML/TOML frontmatter).
- The Librarian's query script reads all playbook files, parses frontmatter, filters by `agents` and `technologies` metadata. No embedding, no vector math.
- Matched chunks (~5-15 per query) are concatenated and returned as the context brief. At ~500 words per chunk, that's 2,500-7,500 words — well within any LLM context window.
- Optional: add basic TF-IDF keyword scoring using stdlib (`collections.Counter`) to rank the filtered set, pushing the most relevant chunks to the top.
- No JSON index file. No GitHub Models API dependency at query time. No `GH_MODELS_TOKEN` needed for the Librarian.

**Pros:**

- Eliminates 3 of 6 modules (`similarity.py`, `embedding_client.py`, `knowledge_index.py`)
- Zero external API dependency — works offline, no rate limits, no cost
- No index file to commit, no git bloat, no CI workflow needed
- Dramatically simpler: ~200 lines total vs. ~600+
- The Librarian could do this with its existing file-read tools — no Python subprocess needed
- Instant queries (filesystem read only, no HTTP round-trip)

**Cons:**

- No semantic matching — "don't repeat yourself" won't match a query for "duplication rules" unless tags cover it
- Requires good tag discipline from playbook authors
- Won't scale past ~200-300 chunks (but we have ~80)
- Less "impressive" as a RAG demo

**Feasibility:** **High** — this is dramatically simpler and works at current scale.

---

#### Alternative 2: "TOML + Consolidated Modules" — Fix the Fragility, Halve the Files

**Core insight:** Keep embeddings (for semantic quality), but fix the two weakest parts of the plan: regex YAML parsing and over-decomposed modules.

**How it works:**

- Replace YAML frontmatter with TOML frontmatter (`+++` delimiters). Use `tomllib` (stdlib since Python 3.11). Zero parsing fragility.
- Consolidate 6 modules into 3: (1) `src/utils/playbook_parser.py` (unchanged), (2) `src/utils/knowledge_base.py` (merges `similarity.py`, `embedding_client.py`, and `knowledge_index.py` — all deal with the same data structure), (3) two CLI scripts (unchanged, but simpler imports).
- `dot_product` and `rank_by_similarity` become private functions inside `knowledge_base.py` — they're implementation details of search, not a public API.
- `embed_texts` and `embed_single` become private functions inside `knowledge_base.py` — they're called only by build/search within the same module.

**Pros:**

- TOML parsing is bulletproof — no regex edge cases, no "minimal YAML parser"
- 3 modules instead of 6 — simpler dependency graph, no `sys.path` hacks for 4 separate layers
- `similarity.py` (2 functions, ~20 lines) doesn't need its own file
- Still gets semantic retrieval quality from embeddings
- Still stdlib-only (TOML is stdlib in 3.11+)

**Cons:**

- `knowledge_base.py` could approach ~200 lines — nearing decomposition threshold
- TOML frontmatter is non-standard for markdown (YAML is the convention)
- Requires Python 3.11+ (reasonable for 2026, but worth stating)
- Authors need to learn TOML syntax for frontmatter (minor learning curve)

**Feasibility:** **High** — straightforward refactoring of the current plan.

---

#### Alternative 3: "Multi-Chunk Files with Hybrid Retrieval" — Best of Both Worlds

**Core insight:** The original spec's multi-chunk idea was better for authoring ergonomics. Combine it with a two-tier retrieval: fast metadata filter first, optional embedding re-rank second.

**How it works:**

- Playbook files group related rules: `docs/playbooks/shared/code-patterns.playbook.md` contains 3-5 chunks separated by `<!-- chunk: {id} -->` markers, each with inline YAML metadata.
- ~45 chunks live in ~10-12 files. Authors see related rules in context. Easier to maintain.
- Retrieval is two-tier: (1) Metadata filter (agent + tech) narrows to ~10-20 chunks. (2) If `GH_MODELS_TOKEN` is available, re-rank by embedding similarity. If not, return all filtered chunks sorted by tag relevance.
- The embedding layer is **optional** — the system works without it (metadata-only mode). Embeddings are an enhancement, not a requirement.
- The index file is `.gitignore`d. CI builds it as a side-effect but it's treated as a cache, not source. If missing, the system degrades to metadata-only retrieval.

**Pros:**

- Better authoring experience — related rules stay together in context
- Graceful degradation — works without API token, offline, or on first clone (before any CI run)
- Index is a cache, not source — no git bloat, no merge conflicts
- Fewer files in `docs/playbooks/` (~12 vs. ~45)
- Embeddings add value when available but aren't a hard dependency

**Cons:**

- Parser is more complex (must handle multi-chunk extraction within files)
- Chunk addressing is by ID, not file path — slightly more indirection
- Two retrieval paths means two code paths to test and maintain
- "Optional" features tend to bit-rot — the non-embedding path may get stale

**Feasibility:** **Medium-High** — more complex parser, but the hybrid retrieval is elegant.

---

#### Alternative 4: "Inverted Retrieval" — Chunks Declare Where They're Needed

**Core insight:** Instead of the Librarian querying for chunks, each chunk declares which agents and scenarios it's needed for. At agent spawn time, the Orchestrator collects all chunks tagged for that agent — no search, no ranking, no API.

**How it works:**

- Each playbook chunk's frontmatter includes a `trigger` field — a list of conditions under which this chunk should be included: `trigger: ["agent:worker", "agent:all", "tech:python", "task:refactor"]`.
- When the Orchestrator spawns an agent, it passes structured context: agent name, technology, task type.
- The Librarian reads all playbook files, matches triggers against the current context, and assembles the brief. Pure string matching — no embeddings.
- Chunks are ordered by specificity: exact agent match > "all" agents > technology match > task match.
- This is the **inversion** lens: instead of "search for what I need," it's "each rule knows where it belongs."

**Pros:**

- Zero ambiguity — chunk authors explicitly control where each rule appears
- No API calls, no index, no embeddings needed
- Deterministic — same context always produces the same brief (easier to test and debug)
- Playbook authors have full control over which agents see which rules
- Works immediately on first clone — no build step required

**Cons:**

- Requires authors to maintain `trigger` lists accurately (burden shifts to humans)
- Can't handle novel queries ("how do I handle rate limiting?" won't match unless tagged)
- Inflexible — a new agent or task type requires updating multiple chunk files
- Doesn't support free-text search at all — only structured metadata matching

**Feasibility:** **Medium** — simple to implement, but shifts maintenance burden to chunk authors and loses ad-hoc query capability.

---

#### Alternative 5: "Embed at Author Time, Not CI Time" — Pre-Computed Embeddings in Frontmatter

**Core insight:** Instead of a CI workflow that calls the embedding API, embed each chunk once when the author writes it (via a dev script) and store the vector directly in the frontmatter. The index becomes a simple concatenation — no API calls at build time.

**How it works:**

- A developer script (`scripts/embed-chunk.py`) takes a `.playbook.md` file, calls the embedding API, and writes the 1536-dim vector into the frontmatter as a base64-encoded string field: `embedding: "base64encodedstring..."`.
- The build script simply reads all playbook files, extracts the pre-computed embeddings from frontmatter, and assembles the index JSON — zero API calls.
- Content hash is still used: if the body changes but `embedding` is stale, the build script warns (or the author re-runs the embed script).
- CI just assembles — it never calls the API. Rate limits become irrelevant for CI.

**Pros:**

- CI never calls the embedding API — zero rate limit risk in CI
- Authors see exactly when their chunk was last embedded
- Build becomes a pure local operation — fast, deterministic, offline-capable
- Still gets full semantic retrieval quality

**Cons:**

- Authors must remember to re-embed after content changes (friction, error-prone)
- Base64 vectors in frontmatter are ugly and inflate file size (~8KB per chunk)
- Embedding model changes require re-embedding all chunks manually
- Shifts API cost from CI to individual developers
- Merge conflicts on the embedding field

**Feasibility:** **Medium** — workable but ergonomically awkward.

---

### Top Recommendation

**Alternative 1 ("Direct File Retrieval") as V1, with Alternative 3 ("Hybrid Retrieval") as the upgrade path.**

**Justification:**

The central question is: **does a system with ~80 chunks need vector embeddings?** The honest answer is no — not yet. Metadata filtering (agent + technology) already narrows to ~5-15 chunks, which is small enough to include directly in a context brief.

Building the full 6-module embedding pipeline for 80 chunks is like building a search engine for a bookshelf. It works, but it's over-engineered for the current scale. The Architect's plan is *technically correct* but violates the Playbook's own principle: "Don't design for hypothetical future requirements."

**Recommended path:**

1. **V1 (now):** Direct file retrieval with metadata filtering. ~200 lines of code. Ship fast. Zero API dependency for queries.
2. **V2 (when chunks exceed ~150-200 or semantic matching becomes demonstrably needed):** Layer on Alternative 3's hybrid retrieval — add embeddings as an optional enhancement that gracefully degrades to metadata-only.

This gives us a working Librarian immediately, avoids over-engineering, and leaves a clear upgrade path when (not if) we actually need semantic search.

**Regardless of which alternative is chosen**, I strongly recommend two changes from the current plan:

1. **Use TOML frontmatter** (`tomllib`, stdlib in 3.11+) instead of regex YAML parsing. The fragility risk of a hand-rolled YAML parser is real and unnecessary.
2. **Merge `similarity.py` into `knowledge_index.py`** (or whatever module does search). Two functions and ~20 lines don't justify their own module.

---

### Architect Response

**Reviewed by:** Architect Agent
**Date:** 2026-03-11

Thank you for the thorough analysis. Here is my evaluation of each assumption challenge and alternative, with decisions:

---

#### Assumption Responses

| # | Innovator Challenge | Architect Decision | Rationale |
| --- | --- | --- | --- |
| 1 | **Embeddings unnecessary for ~80 chunks** | **KEEP embeddings as primary.** Add metadata-only fallback. | The user explicitly chose Option C (live API calls with embeddings). Semantic matching provides genuine value — "don't repeat yourself" matching "duplication rules" is exactly the kind of fuzzy retrieval metadata can't do. However, the Innovator is right that the system shouldn't hard-fail without embeddings. Added graceful degradation to metadata-only filtering. |
| 2 | **Use TOML instead of regex YAML** | **✅ ADOPTED.** Switched to TOML frontmatter with `tomllib`. | Strongly agree. `tomllib` (stdlib 3.11+) eliminates the fragility of hand-rolled YAML regex parsing. Our CI uses Python 3.12, so this is guaranteed available. TOML's explicit syntax (quoted strings, bracket arrays) is less ambiguous than YAML. The `_parse_simple_yaml()` helper is eliminated entirely. |
| 3 | **6 modules / 4 layers over-decomposed** | **✅ PARTIALLY ADOPTED.** Merged `similarity.py` into `knowledge_index.py`. Now 5 modules / 3 layers. | Agree that `similarity.py` (2 functions, ~20 lines) doesn't justify its own file — `_dot_product` and `_rank_by_similarity` are implementation details of `search_chunks`. However, I kept `embedding_client.py` separate from `knowledge_index.py` because they have genuinely different responsibilities (HTTP/API vs. index CRUD) and different dependency profiles. A 3-module merge would push `knowledge_base.py` well past 200 lines. |
| 4 | **One file per chunk creates sprawl (~45 files)** | **KEEP single file per chunk.** | Single-file-per-chunk is simpler for tooling: each file has exactly one `id`, one frontmatter block, one content body. Diffs are per-chunk. CLI tools can address individual chunks by path. Multi-chunk files add parser complexity (`<!-- chunk -->` extraction), make diffs noisier, and create merge conflict risk when two authors edit different chunks in the same file. ~45 files in 3 subdirectories is manageable. |
| 5 | **Git bloat from 1-2MB JSON index** | **KEEP committed + add mitigations.** | The index must be in git so the Librarian works immediately on clone without a build step. To mitigate bloat: (a) added `.gitattributes` with `linguist-generated=true` to suppress diffs in merge requests, (b) incremental builds minimize changes per commit, (c) documented Git LFS migration as an upgrade path if bloat exceeds ~50MB. In practice, rebuilds only happen on playbook content changes — perhaps 1-2x/week, not 100x. |
| 6 | **Shelling out to Python for Librarian** | **KEEP shell-out.** | For embedding-based retrieval, the Librarian must: (a) embed the query string via API, (b) compute dot products against all candidate vectors. The Librarian's built-in file-read tools can't do HTTP calls or vector math. A Python subprocess is the correct interface. The metadata-only fallback *could* be done with file-read tools alone, but having a single consistent interface (the query script) is cleaner. |
| 7 | **Rate limit concerns** | **KEEP current approach + add fallback.** | Rate limits (15 req/min, 150/day) are manageable with incremental builds (typically 1-2 API calls per rebuild). The new metadata-only fallback addresses the worst case: if the API is completely unavailable, the Librarian still gets playbook knowledge. This was a gap in v1 — the Innovator correctly identified it. |

---

#### Alternative Evaluations

| Alternative | Decision | Rationale |
| --- | --- | --- |
| **Alt 1: Direct File Retrieval (no embeddings)** | **NOT ADOPTED as primary.** Adopted as fallback degradation path. | User explicitly chose Option C. However, this approach is now the graceful degradation path — when the index or API is unavailable, the system falls back to exactly this: read files → filter by metadata → return matches. Best of both worlds. |
| **Alt 2: TOML + Consolidated Modules** | **PARTIALLY ADOPTED.** TOML ✅, partial consolidation ✅ (similarity → knowledge_index), full 3-module merge ❌. | TOML is adopted fully. `similarity.py` merged into `knowledge_index.py`. But merging `embedding_client.py` into the same module crosses the 200-line decomposition threshold and mixes HTTP/API concerns with index CRUD. Kept separate. |
| **Alt 3: Multi-Chunk Files + Hybrid Retrieval** | **NOT ADOPTED.** | Multi-chunk files add parser complexity and merge conflict risk for a marginal authoring ergonomics gain. However, the *concept* of hybrid retrieval (metadata filter + optional embedding re-rank) is effectively what we now have with the graceful degradation path. |
| **Alt 4: Inverted Retrieval (chunks declare triggers)** | **NOT ADOPTED.** | Loses ad-hoc query capability, which is the core value proposition of semantic search. The current `agents` and `technologies` fields already serve the structured-matching role that `trigger` would. |
| **Alt 5: Embed at Author Time** | **NOT ADOPTED.** | Shifts API cost and responsibility to authors, creates friction (must remember to re-embed), and base64 vectors in frontmatter inflate file size. The CI-driven approach is more ergonomic and less error-prone. |

---

#### Summary of v1 → v2 Changes

1. **TOML frontmatter** — `+++` delimiters, parsed by `tomllib` (stdlib). Eliminates regex YAML fragility.
2. **Module consolidation** — `similarity.py` merged into `knowledge_index.py` as private helpers. 5 modules / 3 layers (was 6 / 4).
3. **Graceful degradation** — metadata-only fallback when index or API is unavailable. The system never hard-fails.
4. **Git bloat mitigation** — `.gitattributes` with `linguist-generated=true`, documented LFS upgrade path.
5. **Updated all examples and references** — frontmatter format, module numbers, dependency graph.
