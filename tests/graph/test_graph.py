"""Tests for the code-intelligence graph: extractors, store, builder, queries."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from src.graph.builder import build_graph
from src.graph.extractors.js_ts import extract_js_ts
from src.graph.extractors.python_ast import extract_python
from src.graph.models import EDGE_CALLS, EDGE_DEFINED_IN, EDGE_IMPORTS, KIND_FUNCTION
from src.graph.queries import (
    callees_of,
    callers_of,
    dead_code,
    hotspots,
    shortest_call_path,
)
from src.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Python extractor
# ---------------------------------------------------------------------------


def test_python_extracts_top_level_function():
    src = "def foo():\n    pass\n"
    nodes, _ = extract_python("a.py", src)
    fns = [n for n in nodes if n.kind == KIND_FUNCTION]
    assert any(n.name == "foo" for n in fns)


def test_python_extracts_method_qualname():
    src = textwrap.dedent("""
        class A:
            def method(self):
                pass
    """)
    nodes, _ = extract_python("a.py", src)
    fns = {n.name for n in nodes if n.kind == KIND_FUNCTION}
    assert "A.method" in fns


def test_python_emits_call_edges():
    src = textwrap.dedent("""
        def helper():
            pass
        def main():
            helper()
            helper()
    """)
    _, edges = extract_python("a.py", src)
    calls = [e for e in edges if e.kind == EDGE_CALLS]
    assert any(e.dst == "Unresolved:helper" for e in calls)
    assert sum(1 for e in calls if e.dst == "Unresolved:helper") == 2


def test_python_emits_import_edges():
    src = "import os\nfrom pathlib import Path\n"
    _, edges = extract_python("a.py", src)
    imports = {e.dst for e in edges if e.kind == EDGE_IMPORTS}
    assert "Module:os" in imports
    assert "Module:pathlib" in imports


def test_python_handles_syntax_error_gracefully():
    nodes, edges = extract_python("bad.py", "def (")
    assert nodes == [] and edges == []


def test_python_async_function():
    src = "async def aio():\n    pass\n"
    nodes, _ = extract_python("a.py", src)
    fn = next(n for n in nodes if n.kind == KIND_FUNCTION and n.name == "aio")
    assert fn.attrs.get("is_async") is True


# ---------------------------------------------------------------------------
# JS/TS extractor
# ---------------------------------------------------------------------------


def test_js_extracts_function_declaration():
    nodes, _ = extract_js_ts("a.js", "function foo() { return 1; }", "javascript")
    assert any(n.kind == KIND_FUNCTION and n.name == "foo" for n in nodes)


def test_js_extracts_arrow_assigned_to_const():
    nodes, _ = extract_js_ts("a.js", "const bar = (x) => x + 1;", "javascript")
    assert any(n.kind == KIND_FUNCTION and n.name == "bar" for n in nodes)


def test_js_call_edge_from_caller_to_callee():
    src = "function a() {} function b() { a(); a(); }"
    _, edges = extract_js_ts("a.js", src, "javascript")
    calls = [e for e in edges if e.kind == EDGE_CALLS and e.dst == "Unresolved:a"]
    assert len(calls) == 2


def test_ts_extracts_typed_function():
    src = "function add(x: number, y: number): number { return x + y; }"
    nodes, _ = extract_js_ts("a.ts", src, "typescript")
    assert any(n.kind == KIND_FUNCTION and n.name == "add" for n in nodes)


def test_js_import_edge():
    src = 'import { x } from "./mod";\n'
    _, edges = extract_js_ts("a.js", src, "javascript")
    imports = {e.dst for e in edges if e.kind == EDGE_IMPORTS}
    assert "Module:./mod" in imports


def test_js_method_in_class():
    src = "class C { greet() { return 1; } }"
    nodes, _ = extract_js_ts("a.js", src, "javascript")
    fn_names = {n.name for n in nodes if n.kind == KIND_FUNCTION}
    assert any("greet" in name for name in fn_names)


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


def test_store_resolves_unique_call_target():
    store = GraphStore()
    nodes, edges = extract_python(
        "a.py",
        textwrap.dedent("""
            def helper():
                pass
            def main():
                helper()
        """),
    )
    store.extend(nodes, edges)
    resolved = store.resolve_calls()
    assert resolved == 1
    # The unresolved placeholder should be gone.
    assert not store.g.has_node("Unresolved:helper")


def test_store_save_and_load_roundtrip(tmp_path: Path):
    store = GraphStore()
    nodes, edges = extract_python("a.py", "def foo(): pass\ndef bar(): foo()\n")
    store.extend(nodes, edges)
    store.resolve_calls()
    out = tmp_path / "g.json"
    store.save(out)

    loaded = GraphStore.load(out)
    assert loaded.stats()["nodes"] == store.stats()["nodes"]
    assert loaded.stats()["edges"] == store.stats()["edges"]


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def test_builder_walks_directory(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    (tmp_path / "b.ts").write_text("function bar() {}\n")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "skip.js").write_text("function skipme() {}\n")

    store, report = build_graph(tmp_path)
    assert report["files_processed"] == 2
    fn_names = {
        d["name"] for _, d in store.g.nodes(data=True) if d.get("kind") == KIND_FUNCTION
    }
    assert "foo" in fn_names
    assert "bar" in fn_names
    assert "skipme" not in fn_names  # excluded dir


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_store(tmp_path: Path) -> GraphStore:
    (tmp_path / "x.py").write_text(
        textwrap.dedent("""
            def leaf(): pass
            def mid(): leaf()
            def top(): mid()
            def orphan(): pass
        """)
    )
    store, _ = build_graph(tmp_path)
    return store


def test_callers_finds_direct_caller(sample_store: GraphStore):
    result = callers_of(sample_store, "leaf", depth=1)
    assert any("mid" in r for r in result)


def test_callers_transitive_depth(sample_store: GraphStore):
    result = callers_of(sample_store, "leaf", depth=5)
    names = " ".join(result)
    assert "mid" in names and "top" in names


def test_callees_finds_direct_callee(sample_store: GraphStore):
    result = callees_of(sample_store, "top", depth=1)
    assert any("mid" in r for r in result)


def test_dead_code_finds_orphan(sample_store: GraphStore):
    result = dead_code(sample_store)
    # `top` and `orphan` have no callers; `mid` and `leaf` do.
    assert any("orphan" in r for r in result)
    assert any("top" in r for r in result)
    assert not any(r.endswith("::Function:mid") for r in result)


def test_hotspots_orders_by_callers(sample_store: GraphStore):
    result = hotspots(sample_store, top=5)
    # Each of leaf/mid has exactly one caller in this sample.
    assert any("leaf" in r[0] for r in result)


def test_shortest_call_path(sample_store: GraphStore):
    path = shortest_call_path(sample_store, "top", "leaf")
    assert path is not None
    assert "top" in path[0] and "leaf" in path[-1]
    assert len(path) == 3  # top -> mid -> leaf


def test_shortest_call_path_no_path(sample_store: GraphStore):
    assert shortest_call_path(sample_store, "top", "orphan") is None
