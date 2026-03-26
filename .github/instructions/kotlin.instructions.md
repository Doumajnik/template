---
description: "Kotlin coding conventions and best practices. Use when writing, reviewing, or refactoring Kotlin code."
applyTo: "**/*.kt,**/*.kts"
---

# Kotlin Conventions

- Use `data class` for DTOs and value objects — never write manual `equals`/`hashCode`/`toString`/`copy` when a data class generates them
- Use `sealed class` or `sealed interface` to model closed type hierarchies — always handle all subtypes in `when` expressions without a catch-all `else` branch
- Never use `!!` (non-null assertion) — use safe calls (`?.`), `let`, `require()`, or `checkNotNull()` to handle nulls explicitly. The only acceptable `!!` is in test assertions
- Use `?.let { }` for nullable-to-non-null transformations and `?: return`/`?: throw` for early exits — never nest multiple null checks when chaining operators works
- Use `apply` for initializing an object's properties after construction, `also` for side effects (logging, validation), `let` for null-safe transformations, `run` for scoped computations on a receiver, and `with` for calling multiple methods on the same object — never use one scope function where another is more idiomatic
- Use structured concurrency: always launch coroutines inside a `CoroutineScope` or `coroutineScope { }` builder — never use `GlobalScope`. Use `supervisorScope` or `SupervisorJob` only when child failures must not cancel siblings
- Use `Flow<T>` for cold reactive streams — prefer Flow over Channel for most producer-consumer patterns. Use `SharedFlow` for hot streams and `StateFlow` for observable state
- Use `value class` (formerly `inline class`) for type-safe wrappers around primitives — never pass raw `String` or `Int` for domain concepts like `UserId`, `Email`, or `Amount`
- Use `companion object` only for factory methods and constants associated with a class — never as a dumping ground for utility functions. Prefer top-level functions for stateless utilities
- Use delegation with `by` for interface implementation (`class Repo : UserRepo by userRepoImpl`) and property delegates (`by lazy`, `by Delegates.observable`) — avoid manual wrapper classes
- Design DSL-style APIs using lambdas with receivers, `@DslMarker` annotations, and extension functions — restrict scope leakage with `@DslMarker` to prevent calling outer-scope functions inside inner builders
- Rely on smart casts after `is` checks and null checks — never manually cast with `as` after a type guard. Use `as?` for safe casts that return null on failure
- Use destructuring declarations for data classes, pairs, and map entries in lambdas — prefer `val (key, value) = entry` over index access
- Use named arguments for all function calls with more than 2 parameters of the same type or boolean flags — never pass positional booleans (`doThing(true, false)`)
- Use default parameter values instead of method overloads — overloads are only needed for Java interop
- Use `Sequence<T>` for lazy chained operations on large collections — use `List` for small collections where materialization cost is negligible. Convert with `.asSequence()` before chaining 3+ operations
- Use `by lazy { }` for expensive property initialization that should happen at most once — use `lateinit var` only for framework-injected fields (DI, Android views) that are guaranteed to be set before use
- Mark all `suspend` functions that perform I/O with the `Dispatchers.IO` context — never perform blocking I/O on `Dispatchers.Default` or `Dispatchers.Main`
- Prefer `Channel` for one-to-one communication between coroutines and `SharedFlow` for one-to-many broadcasting — never use `Channel` as a broadcast mechanism
- Use `expect`/`actual` declarations for Kotlin Multiplatform shared code — isolate platform-specific implementations behind interfaces in the common module
- Write tests with Kotest (preferred) or JUnit 5. Use Kotest matchers (`shouldBe`, `shouldThrow`) for expressive assertions. Use `runTest` (kotlinx-coroutines-test) for testing suspend functions — never `runBlocking` in tests
- Use `require()` for argument validation and `check()` for state validation — both throw specific exceptions (`IllegalArgumentException`, `IllegalStateException`) with descriptive messages
- Use `object` declarations for singletons — never implement singleton patterns manually with `companion object` and private constructors
- Use `when` as an expression with exhaustive branches — always assign or return the result. Avoid `when` as a statement with side effects
- Prefer extension functions over utility classes — never create `XxxUtils` or `XxxHelper` classes. Place extension functions in a file named after the type they extend
- Use `buildList { }`, `buildMap { }`, `buildSet { }` for constructing collections imperatively — prefer these over `mutableListOf()` followed by mutations when the collection should be immutable after construction
- Use `@JvmStatic`, `@JvmField`, and `@JvmOverloads` on public APIs consumed from Java — ensure Kotlin-first APIs are ergonomic for Java callers
- Use property access syntax for getters/setters — never write `getX()`/`setX()` methods manually in Kotlin. Java interop generates them automatically
- Prefer `Result<T>` or sealed class hierarchies for error modeling over throwing exceptions in business logic — reserve exceptions for truly exceptional/unrecoverable conditions
- Use `typealias` for complex generic types (`typealias UserCache = Map<UserId, List<Session>>`) — never repeat verbose generic signatures across multiple function signatures
- Use `internal` visibility for module-private APIs — never default to `public`. Use `private` for class internals and `protected` sparingly
- Use Kotlin coroutines `withTimeout` and `withTimeoutOrNull` for time-bounded operations — never implement manual timeout logic with `delay` and `cancel`
- Avoid `it` in nested lambdas — name the parameter explicitly when the enclosing scope already uses `it` or when the lambda body exceeds one line
- Use `sealed interface` over `sealed class` (Kotlin 1.5+) when the hierarchy does not need shared state — sealed interfaces allow subtypes to extend other classes
- Use `@OptIn(ExperimentalXxxApi::class)` annotations to explicitly acknowledge experimental APIs — never suppress the warning globally. Isolate experimental usage behind stable wrapper functions
