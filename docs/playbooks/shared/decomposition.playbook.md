+++
id = "shared/decomposition"
title = "Decomposition Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["decomposition", "function-size", "single-responsibility"]
version = 5
+++

### Decomposition

- Each module/file should have a single, clear responsibility
- If a function does two unrelated things, split it into two functions
- Extract complex conditionals into named boolean variables or predicate functions
- If a block of code needs a comment explaining what it does, extract it into a well-named function
- Configuration should be separated from logic — use config files or environment variables
- Side effects (I/O, network, database) should be isolated from pure business logic
- Utility functions that don't depend on module state belong in `src/utils/`
- If a class has more than 7 public methods, consider splitting it into smaller classes
- Long parameter lists (>4 params) suggest the function is doing too much — use a config object or split it
- Entry point scripts should be thin — delegate to library functions for testability
- Separate data validation from business logic — validators should be standalone, composable functions
- API handlers should be thin: parse request → call service → format response. No business logic in handlers
- Middleware/interceptors should do ONE thing (auth, logging, rate limiting) — never combine concerns
- State management should be isolated from rendering logic (MVC, MVVM, or equivalent pattern)
- Background jobs and scheduled tasks should call the same service functions as the API — no duplicated logic
- Database access patterns should be abstracted behind a repository or data access layer
- Transform raw external data (API responses, file content) into internal domain types at the boundary — don't pass raw data deep into the system
- Event handlers should delegate to domain services, not contain business logic directly
- Split read and write operations when a function does both — readers should have no side effects
- Long switch/match statements (>5 cases) suggest a missing abstraction — consider polymorphism, strategy pattern, or lookup tables
- Detect Primitive Obsession: replace repeated use of primitive types (strings for IDs, ints for money, tuples for coordinates) with small domain-specific value objects or dataclasses (Refactoring Guru, Primitive Obsession smell)
- Follow the Law of Demeter: avoid message chains like `a.get_b().get_c().do_thing()` — if a method reaches through more than one level of indirection, introduce a forwarding method (Refactoring Guru, Message Chains smell)
- Detect Feature Envy: if a method uses more data or methods from another class than its own, move it to the class it actually operates on (Refactoring Guru, Feature Envy smell)
- Detect Inappropriate Intimacy: if two classes access each other’s private/internal details extensively, refactor to reduce coupling — extract a shared interface or introduce a mediator (Refactoring Guru, Inappropriate Intimacy smell)
- Avoid Speculative Generality: remove abstract classes, interfaces, or parameters created for anticipated future use that currently have only one consumer (Refactoring Guru, Speculative Generality smell)
- Apply the Dependency Inversion Principle (SOLID — D): high-level modules should depend on abstractions, not concrete implementations — inject dependencies via constructor parameters, not by importing and instantiating directly
- Detect Divergent Change: if a single class is modified for multiple unrelated reasons (e.g., both UI formatting and database schema changes), split it by axis of change so each class has exactly one reason to change (SOLID — SRP)
- Apply Bounded Contexts: define clear boundaries around cohesive domain concepts — each bounded context owns its data, models, and vocabulary, and communicates with other contexts through explicit interfaces, not shared databases (Azure Architecture, Domain-Driven Design)
- Apply CQRS (Command Query Responsibility Segregation): when read and write workloads have significantly different performance or scaling requirements, separate them into distinct models and services rather than forcing a single model to serve both (Azure Architecture Patterns, CQRS)
- Use the Strangler Fig pattern for legacy migration: instead of rewriting an entire module at once, incrementally replace specific functions or routes by routing traffic to new implementations while the old code remains operational (Azure Architecture Patterns, Strangler Fig)
- Apply Interface Segregation (SOLID — I): clients should not be forced to depend on methods they don't use — split large interfaces into smaller, role-specific ones so implementing classes only need to provide relevant behavior
- Use the Pipes and Filters pattern for complex processing: break sequential data transformations into a pipeline of independent, composable stages — each filter does one transformation and passes results to the next, enabling reuse and parallel processing (Azure Architecture Patterns, Pipes and Filters)
- Apply the Gateway Aggregation pattern: when a client operation requires calls to multiple backend services, introduce an aggregation layer that combines results into a single response — this reduces client complexity and network round-trips (Azure Architecture Patterns, Gateway Aggregation)
- Detect God Class / Large Class smell: if a class has more than 200 lines or touches more than 3 distinct responsibilities, decompose it — extract cohesive subsets of fields and methods into smaller focused classes (Refactoring Guru, Large Class smell)
