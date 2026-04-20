# Code Intelligence Graph

A lightweight, in-repo graph of your codebase: functions, files, classes, modules,
calls, imports. Designed to give agents (Librarian, Architect, Critic, Refactor,
Debug) relational queries the flat `CODE_INVENTORY.md` can't answer.

## Why

Flat docs answer *"what exists"*. A graph answers *"what depends on this"*,
*"what's unreachable"*, *"what are the call hotspots"*, *"what breaks if I change X"*.

## Stack

- **Storage:** [NetworkX](https://networkx.org/) `MultiDiGraph` persisted as JSON in
  `.ai/graph/code.json`. Pure Python. No daemon, no native build, no schema migration.
- **Python parser:** stdlib `ast`.
- **JS/TS/TSX parser:** [`tree-sitter-language-pack`](https://pypi.org/project/tree-sitter-language-pack/)
  (prebuilt wheels — no compilation needed).

## Schema

Nodes: `File`, `Function`, `Class`, `Module`.
Edges: `CALLS`, `DEFINED_IN`, `CONTAINS`, `IMPORTS`.

Node ids are canonical strings:

- File: `File:<relpath>`
- Function: `<relpath>::Function:<qualname>` (e.g. `src/utils/foo.py::Function:Bar.method`)
- Class: `<relpath>::Class:<qualname>`
- Module: `Module:<dotted-or-import-spec>`

## Auto-rebuild

The graph keeps itself fresh — you should never need to run `build` manually.

| Trigger | Behaviour |
|---|---|
| Any `query` / `stats` / `export-mermaid` call | Checks mtimes; rebuilds if missing or any source file is newer. Logs `[graph] rebuilt: N files…` to stderr when it does. |
| `git commit` (with `scripts/install-hooks.ps1` installed) | `post-commit` hook runs `ensure` in the background if the commit touched `.py/.js/.jsx/.ts/.tsx/.mjs/.cjs` files. Output goes to `.ai/graph/last-build.log`. Never blocks the commit. |
| Programmatic | `from src.graph.freshness import ensure_fresh; store, _, _ = ensure_fresh()` |

Force a rebuild explicitly: `python -m src.graph.cli build` or `... cli ensure --force`.

The freshness check is cheap — just an mtime walk over source files (excluded
dirs like `node_modules`, `.venv` are skipped). Typically <50ms on medium repos.

## CLI

```powershell
# Build the graph from any directory (always rebuilds)
python -m src.graph.cli build --path src --out .ai/graph/code.json

# Rebuild only if missing or stale (cheap — used by hooks)
python -m src.graph.cli ensure

# Stats
python -m src.graph.cli stats

# Who calls this function?
python -m src.graph.cli query callers parse_playbook_file --depth 3

# What does this function call?
python -m src.graph.cli query callees build_graph --depth 2

# Functions with no callers (likely dead, modulo dynamic dispatch / public API)
python -m src.graph.cli query dead-code

# Most-called functions
python -m src.graph.cli query hotspots --top 10

# Shortest call path between two functions
python -m src.graph.cli query path top_handler db_write

# Render top hotspots as a Mermaid diagram
python -m src.graph.cli export-mermaid --max-nodes 30
```

## Programmatic use

**For agents and helpers — auto-fresh by default.** Import from `src.graph.api`;
every call rebuilds the graph if any source file is newer than the snapshot.

```python
from src.graph import api

# Single queries — each one ensures freshness internally.
api.callers_of("parse_playbook_file", depth=3)
api.dead_code()
api.hotspots(top=10)

# One bundled brief, one rebuild check — what to put in a Librarian context brief.
facts = api.function_facts("parse_playbook_file", caller_depth=3)
# {
#   "found": True,
#   "defined_at": ["src/utils/playbook_parser.py::Function:parse_playbook_file"],
#   "direct_callers": [...],
#   "transitive_callers": [...],
#   "direct_callees": [...],
#   "is_dead_code": False,
# }

# Or hold a snapshot for many queries against one consistent state.
store = api.get_store()
```

**For tests and code that already holds a `GraphStore`** — import the pure
versions from `src.graph.queries`. They take a `store` argument and do no I/O,
so they're easy to test deterministically.

```python
from src.graph.builder import build_graph
from src.graph.queries import callers_of

store, _ = build_graph("src")
callers_of(store, "foo", depth=2)
```

## How call resolution works

Static analysis can't always know which function a call refers to. Extractors
emit `CALLS` edges to placeholder `Unresolved:<name>` nodes. After all files are
parsed, `GraphStore.resolve_calls()` rewires each placeholder to a concrete
function node **only when exactly one function in the project has that short
name**. Ambiguous names (e.g. `__init__`, `run`) stay unresolved — better
honesty than false confidence.

Limitations to be aware of:

- Dynamic dispatch (callbacks, plugins, `getattr`) is invisible.
- Method calls match by short name only — `a.save()` and `b.save()` are conflated
  if both classes define `save`.
- JS/TS `import * as ns` and re-exports aren't traced through.

## Adding a new language

The `EXTRACTORS` registry in `src/graph/extractors/__init__.py` maps file suffix
to a callable `(file_path, source_text) -> (nodes, edges)`. To add a language:

1. **Pick a parser.** For most languages, use `tree_sitter_language_pack` — it
   ships prebuilt wheels for Go, Rust, Java, Kotlin, C#, C++, Ruby, PHP, Swift,
   and many more. Confirm the language name with `from tree_sitter_language_pack
   import get_parser`.

2. **Write the extractor.** Copy `src/graph/extractors/js_ts.py` as a template.
   You'll need to update three things:
   - **Function node types** — the tree-sitter node types that represent function
     definitions in the target grammar (e.g. for Go: `function_declaration`,
     `method_declaration`).
   - **Class/struct/type node types** — the equivalent of `class_declaration`.
   - **Call expression type and callee field** — what node type wraps a call,
     and which child field holds the callee name (often `function` or `name`).

   Use a tree-sitter playground (or `node.sexp()` after a small parse) to discover
   the right node types for the grammar.

3. **Handle imports.** Each language has its own import syntax. Look for the
   import statement node type and pull out the module specifier.

4. **Register the suffix(es)** in `EXTRACTORS`:

   ```python
   from src.graph.extractors.go import extract_go
   EXTRACTORS[".go"] = extract_go
   ```

5. **Add tests** mirroring `tests/graph/test_graph.py`'s JS/TS section: at
   minimum cover function extraction, call edges, and imports.

For languages without a tree-sitter grammar, any AST library that exposes
positions and node types will work — the contract is just `(path, source) ->
(nodes, edges)`.

## What this graph is *not*

- Not a type checker. It records *names*, not types.
- Not a build-system replacement. It doesn't know about packages, monorepo
  workspaces, or `tsconfig` path aliases.
- Not real-time. Rebuild after edits — the Librarian agent does this
  automatically per the orchestrator protocol (see `AGENTS.md`).

## Files

- [src/graph/models.py](../../src/graph/models.py) — `Node`, `Edge`, id helpers.
- [src/graph/extractors/python_ast.py](../../src/graph/extractors/python_ast.py) — Python.
- [src/graph/extractors/js_ts.py](../../src/graph/extractors/js_ts.py) — JS / TS / TSX.
- [src/graph/extractors/__init__.py](../../src/graph/extractors/__init__.py) — language registry.
- [src/graph/store.py](../../src/graph/store.py) — NetworkX-backed graph + persistence.
- [src/graph/builder.py](../../src/graph/builder.py) — directory walker + dispatcher.
- [src/graph/queries.py](../../src/graph/queries.py) — canned queries.
- [src/graph/cli.py](../../src/graph/cli.py) — command-line interface.
- [tests/graph/test_graph.py](../../tests/graph/test_graph.py) — 22 tests.
