"""Freshness check + auto-rebuild for the code intelligence graph.

Strategy: cheap mtime comparison. The graph file's mtime is compared against the
newest source file under the project root. If anything is newer, rebuild.
Skipped if the graph file is fresh — typical "is it stale?" check is <50ms on
medium repos.
"""

from __future__ import annotations

import os
from pathlib import Path

from src.graph.builder import DEFAULT_EXCLUDES, build_graph, iter_source_files
from src.graph.store import GraphStore

DEFAULT_DB_PATH = ".ai/graph/code.json"
DEFAULT_ROOT = "."


def is_stale(
    db_path: str | Path = DEFAULT_DB_PATH,
    root: str | Path = DEFAULT_ROOT,
) -> bool:
    """Return True when the graph DB is missing or older than any source file."""
    db = Path(db_path)
    if not db.exists():
        return True
    db_mtime = db.stat().st_mtime
    root_path = Path(root)
    # Walk only known source-file extensions; cheap because the iterator already
    # honours DEFAULT_EXCLUDES (no node_modules, .venv, etc.).
    for src_file in iter_source_files(root_path):
        try:
            if src_file.stat().st_mtime > db_mtime:
                return True
        except OSError:
            continue
    return False


def ensure_fresh(
    db_path: str | Path = DEFAULT_DB_PATH,
    root: str | Path = DEFAULT_ROOT,
    *,
    force: bool = False,
) -> tuple[GraphStore, dict, bool]:
    """Load the graph, rebuilding first if it's missing or stale.

    Returns ``(store, report, rebuilt)``. ``report`` is the build report when a
    rebuild ran, otherwise ``{"skipped": True}``. ``rebuilt`` indicates whether
    a build actually happened.
    """
    if force or is_stale(db_path, root):
        store, report = build_graph(root)
        store.save(db_path)
        return store, report, True
    store = GraphStore.load(db_path)
    return store, {"skipped": True, "db": str(db_path)}, False
