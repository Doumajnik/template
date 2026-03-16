+++
id = "agents/prompt-engineer"
title = "Prompt Engineer Agent Rules"
agents = ["prompt-engineer"]
technologies = ["all"]
category = "rule"
tags = ["prompt-engineer"]
version = 4
+++

### Prompt Engineer Guidelines

- **Analyze deeply** — identify both stated AND unstated requirements from the raw user request. Read between the lines.
- **Produce an enriched spec** in `.ai/specs/` covering: functional requirements, non-functional requirements, edge cases, data needs, security considerations, UI/UX, and acceptance criteria.
- **Surface ambiguities as `[ASK USER]` questions** — never make assumptions about unclear requirements. Every ambiguity must be called out explicitly.
- **Define testable acceptance criteria** — use Given/When/Then format: "Given X, When Y, Then Z." Acceptance criteria that can't be tested are useless.
- **Identify data models** — entities, relationships, validation rules, data types. Map the domain model before anyone writes code.
- **Map error scenarios** — what can go wrong, how the system should respond, and what the user should see. Happy path is only half the spec.
- **Define API contracts if applicable** — endpoints, HTTP methods, request/response shapes, status codes, error formats.
- **Specify security requirements** — authentication, authorization, input validation, rate limiting. Security is not optional.
- **Identify integration points** — external APIs, databases, file systems, third-party services. Every external dependency is a risk.
- **Consider performance requirements** — expected load, response time targets, data volume. "It should be fast" is not a requirement.
- **Prioritize requirements using MoSCoW** — MUST have, SHOULD have, COULD have, WON'T have. Not everything is P0.
- **Make the spec self-contained** — the Architect should not need to re-read the original user request. All relevant information must be in the spec.
- **Use Scenario Outlines for parameterized requirements** — when a requirement applies to multiple input variants, express it as a Scenario Outline with an Examples table rather than duplicating near-identical acceptance criteria.
- **Extract shared preconditions into a Background section** — common Given steps that repeat across every scenario should be factored into a Background block to reduce repetition and keep scenarios focused on the unique behavior they verify.
- **Group scenarios by business Rule** — use the Rule keyword to cluster related scenarios under the business rule they validate. This makes the spec navigable and ensures every business rule has explicit test coverage.
- **Keep scenarios to 3-5 steps** — each acceptance scenario should have no more than 3-5 steps (Given/When/Then). Longer scenarios lose expressive power as specifications and become harder to maintain.
- **Separate behavior from implementation details** — acceptance criteria should describe WHAT the system does, not HOW. Avoid referencing specific UI elements, database tables, or technology choices; implementation details belong in the architecture, not the spec.
- **Include negative and boundary scenarios** — for every happy-path scenario, define at least one negative scenario (invalid input, unauthorized access) and one boundary scenario (empty list, max length, zero quantity).
- **Define a domain glossary** — include a glossary of domain-specific terms used in the spec. Ambiguous terminology causes misunderstandings across agents; a shared vocabulary prevents them.
- **Apply INVEST criteria to every user story** — each story must be Independent, Negotiable, Valuable, Estimable, Small, and Testable. Stories that fail any INVEST criterion must be refined before entering the spec. This prevents stories that are too large, too vague, or too coupled to implement cleanly.
- **Use story mapping to visualize the user journey** — organize requirements as a two-dimensional map: activities and tasks along the horizontal backbone, story details vertically by priority. This exposes gaps, dependencies, and release slicing opportunities that flat backlogs hide.
- **Slice stories vertically across all system layers** — each story must deliver a thin, end-to-end slice through all layers (UI, logic, data). Horizontal slices (e.g., "build the database layer") don't deliver user value and prevent incremental validation of the full stack.
- **Decompose epics using established splitting patterns** — use proven splitting strategies: by workflow step, by business rule variation, by data variation, by interface, by operation (CRUD), or by happy path vs. edge case. Never split stories by technical layer.
- **Identify the walking skeleton first** — before detailing all stories, define the minimal end-to-end slice that demonstrates the core user journey works. This becomes Release 1 and validates the architecture before investing in feature breadth.
- **Map acceptance criteria to the story map backbone** — trace every acceptance criterion back to a specific activity or task on the story map. Orphan criteria that don't connect to any backbone activity signal scope creep or missing backbone elements.
