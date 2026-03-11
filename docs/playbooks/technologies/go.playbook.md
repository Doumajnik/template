+++
id = "technologies/go"
title = "Go Conventions"
agents = []
technologies = ["go"]
category = "convention"
tags = ["go", "golang", "modules"]
version = 3
+++

### Go Conventions

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
