"""High-level, agent-facing graph API.

This is what callers should import. Every function automatically ensures the
graph is fresh before answering — agents and helpers don't have to remember to
rebuild. For the pure, store-based versions (used in tests and when you already
hold a ``GraphStore``), import from ``src.graph.queries``.

Usage
-----
>>> from src.graph import api
>>> api.callers_of("parse_playbook_file", depth=3)
['src/utils/playbook_parser.py::Function:parse_all_playbooks']
>>> api.hotspots(top=5)
[('src/utils/playbook_parser.py::Function:_validate_frontmatter', 18), ...]
"""

from __future__ import annotations

from src.graph import queries as _q
from src.graph.freshness import DEFAULT_DB_PATH, DEFAULT_ROOT, ensure_fresh
from src.graph.store import GraphStore


def get_store(
    *,
    db_path: str = DEFAULT_DB_PATH,
    root: str = DEFAULT_ROOT,
    force: bool = False,
) -> GraphStore:
    """Return a fresh ``GraphStore``, rebuilding from source if needed.

    Most callers don't need this — use the convenience functions below. Reach
    for ``get_store`` only when you want to run multiple queries against the
    same snapshot, or you need ad-hoc access to the underlying NetworkX graph.
    """
    store, _, _ = ensure_fresh(db_path, root, force=force)
    return store


# ---------------------------------------------------------------------------
# Convenience wrappers — same signatures as src.graph.queries but auto-fresh.
# ---------------------------------------------------------------------------


def find_functions_by_name(name: str, **kw) -> list[str]:
    """Function node ids whose short name equals ``name``."""
    return _q.find_functions_by_name(get_store(**kw), name)


def callers_of(name: str, depth: int = 1, **kw) -> list[str]:
    """Functions that (transitively, up to ``depth``) call any function named ``name``."""
    return _q.callers_of(get_store(**kw), name, depth=depth)


def callees_of(name: str, depth: int = 1, **kw) -> list[str]:
    """Functions called (transitively, up to ``depth``) by any function named ``name``."""
    return _q.callees_of(get_store(**kw), name, depth=depth)


def dead_code(**kw) -> list[str]:
    """Functions with no incoming CALLS edges (likely unused)."""
    return _q.dead_code(get_store(**kw))


def hotspots(top: int = 10, **kw) -> list[tuple[str, int]]:
    """Most-called functions, ordered by incoming CALLS count."""
    return _q.hotspots(get_store(**kw), top=top)


def shortest_call_path(from_name: str, to_name: str, **kw) -> list[str] | None:
    """Shortest CALLS-only path between any function named ``from_name`` and ``to_name``."""
    return _q.shortest_call_path(get_store(**kw), from_name, to_name)


# ---------------------------------------------------------------------------
# Composite helper for context briefs.
# ---------------------------------------------------------------------------


def function_facts(name: str, *, caller_depth: int = 3, **kw) -> dict:
    """Bundle the most useful facts about a function for an agent brief.

    Returns a single dict with definition sites, callers, callees, and whether
    the function appears to be dead code. One graph load, multiple answers.
    """
    store = get_store(**kw)
    matches = _q.find_functions_by_name(store, name)
    if not matches:
        return {"name": name, "found": False}
    return {
        "name": name,
        "found": True,
        "defined_at": matches,
        "direct_callers": _q.callers_of(store, name, depth=1),
        "transitive_callers": _q.callers_of(store, name, depth=caller_depth),
        "direct_callees": _q.callees_of(store, name, depth=1),
        "is_dead_code": all(node in _q.dead_code(store) for node in matches),
    }
