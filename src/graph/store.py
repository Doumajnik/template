"""NetworkX-backed graph store with JSON persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import networkx as nx

from src.graph.models import (
    EDGE_CALLS,
    KIND_FUNCTION,
    Edge,
    Node,
)


class GraphStore:
    """Wraps a ``networkx.MultiDiGraph`` plus add/save/load helpers."""

    def __init__(self) -> None:
        self.g: nx.MultiDiGraph = nx.MultiDiGraph()

    # ---- mutation -----------------------------------------------------

    def add_node(self, node: Node) -> None:
        """Add a node, merging attrs if it already exists."""
        if self.g.has_node(node.id):
            existing = self.g.nodes[node.id]
            existing.setdefault("attrs", {}).update(node.attrs)
            return
        self.g.add_node(
            node.id,
            kind=node.kind,
            name=node.name,
            file=node.file,
            line=node.line,
            attrs=dict(node.attrs),
        )

    def add_edge(self, edge: Edge) -> None:
        """Add an edge. ``src``/``dst`` nodes are auto-created as placeholders if missing."""
        if not self.g.has_node(edge.src):
            self.g.add_node(edge.src, kind="Unknown", name=edge.src, attrs={})
        if not self.g.has_node(edge.dst):
            self.g.add_node(edge.dst, kind="Unknown", name=edge.dst, attrs={})
        self.g.add_edge(edge.src, edge.dst, key=edge.kind, kind=edge.kind, attrs=dict(edge.attrs))

    def extend(self, nodes: list[Node], edges: list[Edge]) -> None:
        """Bulk insert nodes then edges."""
        for n in nodes:
            self.add_node(n)
        for e in edges:
            self.add_edge(e)

    # ---- post-processing ---------------------------------------------

    def resolve_calls(self) -> int:
        """Rewire ``Unresolved:<name>`` CALLS edges to concrete Function nodes when unique.

        Returns the number of edges resolved.
        """
        # Index function nodes by short name (last segment of qualname).
        by_name: dict[str, list[str]] = {}
        for node_id, data in self.g.nodes(data=True):
            if data.get("kind") == KIND_FUNCTION:
                short = str(data.get("name", "")).rsplit(".", 1)[-1]
                by_name.setdefault(short, []).append(node_id)

        resolved = 0
        rewires: list[tuple[str, str, str, dict]] = []
        for src, dst, key, data in list(self.g.edges(keys=True, data=True)):
            if data.get("kind") != EDGE_CALLS:
                continue
            if not dst.startswith("Unresolved:"):
                continue
            short = dst.split(":", 1)[1]
            candidates = by_name.get(short, [])
            if len(candidates) == 1:
                rewires.append((src, dst, candidates[0], dict(data)))
                resolved += 1
            # If 0 or >1 candidates: leave as Unresolved (ambiguous or external).

        for src, old_dst, new_dst, data in rewires:
            self.g.remove_edge(src, old_dst, key=EDGE_CALLS)
            self.g.add_edge(src, new_dst, key=EDGE_CALLS, **data)

        # Drop any orphan Unresolved nodes that no longer have edges.
        orphans = [
            n for n, d in self.g.nodes(data=True)
            if d.get("kind") == "Unknown"
            and n.startswith("Unresolved:")
            and self.g.degree(n) == 0
        ]
        for n in orphans:
            self.g.remove_node(n)

        return resolved

    # ---- persistence --------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a JSON-friendly dict using node-link form."""
        return nx.node_link_data(self.g, edges="edges")

    def save(self, path: str | Path) -> None:
        """Write JSON to ``path`` (creates parent dirs)."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> GraphStore:
        """Load a graph previously saved with ``save``."""
        store = cls()
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        store.g = nx.node_link_graph(data, multigraph=True, directed=True, edges="edges")
        return store

    # ---- introspection ------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """Summary counts by node kind and edge kind."""
        node_counts: dict[str, int] = {}
        for _, d in self.g.nodes(data=True):
            node_counts[d.get("kind", "Unknown")] = node_counts.get(d.get("kind", "Unknown"), 0) + 1
        edge_counts: dict[str, int] = {}
        for _, _, d in self.g.edges(data=True):
            edge_counts[d.get("kind", "?")] = edge_counts.get(d.get("kind", "?"), 0) + 1
        return {
            "nodes": self.g.number_of_nodes(),
            "edges": self.g.number_of_edges(),
            "by_node_kind": node_counts,
            "by_edge_kind": edge_counts,
        }
