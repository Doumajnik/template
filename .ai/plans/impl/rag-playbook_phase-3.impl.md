# Impl: CLI Scripts & CI Workflow (Phase 3)

**Parent plan:** `.ai/plans/2026-03-11_rag-playbook-infrastructure.plan.md`
**Phase:** 3
**Status:** 🟡 Draft

---

## Overview

Implement the Layer-3 CLI entry points and the GitHub Actions CI workflow. Both scripts depend on all Layer-1 and Layer-2 modules. The build script orchestrates the full parse → diff → embed → merge → save pipeline. The query script provides the Librarian's RAG retrieval with graceful degradation to metadata-only filtering.

---

## Functions

### `scripts/build-knowledge-index.py`

**Purpose:** CLI entry point for CI. Parses all playbooks, computes incremental diff, embeds new/changed chunks, writes updated index.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `main` | `() -> None` | Parse args, validate environment, orchestrate build pipeline, exit with appropriate code | `[delegatable]` |
| 2 | `parse_args` | `() -> argparse.Namespace` | Define and parse CLI arguments: `--playbooks-dir`, `--index-path`, `--full-rebuild`, `--dry-run`, `--verbose` | `[delegatable]` |
| 3 | `validate_environment` | `(args: argparse.Namespace) -> str` | Check `GH_MODELS_TOKEN` is set, playbooks dir exists. Returns token. Exits with code 1 on failure | `[delegatable]` |
| 4 | `run_build` | `(args: argparse.Namespace, token: str) -> None` | Core pipeline: discover → parse → diff → embed (skip if `--dry-run`) → merge → save. Calls `print_summary` | `[delegatable]` |
| 5 | `print_summary` | `(total: int, embedded: int, removed: int, skipped: int) -> None` | Print build statistics to stdout | `[delegatable]` |

**sys.path setup:** `sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"))` — compute path relative to script file, not CWD.

**Progress:**

- [ ] #1 `main` `[delegatable]`
- [ ] #2 `parse_args` `[delegatable]`
- [ ] #3 `validate_environment` `[delegatable]`
- [ ] #4 `run_build` `[delegatable]`
- [ ] #5 `print_summary` `[delegatable]`

---

### `scripts/query-knowledge-index.py`

**Purpose:** CLI entry point for Librarian agent. Loads index, embeds query, filters, ranks, outputs results. Degrades gracefully when index or token is unavailable.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | `main` | `() -> None` | Parse args, read token from env (may be `None`), run query, format and output results | `[delegatable]` |
| 2 | `parse_args` | `() -> argparse.Namespace` | Define and parse CLI arguments: `--query` (required), `--agent`, `--tech`, `--top-k`, `--index-path`, `--format` | `[delegatable]` |
| 3 | `run_query` | `(args: argparse.Namespace, token: str or None) -> list[dict]` | Try embedding-based search: load index → embed query → search. On any failure, call `fallback_metadata_retrieval`. If token is `None`, skip directly to fallback | `[delegatable]` |
| 4 | `format_results_markdown` | `(results: list[dict]) -> str` | Format results as markdown: title, score (if present), source file, and content for each chunk | `[delegatable]` |
| 5 | `format_results_json` | `(results: list[dict]) -> str` | Format results as JSON array with `json.dumps(indent=2)` | `[delegatable]` |
| 6 | `fallback_metadata_retrieval` | `(playbooks_dir: str, agent: str or None, tech: str or None) -> list[dict]` | Graceful degradation: discover and parse all playbook files via `playbook_parser`, filter by agent/tech metadata, return matching chunks (unranked). Prints fallback warning to stderr | `[delegatable]` |

**sys.path setup:** `sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src" / "utils"))` — same approach as build script.

**Fallback triggers (consolidated from architecture):**

| # | Trigger Condition | Detection Point |
| --- | --- | --- |
| F1 | `GH_MODELS_TOKEN` not set | `main()` — `os.environ.get()` returns `None` |
| F2 | Index file does not exist | `load_index()` — `FileNotFoundError` |
| F3 | Index file is corrupted (invalid JSON) | `load_index()` — `json.JSONDecodeError` |
| F4 | Index schema version mismatch | `_validate_index()` — `ValueError` |
| F5 | Embedding API call fails after retries | `embed_single()` — any exception after max retries |
| F6 | Embedding API returns invalid response | `embed_single()` — `KeyError` / unexpected response shape |

**Progress:**

- [ ] #1 `main` `[delegatable]`
- [ ] #2 `parse_args` `[delegatable]`
- [ ] #3 `run_query` `[delegatable]`
- [ ] #4 `format_results_markdown` `[delegatable]`
- [ ] #5 `format_results_json` `[delegatable]`
- [ ] #6 `fallback_metadata_retrieval` `[delegatable]`

---

### `.github/workflows/build-knowledge-index.yml`

**Purpose:** GitHub Actions workflow that rebuilds the knowledge index on playbook changes and commits the updated index.

| # | Symbol | Signature | Description | Mode |
| --- | --- | --- | --- | --- |
| 1 | CI workflow file | N/A — YAML config | Triggers on `docs/playbooks/**` push to `main` + `workflow_dispatch`. Sets up Python 3.12, runs build script with `--verbose`, commits updated index with `chore: rebuild knowledge index` message. Includes `concurrency` group and `git pull --rebase` before push | `[delegatable]` |

**Progress:**

- [ ] #1 CI workflow file `[delegatable]`

---

## Constants & Types

*(No standalone constants/types. CLI-specific defaults are defined as `argparse` default values within each script.)*

Build script defaults:
- `--playbooks-dir`: `docs/playbooks`
- `--index-path`: `.ai/knowledge-index.json`

Query script defaults:
- `--top-k`: `10`
- `--index-path`: `.ai/knowledge-index.json`
- `--format`: `markdown`

---

## Dependencies

| Depends on | From | Status |
| --- | --- | --- |
| `playbook_parser` | `src/utils/playbook_parser.py` (Phase 1) | Must be implemented |
| `embedding_client` | `src/utils/embedding_client.py` (Phase 1) | Must be implemented |
| `knowledge_index` | `src/utils/knowledge_index.py` (Phase 2) | Must be implemented |
| Phase 0 playbook stubs | `docs/playbooks/` | Must exist for integration testing |
| Python stdlib: `argparse`, `sys`, `os`, `pathlib`, `json` | stdlib | Available |

---

## Notes

- **Error propagation pattern:** Build script catches all exceptions at top level, prints to stderr, exits with code 1. Query script uses cascading fallback: try embedding-based → on failure → `fallback_metadata_retrieval` → on failure → empty results to stdout, error to stderr. Query script NEVER exits with code 1.
- **Output routing:** Both scripts send results to stdout (for piping/capture). Diagnostics and warnings go to stderr.
- **`--format json`:** The architecture's Critic flagged this as potentially speculative. It's kept because it's trivial to implement (one function) and useful for programmatic consumers.
- **Testing note:** The CLI scripts will be tested via integration tests (Integration Tester agent), not granular unit tests per function. The internal logic they compose (parser, client, index) is thoroughly unit-tested in Phases 1-2.
- **GRANULAR SPAWNING:** 5 + 6 + 1 = 12 Worker spawns for this phase. Test Writers are spawned for the script functions where pure unit tests are feasible (arg parsing, formatting, summary printing).
