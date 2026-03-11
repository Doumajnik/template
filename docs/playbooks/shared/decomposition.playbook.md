+++
id = "shared/decomposition"
title = "Decomposition Rule"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["decomposition", "function-size", "single-responsibility"]
version = 3
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
