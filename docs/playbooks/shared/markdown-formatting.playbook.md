+++
id = "shared/markdown-formatting"
title = "Markdown Formatting Convention"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["markdown", "formatting", "documentation"]
version = 5
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
- Use asterisks (`*`) for bold and italic emphasis, never underscores (`_`) — underscores inside words are handled inconsistently across Markdown processors (Markdown Guide, Bold/Italic Best Practices)
- Do not mix different unordered list delimiters (`-`, `*`, `+`) in the same document — pick one and stick with it for consistency (Markdown Guide, Unordered List Best Practices)
- Use fenced code blocks (triple backticks) instead of indented code blocks — they are easier to read and support syntax highlighting (Markdown Guide, Fenced Code Blocks)
- Put blank lines before and after horizontal rules (`---`) to prevent them from being interpreted as setext headings (Markdown Guide, Horizontal Rule Best Practices)
- Always put a space between heading `#` signs and the heading text — some processors require it for correct rendering (Markdown Guide, Heading Best Practices)
- Use periods after ordered list numbers (`1.`), never parentheses (`1)`) — parenthesis delimiters are not supported by all Markdown processors (Markdown Guide, Ordered List Best Practices)
- When nesting content inside list items (paragraphs, code blocks, images), indent the nested content by 4 spaces to maintain list continuity (Markdown Guide, Adding Elements in Lists)
- Use footnotes for supplementary references and citations: place the reference marker `[^1]` inline and the footnote content `[^1]: ...` at the bottom of the section — avoid cluttering the main text with lengthy URLs or tangential explanations (Markdown Guide, Extended Syntax — Footnotes)
- Use definition lists (term on one line, `: definition` on the next) for glossaries, option descriptions, and configuration parameter documentation — they are more semantically appropriate than bullet lists for key-value explanations (Markdown Guide, Extended Syntax — Definition Lists)
- Format task lists with `- [ ]` (incomplete) and `- [x]` (complete) syntax for checklists, progress tracking, and review items — always include a space inside the brackets for unchecked items (Markdown Guide, Extended Syntax — Task Lists)
- Add custom heading IDs (`### My Heading {#custom-id}`) for long documents to enable deep linking and stable anchor references — this prevents broken links when heading text is edited (Markdown Guide, Extended Syntax — Heading IDs)
- Use table column alignment (`:---` left, `:---:` center, `---:` right) to improve readability of numeric, date, or status columns — always left-align text columns and right-align numeric columns (Markdown Guide, Extended Syntax — Table Alignment)
- Limit emoji usage in documentation to status indicators (✅, ❌, ⚠️) and progress markers — avoid decorative emoji that reduce professional readability or cause rendering issues across platforms (Markdown Guide, Extended Syntax — Emoji)
- Use strikethrough (`~~text~~`) only for documenting deprecated items or removed features in changelogs — never use strikethrough for emphasis or humor in technical documentation (Markdown Guide, Extended Syntax — Strikethrough)
