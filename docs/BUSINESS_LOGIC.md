# Business Logic Overview

> This file describes the system's high-level business logic, data flows, module responsibilities, and how components interact.
> The **planner** reads this FIRST before planning any changes. Keep it up to date after every implementation.

---

## System Purpose

<!-- Describe what this system does at a high level. What problem does it solve? Who uses it? -->

RAG-Powered Playbook Infrastructure. Playbook rules are stored as individual markdown files with TOML frontmatter in `docs/playbooks/`. The `playbook_parser` module parses these files into structured chunk dicts for downstream consumption. The full RAG pipeline (embedding, indexing, semantic search) is designed but only the parser module is currently implemented.

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

---

## Data Flows

<!-- Describe how data moves through the system. What comes in, what gets processed, what goes out? -->

### RAG Pipeline

> **⚠️ Planned — not yet implemented.** Only the playbook parser (step 1) exists on disk. The embedding client, knowledge index, CLI scripts, and CI workflow are designed but not yet built.

The RAG (Retrieval-Augmented Generation) pipeline provides semantically relevant playbook knowledge to agents via the Librarian.

**Intended Flow (designed, not implemented):**

1. **Playbook Chunks** (`docs/playbooks/**/*.playbook.md`) → parsed by `playbook_parser.py` into structured dicts (metadata + body) ✔️ *Implemented*
2. **Parser Output** → fed to `build-knowledge-index.py`, which diffs against the existing index by content hash ❌ *Not yet implemented*
3. **New/Changed Chunks** → embedded via `embedding_client.py` (GitHub Models API, text-embedding-3-small) ❌ *Not yet implemented*
4. **Embeddings** → merged into the **Knowledge Index** (`.ai/knowledge-index.json`) by `knowledge_index.py` ❌ *Not yet implemented*
5. **Librarian Query** → query text embedded, similarity search, ranked results returned ❌ *Not yet implemented*

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

| Dependency | Purpose | Auth | Status |
|------------|---------|------|--------|
| GitHub Models API (`https://models.github.ai/inference`) | Text embedding via `text-embedding-3-small` | `GH_MODELS_TOKEN` env var | ⏸️ *Planned — not yet implemented* |
