---
description: "Rust coding conventions and best practices. Use when writing, reviewing, or refactoring Rust code."
applyTo: "**/*.rs"
---

# Rust Conventions

- Prefer borrowing (`&T`, `&mut T`) over ownership transfer — only take ownership when the function needs to store or consume the value. Minimize `.clone()` — each clone is a code smell that should be justified
- Never use `.unwrap()` or `.expect()` in production code — use `?` operator for propagation, `match`/`if let` for handling, or `.unwrap_or_default()` for safe fallbacks. Reserve `.unwrap()` for tests only
- Use `thiserror` for library error types (derive `Error` with `#[error("...")]`) and `anyhow` for application-level error handling — never implement `Display` and `Error` manually when `thiserror` can derive them
- Model domain states as enums — use enums with data variants as state machines instead of boolean flags or stringly-typed status fields. Leverage exhaustive `match` to ensure all states are handled
- Prefer iterators over `for` loops with index access — use `.iter()`, `.map()`, `.filter()`, `.collect()` chains. Use `.enumerate()` when you need the index
- Derive `Debug` on all types. Derive `Clone`, `PartialEq`, `Eq`, `Hash` only when semantically meaningful — never derive traits just for convenience without considering the contract
- Add explicit lifetime annotations only when the compiler cannot infer them — never add redundant lifetimes that the compiler would elide. Use `'_` for anonymous lifetimes in obvious cases
- Design traits with a single responsibility — prefer multiple small traits over one large trait. Use blanket implementations (`impl<T: Read> MyTrait for T`) to provide defaults for categories of types
- Use `match` with destructuring for enums and structs — never use `if` chains to inspect enum variants when `match` is exhaustive. Use `if let` for single-variant checks
- Organize modules using one file per module (`foo.rs`) rather than `foo/mod.rs` — the `mod.rs` convention is the legacy style. Declare modules in the parent with `mod foo;` and re-export with `pub use`
- Enable strict Clippy lints at the crate level: `#![deny(clippy::all, clippy::pedantic)]` — suppress individual lints with `#[allow()]` only when justified with a comment
- Use `serde` with `#[derive(Serialize, Deserialize)]` for all serialization — never write manual serialization code. Use `#[serde(rename_all = "camelCase")]` for JSON APIs and `#[serde(deny_unknown_fields)]` for strict parsing
- Use the Builder pattern with typestate to enforce required fields at compile time — prefer `TypedBuilder` or manual impl over `Option` fields with runtime validation
- Use `Arc<Mutex<T>>` for shared mutable state across threads — prefer `RwLock` when reads are far more frequent than writes. Never hold a lock across an `.await` point — use `tokio::sync::Mutex` for async code
- Use `tokio` as the async runtime (default). Use `async fn`, `.await`, and `tokio::spawn` for concurrent tasks. Use `tokio::select!` for racing futures — always include a cancellation branch
- Understand `Pin<&mut T>` — use `pin!()` macro (std) for stack pinning. Never implement `Unpin` manually unless you fully understand the safety implications
- Isolate all `unsafe` code into minimal, well-documented functions with `// SAFETY:` comments explaining why the invariants hold — never scatter `unsafe` blocks throughout business logic
- Write `///` doc comments on all public items with examples in doc-tests. Use `//!` for module-level documentation. Include `# Errors`, `# Panics`, and `# Safety` sections where applicable
- Follow Cargo conventions: `src/lib.rs` for libraries, `src/main.rs` for binaries, `tests/` for integration tests, `benches/` for benchmarks, `examples/` for usage examples
- Use Cargo feature flags for optional functionality — gate expensive dependencies and optional features behind `[features]`. Never enable features by default unless most users need them
- For `no_std` crates, use `#![no_std]` with `core` and `alloc` only — provide a `std` feature flag that enables `std`-dependent functionality. Never depend on `std` implicitly
- Write unit tests in a `#[cfg(test)] mod tests { }` block inside each source file. Write integration tests in `tests/` that test the public API only. Use `#[should_panic]` for expected panics and `assert_matches!` for enum variant assertions
- Use `criterion` for benchmarks — never use `#[bench]` (unstable). Benchmark realistic workloads and compare with `cargo bench -- --baseline`
- Prefer `impl Trait` in argument position for simple generic bounds (`fn read(r: impl Read)`) and in return position to hide concrete types — use explicit generics (`<T: Read>`) when the caller needs to name the type
- Use `From`/`Into` conversions for infallible type transformations and `TryFrom`/`TryInto` for fallible ones — implement `From` (not `Into`) to get the reverse for free
- Use `Cow<'_, str>` and `Cow<'_, [T]>` for APIs that may or may not need to allocate — avoid forcing callers to allocate when the data is already in the right form
- Use `#[must_use]` on functions whose return value should not be silently ignored — especially `Result`-returning functions and builder methods
- Prefer `SmallVec` or `ArrayVec` (from `smallvec`/`arrayvec`) for collections that are almost always small — avoid heap allocation for known-small-size cases
- Use `tracing` (not `log`) for structured, span-based instrumentation — use `#[instrument]` on async functions for automatic span creation. Use `tracing-subscriber` for output formatting
- Represent newtype wrappers with single-field tuple structs (`struct UserId(u64)`) — implement `Deref` only when the wrapper truly "is-a" reference to the inner type, not for convenience
- Use `todo!()` for unfinished code during development — never leave empty function bodies or placeholder `unimplemented!()` in committed code. `todo!()` with a message is acceptable in stubs during active development only
- Handle all `Result` values — never use `let _ = fallible_call()` to silently discard errors. If the error is truly ignorable, comment why: `// Error ignored because {reason}`
- Use workspace-level `[dependencies]` in the root `Cargo.toml` and inherit them in member crates with `dep.workspace = true` — never duplicate version specifications across workspace members
- Use `const fn` for functions that can be evaluated at compile time — prefer `const` over `static` for immutable values. Use `LazyLock` (std, Rust 1.80+) instead of `lazy_static!` or `once_cell` for runtime-initialized statics
- Prefer `String` and `Vec<u8>` for owned data and `&str` and `&[u8]` for borrowed data — never use `&String` or `&Vec<T>` as parameter types when `&str` or `&[T]` suffice
