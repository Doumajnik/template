---
description: Re-scan source files and regenerate the code inventory
agent: Doc Updater
---

# Update Code Inventory

Scan all source files in `src/` and regenerate `docs/CODE_INVENTORY.md`.

## Instructions

1. Read the current `docs/CODE_INVENTORY.md` to understand the existing format.

2. **Read the todo file** in `.ai/todos/` for the current session (if one exists):
   - Check if an inventory update task is listed — mark it as 🔵 in-progress

3. Recursively scan all files in `src/`.

4. For each source file, extract:
   - **File path** and one-line purpose
   - **Every exported symbol**: functions, classes, constants, types/interfaces
   - For functions: name, parameters, return type, one-line description
   - For classes: name, key methods, one-line description
   - For constants: name, type, value summary

5. Update `docs/CODE_INVENTORY.md` with the complete registry.

6. Flag any symbols that appear to be **duplicates** (similar names or purposes).

7. Update `docs/files/` — create or refresh one `.md` per source file using the template at `docs/files/_TEMPLATE.file.md`.

8. **Update the todo file** — mark the inventory update task as ✅ done and append to the Progress Log.

9. Report what changed since the last inventory.
