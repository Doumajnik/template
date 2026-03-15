+++
id = "technologies/typescript"
title = "TypeScript Conventions"
agents = []
technologies = ["typescript"]
category = "convention"
tags = ["typescript", "types", "eslint"]
version = 5
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
- Never use `@ts-ignore`, `@ts-expect-error`, or `@ts-nocheck` directives. Fix the underlying type issue instead of suppressing it
- Use `as` syntax for type assertions (`value as Type`). Never use angle-bracket syntax (`<Type>value`) — it conflicts with JSX and is inconsistent
- Do not use the `namespace` keyword. Use ES modules with `import`/`export` for all code organization
- Only throw `Error` objects (or subclasses). Never throw strings, numbers, or plain objects — non-Error values lack stack traces
- Never use `eval()`, `new Function(...string)`, or any dynamic code evaluation. They create injection risks and prevent static analysis
- Do not use ECMAScript `#private` fields. Use TypeScript’s `private` modifier which provides compile-time enforcement and is stripped at runtime
- Prefer `Number()` over `parseInt()`/`parseFloat()` for string-to-number conversion. If you must use `parseInt()`, always specify the radix explicitly
- Always handle or explicitly discard Promise return values — never let Promises float unhandled. Either `await` the promise, `return` it, assign it, or prefix with `void` if deliberately ignoring the result. Unhandled rejections crash Node.js processes and silently swallow errors in browsers
- Do not rely on JavaScript truthiness coercion in boolean positions (conditionals, `&&`, `||`). Explicitly compare with `!== null`, `!== undefined`, `!== 0`, `.length > 0`, etc. instead of using implicit coercion, which mishandles `0`, `""`, and `NaN`
- Use `T[]` syntax for simple array types and `Array<T>` only when the element type is complex (union, intersection, or conditional). Be consistent within a codebase. Use `readonly T[]` over `ReadonlyArray<T>` for the same reason
- Always `return await` inside `try`/`catch`/`finally` blocks so that exceptions from the awaited promise are caught by the local error handler. Outside try/catch, return the promise directly without `await` to avoid unnecessary microtask overhead
- When switching on a discriminated union type, handle all variants explicitly. Add an exhaustiveness check using `default: { const _exhaustive: never = value; throw new Error("Unhandled case"); }` to get a compile-time error when new variants are added
- Always provide a comparison function to `Array.prototype.sort()` and `Array.prototype.toSorted()` — the default sort converts elements to strings, producing incorrect results for numbers (`[10, 2, 1].sort()` → `[1, 10, 2]`) and unexpected ordering for most types
- Do not pass `async` functions where a `void`-returning callback is expected (e.g., `forEach`, `addEventListener`, event emitter handlers). The returned Promise will be silently ignored and rejections will be swallowed. Wrap in a synchronous function that explicitly handles the error
