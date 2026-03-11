# Business Logic Overview

> This file describes the system's high-level business logic, data flows, module responsibilities, and how components interact.
> The **planner** reads this FIRST before planning any changes. Keep it up to date after every implementation.

---

## System Purpose

<!-- Describe what this system does at a high level. What problem does it solve? Who uses it? -->

*Not yet documented. Update this when the first feature is implemented.*

---

## Module Responsibilities

<!-- For each major module/directory, describe its role in the system. -->

| Module | Responsibility |
| -------- | --------------- |
| `src/config/` | Configuration and environment setup |
| `src/models/` | Data models, schemas, types |
| `src/services/` | Business logic and service layer |
| `src/utils/` | Shared helper functions and utilities |
| `src/utils/playbook_parser.py` | Parses `.playbook.md` files with TOML frontmatter into structured chunk dicts |
| `src/utils/embedding_client.py` | Thin wrapper around the GitHub Models embedding API |
| `src/utils/knowledge_index.py` | Knowledge index I/O, diffing, merging, and similarity search |
| `scripts/build-knowledge-index.py` | CLI script to incrementally build the knowledge index |
| `scripts/query-knowledge-index.py` | CLI script to query the knowledge index and output ranked results |

---

## Data Flows

<!-- Describe how data moves through the system. What comes in, what gets processed, what goes out? -->

### RAG Pipeline

The RAG (Retrieval-Augmented Generation) pipeline provides semantically relevant playbook knowledge to agents via the Librarian.

**Index Build Flow:**

1. **Playbook Chunks** (`docs/playbooks/**/*.playbook.md`) → parsed by `playbook_parser.py` into structured dicts (metadata + body)
2. **Parser Output** → fed to `build-knowledge-index.py`, which diffs against the existing index by content hash
3. **New/Changed Chunks** → embedded via `embedding_client.py` (GitHub Models API, text-embedding-3-small)
4. **Embeddings** → merged into the **Knowledge Index** (`.ai/knowledge-index.json`) by `knowledge_index.py`

**Query Flow:**

1. **Librarian Query** (agent type + technology + free-text) → `query-knowledge-index.py`
2. **Query Text** → embedded via `embedding_client.py` into a vector
3. **Similarity Search** → `knowledge_index.py` filters by agent/tech metadata, ranks by cosine similarity
4. **Ranked Results** → returned as markdown or JSON to the Librarian for inclusion in context briefs

**Fallback:** When the knowledge index is missing or `GH_MODELS_TOKEN` is not set, the Librarian falls back to metadata-only filtering (no embeddings) or skips RAG entirely and uses documentation search only.

---

## Key Business Rules

<!-- List the core business rules and invariants the system must maintain. -->

*Not yet documented. Update this when the first feature is implemented.*

---

## Component Interactions

<!-- Describe how modules interact. Which services call which? What are the dependency directions? -->

*Not yet documented. Update this when the first feature is implemented.*

---

## External Dependencies

<!-- List external systems, APIs, databases, or services this system depends on. -->

| Dependency | Purpose | Auth |
|------------|---------|------|
| GitHub Models API (`https://models.github.ai/inference`) | Text embedding via `text-embedding-3-small` | `GH_MODELS_TOKEN` env var |
