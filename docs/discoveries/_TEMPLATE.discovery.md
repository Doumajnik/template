# Discovery Summary Template

> **Instructions:** Copy this template to `docs/discoveries/{YYYY-MM-DD}_{topic}.md` when the Discovery Agent analyzes new data.
> Replace the placeholders below. Delete this instruction block.

---

## Overview

<!-- Layer 1: One-paragraph summary — what is this, what does it do, why does it matter? -->

*Replace with a concise overview paragraph.*

---

## Structure Map

<!-- Layer 2: Section-by-section or file-by-file breakdown. What's where? -->
<!-- Include: directory structure, module boundaries, key files, entry points, configuration -->

### Directory Layout

```text
(paste directory tree here)
```

### Key Modules

| Module / File | Purpose |
| --- | --- |
| `example/main.py` | Entry point, initializes the application |
| `example/config.py` | Configuration loading and validation |

### Entry Points

- **Main:** `example/main.py`
- **API:** `example/api/routes.py`

---

## Detailed Notes

<!-- Layer 3: Key functions, APIs, patterns, data structures, gotchas, dependencies -->

### Key Functions & APIs

| Symbol | File | Description |
| --- | --- | --- |
| `initialize()` | `main.py` | Sets up the application context |
| `get_config()` | `config.py` | Loads and validates config from env |

### Patterns & Conventions

- *(list patterns found in the codebase)*

### Dependencies

| Package | Version | Purpose |
| --- | --- | --- |
| `example-lib` | `^2.0` | Core processing engine |

### Gotchas & Risks

- *(list any tricky behavior, undocumented APIs, or security concerns)*

---

## Ambiguities & Open Questions

- *(list anything unclear that needs user clarification)*
