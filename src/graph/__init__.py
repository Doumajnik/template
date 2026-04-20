"""Code intelligence graph: nodes/edges representing functions, files, calls, imports.

Agent-facing entry points live in :mod:`src.graph.api` — every function there
auto-ensures the graph is fresh before answering. Pure store-based queries live
in :mod:`src.graph.queries`.
"""

from src.graph.models import Edge, Node

__all__ = ["Edge", "Node"]
