# Tool Manifest

> Single source of truth for which tools each agent is allowed to use.
> Referenced by the Librarian (context briefs) and enforced by the `PreToolUse` hook (`scripts/tool-guard.py`).

---

## Restricted Tool Categories

### Web Access Tools

Tools that access the internet. Only agents with explicit web research responsibilities may use these.

**Tool patterns:** `fetch_webpage`, `mcp_playwright_*`, `open_browser_page`

| Agent | Web Access | Reason |
|---|---|---|
| Research | **ALLOWED** | Web research is its primary purpose |
| All others | **DENIED** | No web access needed — work with local codebase/docs only |

### Source File Reading Tools

Tools that read source/implementation files. The Test Writer is denied access to enforce black-box testing — tests are written from Librarian-provided signatures and descriptions only.

**Tool patterns:** `read_file`, `grep_search`, `semantic_search` (when targeting `src/` paths)

| Agent | Source File Reading | Reason |
|---|---|---|
| Test Writer | **DENIED** (for `src/` paths) | Black-box testing: must write tests from function contracts only, never from implementation. May read/write `tests/` and `docs/` freely. |
| All others | **ALLOWED** | Need source access to implement, review, debug, or analyze code |

---

## How This Is Enforced

1. **Soft enforcement (Librarian briefs):** The Librarian includes a `### Tool Restrictions` section in every context brief, listing denied tools. Agents are instructed not to use them.
2. **Hard enforcement (PreToolUse hook):** The hook script `scripts/tool-guard.py` intercepts every tool call and denies calls that violate this manifest. See `.github/hooks/tool-guard.json`.

## Adding New Restrictions

1. Add a new section under **Restricted Tool Categories** with the tool patterns and agent permission table.
2. Update `scripts/tool-guard.py` with the new deny rules.
3. The Librarian will automatically pick up new sections when assembling context briefs.
