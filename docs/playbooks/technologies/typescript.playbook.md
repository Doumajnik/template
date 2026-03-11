+++
id = "technologies/typescript"
title = "TypeScript Conventions"
agents = []
technologies = ["typescript"]
category = "convention"
tags = ["typescript", "types", "eslint"]
version = 3
+++

### TypeScript Conventions

- Use `const` by default. Use `let` only when reassignment is needed. Never use `var`
- Use named exports in all modules. Avoid default exports — they make refactoring and auto-imports harder
- Always use `===` and `!==` for comparison. Never use `==` or `!=`
- Use `interface` for object shapes and class contracts. Use `type` for unions, intersections, mapped types, and conditional types
- Never use `any`. Use `unknown` when the type is genuinely unknown, then narrow with type guards before use
- Use optional chaining (`?.`) and nullish coalescing (`??`) instead of manual null/undefined checks
- Enable `strict` mode in `tsconfig.json`. Ensure `strictNullChecks`, `noImplicitAny`, and `noUncheckedIndexedAccess` are all enabled
- Mark properties and arrays as `readonly` when they should not be mutated after creation
- Use `Record<K, V>` for index signatures instead of `{ [key: string]: V }`
- Use `async`/`await` for all asynchronous code. Never mix callbacks and promises. Avoid raw `.then()` chains
- Destructure objects and arrays at the call site when accessing multiple properties for clarity
- Use `enum` sparingly — prefer union types of string literals (`type Status = 'active' | 'inactive'`) for simple cases
- Use template literals for string building. Never use `+` concatenation for multi-part strings
- Use `Array.isArray()` for array type checks — never `instanceof Array` (fails across realms)
- Module organization: one class or interface per file for large types. Group small, closely related types in a single file
- Add JSDoc comments on all exported functions with `@param`, `@returns`, and `@throws` tags
- Use `Map` and `Set` instead of plain objects when keys are dynamic or non-string
- Prefer functional array methods (`map`, `filter`, `reduce`) over `for` loops for collection transformations. Use `for...of` for side-effectful iteration
- Use `satisfies` operator for type-safe object literals while preserving narrowed types
- Prefer `Readonly<T>` and `ReadonlyArray<T>` for function parameters that shouldn't be mutated
- Use discriminated unions with a `type` or `kind` field for tagged union patterns
- Use `as const` for literal type inference on objects and arrays
- Prefer `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>` utility types over manual re-definitions
- Use `zod`, `io-ts`, or similar for runtime type validation at API boundaries — TypeScript types disappear at runtime
- Use `AbortController` with `AbortSignal` for cancellable async operations
- Prefer `structuredClone()` over `JSON.parse(JSON.stringify())` for deep cloning
- Use `Promise.allSettled()` when you need results from all promises regardless of individual failures
- Use `import type { ... }` for type-only imports — enforced by `verbatimModuleSyntax` in tsconfig
- Use `URL` constructor for URL manipulation — never string concatenation for query parameters
- Prefer `crypto.randomUUID()` for generating unique IDs — never `Math.random().toString(36)`
