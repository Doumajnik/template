+++
id = "shared/markdown-formatting"
title = "Markdown Formatting Convention"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["markdown", "formatting", "documentation"]
version = 3
+++

### Markdown Formatting

- Always leave a blank line before and after headings, lists, code fences, and block quotes
- Use ATX-style headings (#, ##, ###) — never setext-style (underlines)
- Code blocks must specify the language after opening fences (```python, ```typescript)
- Lists must use `-` for unordered items, `1.` for ordered items — be consistent within a file
- Tables must have header separators. Align columns with spaces for readability
- Links should use reference-style `[text][ref]` for URLs used multiple times
- Wrap lines at 80 characters in doc files when possible (except for URLs and tables)
- Use bold for emphasis on key terms, italic for introducing new terms
- Never use HTML in markdown unless absolutely necessary (e.g., `<details>` for collapsible sections)
- Follow the heading hierarchy: # for title, ## for sections, ### for subsections — never skip levels
- Use `<details><summary>` tags for long code examples or output that would break flow
- TOC (table of contents) is required for documents longer than 5 sections
- Use descriptive link text — never "click here" or bare URLs as link text
- Images must have alt text that describes the content, not just the filename
- Use relative links for internal documentation references — never absolute URLs to the same repo
- Admonitions (> **Note:**, > **Warning:**) should use blockquote format with bold label
- Changelog entries must follow Keep a Changelog format: Added, Changed, Deprecated, Removed, Fixed, Security
- API documentation uses consistent verb tense: imperative for descriptions ("Returns the user"), past tense for changelogs ("Added endpoint")
- Document file must have exactly one H1 heading. Use H2+ for all subsequent sections
- Use line breaks within table cells sparingly — if a table cell needs multiple lines, consider restructuring as a list
