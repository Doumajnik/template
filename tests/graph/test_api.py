"""Tests for the agent-facing api module (auto-freshness wrappers)."""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from src.graph import api


@pytest.fixture
def project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A temp project with a few Python files; api defaults point at it."""
    (tmp_path / "a.py").write_text(
        "def helper(): pass\n"
        "def main(): helper()\n"
        "def orphan(): pass\n"
    )
    monkeypatch.chdir(tmp_path)
    # api defaults are relative paths (".", ".ai/graph/code.json"); chdir is enough.
    return tmp_path


def test_hotspots_auto_builds_when_missing(project: Path):
    db = project / ".ai" / "graph" / "code.json"
    assert not db.exists()
    result = api.hotspots(top=5)
    assert db.exists()
    assert any("helper" in node_id for node_id, _ in result)


def test_callers_returns_fresh_results_after_edit(project: Path):
    api.hotspots(top=1)  # force initial build
    # Add a new caller of `helper`.
    time.sleep(0.05)  # ensure mtime ticks forward on coarse filesystems
    (project / "b.py").write_text("def extra(): helper()\n")
    os.utime(project / "b.py", (time.time() + 1, time.time() + 1))
    result = api.callers_of("helper", depth=1)
    assert any("extra" in r for r in result)


def test_function_facts_bundle(project: Path):
    facts = api.function_facts("helper")
    assert facts["found"] is True
    assert any("main" in c for c in facts["direct_callers"])
    assert facts["is_dead_code"] is False


def test_function_facts_unknown_name(project: Path):
    facts = api.function_facts("does_not_exist")
    assert facts == {"name": "does_not_exist", "found": False}


def test_dead_code_includes_orphan(project: Path):
    result = api.dead_code()
    assert any("orphan" in r for r in result)


def test_get_store_force_rebuilds(project: Path):
    api.hotspots(top=1)
    db = project / ".ai" / "graph" / "code.json"
    first_mtime = db.stat().st_mtime
    time.sleep(0.05)
    api.get_store(force=True)
    assert db.stat().st_mtime > first_mtime
