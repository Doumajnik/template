"""Summarize collected feedback into a human-readable report.

Reads feedback/.feedback-collected.json (produced by collect-feedback.py),
groups entries by category, identifies common themes, and outputs a summary.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = REPO_ROOT / "feedback" / ".feedback-collected.json"
OUTPUT_FILE = REPO_ROOT / "feedback" / ".feedback-summary.md"

STOP_WORDS = frozenset(
    "the a an and or but in on at to for of is it that this with from by as are was be".split()
)


def load_feedback(path: Path) -> dict:
    """Load the collected JSON, returning an empty structure on failure."""
    if not path.exists():
        return {"automatic_feedback": [], "manual_notes": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        print("Warning: malformed JSON in", path)
        return {"automatic_feedback": [], "manual_notes": []}


def extract_keywords(texts: list[str], top_n: int = 10) -> list[tuple[str, int]]:
    """Return the most frequent meaningful words across all texts."""
    counter: Counter[str] = Counter()
    for text in texts:
        words = re.findall(r"[a-z]{3,}", text.lower())
        counter.update(w for w in words if w not in STOP_WORDS)
    return counter.most_common(top_n)


def format_summary(data: dict) -> str:
    """Build a Markdown summary string from collected feedback data."""
    auto = data.get("automatic_feedback", [])
    notes = data.get("manual_notes", [])
    collected_at = data.get("collected_at", "unknown")

    lines = [
        "# Feedback Summary",
        "",
        f"Generated from data collected at: {collected_at}",
        "",
        "## Statistics",
        "",
        f"- Automatic entries: {len(auto)}",
        f"- Manual notes: {len(notes)}",
        f"- Total items: {len(auto) + len(notes)}",
        "",
    ]

    # Common themes
    all_text = [e.get("body", "") for e in auto] + notes
    if all_text:
        keywords = extract_keywords(all_text)
        if keywords:
            lines.append("## Common Themes")
            lines.append("")
            for word, count in keywords:
                lines.append(f"- **{word}** ({count})")
            lines.append("")

    # Automatic feedback
    if auto:
        lines.append("## Automatic Feedback (Retrospective Agent)")
        lines.append("")
        for i, entry in enumerate(auto, 1):
            title = entry.get("title", "Untitled")
            body = entry.get("body", "").strip()
            lines.append(f"### {i}. {title}")
            lines.append("")
            lines.append(body if body else "*No body*")
            lines.append("")
    else:
        lines.append("## Automatic Feedback")
        lines.append("")
        lines.append("*No automatic feedback entries.*")
        lines.append("")

    # Manual notes
    if notes:
        lines.append("## Manual Notes")
        lines.append("")
        for i, note in enumerate(notes, 1):
            lines.append(f"### Note {i}")
            lines.append("")
            lines.append(note)
            lines.append("")
    else:
        lines.append("## Manual Notes")
        lines.append("")
        lines.append("*No manual notes.*")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """CLI entry point for feedback summarization."""
    parser = argparse.ArgumentParser(description="Summarize collected feedback.")
    parser.add_argument(
        "--write", action="store_true", help="Write summary to feedback/.feedback-summary.md"
    )
    parser.add_argument(
        "--input", type=Path, default=INPUT_FILE, help="Path to collected JSON file"
    )
    args = parser.parse_args()

    data = load_feedback(args.input)
    summary = format_summary(data)
    print(summary)

    if args.write:
        OUTPUT_FILE.write_text(summary, encoding="utf-8")
        print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
