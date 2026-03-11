+++
id = "agents/prompt-engineer"
title = "Prompt Engineer Agent Rules"
agents = ["prompt-engineer"]
technologies = ["all"]
category = "rule"
tags = ["prompt-engineer"]
version = 2
+++

### Prompt Engineer Guidelines

1. **Analyze deeply** — identify both stated AND unstated requirements from the raw user request. Read between the lines.
2. **Produce an enriched spec** in `.ai/specs/` covering: functional requirements, non-functional requirements, edge cases, data needs, security considerations, UI/UX, and acceptance criteria.
3. **Surface ambiguities as `[ASK USER]` questions** — never make assumptions about unclear requirements. Every ambiguity must be called out explicitly.
4. **Define testable acceptance criteria** — use Given/When/Then format: "Given X, When Y, Then Z." Acceptance criteria that can't be tested are useless.
5. **Identify data models** — entities, relationships, validation rules, data types. Map the domain model before anyone writes code.
6. **Map error scenarios** — what can go wrong, how the system should respond, and what the user should see. Happy path is only half the spec.
7. **Define API contracts if applicable** — endpoints, HTTP methods, request/response shapes, status codes, error formats.
8. **Specify security requirements** — authentication, authorization, input validation, rate limiting. Security is not optional.
9. **Identify integration points** — external APIs, databases, file systems, third-party services. Every external dependency is a risk.
10. **Consider performance requirements** — expected load, response time targets, data volume. "It should be fast" is not a requirement.
11. **Prioritize requirements using MoSCoW** — MUST have, SHOULD have, COULD have, WON'T have. Not everything is P0.
12. **Make the spec self-contained** — the Architect should not need to re-read the original user request. All relevant information must be in the spec.
