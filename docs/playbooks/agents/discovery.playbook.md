+++
id = "agents/discovery"
title = "Discovery Agent Rules"
agents = ["discovery"]
technologies = ["all"]
category = "rule"
tags = ["discovery"]
version = 2
+++

### Discovery Guidelines

- Read ALL files in the new data systematically — don't skip files based on name or extension
- Produce a structured summary in `docs/discoveries/` following the discovery template
- Identify: purpose, architecture patterns, dependencies, entry points, key abstractions
- Document the technology stack: languages, frameworks, libraries, and their versions
- Map module dependencies: who imports whom, data flow direction
- Flag potential issues: deprecated APIs, security concerns, missing tests, dead code
- Note coding conventions used: naming style, error handling patterns, testing patterns
- Document public APIs: endpoints, function signatures, data shapes
- Identify configuration: env vars, config files, feature flags, secrets management
- Keep summaries concise but complete — other agents will rely solely on this summary, not raw source
- Never modify the source data — discovery is read-only
- Tag the discovery file with relevant categories for the Librarian to index
