---
description: "Go coding conventions and best practices. Use when writing, reviewing, or refactoring Go code."
applyTo: "**/*.go"
---

# Go Conventions

- Follow Effective Go and the Go Code Review Comments wiki for idiomatic patterns
- Check errors immediately after every function call. Never discard errors with `_`. Handle or return every error
- Use `errors.Is()` and `errors.As()` for error comparison and unwrapping — never compare errors with `==`
- Wrap errors with `fmt.Errorf("context: %w", err)` to add context while preserving the error chain for `errors.Is`/`errors.As`
- Use short variable names for local scope (`i`, `r`, `ctx`, `err`) and descriptive names for package-level identifiers (`UserService`, `ParseConfig`)
- Exported names use `PascalCase`, unexported use `camelCase`. Never use underscores in Go names (except in test functions)
- Package names must be short, lowercase, single-word. Do not stutter — use `http.Client`, not `http.HTTPClient`
- Pass `context.Context` as the first parameter of any function that performs I/O, makes network calls, or might need cancellation
- Write table-driven tests using the `[]struct{ name string; ... }` pattern with `t.Run(tt.name, ...)` subtests
- Call `t.Helper()` at the start of test helper functions so test failure output reports the correct calling line
- Use `sync.Mutex` for simple shared-state protection. Reserve channels for communication between goroutines, not for locking
- Use `defer` for resource cleanup (closing files, unlocking mutexes). Understand that deferred calls execute in LIFO order
- Keep interfaces small — 1 to 3 methods. Accept interfaces as parameters, return concrete structs from constructors
- Use `io.Reader` and `io.Writer` interfaces for I/O abstraction instead of concrete file or buffer types
- Use `make([]T, 0, cap)` when the slice capacity is known in advance to avoid repeated allocations
- Avoid `init()` functions unless absolutely necessary (e.g., registering drivers). Prefer explicit initialization in `main` or constructors
- Run `golangci-lint` in CI with a `.golangci.yml` config. Enable at minimum: `govet`, `errcheck`, `staticcheck`, `unused`
- Use `errors.Join()` (Go 1.20+) to combine multiple errors — never concatenate error strings
- Use `slog` (Go 1.21+) for structured logging — avoid third-party loggers unless `slog` is insufficient
- Use `sync.Once` for one-time initialization — never use flags or mutexes for init-once patterns
- Use `embed.FS` for embedding static files — never read from filesystem for bundled assets
- Prefer `slices` package (Go 1.21+) functions (`slices.Contains`, `slices.Sort`) over manual loops
- Use `maps` package (Go 1.21+) for map operations (`maps.Keys`, `maps.Clone`)
- Use `cmp.Or()` (Go 1.22+) for default values — cleaner than if/else chains
- Prefer struct embedding over inheritance-style patterns — compose, don't inherit
- Use `httptest.NewServer` and `httptest.NewRecorder` for HTTP handler testing — never start real servers in tests
- Use `testify/assert` and `testify/require` for cleaner test assertions — `require` for must-pass preconditions, `assert` for checks
- Use `build tags` (`//go:build integration`) to separate unit and integration tests
- Always close response bodies: `defer resp.Body.Close()` after checking for error
- Use `crypto/rand` (not `math/rand` or `math/rand/v2`) for generating keys, tokens, and any security-sensitive random values. Use `crypto/rand.Text` for random strings
- Declare empty slices with `var t []string` (nil slice) — not `t := []string{}` — unless JSON encoding requires a non-nil empty array (`[]` vs `null`)
- Error strings should not be capitalized (unless starting with a proper noun) and should not end with punctuation — they are usually printed following other context like `log.Printf("reading %s: %v", file, err)`
- Prefer synchronous functions that return results directly over asynchronous ones. Let callers add concurrency by calling from a separate goroutine — never force concurrency on the caller
- Define interfaces in the consumer package, not the implementation package. Do not define interfaces on the implementor side "for mocking" — return concrete types from constructors and let consumers define the interfaces they need
- Use `goimports` (superset of `gofmt`) to format code and manage import grouping automatically. Group imports: stdlib, then blank line, then third-party
- Document goroutine lifetimes explicitly — make it clear when and whether goroutines exit. Never leave goroutines in-flight when they are no longer needed; they leak even if their channels are unreachable
- Use a one or two letter abbreviation of the receiver's type name as the method receiver name (e.g., `c` for `Client`, `s` for `Server`). Never use `this`, `self`, or `me`. Be consistent — use the same receiver name across all methods of a type. Do not mix receiver types (pointer vs value) on the same type without good reason
- Never use `panic` for normal error handling — only for truly unrecoverable programmer errors (impossible state, violated invariants). Library code must never panic; always return errors. Use `recover()` only at goroutine boundaries (e.g., HTTP middleware) to prevent a single goroutine crash from taking down the entire program
- Indent error handling, not the happy path — check errors first, return early, and keep the normal code flow at minimal indentation. Write `if err != nil { return err }` followed by the success path, never `if err != nil { ... } else { ... }`
- Don't pass pointers as function arguments just to save a few bytes. If a function only dereferences the pointer (`*x`), pass the value directly. Strings, interface values, and small structs are cheap to copy — reserve pointer parameters for large structs or when mutation/nil-signaling is needed
- Use `sync.Pool` to reuse frequently allocated temporary objects (byte buffers, structs) in hot paths — it significantly reduces GC pressure. Always reset pooled objects before returning them to the pool with `Put()`. Type-assert safely when retrieving with `Get()`
- Avoid named result parameters unless they materially improve godoc clarity (e.g., disambiguating multiple return values of the same type like `lat, long float64`). Never use naked returns in functions longer than a few lines — they harm readability and make the return values ambiguous
- Prefer returning concrete types from constructors and exported functions — only accept interfaces as parameters. This follows the "accept interfaces, return structs" principle and allows adding new methods to implementations without breaking consumers
