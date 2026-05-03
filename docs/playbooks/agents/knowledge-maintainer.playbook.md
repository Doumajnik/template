+++
id = "agents/knowledge-maintainer"
title = "Knowledge Maintainer Agent Rules"
agents = ["knowledge-maintainer"]
technologies = ["all"]
category = "rule"
tags = ["maintenance", "playbooks", "skills", "freshness"]
version = 1
+++

### Research Before Writing

- **Always fetch the official docs** for the technology/framework before updating a playbook rule
- **Check at least 3 sources** for any new best practice before adding it
- **Cite your sources** — include a URL or doc reference for every addition
- **Date your additions** — include `<!-- added: YYYY-MM-DD, source: URL -->` comments for traceability

### Minimal Edits

- **Don't rewrite entire files** — add, update, or remove specific rules
- **Preserve structure** — don't reorganize headings, change frontmatter schema, or alter formatting conventions
- **One logical change per edit** — don't bundle unrelated updates in a single edit
- **Increment version** — always bump the `version` field in TOML frontmatter after changes

### Quality Guardrails

- **Never invent patterns** — every rule must be backed by established practice
- **Flag uncertainty** — use `<!-- NEEDS_REVIEW: ... -->` for items you're not 100% confident about
- **Don't break downstream** — if a rule change would invalidate an agent's behavior, note it in the report but don't edit the agent file
- **Check for contradictions** — before adding a rule, verify it doesn't conflict with existing rules in the same file
- **Respect category boundaries** — security rules go in security playbooks, not general coding playbooks

### Source Quality

- Prefer official documentation over blog posts
- Prefer blog posts from core maintainers over community tutorials
- Prefer recent sources (<2 years) for fast-moving ecosystems
- Verify that patterns work with the version pinned in the project
- Discount sources with no date or author attribution
