+++
id = "agents/doc-site"
title = "Doc-Site Generator Agent Rules"
agents = ["doc-site"]
technologies = ["all"]
category = "rule"
tags = ["documentation", "doc-site", "tutorials"]
version = 1
+++

### Doc-Site Generator Guidelines

- **Distinct from Doc Updater.** Doc Updater maintains internal docs (CODE_INVENTORY, BUSINESS_LOGIC, per-file); Doc-Site produces user-facing docs (getting started, tutorials, how-tos, reference, explanation, runbooks, migrations).
- **Diátaxis quadrants.** Tutorial / How-to / Reference / Explanation each serve a distinct purpose. Never mix them in one document.
- **Audience-first.** Beginner / Integrator / Operator / Migrator read differently — pick one per document.
- **Working examples mandatory.** Every public-facing doc has at least one runnable example. Examples are tested in CI (or explicitly marked skip-doctest with reason).
- **No `<placeholder>` without concrete fallback.** Copy-paste must work; if the user must substitute, give them a working default first.
- **Reference is auto-derived where possible.** API reference from `docs/API_DOCUMENTATION.md`, CLI reference from `--help`, config reference from schema. Hand-written reference drifts.
- **Cross-link aggressively.** Every doc links to at least one prerequisite + one next-step + related concepts.
- **Migration guides mandatory for breaking changes.** Every Deprecation Manager entry produces a migration guide before the deprecation completes; include automated migration scripts where possible.
- **Runbooks from real incidents only.** Generic runbooks are useless; pull symptoms / diagnoses / mitigations from `docs/incidents/` postmortems.
- **No marketing voice.** Documentation is matter-of-fact. Marketing voice belongs in README intro and landing pages.
- **Locale-aware examples.** Show how to handle non-ASCII, RTL, currency, dates where relevant — many bugs surface only at locale boundaries.
- **Output to `docs/site/`** with the standard quadrant subfolders + runbooks + migrations. Each subfolder has its own index.
- **Link-check before reporting back.** Broken internal links block.
- **Never overwrite without versioning.** When a doc materially changes, keep the previous version under `docs/site/_archive/` for at least one major release cycle.
