"""Validate all playbook files in docs/playbooks/ parse correctly.

Usage:
    python scripts/validate-playbooks.py

Exit code:
    0 — all playbooks valid
    1 — one or more playbooks failed validation
"""

import sys
from pathlib import Path

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from utils.playbook_parser import parse_all_playbooks  # noqa: E402

PLAYBOOK_DIR = str(Path(__file__).resolve().parent.parent / "docs" / "playbooks")


def main() -> int:
    try:
        chunks = parse_all_playbooks(PLAYBOOK_DIR)
        print(f"✅ All {len(chunks)} playbooks valid.")
        return 0
    except Exception as exc:
        print(f"❌ Playbook validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
