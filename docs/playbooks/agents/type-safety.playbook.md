+++
id = "agents/type-safety"
title = "Type Safety Agent Rules"
agents = ["type-safety"]
technologies = ["all"]
category = "rule"
tags = ["type-safety"]
version = 2
+++

### Type Safety Audit Rules

1. Scan for `any` types (TypeScript), missing type annotations (Python), or `object` overuse (C#).
2. Flag `as` type casts that bypass the type system — each must be justified with a comment explaining why.
3. Verify all public function signatures have complete type annotations — parameters AND return types.
4. Check for type narrowing gaps: after a type guard check, the narrowed type should be used consistently.
5. Verify generic types are constrained when possible — `T extends Base` not just bare `T`.
6. Flag schema drift: API types, database types, and frontend types for the same entity must match.
7. Check for nullability gaps: optional fields must be handled at every usage site, not just the definition.
8. Verify discriminated unions have exhaustive checks — a switch/match over a union must cover all variants.
9. Flag `// @ts-ignore` and `# type: ignore` comments — each must have a justification explaining why the suppression is needed.
10. Check that runtime validation (zod, pydantic) matches the static types — they must not diverge.
11. Produce a report with: file, line, issue, severity, recommended fix.
12. CRITICAL findings (untyped public APIs, schema drift) must be fixed before release.
