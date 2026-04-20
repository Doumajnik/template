"""Canned graph queries used by agents and the CLI."""

from __future__ import annotations

from src.graph.models import EDGE_CALLS, KIND_FUNCTION
from src.graph.store import GraphStore


def find_functions_by_name(store: GraphStore, name: str) -> list[str]:
    """Return function node ids whose short name equals ``name``."""
    out: list[str] = []
    for node_id, data in store.g.nodes(data=True):
        if data.get("kind") != KIND_FUNCTION:
            continue
        short = str(data.get("name", "")).rsplit(".", 1)[-1]
        if short == name or data.get("name") == name:
            out.append(node_id)
    return out


def callers_of(store: GraphStore, name: str, depth: int = 1) -> list[str]:
    """Functions that (transitively, up to ``depth``) call any function named ``name``."""
    targets = set(find_functions_by_name(store, name))
    if not targets:
        return []
    result: set[str] = set()
    frontier = set(targets)
    for _ in range(depth):
        next_frontier: set[str] = set()
        for node in frontier:
            for pred, _, key in store.g.in_edges(node, keys=True):
                if key == EDGE_CALLS and pred not in targets and pred not in result:
                    next_frontier.add(pred)
        if not next_frontier:
            break
        result.update(next_frontier)
        frontier = next_frontier
    return sorted(result)


def callees_of(store: GraphStore, name: str, depth: int = 1) -> list[str]:
    """Functions called (transitively, up to ``depth``) by any function named ``name``."""
    sources = set(find_functions_by_name(store, name))
    if not sources:
        return []
    result: set[str] = set()
    frontier = set(sources)
    for _ in range(depth):
        next_frontier: set[str] = set()
        for node in frontier:
            for _, succ, key in store.g.out_edges(node, keys=True):
                if key == EDGE_CALLS and succ not in sources and succ not in result:
                    next_frontier.add(succ)
        if not next_frontier:
            break
        result.update(next_frontier)
        frontier = next_frontier
    return sorted(result)


def dead_code(store: GraphStore) -> list[str]:
    """Functions with no incoming CALLS edges (likely unused, modulo dynamic dispatch)."""
    out: list[str] = []
    for node_id, data in store.g.nodes(data=True):
        if data.get("kind") != KIND_FUNCTION:
            continue
        has_caller = any(
            key == EDGE_CALLS for _, _, key in store.g.in_edges(node_id, keys=True)
        )
        if not has_caller:
            out.append(node_id)
    return sorted(out)


def hotspots(store: GraphStore, top: int = 10) -> list[tuple[str, int]]:
    """Functions with the highest number of incoming CALLS edges."""
    counts: list[tuple[str, int]] = []
    for node_id, data in store.g.nodes(data=True):
        if data.get("kind") != KIND_FUNCTION:
            continue
        n = sum(
            1 for _, _, key in store.g.in_edges(node_id, keys=True) if key == EDGE_CALLS
        )
        if n > 0:
            counts.append((node_id, n))
    counts.sort(key=lambda x: (-x[1], x[0]))
    return counts[:top]


def shortest_call_path(store: GraphStore, from_name: str, to_name: str) -> list[str] | None:
    """Shortest CALLS-only path between any function named ``from_name`` and ``to_name``."""
    import networkx as nx

    sources = find_functions_by_name(store, from_name)
    targets = set(find_functions_by_name(store, to_name))
    if not sources or not targets:
        return None
    # Build a CALLS-only view to avoid mixing edge kinds.
    sub = store.g.edge_subgraph(
        [
            (u, v, k)
            for u, v, k in store.g.edges(keys=True)
            if k == EDGE_CALLS
        ]
    )
    best: list[str] | None = None
    for src in sources:
        for tgt in targets:
            try:
                path = nx.shortest_path(sub, src, tgt)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            if best is None or len(path) < len(best):
                best = path
    return best
