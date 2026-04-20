"""Python source extractor using the stdlib ``ast`` module.

Emits Function/Class/File/Module nodes and CALLS/DEFINED_IN/CONTAINS/IMPORTS
edges. Call resolution is best-effort by name (last segment of attribute chain),
which is the common limitation of static analysis.
"""

import ast

from src.graph.models import (
    EDGE_CALLS,
    EDGE_CONTAINS,
    EDGE_DEFINED_IN,
    EDGE_IMPORTS,
    KIND_CLASS,
    KIND_FILE,
    KIND_FUNCTION,
    KIND_MODULE,
    Edge,
    Node,
    class_id,
    file_id,
    function_id,
    module_id,
)


def extract_python(file_path: str, source: str) -> tuple[list[Node], list[Edge]]:
    """Extract nodes and edges from a Python source file."""
    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        return [], []

    nodes: list[Node] = []
    edges: list[Edge] = []

    fid = file_id(file_path)
    nodes.append(Node(id=fid, kind=KIND_FILE, name=file_path, file=file_path))

    visitor = _PythonVisitor(file_path)
    visitor.visit(tree)

    for func in visitor.functions:
        node_id = function_id(file_path, func["qualname"])
        nodes.append(
            Node(
                id=node_id,
                kind=KIND_FUNCTION,
                name=func["qualname"],
                file=file_path,
                line=func["line"],
                attrs={"is_async": func["is_async"]},
            )
        )
        edges.append(Edge(src=node_id, dst=fid, kind=EDGE_DEFINED_IN))
        edges.append(Edge(src=fid, dst=node_id, kind=EDGE_CONTAINS))

    for cls in visitor.classes:
        node_id = class_id(file_path, cls["qualname"])
        nodes.append(
            Node(
                id=node_id,
                kind=KIND_CLASS,
                name=cls["qualname"],
                file=file_path,
                line=cls["line"],
            )
        )
        edges.append(Edge(src=node_id, dst=fid, kind=EDGE_DEFINED_IN))
        edges.append(Edge(src=fid, dst=node_id, kind=EDGE_CONTAINS))

    for caller_qualname, callee_name, line in visitor.calls:
        src_id = function_id(file_path, caller_qualname)
        # Unresolved at extract time: store the callee as a name reference.
        # The store-merge step rewires these to concrete function ids when possible.
        dst_id = f"Unresolved:{callee_name}"
        edges.append(
            Edge(src=src_id, dst=dst_id, kind=EDGE_CALLS, attrs={"line": line})
        )

    for module_name, line in visitor.imports:
        mid = module_id(module_name)
        nodes.append(Node(id=mid, kind=KIND_MODULE, name=module_name))
        edges.append(Edge(src=fid, dst=mid, kind=EDGE_IMPORTS, attrs={"line": line}))

    return nodes, edges


class _PythonVisitor(ast.NodeVisitor):
    """AST walker that records functions, classes, calls, and imports."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.functions: list[dict] = []
        self.classes: list[dict] = []
        self.calls: list[tuple[str, str, int]] = []
        self.imports: list[tuple[str, int]] = []
        self._scope: list[str] = []

    def _qualname(self, name: str) -> str:
        return ".".join([*self._scope, name]) if self._scope else name

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self._handle_func(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
        self._handle_func(node, is_async=True)

    def _handle_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef, *, is_async: bool) -> None:
        qualname = self._qualname(node.name)
        self.functions.append(
            {"qualname": qualname, "line": node.lineno, "is_async": is_async}
        )
        self._scope.append(node.name)
        for child in node.body:
            for sub in ast.walk(child):
                if isinstance(sub, ast.Call):
                    callee = _call_name(sub.func)
                    if callee:
                        self.calls.append((qualname, callee, sub.lineno))
        # Visit nested defs for nodes/edges, but skip re-walking calls (already done).
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.visit(child)
        self._scope.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
        qualname = self._qualname(node.name)
        self.classes.append({"qualname": qualname, "line": node.lineno})
        self._scope.append(node.name)
        for child in node.body:
            self.visit(child)
        self._scope.pop()

    def visit_Import(self, node: ast.Import) -> None:  # noqa: N802
        for alias in node.names:
            self.imports.append((alias.name, node.lineno))

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # noqa: N802
        if node.module:
            self.imports.append((node.module, node.lineno))


def _call_name(func_expr: ast.expr) -> str | None:
    """Extract the most useful callee name from a Call.func expression."""
    if isinstance(func_expr, ast.Name):
        return func_expr.id
    if isinstance(func_expr, ast.Attribute):
        return func_expr.attr
    return None
