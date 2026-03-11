# Code Inventory

> **This is a living document.** AI agents MUST update it after creating or modifying any source file.
> Agents MUST search this file before creating new functions, classes, or utilities to prevent duplication.

**Last updated:** *(not yet — no source files exist)*

---

## How to Read This File

Each source file gets a section with:

- **File path** and one-line purpose
- **Symbol table** listing every exported function, class, constant, and type

## How to Update This File

After creating or modifying a source file:

1. Find the section for that file (or create a new one in alphabetical order).
2. Update the symbol table to reflect the current state of the file.
3. Update the "Last updated" timestamp at the top.

### Entry Format

```markdown
### `src/path/to/file.ext`

**Purpose:** One-line description of what this file does.

| Symbol | Type | Signature / Value | Description |
|--------|------|-------------------|-------------|
| `functionName` | function | `(param: Type) → ReturnType` | What it does |
| `ClassName` | class | — | What it represents |
| `CONSTANT_NAME` | const | `"value"` or `Type` | What it holds |
| `TypeName` | type/interface | — | What it describes |
```

---

## Inventory

<!-- 
  Add entries below as source files are created.
  Keep entries in alphabetical order by file path.
  Remove entries when files are deleted.
-->

### `src/utils/playbook_parser.py`

**Purpose:** Parses `.playbook.md` files with TOML frontmatter into structured chunk dicts.

| Symbol | Type | Signature / Value | Description |
|--------|------|-------------------|-------------|
| `VALID_CATEGORIES` | const | `frozenset` | Valid playbook category values |
| `REQUIRED_FIELDS` | const | `tuple` | Required TOML frontmatter fields |
| `parse_playbook_file` | function | `(file_path: str) -> dict` | Parse a single .playbook.md file |
| `discover_playbook_files` | function | `(base_dir: str) -> list[str]` | Recursively find *.playbook.md files |
| `parse_all_playbooks` | function | `(base_dir: str) -> list[dict]` | Discover, parse, and validate all playbooks |

### `src/utils/embedding_client.py`

**Purpose:** Thin wrapper around the GitHub Models embedding API.

| Symbol | Type | Signature / Value | Description |
|--------|------|-------------------|-------------|
| `API_URL` | const | `str` | GitHub Models embedding API endpoint |
| `MODEL` | const | `str` | Embedding model name |
| `DIMENSIONS` | const | `int` | Embedding vector dimensions (1536) |
| `embed_texts` | function | `(texts: list[str], token: str) -> list[list[float]]` | Batch embed texts via GitHub Models API |
| `embed_single` | function | `(text: str, token: str) -> list[float]` | Embed a single text |

### `src/utils/knowledge_index.py`

**Purpose:** Manages the knowledge index — loading, saving, diffing, merging, and searching.

| Symbol | Type | Signature / Value | Description |
|--------|------|-------------------|-------------|
| `INDEX_VERSION` | const | `int` | Current index schema version |
| `MODEL_NAME` | const | `str` | Embedding model identifier |
| `DIMENSIONS` | const | `int` | Embedding vector dimensions |
| `load_index` | function | `(index_path: str) -> dict` | Load and validate knowledge index from JSON |
| `save_index` | function | `(index: dict, index_path: str) -> None` | Atomically write index to disk |
| `diff_chunks` | function | `(current_chunks, existing_index) -> tuple` | Incremental diff by content hash |
| `merge_embeddings` | function | `(existing, new_chunks, embeddings, removed_ids) -> dict` | Merge new embeddings into index |
| `search_chunks` | function | `(index, query_embedding, agent, tech, top_k) -> list[dict]` | Filter and rank chunks by similarity |
