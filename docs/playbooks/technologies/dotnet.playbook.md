+++
id = "technologies/dotnet"
title = ".NET Conventions"
agents = []
technologies = ["dotnet"]
category = "convention"
tags = ["dotnet", "csharp", "aspnet"]
version = 5
+++

### .NET Conventions

- Follow Microsoft naming conventions: `PascalCase` for public members, types, and methods. `camelCase` for local variables and parameters. `_camelCase` for private fields
- Use `async`/`await` for all asynchronous code. Never use `.Result` or `.Wait()` on tasks — they cause deadlocks in synchronization contexts
- Return `IReadOnlyList<T>` and `IReadOnlyDictionary<K,V>` from public methods to prevent callers from mutating internal collections
- Use `record` types for immutable data transfer objects and value-like types. Use `record struct` for small, stack-allocated value types
- Use constructor injection for dependency injection. Register all services in `Program.cs` or a startup extension method — never use the service locator pattern
- Use `ILogger<T>` for structured logging. Never use `Console.WriteLine` in production code
- Enable nullable reference types project-wide: set `<Nullable>enable</Nullable>` in the `.csproj` file
- Use `string.IsNullOrWhiteSpace()` for string validation — never manually check for `null`, empty, or whitespace separately
- Use `StringBuilder` for string concatenation inside loops. Single-expression concatenation or interpolation is fine with `+` or `$""`
- Use `ConfigureAwait(false)` in library code to avoid capturing the synchronization context. Do not use it in application-level code (ASP.NET, UI)
- Pass `CancellationToken` through all async method signatures that perform I/O or long-running work. Honor cancellation by passing the token to downstream calls
- Use LINQ for simple collection queries (`Where`, `Select`, `Any`, `FirstOrDefault`). For complex multi-step transformations, use explicit loops for readability
- Mark classes as `sealed` unless they are explicitly designed for inheritance. This improves performance and signals intent
- Use `using` declarations or `using` statements for all `IDisposable` resources. Prefer `using` declarations (C# 8+) for shorter syntax
- Validate inputs at API boundaries using FluentValidation or `DataAnnotations`. Do not add defensive null checks deep inside internal methods
- Use xUnit for unit testing with `[Theory]` and `[InlineData]` for parameterized tests. Use `[Fact]` for single-case tests
- Use `TimeProvider` (NET 8+) for testable time-dependent code — never `DateTime.Now` or `DateTime.UtcNow` directly
- Prefer `Span<T>` and `Memory<T>` for high-performance memory operations over array slicing
- Use `IOptions<T>`, `IOptionsSnapshot<T>`, or `IOptionsMonitor<T>` for configuration — never read from `IConfiguration` directly in business logic
- Use `ValueTask<T>` instead of `Task<T>` for hot-path async methods that often complete synchronously
- Use `Channel<T>` for producer-consumer patterns — never build your own queue with locks
- Implement `IAsyncDisposable` with `await using` for async cleanup (database connections, streams)
- Use `source generators` for serialization (`System.Text.Json`) — never reflection-based serializers in hot paths
- Use `ArgumentNullException.ThrowIfNull()` (NET 6+) for parameter validation — cleaner than manual checks
- Prefer `HashSet<T>` over `List<T>` for membership checks — O(1) vs O(n)
- Use `FrozenDictionary<K,V>` and `FrozenSet<T>` (NET 8+) for read-only lookup collections
- Use `Polly` library for retry policies, circuit breakers, and timeout policies on external calls
- Use `MediatR` or in-process messaging for decoupled command/query handling — avoid injecting services into services
- Use primary constructors (C# 12) for classes and structs that capture dependencies or parameters — eliminates boilerplate field assignments. Use camelCase for class/struct primary constructor parameters, PascalCase for record primary constructor parameters
- Use collection expressions (`[1, 2, 3]`) for initializing arrays, lists, spans, and other collection types. Use the spread element (`..`) to merge collections
- Use file-scoped namespace declarations (`namespace MyApp;`) — never block-scoped namespaces. This reduces nesting by one level across the entire file
- Use `using` alias directive to alias any type (C# 12) including tuples, arrays, and generic types — e.g., `using Point = (int X, int Y);` for domain-specific type clarity
- Place `using` directives outside namespace declarations to avoid ambiguous name resolution when other namespaces share a common prefix
- Use raw string literals (`"""..."""`) for multi-line strings containing special characters, JSON, or XML — avoid escape sequences or verbatim strings for complex embedded content
- Use `required` properties (C# 11+) to enforce initialization of property values at construction — prefer over constructor parameters when the type has many optional properties
- Use `StringComparison` explicitly in all string comparison methods (`Equals`, `Compare`, `IndexOf`, `StartsWith`, `EndsWith`) — never use overloads without it. Use `StringComparison.Ordinal` for internal/technical comparisons and `StringComparison.OrdinalIgnoreCase` for case-insensitive lookups. Use culture-aware comparisons only for user-facing text (CA1307/CA1310)
- Use `decimal` for monetary values and financial calculations — never `double` or `float`. Floating-point types have inherent rounding errors that are unacceptable for currency. Reserve `double` for scientific or graphics computation where approximate results are acceptable
- Centralize project-wide imports in a single `GlobalUsings.cs` file using `global using` directives (C# 10+). Keep commonly referenced namespaces (e.g., `System.Collections.Generic`, `Microsoft.Extensions.Logging`) there to reduce repetitive `using` statements across files
- Use `AsSpan()` instead of `Substring()` for read-only string slicing operations — parsing, comparison, and searching within a portion of a string. `AsSpan()` avoids heap allocation of a new string (CA1831)
- Use `throw;` to rethrow exceptions — never `throw ex;`. The latter resets the stack trace and loses the original callsite information, making debugging significantly harder (CA2200)
- Enable the recommended set of .NET code analyzers by setting `<AnalysisMode>Recommended</AnalysisMode>` in `.csproj`. Escalate analyzer warnings to errors in CI builds with `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` for zero-warning enforcement
- Avoid capturing variables in lambdas passed to hot-path methods (`Where`, `Select`, logging interpolation) — captured variables cause closure heap allocations on every invocation. Extract captured values into local variables or pass them as method parameters to avoid allocation pressure
