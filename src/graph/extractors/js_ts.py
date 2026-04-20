"""JavaScript / TypeScript / TSX extractor using tree-sitter.

Emits Function/Class/File/Module nodes and CALLS/DEFINED_IN/CONTAINS/IMPORTS
edges. Handles function declarations, method definitions, arrow functions
assigned to const/let/var, and class declarations.
"""

from typing import Any

from tree_sitter_language_pack import get_parser

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

_FUNC_NODE_TYPES = {
    "function_declaration",
    "function_expression",
    "method_definition",
    "arrow_function",
    "generator_function_declaration",
}
_CLASS_NODE_TYPES = {"class_declaration"}


def extract_js_ts(
    file_path: str, source: str, language: str
) -> tuple[list[Node], list[Edge]]:
    """Extract nodes and edges from a JS/TS/TSX source file.

    ``language`` must be one of: ``javascript``, ``typescript``, ``tsx``.
    """
    parser = get_parser(language)
    src_bytes = source.encode("utf-8")
    tree = parser.parse(src_bytes)

    nodes: list[Node] = []
    edges: list[Edge] = []

    fid = file_id(file_path)
    nodes.append(Node(id=fid, kind=KIND_FILE, name=file_path, file=file_path))

    state = _WalkState(file_path=file_path, src_bytes=src_bytes)
    _walk(tree.root_node, state, scope=[], current_func=None)

    for func in state.functions:
        node_id = function_id(file_path, func["qualname"])
        nodes.append(
            Node(
                id=node_id,
                kind=KIND_FUNCTION,
                name=func["qualname"],
                file=file_path,
                line=func["line"],
            )
        )
        edges.append(Edge(src=node_id, dst=fid, kind=EDGE_DEFINED_IN))
        edges.append(Edge(src=fid, dst=node_id, kind=EDGE_CONTAINS))

    for cls in state.classes:
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

    for caller_qualname, callee_name, line in state.calls:
        src_id = function_id(file_path, caller_qualname)
        dst_id = f"Unresolved:{callee_name}"
        edges.append(
            Edge(src=src_id, dst=dst_id, kind=EDGE_CALLS, attrs={"line": line})
        )

    for module_name, line in state.imports:
        mid = module_id(module_name)
        nodes.append(Node(id=mid, kind=KIND_MODULE, name=module_name))
        edges.append(Edge(src=fid, dst=mid, kind=EDGE_IMPORTS, attrs={"line": line}))

    return nodes, edges


class _WalkState:
    """Mutable accumulator passed through the recursive walk."""

    def __init__(self, file_path: str, src_bytes: bytes) -> None:
        self.file_path = file_path
        self.src_bytes = src_bytes
        self.functions: list[dict] = []
        self.classes: list[dict] = []
        self.calls: list[tuple[str, str, int]] = []
        self.imports: list[tuple[str, int]] = []

    def text(self, node: Any) -> str:
        return self.src_bytes[node.start_byte : node.end_byte].decode(
            "utf-8", errors="replace"
        )


def _walk(node: Any, state: _WalkState, scope: list[str], current_func: str | None) -> None:
    """Recursively walk the syntax tree, recording defs and calls."""
    new_scope = scope
    new_current = current_func

    if node.type in _FUNC_NODE_TYPES:
        name = _func_name(node, state)
        qualname = ".".join([*scope, name]) if scope else name
        state.functions.append({"qualname": qualname, "line": node.start_point[0] + 1})
        new_scope = [*scope, name]
        new_current = qualname

    elif node.type in _CLASS_NODE_TYPES:
        name = _named_child_text(node, "name", state) or "<anonymous>"
        qualname = ".".join([*scope, name]) if scope else name
        state.classes.append({"qualname": qualname, "line": node.start_point[0] + 1})
        new_scope = [*scope, name]

    elif node.type == "lexical_declaration" or node.type == "variable_declaration":
        # const foo = () => ...   /   const foo = function() ...
        for declarator in node.children:
            if declarator.type == "variable_declarator":
                _handle_var_decl(declarator, state, scope, current_func)
        # Children handled; don't double-walk into them.
        return

    elif node.type == "call_expression" and current_func:
        callee = _callee_name(node, state)
        if callee:
            state.calls.append((current_func, callee, node.start_point[0] + 1))

    elif node.type in ("import_statement", "import_clause"):
        mod = _import_source(node, state)
        if mod:
            state.imports.append((mod, node.start_point[0] + 1))

    for child in node.children:
        _walk(child, state, new_scope, new_current)


def _handle_var_decl(
    declarator: Any, state: _WalkState, scope: list[str], current_func: str | None
) -> None:
    """Handle ``const foo = () => ...`` and similar arrow/function assignments."""
    name_node = declarator.child_by_field_name("name")
    value_node = declarator.child_by_field_name("value")
    if name_node and value_node and value_node.type in _FUNC_NODE_TYPES:
        name = state.text(name_node)
        qualname = ".".join([*scope, name]) if scope else name
        state.functions.append({"qualname": qualname, "line": value_node.start_point[0] + 1})
        # Walk the function body with this name in scope.
        new_scope = [*scope, name]
        for child in value_node.children:
            _walk(child, state, new_scope, qualname)
    else:
        # Walk normally.
        for child in declarator.children:
            _walk(child, state, scope, current_func)


def _func_name(node: Any, state: _WalkState) -> str:
    name_node = node.child_by_field_name("name")
    if name_node:
        return state.text(name_node)
    return "<anonymous>"


def _named_child_text(node: Any, field: str, state: _WalkState) -> str | None:
    child = node.child_by_field_name(field)
    return state.text(child) if child else None


def _callee_name(call_node: Any, state: _WalkState) -> str | None:
    func = call_node.child_by_field_name("function")
    if not func:
        return None
    if func.type == "identifier":
        return state.text(func)
    if func.type == "member_expression":
        prop = func.child_by_field_name("property")
        if prop:
            return state.text(prop)
    return None


def _import_source(node: Any, state: _WalkState) -> str | None:
    """Pull the module specifier out of an import statement."""
    for child in node.children:
        if child.type == "string":
            text = state.text(child)
            return text.strip("\"'`")
    return None
