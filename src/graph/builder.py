"""Walk a project directory, dispatch extractors, populate a GraphStore."""

from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

from src.graph.extractors import get_extractor
from src.graph.store import GraphStore

# Directory names skipped by default during traversal.
DEFAULT_EXCLUDES = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build",
    ".next", ".turbo", "coverage", ".tox",
})


def iter_source_files(
    root: str | Path,
    excludes: Iterable[str] = DEFAULT_EXCLUDES,
) -> list[Path]:
    """Yield all files under ``root`` whose extension has a registered extractor."""
    root_path = Path(root)
    excludes_set = set(excludes)
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in excludes_set]
        for filename in filenames:
            full = Path(dirpath) / filename
            if get_extractor(str(full)) is not None:
                out.append(full)
    return sorted(out)


def build_graph(
    root: str | Path,
    excludes: Iterable[str] = DEFAULT_EXCLUDES,
) -> tuple[GraphStore, dict]:
    """Build a graph from all supported source files under ``root``.

    Returns the populated store and a small report dict.
    """
    root_path = Path(root).resolve()
    store = GraphStore()
    files_processed = 0
    files_failed = 0

    for file in iter_source_files(root_path, excludes):
        extractor = get_extractor(str(file))
        if extractor is None:
            continue
        try:
            source = file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            files_failed += 1
            continue
        rel_path = str(file.relative_to(root_path)).replace(os.sep, "/")
        try:
            nodes, edges = extractor(rel_path, source)
        except Exception:  # noqa: BLE001 - extractor crashes shouldn't kill the build
            files_failed += 1
            continue
        store.extend(nodes, edges)
        files_processed += 1

    resolved = store.resolve_calls()
    report = {
        "root": str(root_path),
        "files_processed": files_processed,
        "files_failed": files_failed,
        "calls_resolved": resolved,
    }
    return store, report
