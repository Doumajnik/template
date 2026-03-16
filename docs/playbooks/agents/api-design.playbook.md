+++
id = "agents/api-design"
title = "API Design Agent Rules"
agents = ["api-design"]
technologies = ["all"]
category = "rule"
tags = ["api-design"]
version = 4
+++

### API Design Agent Rules

- Design APIs contract-first: define the spec (OpenAPI/AsyncAPI) before implementation.
- Use RESTful naming: plural nouns for resources (`/users`, `/orders`), kebab-case for multi-word.
- Use standard HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
- Use standard HTTP status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 500 Internal Server Error.
- Version APIs in the URL path: `/api/v1/users` — never in headers or query parameters.
- Pagination for list endpoints: use `limit`/`offset` or cursor-based pagination. Return total count.
- Error responses must include: error code (machine-readable), message (human-readable), request_id.
- Use consistent field naming: `camelCase` for JSON APIs, `snake_case` for internal Python APIs.
- Rate-limit all public endpoints — return `429 Too Many Requests` with `Retry-After` header.
- Document every endpoint: method, path, request body, response body, error responses, authentication requirements.
- Validate all request input — return 400/422 with specific field-level errors.
- Never expose internal IDs, stack traces, or implementation details in API responses.
- Ensure PUT and DELETE operations are idempotent — repeated identical requests must produce the same result. Use idempotency keys for non-idempotent POST requests.
- Support HATEOAS where practical — include hypermedia links in responses (`rel`, `href`, `action`) to enable client discovery of related resources and available operations.
- Return 202 Accepted with a status polling endpoint URI in the `Location` header for long-running asynchronous operations.
- Implement content negotiation via `Accept` and `Content-Type` headers — return 406 Not Acceptable when the requested media type is unsupported and 415 Unsupported Media Type for unrecognized request content types.
- Support filtering and sorting via query parameters (e.g., `?sort=created_at&status=active`) — validate and whitelist allowed filter fields to prevent injection.
- Propagate distributed tracing headers (`Correlation-ID`, `X-Request-ID`) through all API layers for end-to-end request tracking and debugging.
- Support sparse fieldsets via a `fields` query parameter (e.g., `?fields=id,name,email`) to reduce payload size — validate requested fields against the allowed set.
- Implement conditional requests using ETags: return `ETag` headers on GET responses, support `If-None-Match` for cache validation (returning 304 Not Modified), and `If-Match` for optimistic concurrency on PUT/DELETE (returning 412 Precondition Failed).
- Expose a health check endpoint (`/health` or `/healthz`) that returns the service's operational status and dependency health — use HTTP 200 for healthy and HTTP 503 for degraded or unavailable states.
- Support HTTP compression (`Accept-Encoding: gzip`) for responses and chunked transfer encoding for streaming large payloads — return 413 Request Entity Too Large when request bodies exceed acceptable limits.
- Implement a global exception handler that maps all unhandled exceptions to structured error responses with appropriate HTTP status codes — distinguish client errors (4xx) from server errors (5xx) consistently.
- Deploy APIs behind an API gateway to centralize cross-cutting concerns: authentication, rate limiting, request routing, SSL termination, and response caching — keep business logic in the API service, not the gateway.
- Implement PATCH using JSON Merge Patch (RFC 7396) or JSON Patch (RFC 6902) for partial updates — clearly document which format is supported and validate patch operations against the resource schema.
- Avoid chatty API designs — provide batch endpoints or collection-level operations (batch POST, bulk DELETE) to reduce round-trips; every request carries protocol, network, and compute overhead.
