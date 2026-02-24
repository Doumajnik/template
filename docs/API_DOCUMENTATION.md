# API Documentation

> **This is a living document.** AI agents MUST update it whenever they discover API usage in the codebase.
> This covers both **APIs the project exposes** (endpoints, webhooks) and **external APIs it consumes** (REST calls, SDKs, third-party services).
> Agents read this file to understand integrations, avoid duplicate clients, and ensure consistent error handling.

**Last updated:** *(not yet — no APIs documented)*

---

## How to Read This File

- **Exposed APIs** — endpoints, routes, webhooks, or services this project provides to consumers.
- **Consumed APIs** — external services, SDKs, REST/GraphQL calls this project makes to third-party systems.
- Each API entry includes: base URL, authentication method, endpoints/methods used, request/response formats, error handling, and rate limits.

## How to Update This File

When you encounter API usage in the codebase (during Discovery, implementation, or review):

1. Determine if it's an **exposed** or **consumed** API.
2. Find the section for that API (or create a new one in alphabetical order).
3. Fill in all known details using the entry format below.
4. Cross-reference with `docs/CODE_INVENTORY.md` to link the API client/handler to its source file.

---

## Exposed APIs

<!-- APIs that this project provides to external consumers. -->
<!-- Add entries as the project exposes endpoints, webhooks, or services. -->

*No exposed APIs yet.*

### Entry Format (Exposed)

```markdown
### {API Name} — `{base path}`

**Type:** REST | GraphQL | WebSocket | gRPC | Webhook
**Auth:** None | API Key | Bearer Token | OAuth2 | Basic
**Base Path:** `/api/v1/{resource}`

#### Endpoints

| Method | Path | Description | Request Body | Response | Status Codes |
| --- | --- | --- | --- | --- | --- |
| `GET` | `/resource` | List all | — | `Resource[]` | 200, 401, 500 |
| `POST` | `/resource` | Create one | `CreateResourceDto` | `Resource` | 201, 400, 401 |

#### Models

| Name | Fields | Notes |
| --- | --- | --- |
| `Resource` | `id: string, name: string, ...` | Main entity |

#### Error Handling

- `400` — validation errors, body: `{ error: string, details: string[] }`
- `401` — unauthorized
- `500` — internal server error
```

---

## Consumed APIs

<!-- External APIs and SDKs that this project calls. -->
<!-- Add entries as the project integrates with third-party services. -->

*No consumed APIs yet.*

### Entry Format (Consumed)

```markdown
### {Service Name} — `{SDK/client name}`

**Docs:** {link to official docs}
**SDK/Package:** `{package name}` v{version}
**Auth:** API Key in header | OAuth2 | Service account | ENV var: `{VAR_NAME}`
**Base URL:** `https://api.example.com/v1`
**Client Location:** `src/utils/{client_file}` or `src/services/{service_file}`

#### Methods Used

| Method / Endpoint | Purpose | Request | Response | Error Handling |
| --- | --- | --- | --- | --- |
| `client.get_users()` | Fetch user list | `params: {limit, offset}` | `List[User]` | Retry 3x, raise on 4xx |
| `POST /webhooks` | Register webhook | `{url, events}` | `{id, status}` | Log and skip on failure |

#### Rate Limits

- {X} requests per {time period}
- Retry strategy: {exponential backoff / fixed delay / none}

#### Environment Variables

| Variable | Purpose | Example |
| --- | --- | --- |
| `SERVICE_API_KEY` | Authentication | `sk-...` |
| `SERVICE_BASE_URL` | Override base URL | `https://api.example.com` |

#### Notes

- {Any gotchas, version-specific behavior, known issues}
```

---

## API Changelog

<!-- Brief log of when APIs were added, changed, or removed. -->

| Date | API | Change |
| --- | --- | --- |
| *(template)* | — | Initial API documentation template created |
