---
description: "Java coding conventions and best practices. Use when writing, reviewing, or refactoring Java code."
applyTo: "**/*.java"
---

# Java Conventions

- Use records for DTOs, value objects, and any immutable data carrier — never write a POJO with manual getters/equals/hashCode when a record suffices
- Use sealed classes and sealed interfaces to model closed type hierarchies — always list all `permits` subtypes explicitly
- Use pattern matching in `switch` expressions (Java 21+) with exhaustiveness checking — never use `default` as a catch-all when all cases can be enumerated
- Use `instanceof` pattern matching (`if (obj instanceof String s)`) — never cast after a separate `instanceof` check
- Never return `null` from a method that can have no result — return `Optional<T>` instead. Never call `Optional.get()` without `isPresent()` — use `orElse()`, `orElseThrow()`, or `map()`/`flatMap()`
- Never pass `Optional` as a method parameter or store it as a field — it is only for return types
- Use the Stream API for collection transformations — prefer `stream().filter().map().collect()` over manual loops with accumulators
- Prefer `Collectors.toList()` for mutable lists and `stream().toList()` (Java 16+) for unmodifiable lists — be explicit about mutability
- Use `var` for local variables only when the type is obvious from the right-hand side (constructor call, literal, factory method) — never use `var` when the type is ambiguous or comes from a long method chain
- Use text blocks (`"""`) for multi-line strings: SQL queries, JSON templates, HTML — always call `.stripIndent()` or manage trailing whitespace explicitly
- Use `List.of()`, `Set.of()`, `Map.of()` for immutable collection literals — never use `Collections.unmodifiableList(new ArrayList<>())` for static data
- Always use try-with-resources for `AutoCloseable` resources: streams, connections, readers — never close resources manually in a `finally` block
- Use `CompletableFuture.supplyAsync()` for async computations and chain with `thenApply()`/`thenCompose()` — never block with `.get()` on the calling thread without a timeout
- Use virtual threads (`Thread.ofVirtual()`, Java 21+) for I/O-bound concurrent tasks — never create platform thread pools for blocking I/O workloads
- Use structured concurrency (`StructuredTaskScope`, Java 21+ preview) when coordinating multiple concurrent subtasks that must all succeed or all cancel
- Throw unchecked exceptions (`IllegalArgumentException`, `IllegalStateException`) for programming errors and checked exceptions for recoverable conditions the caller must handle
- Never catch `Throwable` or `Error` — catch the most specific exception type possible. Always include context in exception messages (what went wrong, what value was invalid)
- Use the Builder pattern (manual or via annotation processor) for objects with more than 4 constructor parameters — never use telescoping constructors
- Always override `hashCode()` when overriding `equals()` — use `Objects.hash()` for concise implementations. Records handle this automatically
- Implement `Comparable<T>` with `Comparator.comparing().thenComparing()` chains — never write manual comparison logic with subtraction or nested ifs
- Always use `@Override` on every method that overrides a superclass or interface method — rely on the compiler to catch signature mismatches
- Use `@NonNull`/`@Nullable` annotations (from `jakarta.annotation` or `org.jspecify`) on all public API parameters and return types to enable static null analysis
- Use SLF4J with parameterized messages (`log.info("Processing {}", id)`) — never concatenate strings in log statements. Guard expensive log computations with `log.isDebugEnabled()`
- Use constructor injection for all dependencies — never field injection with `@Autowired`. Mark injected fields `final`. Use `@RequiredArgsConstructor` (Lombok) or records to reduce boilerplate
- Write tests with JUnit 5 (`@Test`, `@ParameterizedTest`, `@Nested`) — never JUnit 4. Use `assertThat` (AssertJ) for readable fluent assertions — never `assertEquals` with swapped expected/actual
- Use Mockito `@ExtendWith(MockitoExtension.class)` — never `MockitoAnnotations.openMocks()`. Use `verify()` sparingly — assert on behavior, not on call counts
- Define Maven/Gradle dependency versions in a BOM or version catalog (`libs.versions.toml`) — never inline version strings in individual dependency declarations
- Use `module-info.java` for modular projects — declare `requires`, `exports`, and `opens` explicitly. Never use automatic modules in production
- Prefer `java.time` (LocalDate, Instant, ZonedDateTime) for all date/time operations — never use `java.util.Date` or `java.util.Calendar`
- Use `String.formatted()` (Java 15+) or `MessageFormat` for user-facing messages that need localization — reserve f-string-style concatenation for log messages only
- Annotate `@FunctionalInterface` on all interfaces intended for lambda use — the compiler enforces the single-abstract-method constraint
- Use `EnumMap` and `EnumSet` instead of `HashMap`/`HashSet` when the key type is an enum — they are more memory-efficient and faster
- Use `switch` expressions (not statements) with arrow syntax (`->`) and yield — never fall through between cases
- Prefer `Stream.mapMulti()` (Java 16+) over `flatMap()` when the mapping is imperative or produces zero-to-few elements — avoids intermediate stream creation
- Never expose mutable internal collections from a class — return `Collections.unmodifiableList()` or a defensive copy. Records with `List` components should perform defensive copies in compact constructors
