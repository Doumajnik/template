+++
id = "agents/architect"
title = "Architect Agent Rules"
agents = ["architect"]
technologies = ["all"]
category = "rule"
tags = ["architect"]
version = 4
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
- Apply the Anti-Corruption Layer pattern when integrating with legacy or third-party systems — isolate your domain model from external data formats and protocols (source: Microsoft Azure Architecture Patterns)
- Use the Strangler Fig pattern for incremental migration — never plan a big-bang rewrite of existing systems (source: Martin Fowler, "Strangler Fig Application")
- Apply CQRS (Command Query Responsibility Segregation) when read and write workloads have fundamentally different scaling or modeling needs (source: Microsoft Azure Architecture Patterns)
- Apply the Single Responsibility Principle at every level: each module, class, and function should have exactly one reason to change
- Use the External Configuration Store pattern — externalize all environment-specific configuration so the same build artifact can deploy to any environment (source: Microsoft Azure Architecture Patterns)
- Document every significant architecture decision in an ADR (Architecture Decision Record) with context, decision, status, and consequences — decisions without records are decisions without accountability
- Design for observability from the start — ensure every component emits structured logs, metrics, and traces rather than adding them retroactively
- Apply the Ambassador pattern to offload cross-cutting client connectivity concerns (monitoring, logging, routing, retries, circuit breaking) into an out-of-process proxy co-located with the application — especially when supporting multiple languages or frameworks (source: Microsoft Azure Architecture Patterns, "Ambassador")
- Use the Sidecar pattern to deploy peripheral tasks (logging, configuration, security, telemetry) alongside the primary application in a separate process or container that shares its lifecycle — this provides language independence and shared resource access without tight coupling (source: Microsoft Azure Architecture Patterns, "Sidecar")
- Apply the Bulkhead pattern to isolate service instances into separate pools so that a failure in one pool does not cascade to others — partition by consumer priority, criticality, or bounded context to contain blast radius (source: Microsoft Azure Architecture Patterns, "Bulkhead")
- Design throttling into the architecture early — control resource consumption with rate limits and graceful degradation strategies (HTTP 429/503) rather than relying solely on autoscaling, which has provisioning delays (source: Microsoft Azure Architecture Patterns, "Throttling")
- Apply Queue-based Load Leveling to decouple producers and consumers that operate at different rates — use a queue as a buffer to smooth traffic spikes and prevent overloading downstream services (source: Microsoft Azure Architecture Patterns, "Queue-based Load Leveling")
