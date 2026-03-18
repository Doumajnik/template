# Tool Manifest

> Single source of truth for which tools each agent is allowed to use.
> Referenced by the Librarian (context briefs) and enforced by the `PreToolUse` hook (`scripts/tool-guard.ps1`).

---

## Restricted Tool Categories

### Web Access Tools

Tools that access the internet. Only agents with explicit web research responsibilities may use these.

**Tool patterns:** `fetch_webpage`, `mcp_playwright_*`, `open_browser_page`

| Agent | Web Access | Reason |
|---|---|---|
| Research | **ALLOWED** | Web research is its primary purpose |
| All others | **DENIED** | No web access needed — work with local codebase/docs only |

---

## How This Is Enforced

1. **Soft enforcement (Librarian briefs):** The Librarian includes a `### Tool Restrictions` section in every context brief, listing denied tools. Agents are instructed not to use them.
2. **Hard enforcement (PreToolUse hook):** The hook script `scripts/tool-guard.ps1` intercepts every tool call and denies calls that violate this manifest. See `.github/hooks/tool-guard.json`.

## Adding New Restrictions

1. Add a new section under **Restricted Tool Categories** with the tool patterns and agent permission table.
2. Update `scripts/tool-guard.ps1` with the new deny rules.
3. The Librarian will automatically pick up new sections when assembling context briefs.
