"""CLI for the code-intelligence graph.

Usage:
    python -m src.graph.cli build [--path PATH] [--out PATH]
    python -m src.graph.cli stats [--db PATH]
    python -m src.graph.cli query callers <name> [--depth N] [--db PATH]
    python -m src.graph.cli query callees <name> [--depth N] [--db PATH]
    python -m src.graph.cli query dead-code [--db PATH]
    python -m src.graph.cli query hotspots [--top N] [--db PATH]
    python -m src.graph.cli query path <from> <to> [--db PATH]
    python -m src.graph.cli export-mermaid [--max-nodes N] [--db PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from src.graph.builder import build_graph
from src.graph.freshness import ensure_fresh
from src.graph.queries import (
    callees_of,
    callers_of,
    dead_code,
    hotspots,
    shortest_call_path,
)
from src.graph.store import GraphStore

DEFAULT_DB = ".ai/graph/code.json"
DEFAULT_BUILD_PATH = "."


def _load(db_path: str, *, auto: bool = True, root: str = DEFAULT_BUILD_PATH) -> GraphStore:
    """Load the graph, auto-rebuilding if missing/stale (unless ``auto=False``)."""
    if not auto:
        p = Path(db_path)
        if not p.exists():
            sys.stderr.write(f"Graph DB not found at {db_path}. Run `build` first.\n")
            sys.exit(2)
        return GraphStore.load(p)
    store, report, rebuilt = ensure_fresh(db_path, root)
    if rebuilt:
        sys.stderr.write(
            f"[graph] rebuilt: {report.get('files_processed', '?')} files, "
            f"{report.get('calls_resolved', '?')} calls resolved\n"
        )
    return store


def cmd_build(args: argparse.Namespace) -> int:
    store, report = build_graph(args.path)
    store.save(args.out)
    print(json.dumps({**report, "out": args.out, **store.stats()}, indent=2))
    return 0


def cmd_ensure(args: argparse.Namespace) -> int:
    """Rebuild only when stale. Cheap to call from hooks/wrappers."""
    _, report, rebuilt = ensure_fresh(args.db, args.path, force=args.force)
    print(json.dumps({"rebuilt": rebuilt, **report}, indent=2))
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    store = _load(args.db)
    print(json.dumps(store.stats(), indent=2))
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    store = _load(args.db)
    if args.subcmd == "callers":
        for n in callers_of(store, args.name, depth=args.depth):
            print(n)
    elif args.subcmd == "callees":
        for n in callees_of(store, args.name, depth=args.depth):
            print(n)
    elif args.subcmd == "dead-code":
        for n in dead_code(store):
            print(n)
    elif args.subcmd == "hotspots":
        for node_id, count in hotspots(store, top=args.top):
            print(f"{count}\t{node_id}")
    elif args.subcmd == "path":
        path = shortest_call_path(store, args.from_name, args.to_name)
        if path is None:
            print("(no path)")
            return 1
        for n in path:
            print(n)
    return 0


def cmd_export_mermaid(args: argparse.Namespace) -> int:
    store = _load(args.db)
    print(_to_mermaid(store, max_nodes=args.max_nodes))
    return 0


def _to_mermaid(store: GraphStore, max_nodes: int) -> str:
    """Render a Mermaid flowchart of the top hotspot subgraph."""
    top = [n for n, _ in hotspots(store, top=max_nodes)]
    seen: set[str] = set(top)
    # Pull in direct callers of the hot nodes for context.
    for node in top:
        for pred, _, _ in store.g.in_edges(node, keys=True):
            seen.add(pred)
            if len(seen) >= max_nodes * 3:
                break
    lines = ["flowchart LR"]
    aliases: dict[str, str] = {}
    for i, node_id in enumerate(seen):
        alias = f"n{i}"
        aliases[node_id] = alias
        label = node_id.split("::")[-1].replace('"', "'")
        lines.append(f'    {alias}["{label}"]')
    for u, v, k in store.g.edges(keys=True):
        if u in aliases and v in aliases and k == "CALLS":
            lines.append(f"    {aliases[u]} --> {aliases[v]}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="src.graph.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Build the graph from a directory (always)")
    p_build.add_argument("--path", default=DEFAULT_BUILD_PATH)
    p_build.add_argument("--out", default=DEFAULT_DB)
    p_build.set_defaults(func=cmd_build)

    p_ensure = sub.add_parser(
        "ensure", help="Rebuild only if missing or stale (cheap)"
    )
    p_ensure.add_argument("--path", default=DEFAULT_BUILD_PATH)
    p_ensure.add_argument("--db", default=DEFAULT_DB)
    p_ensure.add_argument("--force", action="store_true")
    p_ensure.set_defaults(func=cmd_ensure)

    p_stats = sub.add_parser("stats", help="Print node/edge counts")
    p_stats.add_argument("--db", default=DEFAULT_DB)
    p_stats.set_defaults(func=cmd_stats)

    p_q = sub.add_parser("query", help="Run a canned query")
    p_q.add_argument("--db", default=DEFAULT_DB)
    qsub = p_q.add_subparsers(dest="subcmd", required=True)

    q_callers = qsub.add_parser("callers")
    q_callers.add_argument("name")
    q_callers.add_argument("--depth", type=int, default=1)

    q_callees = qsub.add_parser("callees")
    q_callees.add_argument("name")
    q_callees.add_argument("--depth", type=int, default=1)

    qsub.add_parser("dead-code")

    q_hot = qsub.add_parser("hotspots")
    q_hot.add_argument("--top", type=int, default=10)

    q_path = qsub.add_parser("path")
    q_path.add_argument("from_name")
    q_path.add_argument("to_name")

    p_q.set_defaults(func=cmd_query)

    p_export = sub.add_parser("export-mermaid", help="Render a Mermaid flowchart")
    p_export.add_argument("--db", default=DEFAULT_DB)
    p_export.add_argument("--max-nodes", type=int, default=30)
    p_export.set_defaults(func=cmd_export_mermaid)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
