---
description: Re-scan source files and regenerate the code inventory
agent: Reviewer
tools: ['search', 'read', 'edit']
---

# Update Code Inventory

Scan all source files in `src/` and regenerate `docs/CODE_INVENTORY.md`.

## Instructions

1. Read the current `docs/CODE_INVENTORY.md` to understand the existing format.
2. Recursively scan all files in `src/`.
3. For each source file, extract:
   - **File path** and one-line purpose
   - **Every exported symbol**: functions, classes, constants, types/interfaces
   - For functions: name, parameters, return type, one-line description
   - For classes: name, key methods, one-line description
   - For constants: name, type, value summary
4. Update `docs/CODE_INVENTORY.md` with the complete registry.
5. Flag any symbols that appear to be **duplicates** (similar names or purposes).
6. Report what changed since the last inventory.
