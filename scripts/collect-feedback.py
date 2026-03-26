"""Collect feedback from FEEDBACK.md and PUSH_NOTE.md into a structured JSON file.

Reads the append-only Retrospective Agent log and optional user push notes,
combines them into a single JSON output at feedback/.feedback-collected.json.
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FEEDBACK_FILE = REPO_ROOT / "feedback" / "FEEDBACK.md"
PUSH_NOTE_FILE = REPO_ROOT / "feedback" / "PUSH_NOTE.md"
OUTPUT_FILE = REPO_ROOT / "feedback" / ".feedback-collected.json"
MARKER = "<!-- Retrospective Agent: append new entries below this line -->"

PUSH_NOTE_HEADER = (
    "# Push Note\n\n"
    "<!-- Add your feedback here before pushing. This file is cleared after each send. -->\n"
    "<!-- Prefix the first line with DRAFT to hold the note without sending. -->\n"
)


def parse_automatic_entries(text: str) -> list[dict]:
    """Extract entries after the HTML comment marker in FEEDBACK.md."""
    idx = text.find(MARKER)
    if idx == -1:
        return []
    content = text[idx + len(MARKER) :].strip()
    if not content:
        return []
    # Split on heading-2 boundaries (each entry starts with ##)
    sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)
    entries = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        heading_match = re.match(r"^## (.+)", section)
        title = heading_match.group(1).strip() if heading_match else "Untitled"
        body = section[heading_match.end() :].strip() if heading_match else section
        entries.append({"title": title, "body": body})
    return entries


def parse_manual_notes(text: str) -> list[str]:
    """Extract non-draft, non-comment lines from PUSH_NOTE.md."""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("DRAFT"):
            return []  # entire note is a draft — skip all
        if stripped.startswith("#") and stripped.startswith("# Push Note"):
            continue
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        lines.append(line)
    content = "\n".join(lines).strip()
    if not content:
        return []
    return [content]


def collect(dry_run: bool = False, clear: bool = False) -> dict:
    """Collect feedback from both sources and return the combined payload."""
    auto_entries: list[dict] = []
    if FEEDBACK_FILE.exists():
        auto_entries = parse_automatic_entries(FEEDBACK_FILE.read_text(encoding="utf-8"))

    manual_notes: list[str] = []
    if PUSH_NOTE_FILE.exists():
        manual_notes = parse_manual_notes(PUSH_NOTE_FILE.read_text(encoding="utf-8"))

    payload = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "automatic_feedback": auto_entries,
        "manual_notes": manual_notes,
    }

    print(f"Collected: {len(auto_entries)} automatic entries, {len(manual_notes)} manual notes")

    if dry_run:
        print("[dry-run] Would write to:", OUTPUT_FILE)
        print(json.dumps(payload, indent=2))
        return payload

    OUTPUT_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Written to {OUTPUT_FILE}")

    if clear and manual_notes:
        PUSH_NOTE_FILE.write_text(PUSH_NOTE_HEADER, encoding="utf-8")
        print("Cleared PUSH_NOTE.md (header preserved)")

    return payload


def main() -> None:
    """CLI entry point for feedback collection."""
    parser = argparse.ArgumentParser(description="Collect project feedback into JSON.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would be collected without writing"
    )
    parser.add_argument(
        "--clear", action="store_true", help="Clear PUSH_NOTE.md after collection"
    )
    args = parser.parse_args()
    collect(dry_run=args.dry_run, clear=args.clear)


if __name__ == "__main__":
    main()
