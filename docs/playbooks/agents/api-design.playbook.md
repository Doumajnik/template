+++
id = "agents/api-design"
title = "API Design Agent Rules"
agents = ["api-design"]
technologies = ["all"]
category = "rule"
tags = ["api-design"]
version = 2
+++

### API Design Agent Rules

1. Design APIs contract-first: define the spec (OpenAPI/AsyncAPI) before implementation.
2. Use RESTful naming: plural nouns for resources (`/users`, `/orders`), kebab-case for multi-word.
3. Use standard HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
4. Use standard HTTP status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 500 Internal Server Error.
5. Version APIs in the URL path: `/api/v1/users` — never in headers or query parameters.
6. Pagination for list endpoints: use `limit`/`offset` or cursor-based pagination. Return total count.
7. Error responses must include: error code (machine-readable), message (human-readable), request_id.
8. Use consistent field naming: `camelCase` for JSON APIs, `snake_case` for internal Python APIs.
9. Rate-limit all public endpoints — return `429 Too Many Requests` with `Retry-After` header.
10. Document every endpoint: method, path, request body, response body, error responses, authentication requirements.
11. Validate all request input — return 400/422 with specific field-level errors.
12. Never expose internal IDs, stack traces, or implementation details in API responses.
