"""Tests for freshness check and auto-rebuild."""

from __future__ import annotations

import os
import time
from pathlib import Path

from src.graph.freshness import ensure_fresh, is_stale


def _touch(path: Path, mtime: float) -> None:
    """Force a specific mtime on a file (helps avoid filesystem timestamp races)."""
    os.utime(path, (mtime, mtime))


def test_is_stale_when_db_missing(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    assert is_stale(db, tmp_path) is True


def test_ensure_fresh_creates_db_when_missing(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    _, report, rebuilt = ensure_fresh(db, tmp_path)
    assert rebuilt is True
    assert db.exists()
    assert report["files_processed"] == 1


def test_ensure_fresh_skips_when_up_to_date(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    ensure_fresh(db, tmp_path)
    # Make sure DB is newer than source.
    _touch(tmp_path / "a.py", time.time() - 100)
    _touch(db, time.time())
    _, report, rebuilt = ensure_fresh(db, tmp_path)
    assert rebuilt is False
    assert report.get("skipped") is True


def test_ensure_fresh_rebuilds_after_source_change(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    ensure_fresh(db, tmp_path)
    # Make the DB look old, then touch the source.
    _touch(db, time.time() - 100)
    _touch(tmp_path / "a.py", time.time())
    _, report, rebuilt = ensure_fresh(db, tmp_path)
    assert rebuilt is True
    assert report.get("files_processed") == 1


def test_ensure_fresh_force_rebuild(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    ensure_fresh(db, tmp_path)
    _, report, rebuilt = ensure_fresh(db, tmp_path, force=True)
    assert rebuilt is True
    assert "files_processed" in report


def test_is_stale_ignores_excluded_dirs(tmp_path: Path):
    (tmp_path / "a.py").write_text("def foo(): pass\n")
    db = tmp_path / "graph.json"
    ensure_fresh(db, tmp_path)
    # Newer files inside an excluded dir must NOT mark the DB stale.
    nm = tmp_path / "node_modules"
    nm.mkdir()
    (nm / "ignored.js").write_text("function x(){}\n")
    _touch(db, time.time() - 50)
    _touch(nm / "ignored.js", time.time())
    # Also age a.py so it doesn't trip the check by accident.
    _touch(tmp_path / "a.py", time.time() - 100)
    assert is_stale(db, tmp_path) is False
