# Code Inventory

> **This is a living document.** AI agents MUST update it after creating or modifying any source file.
> Agents MUST search this file before creating new functions, classes, or utilities to prevent duplication.

**Last updated:** *(not yet — no source files exist)*

---

## How to Read This File

Each source file gets a section with:

- **File path** and one-line purpose
- **Symbol table** listing every exported function, class, constant, and type

## How to Update This File

After creating or modifying a source file:

1. Find the section for that file (or create a new one in alphabetical order).
2. Update the symbol table to reflect the current state of the file.
3. Update the "Last updated" timestamp at the top.

### Entry Format

```markdown
### `src/path/to/file.ext`

**Purpose:** One-line description of what this file does.

| Symbol | Type | Signature / Value | Description |
|--------|------|-------------------|-------------|
| `functionName` | function | `(param: Type) → ReturnType` | What it does |
| `ClassName` | class | — | What it represents |
| `CONSTANT_NAME` | const | `"value"` or `Type` | What it holds |
| `TypeName` | type/interface | — | What it describes |
```

---

## Inventory

<!-- 
  Add entries below as source files are created.
  Keep entries in alphabetical order by file path.
  Remove entries when files are deleted.
-->

*No source files yet. The inventory will be populated as the project grows.*
