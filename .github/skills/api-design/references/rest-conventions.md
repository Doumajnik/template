# REST API Conventions Reference

## Resource Naming

- Use **plural nouns** for collections: `/users`, `/orders`, `/products`.
- Use **kebab-case** for multi-word resources: `/order-items`, `/user-profiles`.
- Nest resources to express ownership: `/users/{userId}/orders`.
- Limit nesting to **2 levels max** — deeper nesting indicates a missing top-level resource.
- Use resource identifiers in the path, never in query params for CRUD: `/users/123` not `/users?id=123`.
- Avoid verbs in paths — use HTTP methods to express actions.
- For non-CRUD actions, use a sub-resource verb: `POST /orders/{id}/cancel`.

## HTTP Method Semantics

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| `GET` | Retrieve resource(s) | Yes | Yes | No |
| `POST` | Create resource or trigger action | No | No | Yes |
| `PUT` | Full replacement of resource | Yes | No | Yes |
| `PATCH` | Partial update of resource | No* | No | Yes |
| `DELETE` | Remove resource | Yes | No | No |

- `PUT` replaces the entire resource — omitted fields reset to defaults.
- `PATCH` updates only the provided fields — omitted fields unchanged.
- `POST` to a collection creates a new resource and returns `201` with `Location` header.
- `DELETE` returns `204` on success — return `404` if the resource never existed, `204` if already deleted (idempotent).

## Status Code Guide

### Success Codes

| Code | When to Use |
|------|-------------|
| `200 OK` | Successful GET, PUT, PATCH. Body contains the resource. |
| `201 Created` | Successful POST that creates a resource. Include `Location` header. |
| `204 No Content` | Successful DELETE or action with no response body. |

### Client Error Codes

| Code | When to Use |
|------|-------------|
| `400 Bad Request` | Malformed syntax, invalid JSON, missing required fields. |
| `401 Unauthorized` | Missing or invalid authentication credentials. |
| `403 Forbidden` | Authenticated but lacks permission for this action. |
| `404 Not Found` | Resource does not exist at this path. |
| `409 Conflict` | State conflict — duplicate key, version mismatch, conflicting update. |
| `422 Unprocessable Entity` | Syntactically valid but semantically invalid — business rule violation. |
| `429 Too Many Requests` | Rate limit exceeded. Include `Retry-After` header. |

### Server Error Codes

| Code | When to Use |
|------|-------------|
| `500 Internal Server Error` | Unexpected server failure. Never expose stack traces. |
| `502 Bad Gateway` | Upstream service returned an invalid response. |
| `503 Service Unavailable` | Server temporarily overloaded or in maintenance. Include `Retry-After`. |

## Error Response Format (RFC 7807)

Use the Problem Details format for all error responses:

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The 'email' field must be a valid email address.",
  "instance": "/users/123",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_FORMAT"
    }
  ]
}
```

- `type` — URI identifying the error type (use as stable error identifier).
- `title` — short human-readable summary (same for all instances of this type).
- `status` — HTTP status code (duplicated for convenience).
- `detail` — human-readable explanation specific to this occurrence.
- `instance` — URI of the resource involved (optional).
- `errors` — array of field-level errors for validation failures (optional).

## Pagination

### Cursor-Based (preferred for large/real-time datasets)

```
GET /orders?cursor=eyJpZCI6MTIzfQ&limit=25
```

Response includes navigation links:

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQ4fQ",
    "has_more": true
  }
}
```

- Stable under concurrent writes — no skipped or duplicated items.
- Cursor is an opaque, base64-encoded token (never expose raw DB IDs).

### Offset-Based (simple lists with known total)

```
GET /products?offset=50&limit=25
```

```json
{
  "data": [...],
  "pagination": {
    "total": 243,
    "offset": 50,
    "limit": 25
  }
}
```

- Include `Link` header with `rel="next"`, `rel="prev"`, `rel="first"`, `rel="last"`.
- Cap `limit` at a maximum (e.g., 100) to prevent abuse.

## Filtering, Sorting, and Field Selection

### Filtering

```
GET /orders?status=shipped&created_after=2025-01-01
```

- Use query parameters with field names.
- Support operators for ranges: `min_price=10&max_price=50` or `price[gte]=10&price[lte]=50`.
- Document all supported filter fields per endpoint.

### Sorting

```
GET /products?sort=price,-created_at
```

- Comma-separated field names. Prefix with `-` for descending.
- Default sort must be deterministic (include a tiebreaker like `id`).

### Field Selection

```
GET /users/123?fields=id,name,email
```

- Return only requested fields to reduce payload size.
- Always include `id` regardless of selection.

## Headers

### Request Headers

| Header | Purpose |
|--------|---------|
| `Content-Type: application/json` | Request body format. Required for POST/PUT/PATCH. |
| `Accept: application/json` | Requested response format. Return `406` if unsupported. |
| `Authorization: Bearer {token}` | Authentication credential. |
| `If-None-Match: "{etag}"` | Conditional GET — return `304` if unchanged. |
| `If-Match: "{etag}"` | Conditional PUT/PATCH — return `412` if resource changed. |
| `Idempotency-Key: {uuid}` | Safe retry for POST requests. |

### Response Headers

| Header | Purpose |
|--------|---------|
| `Location: /users/456` | URI of newly created resource (with `201`). |
| `ETag: "abc123"` | Resource version for caching and conditional requests. |
| `Cache-Control: max-age=3600` | Caching directive. |
| `X-RateLimit-Limit: 100` | Maximum requests per window. |
| `X-RateLimit-Remaining: 42` | Requests remaining in current window. |
| `X-RateLimit-Reset: 1672531200` | Unix timestamp when the window resets. |
| `Retry-After: 30` | Seconds to wait before retrying (with `429` or `503`). |

## Bulk Operations

- Use `POST /users/batch` for bulk creation — accept an array, return an array of results.
- Each item in the response includes its own status code and error (partial success is allowed).
- Set a maximum batch size (e.g., 100 items) and return `400` if exceeded.
- For bulk deletes: `DELETE /users/batch` with a body of IDs (some frameworks require `POST` for body support).
- Always make bulk operations atomic or clearly document partial-success behavior.

## HATEOAS Considerations

- Include `_links` or `links` with `rel` and `href` for discoverability (optional but recommended for public APIs).
- At minimum, include `self` link on every resource.
- Use for pagination (`next`, `prev`), related resources (`orders`, `profile`), and available actions (`cancel`, `approve`).
