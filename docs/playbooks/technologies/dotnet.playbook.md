+++
id = "technologies/dotnet"
title = ".NET Conventions"
agents = []
technologies = ["dotnet"]
category = "convention"
tags = ["dotnet", "csharp", "aspnet"]
version = 3
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
