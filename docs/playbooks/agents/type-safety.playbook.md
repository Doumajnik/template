+++
id = "agents/type-safety"
title = "Type Safety Agent Rules"
agents = ["type-safety"]
technologies = ["all"]
category = "rule"
tags = ["type-safety"]
version = 4
+++

### Type Safety Audit Rules

- Scan for `any` types (TypeScript), missing type annotations (Python), or `object` overuse (C#).
- Flag `as` type casts that bypass the type system — each must be justified with a comment explaining why.
- Verify all public function signatures have complete type annotations — parameters AND return types.
- Check for type narrowing gaps: after a type guard check, the narrowed type should be used consistently.
- Verify generic types are constrained when possible — `T extends Base` not just bare `T`.
- Flag schema drift: API types, database types, and frontend types for the same entity must match.
- Check for nullability gaps: optional fields must be handled at every usage site, not just the definition.
- Verify discriminated unions have exhaustive checks — a switch/match over a union must cover all variants.
- Flag `// @ts-ignore` and `# type: ignore` comments — each must have a justification explaining why the suppression is needed.
- Check that runtime validation (zod, pydantic) matches the static types — they must not diverge.
- Produce a report with: file, line, issue, severity, recommended fix.
- CRITICAL findings (untyped public APIs, schema drift) must be fixed before release.
- Ensure all `__init__` methods have explicit return type annotations (`-> None`) — omitting this causes implicit `Any` types to leak into all instance variables.
- Prefer immutable collection types in function signatures (`Sequence` over `list`, `Mapping` over `dict`) to avoid invariance issues and support covariant subtyping.
- Flag functions with no type annotations at all — these are completely unchecked by type checkers and silently pass even with obvious errors.
- Check for blanket `--ignore-missing-imports` or `follow_imports = skip` in type checker config — these silently replace entire modules with `Any`, masking real type errors.
- Verify `TypedDict`, dataclass, and Pydantic model field definitions match across code generation boundaries (API clients, ORM models, serializers).
- Flag `cast()` usage without an adjacent runtime assertion or type guard — prefer `isinstance` checks or `assert` statements that provide runtime-verifiable narrowing.
- Audit for invariance vs covariance mismatches — mutable generic collections (`list[T]`, `dict[K, V]`) are invariant; assigning `list[SubClass]` to `list[BaseClass]` is a type error.
- Prefer `Protocol` classes (structural subtyping) over ABC inheritance for defining interfaces — this enables duck-typing compatibility without requiring explicit base class inheritance (PEP 544).
- Use `@runtime_checkable` on Protocol classes only when runtime `isinstance` checks are genuinely needed — runtime checks only verify method/attribute existence, not signature correctness or return types.
- Declare mutable Protocol attributes as `@property` (read-only) to avoid invariance pitfalls — a Protocol with a mutable `content: object` attribute will reject `content: int` implementations due to invariance.
- Use callback protocols (Protocol with `__call__`) for complex callable signatures that cannot be expressed with `Callable[...]` — this supports keyword arguments, overloads, and variadic parameters with full type checking.
- Prefer `ParamSpec` and `Concatenate` for decorator type annotations that preserve the decorated function's parameter types — avoid losing parameter type information by typing decorators as `Callable[..., Any]`.
- Use `TypeGuard` (or `TypeIs` in Python 3.13+) for custom type narrowing functions — return `TypeGuard[T]` from predicate functions so type checkers narrow the type in conditional branches.
- Flag `@overload` definitions that lack a non-overloaded implementation — every set of `@overload` signatures must have exactly one non-decorated implementation that handles all cases at runtime.
