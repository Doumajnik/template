# Per-File Documentation

This directory contains one Markdown file per source file, describing each file's:

- **Purpose** — what the file does and why it exists
- **Public API** — exported functions, classes, constants with signatures
- **Dependencies** — what it imports and depends on
- **Key Implementation Notes** — important design decisions or gotchas

## Naming Convention

Mirror the `src/` structure. Examples:

- `src/utils/math.py` → `docs/files/utils/math.md`
- `src/services/auth_service.py` → `docs/files/services/auth_service.md`
- `src/config/settings.py` → `docs/files/config/settings.md`

## When to Update

- **After creating a new source file** — create the corresponding doc file.
- **After modifying a source file** — update the doc to reflect changes.
- **The planner reads these** instead of reading raw source code. Keep them accurate.
