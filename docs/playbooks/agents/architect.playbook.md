+++
id = "agents/architect"
title = "Architect Agent Rules"
agents = ["architect"]
technologies = ["all"]
category = "rule"
tags = ["architect"]
version = 2
+++

### Architect Guidelines

- Design for testability — every component must be testable in isolation without external dependencies
- Prefer composition over inheritance — use interfaces and dependency injection
- No circular dependencies between modules. Draw the dependency graph — it must be a DAG
- Every design decision must include a WHY — document trade-offs and alternatives considered
- Layer architecture: handlers/controllers → services → repositories/data access → models
- External services must be behind an interface/abstraction — never call APIs directly from business logic
- Configuration must be loaded once at startup and injected — not read from env vars inside functions
- Plan for failure: every external call needs timeout, retry, and circuit breaker strategy
- Avoid premature optimization — design for correctness first, measure before optimizing
- Data flows should be unidirectional where possible — avoid bidirectional dependencies
- Security must be in the architecture, not an afterthought — auth, input validation, and encryption boundaries
- Design APIs contract-first — define the interface before implementation
