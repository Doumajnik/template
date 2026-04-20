"""Graph node and edge data models."""

from dataclasses import dataclass, field
from typing import Any

# Node kinds
KIND_FILE = "File"
KIND_FUNCTION = "Function"
KIND_CLASS = "Class"
KIND_MODULE = "Module"

# Edge kinds
EDGE_CALLS = "CALLS"
EDGE_DEFINED_IN = "DEFINED_IN"
EDGE_IMPORTS = "IMPORTS"
EDGE_CONTAINS = "CONTAINS"
EDGE_COVERS = "COVERS"

ALL_NODE_KINDS = frozenset({KIND_FILE, KIND_FUNCTION, KIND_CLASS, KIND_MODULE})
ALL_EDGE_KINDS = frozenset(
    {EDGE_CALLS, EDGE_DEFINED_IN, EDGE_IMPORTS, EDGE_CONTAINS, EDGE_COVERS}
)


@dataclass(frozen=True)
class Node:
    """A graph node. `id` is canonical and unique across the graph."""

    id: str
    kind: str
    name: str
    file: str | None = None
    line: int | None = None
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Edge:
    """A directed edge from `src` node id to `dst` node id."""

    src: str
    dst: str
    kind: str
    attrs: dict[str, Any] = field(default_factory=dict)


def function_id(file_path: str, qualname: str) -> str:
    """Canonical id for a function: ``<file>::Function:<qualname>``."""
    return f"{file_path}::Function:{qualname}"


def class_id(file_path: str, qualname: str) -> str:
    """Canonical id for a class."""
    return f"{file_path}::Class:{qualname}"


def file_id(file_path: str) -> str:
    """Canonical id for a file."""
    return f"File:{file_path}"


def module_id(module_name: str) -> str:
    """Canonical id for a module reference (external or unresolved)."""
    return f"Module:{module_name}"
