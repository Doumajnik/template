+++
id = "agents/discovery"
title = "Discovery Agent Rules"
agents = ["discovery"]
technologies = ["all"]
category = "rule"
tags = ["discovery"]
version = 4
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
- Identify seams in the codebase — boundaries where behavior can be intercepted, redirected, or replaced without modifying the original code (source: Martin Fowler, "Strangler Fig Application")
- Map the domain model explicitly — document entity relationships, aggregate boundaries, and domain language (ubiquitous language) used in the codebase
- Document the test coverage landscape — note which modules have tests, which lack them, and the overall testing strategy or patterns in use
- Record coupling metrics — identify tightly coupled modules (many cross-references) that would be difficult to modify, test, or replace independently
- Document the build and deployment pipeline — how the system is built, tested, packaged, and deployed, including CI/CD configuration
- Identify technical debt hotspots — modules with high complexity, frequent modifications, accumulated TODOs/FIXMEs, or workarounds that indicate maintenance risk
- Identify anti-corruption layer candidates — flag boundaries where external or legacy system semantics differ from the internal domain model and would benefit from a translation layer to prevent model corruption (source: Microsoft Azure Architecture Patterns, "Anti-corruption Layer")
- Map bounded contexts — document distinct areas where specific domain models and ubiquitous language apply, noting where context boundaries align with module or service boundaries (source: Eric Evans, "Domain-Driven Design"; Microsoft Azure Architecture Patterns)
- Document event and message flows — map the events, commands, and messages flowing between components and systems, including direction, payload shape, and ordering constraints (event storming output)
- Identify API versioning and compatibility constraints — document which APIs are versioned, what backward-compatibility guarantees exist, and where breaking changes would cascade across system boundaries
- Document data ownership — for each significant data entity, record which component or team owns it, who has read vs. write access, and where data is duplicated or synchronized across boundaries
