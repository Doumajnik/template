---
name: api-design
description: "Full workflow for REST/GraphQL API design, OpenAPI spec generation, endpoint validation, and versioning strategy. Use when designing new APIs, reviewing existing endpoints, or migrating API versions. Triggers on: API, endpoint, REST, GraphQL, OpenAPI, swagger."
---

# API Design Skill

## When to Use

- Designing a new REST or GraphQL API from scratch
- Reviewing or auditing existing API endpoints for consistency
- Generating or updating OpenAPI/Swagger specifications
- Planning API versioning strategy or version migration
- Defining resource schemas, naming conventions, or error formats
- Adding pagination, filtering, or sorting to endpoints
- Reviewing API security (auth flows, rate limiting, CORS, input validation)
- Writing consumer-driven contract tests for API consumers

## Pipeline

### Phase 1 — Requirements & Analysis

1. Identify the **resource model** — entities, relationships, cardinality, ownership boundaries.
2. Map **consumer needs** — who calls the API (frontend, mobile, third-party, internal services), what data they need, and in what shape.
3. Document **use cases** — list every operation consumers perform (CRUD, search, bulk, async).
4. Define **authentication and authorization requirements** — API keys, OAuth 2.0 flows, JWT, RBAC/ABAC, scopes.
5. Identify **non-functional requirements** — rate limits, latency targets, payload size limits, caching strategy.
6. Review existing APIs (if any) for patterns to preserve or deprecate.
7. Output: requirements brief with resource map, consumer matrix, and auth model.

### Phase 2 — API Design

1. Spawn **API Design Agent** with the requirements brief.
2. Define **resource endpoints** following REST conventions (see `./references/rest-conventions.md`).
3. Design **request/response schemas** — use JSON Schema, define required vs optional fields, nullable rules.
4. Choose **naming conventions** — plural nouns, kebab-case paths, camelCase fields (or snake_case per project standard).
5. Define **versioning strategy** (see `./references/versioning-strategy.md`) — URL prefix, header, or query param.
6. Design **error response format** — adopt RFC 7807 Problem Details or project-standard error envelope.
7. Define **pagination strategy** — cursor-based for large/real-time datasets, offset-based for simple lists.
8. Design **filtering, sorting, and field selection** query parameters.
9. Output: endpoint inventory with method, path, request/response schemas, status codes, and auth requirements.

### Phase 3 — OpenAPI Specification

1. Generate **OpenAPI 3.1 YAML** spec from the endpoint inventory.
2. Include `info`, `servers`, `paths`, `components/schemas`, `components/securitySchemes`, and `tags`.
3. Add `description` and `example` to every schema property and response.
4. Define **reusable components** — shared error schemas, pagination wrappers, common headers.
5. Validate the spec with an OpenAPI linter (e.g., Spectral, redocly lint).
6. Fix all linter warnings — zero tolerance for spec violations.
7. Output: validated OpenAPI 3.1 YAML file committed to the repo.

### Phase 4 — Security Review

1. Spawn **Security Agent** with the OpenAPI spec and auth model.
2. Verify **authentication flows** — token issuance, refresh, revocation, expiry.
3. Validate **authorization rules** — every endpoint has explicit auth requirements, no open-by-default.
4. Check **input validation** — max lengths, allowed characters, type constraints on all parameters.
5. Review **rate limiting** — per-endpoint and per-consumer limits, proper `429` responses with `Retry-After`.
6. Audit **CORS configuration** — allowed origins, methods, headers, credentials policy.
7. Check for **mass assignment** — ensure request schemas don't accept admin-only or internal fields.
8. Verify **sensitive data handling** — no secrets in URLs, PII redacted in logs, proper `Cache-Control`.
9. Output: security findings appended to `docs/SECURITY_REPORT.md`.

### Phase 5 — Implementation

1. Spawn **Worker** (one per route handler) with the OpenAPI spec as the contract.
2. Implement route handlers matching the spec exactly — method, path, request validation, response shape, status codes.
3. Add **request validation middleware** — reject malformed requests with `400`/`422` before hitting business logic.
4. Implement **pagination, filtering, sorting** according to the spec.
5. Add **proper error handling** — map domain errors to HTTP status codes, return RFC 7807 bodies.
6. Implement **auth middleware** — verify tokens, enforce scopes, return `401`/`403` as appropriate.
7. Add **response serialization** — ensure responses match the schema, strip internal fields.
8. Run unit tests in red-green loop until all pass.

### Phase 6 — Contract Testing

1. Spawn **Integration Tester** with the OpenAPI spec.
2. Write **consumer-driven contract tests** — verify every endpoint returns the documented schema.
3. Test **error paths** — invalid input (`400`/`422`), unauthorized (`401`), forbidden (`403`), not found (`404`), conflict (`409`).
4. Test **pagination** — first page, last page, empty results, invalid cursor/offset.
5. Test **rate limiting** — verify `429` responses include `Retry-After` header.
6. Test **versioning** — requests with version header/URL, deprecated version warnings.
7. Test **content negotiation** — `Accept` header handling, `406` for unsupported types.
8. Run full suite and verify zero failures.

### Phase 7 — Documentation

1. Spawn **Doc Updater** with the OpenAPI spec and implementation details.
2. Generate human-readable API docs from the OpenAPI spec (e.g., Redoc, Swagger UI).
3. Update `docs/API_DOCUMENTATION.md` with endpoint summaries, auth instructions, and examples.
4. Add **getting started** section — base URL, authentication setup, first request example.
5. Document **rate limits, pagination patterns, error format** for consumers.
6. Update `docs/BUSINESS_LOGIC.md` with API-related data flows and module responsibilities.
7. Update `docs/CODE_INVENTORY.md` with new route handlers, middleware, and schemas.

## Reference Files

- [`./references/rest-conventions.md`](./references/rest-conventions.md) — REST naming, HTTP methods, status codes, pagination, filtering, error format
- [`./references/versioning-strategy.md`](./references/versioning-strategy.md) — URL vs header versioning, deprecation timelines, backward compatibility rules
