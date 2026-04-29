"""Propagate sub-agent model assignments from AGENTS.md to .agent.md files.

The Sub-Agent Roster table in AGENTS.md (between the
``<!-- AGENT_MODEL_TABLE_START -->`` / ``<!-- AGENT_MODEL_TABLE_END -->``
markers) is the single source of truth for which model each sub-agent
uses. This script reads that table and updates the ``model:`` line in
the YAML frontmatter of every referenced ``.agent.md`` file so the two
cannot drift.

Usage::

    python scripts/update-agent-model.py            # apply changes
    python scripts/update-agent-model.py --check    # exit 1 on drift, no writes
    python scripts/update-agent-model.py --dry-run  # show diffs, no writes

Exit codes:
    0  no drift / all updates applied
    1  drift detected (--check) or unrecoverable error
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_MD = ROOT / "AGENTS.md"

TABLE_START = "<!-- AGENT_MODEL_TABLE_START -->"
TABLE_END = "<!-- AGENT_MODEL_TABLE_END -->"

# Captures the path inside backticks in the last column (e.g.
# `.github/agents/discovery.agent.md`) and the model in column 3.
ROW_RE = re.compile(
    r"^\|\s*\*\*(?P<name>[^*]+?)\*\*\s*"
    r"\|\s*(?P<resp>.+?)\s*"
    r"\|\s*(?P<model>[^|]+?)\s*"
    r"\|\s*`(?P<path>[^`]+?)`\s*\|\s*$"
)

FRONTMATTER_MODEL_RE = re.compile(
    r"^(model:\s*)(['\"]?)([^'\"\n]+?)\2\s*$",
    re.MULTILINE,
)


def parse_roster(agents_md_text: str) -> list[tuple[str, str, str]]:
    """Return ``[(agent_name, model, agent_file_path), ...]`` from AGENTS.md.

    Only rows that fall inside the table-marker block are considered, so
    other tables in the file are not picked up by accident.
    """
    if TABLE_START not in agents_md_text or TABLE_END not in agents_md_text:
        raise SystemExit(
            f"❌ AGENTS.md is missing {TABLE_START} / {TABLE_END} markers"
        )
    block = agents_md_text.split(TABLE_START, 1)[1].split(TABLE_END, 1)[0]
    rows: list[tuple[str, str, str]] = []
    for line in block.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        rows.append(
            (
                match.group("name").strip(),
                match.group("model").strip(),
                match.group("path").strip(),
            )
        )
    if not rows:
        raise SystemExit("❌ no roster rows parsed from AGENTS.md")
    return rows


def update_agent_file(
    path: Path, target_model: str, *, dry_run: bool, check_only: bool
) -> str:
    """Update one ``.agent.md`` frontmatter; return a status string."""
    if not path.exists():
        return f"❌ missing file: {path.relative_to(ROOT)}"

    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_MODEL_RE.search(text)
    if not match:
        return (
            f"❌ {path.relative_to(ROOT)}: no `model:` line in frontmatter"
        )
    current = match.group(3).strip()
    if current == target_model:
        return f"✓  {path.relative_to(ROOT)}: already {target_model}"

    if check_only:
        return (
            f"❌ {path.relative_to(ROOT)}: drift "
            f"(file={current!r}, AGENTS.md={target_model!r})"
        )

    new_line = f"{match.group(1)}{target_model}"
    new_text = (
        text[: match.start()] + new_line + text[match.end():]
    )
    if dry_run:
        return (
            f"~  {path.relative_to(ROOT)}: would update "
            f"{current!r} → {target_model!r}"
        )
    path.write_text(new_text, encoding="utf-8")
    return (
        f"✏  {path.relative_to(ROOT)}: {current!r} → {target_model!r}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any agent file has drift; do not write",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show changes that would be made without writing",
    )
    args = parser.parse_args()

    rows = parse_roster(AGENTS_MD.read_text(encoding="utf-8"))

    statuses = [
        update_agent_file(
            ROOT / rel_path,
            model,
            dry_run=args.dry_run,
            check_only=args.check,
        )
        for _name, model, rel_path in rows
    ]
    for status in statuses:
        print(status)

    has_failure = any(s.startswith("❌") for s in statuses)
    has_change = any(s.startswith(("✏", "~")) for s in statuses)

    print()
    print(f"Processed {len(rows)} agent(s).")
    if args.check and has_failure:
        print("Drift detected. Run without --check to apply.")
        return 1
    if has_failure and not args.check:
        return 1
    if args.dry_run and has_change:
        print("Dry-run only. Re-run without --dry-run to apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
