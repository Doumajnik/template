"""Validate consistency between .ai/TOOL_MANIFEST.md and scripts/tool-guard.py.

The manifest is the human-readable source of truth for which agents are
allowed to use which tools. The tool-guard hook is the runtime enforcer.
This script reports drift between the two so they cannot disagree silently.

Strategy (loose on column naming, strict on agent membership):

- Extract every agent slug marked **DENIED** (or '❌') in any manifest table.
- Extract every agent slug appearing in any *_DENIED_AGENTS literal in
  scripts/tool-guard.py.
- Report agents that appear in one side but not the other.

Exit code 0 = no drift; non-zero = drift found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".ai" / "TOOL_MANIFEST.md"
GUARD = ROOT / "scripts" / "tool-guard.py"


def _slug(name: str) -> str:
    """Normalise an agent label to alphanumerics-only for comparison.

    Accepts 'Test Writer', 'test_writer', 'test-writer', 'testwriter' and
    returns the same canonical form 'testwriter' for all of them. The
    tool-guard.py file intentionally lists multiple separator variants per
    agent, so collapsing separators avoids false-positive drift.
    """
    cleaned = re.sub(r"[*_`]", "", name)
    return re.sub(r"[^a-z0-9]+", "", cleaned.strip().lower())


def parse_guard_denied_agents(guard_text: str) -> set[str]:
    """Union of every agent slug appearing in any *_DENIED_AGENTS literal."""
    denied: set[str] = set()
    pattern = re.compile(
        r"[A-Z_]+_DENIED_AGENTS\s*[:=][^=]*?[\{\[\(]([^\}\]\)]*)[\}\]\)]",
        re.MULTILINE | re.DOTALL,
    )
    for match in pattern.finditer(guard_text):
        body = match.group(1)
        for item in re.split(r"[,\n]", body):
            value = item.strip().strip("'\"")
            if value and not value.startswith("#"):
                denied.add(_slug(value))
    return denied


def parse_manifest_denied_agents(manifest_text: str) -> set[str]:
    """Every agent slug whose manifest row contains 'DENIED' or '❌'."""
    denied: set[str] = set()
    skip_labels = {"allothers", "everyoneelse", "allotheragents"}
    for line in manifest_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0].lower()
        if first in {"agent", ""} or first.startswith("agent "):
            continue
        row_text = " ".join(cells[1:]).upper()
        if "DENIED" in row_text or "❌" in row_text:
            slug = _slug(cells[0])
            if slug and slug not in skip_labels:
                denied.add(slug)
    return denied


def main() -> int:
    if not MANIFEST.exists():
        print(f"❌ manifest not found: {MANIFEST}")
        return 2
    if not GUARD.exists():
        print(f"❌ tool-guard not found: {GUARD}")
        return 2

    manifest_denied = parse_manifest_denied_agents(
        MANIFEST.read_text(encoding="utf-8")
    )
    guard_denied = parse_guard_denied_agents(
        GUARD.read_text(encoding="utf-8")
    )

    only_guard = guard_denied - manifest_denied
    only_manifest = manifest_denied - guard_denied

    drift: list[str] = []
    for agent in sorted(only_guard):
        drift.append(
            f"❌ guard denies tools for '{agent}' "
            f"but manifest does not document it"
        )
    for agent in sorted(only_manifest):
        drift.append(
            f"❌ manifest restricts '{agent}' "
            f"but guard does not enforce it"
        )

    if drift:
        print("Tool manifest / guard drift:")
        for line in drift:
            print(f"  {line}")
        return 1

    print(
        "✅ Tool manifest and tool-guard.py agree on "
        f"{len(manifest_denied)} restricted agent(s): "
        + ", ".join(sorted(manifest_denied))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
