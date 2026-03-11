# Feature Specification: RAG-Based Playbook Infrastructure

**Date:** 2026-03-11
**Raw Request:** "I want the playbook system to be scalable and large so agents can have per-agent playbooks and tech-specific playbooks. The Librarian should use RAG (embeddings) to find relevant chunks instead of searching whole playbooks. Tags help filter but aren't enough at scale. Build the chunking format, embedding pipeline (via GitHub Models API), the knowledge index, and update the Librarian to do two-stage retrieval (tag filter → embedding similarity)."
**Scope:** feature

---

## Summary

Build a scalable playbook system where knowledge is organized into per-agent and per-technology playbooks, each split into self-contained markdown chunks with structured YAML metadata. A Python embedding pipeline (run via GitHub Actions) processes these chunks through a GitHub Models API embedding model, producing a portable JSON knowledge index (`.ai/knowledge-index.json`). The Librarian agent is enhanced with two-stage retrieval: first filter chunks by tag/agent/tech metadata, then rank by cosine similarity against the query embedding to return only the most relevant context.

---

## User Stories

1. As a **template maintainer**, I want to add playbook rules organized by agent or technology so that knowledge scales without becoming a monolith.
2. As the **Librarian agent**, I want to retrieve only the most relevant chunks for a query so that downstream agents receive minimal, high-quality context.
3. As a **sub-agent** (Worker, Architect, etc.), I want playbook guidance specific to my role and the technologies in use so that I follow the right patterns without wading through irrelevant rules.
4. As a **CI pipeline**, I want embedding generation to run automatically when playbooks change so that the knowledge index stays current.
5. As a **template consumer**, I want the RAG system to be fully self-contained (no external vector DB, no paid APIs beyond GitHub Models) so that I can fork the template and have it work immediately.

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
| --- | --- | --- | --- |
| FR-1 | Standardized playbook chunk format with YAML frontmatter (tags, agents, tech, title, category) | MUST | Machine-parseable, human-readable |
| FR-2 | Playbook directory structure: `docs/playbooks/` with `agents/`, `technologies/`, `shared/` subdirs | MUST | Replaces monolithic `docs/PLAYBOOK.md` for new rules |
| FR-3 | Template playbook file: `docs/playbooks/_TEMPLATE.playbook.md` | MUST | Shows the exact chunk format for contributors |
| FR-4 | Python script `scripts/build-knowledge-index.py` that: reads all playbook files, extracts chunks, calls embedding API, writes JSON index | MUST | Single entry point |
| FR-5 | GitHub Actions workflow `.github/workflows/build-knowledge-index.yml` that runs the script on playbook changes | MUST | Triggers on push to `docs/playbooks/**` |
| FR-6 | Knowledge index format: `.ai/knowledge-index.json` with chunk text, metadata, and embedding vectors | MUST | Committed to git, reasonable size |
| FR-7 | Librarian agent two-stage retrieval: tag/metadata filter → cosine similarity ranking | MUST | Updated `librarian.agent.md` instructions |
| FR-8 | Cosine similarity computation in the Librarian's query workflow (pure Python, no deps) | MUST | Librarian agents run in Copilot context — they read the index and compute similarity |
| FR-9 | Existing `docs/PLAYBOOK.md` rules migrated into chunk format under `docs/playbooks/shared/` | SHOULD | Preserve all existing rules |
| FR-10 | Per-agent playbook stubs for the 32 existing agents | SHOULD | Even if initially empty, establishes the pattern |
| FR-11 | Configurable top-K retrieval (default K=10) | SHOULD | Prevents context bloat |
| FR-12 | Chunk deduplication in the index (content hash) | SHOULD | Prevents duplicate embeddings |
| FR-13 | Index metadata: build timestamp, model used, chunk count, index version | MUST | For staleness detection |
| FR-14 | Fallback behavior when index is missing or stale | MUST | Librarian falls back to full-text search of playbook files |

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior |
| --- | --- |
| Knowledge index file (`.ai/knowledge-index.json`) does not exist | Librarian falls back to keyword search across `docs/playbooks/` files directly, logs warning "⚠️ Knowledge index missing — using fallback search" |
| Knowledge index is stale (older than most recent playbook edit) | Librarian uses the index but appends "⚠️ Index may be stale — recommend rebuilding" to context brief |
| GitHub Models API rate limit hit during embedding generation | Script retries with exponential backoff (3 retries, 2s/4s/8s delays). If still failing, exits with error and partial index is NOT written (atomic write) |
| GitHub Models API returns error (401, 500, etc.) | Script logs the error with HTTP status and response body, exits non-zero. Workflow fails visibly |
| `GH_MODELS_TOKEN` secret is missing or invalid | Workflow fails at the embedding step with clear error: "GH_MODELS_TOKEN not set or invalid" |
| Playbook file has malformed YAML frontmatter | Script logs a warning with file path and line number, skips the malformed chunk, continues processing other chunks. Exit code 0 but summary shows skipped chunks |
| Playbook file has no chunks (empty or only frontmatter) | Skip silently — not an error. Some playbook files may be stubs |
| A chunk exceeds the embedding model's token limit | Script truncates to model's max input tokens, logs a warning "Chunk truncated: {chunk_id} ({actual} tokens > {max} limit)" |
| Two chunks have identical content but different metadata | Both are embedded separately (metadata matters for filtering), but a warning is logged |
| Query returns zero relevant chunks after filtering | Librarian returns a brief stating "No playbook guidance found for this query" and the agent proceeds with general rules from `docs/PLAYBOOK.md` |
| Index file is corrupt (invalid JSON) | Librarian falls back to file-based search, logs "⚠️ Knowledge index corrupt — using fallback" |
| Very large index file (>15 MB) | Build script warns if index exceeds 12 MB. Consider excluding low-priority chunks. The workflow does NOT fail — this is advisory |
| Playbook directory is empty (fresh template) | Build script produces a valid but empty index `{"version": 1, "chunks": [], "metadata": {...}}`. Librarian handles empty gracefully |
| Concurrent workflow runs (multiple playbook commits) | GitHub Actions concurrency group ensures only one build runs at a time (cancel-in-progress) |
| Embedding model unavailable on GitHub Models | Script fails with clear message. [ARCHITECT DECIDES] whether to support model fallback |

---

## Data Requirements

### Playbook Chunk Format (Markdown with YAML Frontmatter)

Each playbook file contains one or more chunks. Chunks are separated by a horizontal rule (`---`) after the frontmatter. Each chunk is a self-contained unit of knowledge.

```markdown
---
title: "Descriptive Chunk Title"
tags: [error-handling, validation, input-sanitization]
agents: [worker, debug, security]    # Which agents this is relevant to ("all" = universal)
technologies: [python, typescript]    # Tech-specific ("all" = language-agnostic)
category: pattern                     # pattern | anti-pattern | rule | convention | decision | strategy
priority: high                        # high | medium | low — for ranking when many chunks match
---

The actual rule/pattern/guidance content goes here. This is the text that gets embedded
and retrieved. It should be self-contained — an agent reading only this chunk should
understand the guidance without needing surrounding context.

## Examples

(Optional code examples, before/after comparisons, etc.)
```

### Knowledge Index Format (`.ai/knowledge-index.json`)

```json
{
  "version": 1,
  "metadata": {
    "built_at": "2026-03-11T14:30:00Z",
    "model": "text-embedding-3-small",
    "embedding_dimensions": 1536,
    "chunk_count": 142,
    "playbook_files_processed": 28,
    "skipped_chunks": 0,
    "index_size_bytes": 4200000
  },
  "chunks": [
    {
      "id": "shared/error-handling/never-swallow-errors",
      "source_file": "docs/playbooks/shared/error-handling.playbook.md",
      "title": "Never Swallow Errors Silently",
      "content": "Every catch block must log, re-throw, or return a meaningful error...",
      "tags": ["error-handling", "logging"],
      "agents": ["all"],
      "technologies": ["all"],
      "category": "rule",
      "priority": "high",
      "content_hash": "sha256:a1b2c3...",
      "embedding": [0.0123, -0.0456, ...]
    }
  ]
}
```

### Chunk ID Convention

`{subdir}/{playbook-name}/{chunk-slug}` — e.g., `agents/worker/red-green-loop`, `technologies/python/virtual-environments`, `shared/naming/kebab-case-files`.

---

## Playbook Directory Structure

```text
docs/playbooks/
├── _TEMPLATE.playbook.md          # Template showing chunk format
├── shared/                         # Universal rules (all agents, all tech)
│   ├── anti-duplication.playbook.md
│   ├── decomposition.playbook.md
│   ├── error-handling.playbook.md
│   ├── markdown-formatting.playbook.md
│   ├── naming-conventions.playbook.md
│   ├── file-organization.playbook.md
│   ├── testing-strategy.playbook.md
│   └── dependencies-policy.playbook.md
├── agents/                         # Per-agent playbooks
│   ├── worker.playbook.md
│   ├── architect.playbook.md
│   ├── test-writer.playbook.md
│   ├── security.playbook.md
│   ├── reviewer.playbook.md
│   └── ...                        # One per agent (32 files)
└── technologies/                   # Per-technology playbooks
    ├── python.playbook.md
    ├── typescript.playbook.md
    ├── github-actions.playbook.md
    └── ...                        # Added as the project adopts tech
```

**Relationship to existing `docs/PLAYBOOK.md`:** The monolithic `PLAYBOOK.md` remains as the single-page human-readable reference and the Retrospective Agent's write target. The `docs/playbooks/` directory contains the machine-parseable chunked versions of the same rules (plus new per-agent/per-tech rules). During migration (FR-9), existing `PLAYBOOK.md` sections are extracted into chunks. Going forward, the Retrospective Agent writes to BOTH `PLAYBOOK.md` and the appropriate chunk file.

---

## API Surface

### Embedding API (GitHub Models)

- **Endpoint:** `https://models.inference.ai.azure.com/embeddings`
- **Model:** `text-embedding-3-small` (1536 dimensions, available on GitHub Models)
- **Auth:** `Authorization: Bearer $GH_MODELS_TOKEN`
- **Request:** `{"input": ["chunk text..."], "model": "text-embedding-3-small"}`
- **Response:** `{"data": [{"embedding": [0.01, ...], "index": 0}], "usage": {"total_tokens": N}}`
- **Batch size:** Send up to 20 chunks per request to minimize API calls
- **Rate limits:** [ARCHITECT DECIDES] exact retry/backoff strategy based on GitHub Models limits

### Build Script CLI

```bash
python scripts/build-knowledge-index.py \
  --playbooks-dir docs/playbooks \
  --output .ai/knowledge-index.json \
  --model text-embedding-3-small \
  --batch-size 20 \
  --top-k-default 10
```

- `--playbooks-dir`: path to playbooks directory (default: `docs/playbooks`)
- `--output`: path to write index file (default: `.ai/knowledge-index.json`)
- `--model`: embedding model name (default: `text-embedding-3-small`)
- `--batch-size`: chunks per API call (default: 20)
- `--top-k-default`: stored in index metadata for Librarian default (default: 10)

---

## Security Considerations

| Concern | Mitigation |
| --- | --- |
| `GH_MODELS_TOKEN` exposure | Token is a GitHub secret, never logged or echoed. Script reads from env var only. The build script must NOT print the token in logs or error messages |
| Playbook content in embeddings sent to external API | Playbook content is project documentation (not secrets). However, chunks MUST NOT contain hardcoded secrets, API keys, or credentials. Build script should scan for common secret patterns and warn |
| Index file committed to git | The index contains playbook text (public docs) and embeddings (opaque floats). No sensitive data. Validated via the "no secrets in chunks" scan |
| Token in workflow logs | Use `::add-mask::` for the token in the workflow. Ensure `curl -s` (silent) mode |
| Injection via malformed playbook YAML | The YAML parser must use safe loading (`yaml.safe_load`), never `yaml.load` with arbitrary constructors |
| Supply chain — Python dependencies | The build script should minimize dependencies: `pyyaml` (YAML parsing), `requests` (HTTP, or use `urllib` from stdlib). Pin versions in `requirements.txt`. [ARCHITECT DECIDES] whether to use only stdlib |

---

## UI Requirements

Not applicable — this is a backend/infrastructure feature with no user-facing UI.

---

## Integration Points

### Existing Systems Affected

| System | How It's Affected |
| --- | --- |
| `docs/PLAYBOOK.md` | Remains as human-readable reference. New chunks are the machine-readable parallel. Retrospective Agent must update both |
| `.github/agents/librarian.agent.md` | Major update — new Query Mode with two-stage retrieval instructions |
| `.github/agents/retrospective.agent.md` | Minor update — must write to `docs/playbooks/` when updating rules, not just `PLAYBOOK.md` |
| `.github/copilot-instructions.md` | May need a note about the playbook structure |
| `AGENTS.md` | May need a note about the playbook structure |
| `.ai/PREFERENCES.md` | No change needed |
| GitHub Actions workflows | New workflow added. No changes to existing feedback workflows |
| `.gitignore` | Should NOT ignore `.ai/knowledge-index.json` (it must be committed) |

### New Files Created

| File | Purpose |
| --- | --- |
| `docs/playbooks/_TEMPLATE.playbook.md` | Template for creating new playbooks |
| `docs/playbooks/shared/*.playbook.md` | Shared rules (migrated from PLAYBOOK.md) |
| `docs/playbooks/agents/*.playbook.md` | Per-agent playbooks (stubs initially) |
| `docs/playbooks/technologies/*.playbook.md` | Per-technology playbooks (stubs initially) |
| `scripts/build-knowledge-index.py` | Python script: parse chunks → embed → write index |
| `scripts/requirements-knowledge-index.txt` | Pinned Python dependencies for the build script |
| `.github/workflows/build-knowledge-index.yml` | GitHub Actions workflow to build index on playbook changes |
| `.ai/knowledge-index.json` | The built index (generated, committed) |

### Dependencies

| Dependency | Version | Why |
| --- | --- | --- |
| Python 3.11+ | (already in CI) | Script runtime |
| `pyyaml` | >=6.0 | Parse YAML frontmatter from playbook chunks |
| `requests` | >=2.31 | Call GitHub Models embedding API (or use `urllib.request` from stdlib) |

[ARCHITECT DECIDES] whether to use only stdlib (`urllib.request` + a simple YAML frontmatter parser) to avoid any pip dependencies. A custom frontmatter parser is ~20 lines for this simple format.

---

## Librarian Agent Enhancement — Two-Stage Retrieval

### Current Behavior (Mode 2: Query)

1. Parse query
2. Read `docs/CODE_INVENTORY.md`, `docs/files/`, `docs/BUSINESS_LOGIC.md`, `docs/PLAYBOOK.md`, etc.
3. Assemble brief from matching content
4. Return brief

### New Behavior (Mode 2: Query — Enhanced)

1. Parse query — extract topic, target agent, technologies mentioned
2. **Stage 1: Tag Filter** — Load `.ai/knowledge-index.json`. Filter chunks where:
   - `agents` includes the target agent name OR `"all"`
   - `technologies` includes any mentioned tech OR `"all"`
   - `tags` overlap with query keywords
   - Result: candidate set (typically 20-60% of all chunks)
3. **Stage 2: Embedding Similarity** — Compute cosine similarity between query embedding and each candidate chunk's embedding. Rank by similarity score. Take top K (default 10).
   - **Query embedding:** The Librarian does NOT call the embedding API at query time (it runs in Copilot agent context, not in CI). Instead, it uses keyword matching as a proxy OR the index includes pre-computed query templates.
   - [ARCHITECT DECIDES] the exact query-time similarity approach — see Ambiguities section.
4. **Merge with existing search** — The playbook chunks are ADDED to the existing context brief, not replacing it. The Librarian still searches `docs/files/`, `CODE_INVENTORY.md`, etc. as before.
5. **Return enriched brief** — Include the top-K playbook chunks as a "Relevant Playbook Rules" section.

### Context Brief Format Update

```markdown
## Context Brief: {topic}

**For:** {agent type} — {task description}

### Relevant Playbook Rules ← NEW SECTION

> Retrieved via RAG (top {K} chunks, similarity ≥ {threshold})

1. **{chunk.title}** ({chunk.category}, priority: {chunk.priority})
   Source: `{chunk.source_file}`
   {chunk.content — first ~200 chars or full if short}

2. ...

### Relevant Files
(existing section — unchanged)

### Related Business Logic
(existing section — unchanged)
...
```

---

## Testing Priorities

| Priority | Test Scenario | Type |
| --- | --- | --- |
| CRITICAL | Chunk parser correctly extracts YAML frontmatter and content from single-chunk files | Unit |
| CRITICAL | Chunk parser correctly extracts multiple chunks from multi-chunk files | Unit |
| CRITICAL | Chunk parser handles malformed YAML gracefully (skip + warn, not crash) | Unit |
| CRITICAL | Index builder produces valid JSON with correct schema | Unit |
| CRITICAL | Cosine similarity computation returns correct values for known vectors | Unit |
| CRITICAL | Tag filtering correctly matches agent names, tech, and tags | Unit |
| HIGH | Embedding API client handles rate limits (retry + backoff) | Unit |
| HIGH | Embedding API client handles auth failure (clear error) | Unit |
| HIGH | Build script handles empty playbooks directory | Unit |
| HIGH | Build script handles chunks exceeding token limit (truncation) | Unit |
| HIGH | Index metadata is correct (timestamp, model, counts) | Unit |
| HIGH | Knowledge index is atomic — partial writes don't corrupt existing index | Integration |
| MEDIUM | End-to-end: playbook files → build script → valid index → Librarian retrieval | Integration |
| MEDIUM | Fallback behavior when index is missing | Integration |
| MEDIUM | Content hash deduplication works correctly | Unit |
| MEDIUM | Batch embedding API calls respect batch size limit | Unit |
| LOW | Index size stays within bounds (~3-12 MB for 100-500 chunks) | Benchmark |

---

## Ambiguities

### [ASK USER] — RESOLVED

1. **Embedding dimensions:** ✅ **1536 (full)** — user wants best quality embeddings.

2. **Query-time embedding:** ✅ **Option C — Live API call.** The Librarian calls the GitHub Models embedding API at query time via terminal/curl. The `GH_MODELS_TOKEN` is stored in a local `.env` file (already gitignored). Best quality retrieval.

3. **Existing PLAYBOOK.md migration:** ✅ **Keep as-is.** Do NOT migrate existing `docs/PLAYBOOK.md` rules into chunks. The old playbook remains the human-readable reference. New chunked playbooks in `docs/playbooks/` are a parallel system.

4. **Per-agent playbook scope:** ✅ **All 32 agents.** Create stub playbook files for all 32 agents immediately to establish the pattern.

### [ASSUMPTION]

1. **`text-embedding-3-small` is available on GitHub Models.** The GitHub Models catalog includes OpenAI models. If this specific model isn't available, `text-embedding-ada-002` or another OpenAI embedding model should work as a drop-in replacement.

2. **The index file will be committed to git.** At 1536 dimensions × 4 bytes × 500 chunks ≈ ~3 MB for vectors alone plus metadata. This is within the stated 3-12 MB budget. Git handles this fine (it's a single file, not binary).

3. **Python 3.11+ is available in GitHub Actions.** The existing workflows already use Python, so this is safe.

4. **The Librarian agent instructions are the primary integration point.** The Librarian's `.agent.md` file will be updated with detailed instructions for the new retrieval flow. The Librarian doesn't run code — it follows instructions and uses read/search tools.

5. **Multi-chunk files are supported.** A single `.playbook.md` file can contain multiple chunks separated by `---` (horizontal rule). The first `---` block is always YAML frontmatter for the first chunk. Subsequent `---` separators separate the next chunk's frontmatter from the previous chunk's content.

6. **The workflow runs on `push` to `main`/`master` only** (not on every branch push) to avoid unnecessary API calls. [ARCHITECT DECIDES] exact trigger.

7. **No vector database is needed.** The JSON index is loaded fully into memory for cosine similarity. At 500 chunks, this is trivially fast. At 5000 chunks, it would still be <50 MB and computable in seconds. A vector DB would be over-engineering for this template.

### [ARCHITECT DECIDES]

1. **Stdlib-only vs. pip dependencies:** Use only Python stdlib (`urllib.request` for HTTP, custom frontmatter parser) or allow `pyyaml` + `requests`? Stdlib-only means zero install step but slightly more code.

2. **Embedding dimensions:** Full 1536 or reduced (256/512) via the API's `dimensions` parameter? Reduced dims = smaller index but slightly lower quality.

3. **Chunk size limits:** What's the max chunk size in tokens? Recommendation: 500 tokens (≈375 words). Chunks larger than this should be split further.

4. **Workflow trigger:** On push to `docs/playbooks/**` on main/master? On PR merge? Manual dispatch?

5. **Query-time strategy** (see [ASK USER] #2 above) — if user doesn't have a preference, Architect should design the most pragmatic approach.

6. **Index versioning:** Should old index versions be kept (e.g., `knowledge-index.v1.json`, `knowledge-index.v2.json`) or just overwrite? Recommendation: just overwrite — git history preserves old versions.

7. **Multi-chunk file format:** Use `---` as separator (conflicts with YAML frontmatter convention) or use a custom separator like `<!-- chunk -->` or `## ---`? Recommendation: use `<!-- chunk -->` HTML comment to avoid ambiguity with YAML's `---`.

---

## Acceptance Criteria

1. A `docs/playbooks/_TEMPLATE.playbook.md` file exists with the standard chunk format, including YAML frontmatter schema documentation.
2. `docs/playbooks/shared/` contains at least the rules currently in `docs/PLAYBOOK.md`, split into logical chunk files.
3. `scripts/build-knowledge-index.py` reads all `*.playbook.md` files, extracts chunks, calls the GitHub Models embedding API, and writes `.ai/knowledge-index.json`.
4. The build script handles errors gracefully: malformed YAML (skip + warn), API failures (retry + fail), missing token (clear error).
5. `.github/workflows/build-knowledge-index.yml` triggers on playbook changes and runs the build script.
6. `.ai/knowledge-index.json` contains valid JSON matching the specified schema, with all chunks embedded.
7. The Librarian agent's `.agent.md` instructions include the two-stage retrieval workflow (tag filter → similarity ranking).
8. The Librarian instructions include fallback behavior when the index is missing or stale.
9. The context brief format includes a "Relevant Playbook Rules" section with retrieved chunks.
10. The index file is ≤12 MB for up to 500 chunks.
11. All Python code has 15+ unit tests per public function.
12. The build script runs successfully in GitHub Actions with the `GH_MODELS_TOKEN` secret.
13. No secrets are logged, echoed, or embedded in the index file.
14. The `GH_MODELS_TOKEN` is masked in workflow logs.
