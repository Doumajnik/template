# API Versioning Strategy Reference

## Versioning Approaches

### URL Path Versioning (recommended for most projects)

```
GET /api/v1/users
GET /api/v2/users
```

- **Pros:** explicit, easy to route, cache-friendly, visible in logs and docs.
- **Cons:** proliferates routes, harder to share middleware across versions.
- **When to use:** public APIs, APIs with multiple external consumers, when simplicity matters.

### Header Versioning

```
GET /api/users
Accept: application/vnd.myapi+json;version=2
```

Or with a custom header:

```
GET /api/users
X-API-Version: 2
```

- **Pros:** clean URLs, single route per resource, content negotiation friendly.
- **Cons:** less visible, harder to test in browser, requires header inspection in middleware.
- **When to use:** internal APIs, APIs where URL cleanliness is critical.

### Query Parameter Versioning (discouraged)

```
GET /api/users?version=2
```

- **Cons:** pollutes query namespace, caching issues, easy to forget.
- **When to use:** only as a fallback when neither URL nor header versioning is feasible.

## When to Bump Versions

### Breaking Changes (MUST bump major version)

- Removing a field from a response
- Removing an endpoint
- Renaming a field
- Changing a field's data type (string → integer, object → array)
- Changing the meaning/semantics of a field
- Making an optional field required
- Changing authentication mechanism
- Changing error response format
- Modifying enum values (removing or renaming)

### Non-Breaking Changes (NO version bump needed)

- Adding a new field to a response (additive)
- Adding a new endpoint
- Adding a new optional query parameter
- Adding a new optional request body field
- Adding new enum values (if consumers handle unknown values)
- Improving error messages (without changing structure)
- Adding new HTTP headers
- Performance improvements with identical behavior

## Backward Compatibility Rules

1. **Never remove fields** from a response without a version bump.
2. **Never change field types** — if `price` was a string, it stays a string in that version.
3. **New required fields** on requests must have a default value or go in a new version.
4. **Enum expansions** are safe only if consumers are documented to handle unknown values.
5. **Test backward compatibility** — maintain contract tests for every supported version.
6. **Document assumptions** — if consumers must handle unknown fields gracefully, state it in the API contract.

## Deprecation Timeline

### Phase 1 — Announce (minimum 3 months before sunset)

- Add `Deprecated: true` to the OpenAPI spec for affected endpoints.
- Return `Sunset: Sat, 01 Mar 2026 00:00:00 GMT` header on all deprecated endpoint responses.
- Return `Deprecation: true` header.
- Log a warning for every request to deprecated endpoints.
- Notify consumers via changelog, email, or developer portal.

### Phase 2 — Migration Period (3–6 months)

- Publish a **migration guide** documenting every change and how to update.
- Provide **side-by-side examples** — old request/response vs new request/response.
- Offer **tooling support** — codemods, migration scripts, compatibility shims.
- Monitor usage of deprecated endpoints — reach out to remaining consumers.

### Phase 3 — Sunset

- Return `410 Gone` for all requests to the deprecated version.
- Include a response body with migration instructions and a link to the new version.
- Remove deprecated version from API docs (archive separately).
- Keep deprecated route handlers in code for 1 release cycle, then remove.

## Feature Flags as Alternative to Versioning

For internal APIs or APIs with few consumers, feature flags can replace versioning:

```
GET /api/users
X-Feature-Flags: new-user-schema
```

- **Use when:** changes affect a small number of consumers, rollout is gradual, or A/B testing is needed.
- **Avoid when:** breaking changes affect all consumers, or the API is public.
- Feature flags must have a **defined expiration** — they are temporary, not permanent forks.
- Remove the flag and make the new behavior default once migration is complete.

## API Lifecycle Stages

| Stage | Description | Stability | SLA |
|-------|-------------|-----------|-----|
| **Alpha** | Experimental, may change without notice | None | No |
| **Beta** | Feature-complete, may have breaking changes with notice | Low | Best-effort |
| **Stable** | Production-ready, follows versioning and deprecation policy | High | Yes |
| **Deprecated** | Still functional but scheduled for removal | High (maintained) | Yes (until sunset) |
| **Sunset** | Removed, returns `410 Gone` | N/A | N/A |

- Mark the lifecycle stage in the OpenAPI spec `info.x-lifecycle: stable`.
- Alpha/Beta APIs must include a warning header: `Warning: 299 - "This API is in beta and may change."`.
- Never promote directly from Alpha to Stable — always go through Beta first.
- Document the lifecycle stage prominently in API docs.

## Version Negotiation Flow

1. Client sends request with version indicator (URL path, header, or query param).
2. Server resolves the version — if missing, use the **latest stable** version (never default to alpha/beta).
3. If the requested version is deprecated, serve the response but include `Sunset` and `Deprecation` headers.
4. If the requested version is sunset, return `410 Gone` with migration info.
5. If the requested version is unknown, return `400 Bad Request` with a list of supported versions.
