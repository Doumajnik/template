---
description: "FastAPI coding conventions and best practices. Use when writing, reviewing, or refactoring FastAPI applications."
applyTo: "**/*.py"
---

# FastAPI Conventions

- Organize routes with `APIRouter` per domain module (e.g., `routers/users.py`, `routers/orders.py`). Set `prefix`, `tags`, and `dependencies` on each router. Mount routers in a central `app.py` — never define routes directly on the `FastAPI()` instance in large projects
- Define all request and response shapes as Pydantic `BaseModel` subclasses. Use `Field()` with `description`, `examples`, and constraints (`min_length`, `ge`, `le`). Set `model_config = ConfigDict(strict=True)` to reject type coercion where precision matters
- Use `@field_validator` and `@model_validator` (Pydantic v2) for custom validation logic. Return the validated value from field validators. Use `mode='before'` for input normalization and `mode='after'` for cross-field checks
- Use `Depends()` for all shared logic: database sessions, auth, pagination, feature flags. Compose dependencies — a dependency can depend on other dependencies. Never use module-level global state for request-scoped resources
- Use `async def` for route handlers that perform I/O (database, HTTP calls, file access). Use plain `def` for CPU-bound handlers — FastAPI runs them in a thread pool automatically. Never call blocking I/O inside `async def` without `run_in_executor`
- Register custom exception handlers with `@app.exception_handler(CustomError)` for domain-specific errors. Return structured JSON error responses with `detail`, `code`, and optional `field` keys. Never let raw Python exceptions leak to clients
- Always declare an explicit `response_model` on route decorators to control serialized output. Use `response_model_exclude_unset=True` for PATCH endpoints. Never return ORM models or internal objects directly — always map through a Pydantic schema
- Use the correct HTTP status codes: `201` for resource creation, `204` for deletion with no body, `422` for validation errors. Import from `fastapi.status` for readability (e.g., `status.HTTP_201_CREATED`)
- Use `Path()` for path parameters with validation, `Query()` for query parameters with defaults and constraints, `Body()` for non-model body fields. Always add `description` to parameters that appear in OpenAPI docs
- Use `BackgroundTasks` for lightweight post-response work (sending emails, logging). For heavy or unreliable tasks, delegate to a proper task queue (Celery, ARQ) — `BackgroundTasks` has no retry or persistence
- Use the `lifespan` context manager (async generator) on the `FastAPI()` app for startup/shutdown logic (connection pools, caches). Never use the deprecated `@app.on_event("startup")` / `@app.on_event("shutdown")`
- Configure CORS with `CORSMiddleware` specifying explicit `allow_origins` — never use `["*"]` in production. Set `allow_credentials`, `allow_methods`, and `allow_headers` to the minimum required
- Implement authentication with `OAuth2PasswordBearer` or custom `HTTPBearer` security schemes. Validate JWTs in a dependency — decode, verify signature and expiry, and return the user. Never store secrets in code — load from `pydantic-settings`
- Use SQLAlchemy 2.0 async with `create_async_engine` and `async_sessionmaker`. Yield sessions from a `Depends` function with `async with` to ensure cleanup. Never share a single session across requests or store sessions in module-level globals
- Write tests with `httpx.AsyncClient` and `ASGITransport` for async routes. Use `TestClient` (sync) only for sync-only apps. Override dependencies with `app.dependency_overrides[dep] = mock_dep` for isolated testing — always clean up overrides after tests
- Customize OpenAPI metadata on the `FastAPI()` constructor: `title`, `version`, `description`, `servers`. Use `openapi_extra` on routes for schema extensions. Generate clients from the `/openapi.json` endpoint
- Use `UploadFile` for file uploads — access `.file` (SpooledTemporaryFile) for streaming reads. Validate file size and content type before processing. Never read the entire file into memory for large uploads — stream to disk or object storage
- Use `WebSocket` routes with proper accept/disconnect handling. Wrap receive loops in `try`/`WebSocketDisconnect` to handle client disconnects gracefully. Authenticate WebSocket connections in the handshake phase via query params or first message
- Implement rate limiting with a middleware or dependency (e.g., `slowapi` or a custom Redis-based limiter). Apply per-route or per-user limits. Return `429 Too Many Requests` with a `Retry-After` header
- Use `pydantic-settings` (`BaseSettings` with `SettingsConfigDict`) for all configuration. Load from environment variables and `.env` files. Define `model_config = SettingsConfigDict(env_file='.env', env_prefix='APP_')`. Never hardcode configuration values
- Use `Annotated` types with `Depends` for reusable dependency declarations (e.g., `CurrentUser = Annotated[User, Depends(get_current_user)]`). This keeps route signatures clean and dependency intent explicit
- Return `JSONResponse` with custom status codes for non-default responses. Use `Response` with `media_type` for non-JSON payloads (CSV, PDF). Use `StreamingResponse` for large outputs and `FileResponse` for static file downloads
- Use middleware sparingly and keep it lightweight — expensive middleware runs on every request. Use dependencies for route-specific concerns. Register middleware in reverse priority order (last added runs first)
- Structure the project as: `app/main.py` (app factory), `app/routers/` (route modules), `app/schemas/` (Pydantic models), `app/models/` (ORM models), `app/services/` (business logic), `app/dependencies/` (shared deps), `app/core/` (config, security)
- Use `HTTPException` for expected client errors only. For internal errors, let them propagate to a global exception handler that logs the traceback and returns a generic 500 response. Never expose internal error details to clients in production
- Use sub-applications (`app.mount("/admin", admin_app)`) for fully independent modules with their own OpenAPI docs. Use routers for related endpoints under the same app
- Implement health check endpoints (`/health`, `/ready`) that verify database connectivity and dependency availability. Return structured JSON with component status. Use these for container orchestration probes
- Use `Enum` types in Pydantic models and path/query params for fixed option sets — FastAPI auto-generates the allowed values in OpenAPI. Never accept raw strings where a fixed set of values is expected
- Apply security headers via middleware: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`. Use `secure` and `httponly` flags on all cookies. Never store tokens in cookies without `SameSite=Strict`
- Use `orjson` or `ujson` as the response serializer (`default_response_class=ORJSONResponse`) for performance on large payloads. Install `python-multipart` when using `Form` or `UploadFile` — FastAPI does not include it by default
- Use response caching with `Cache-Control` headers for GET endpoints that return stable data. Implement `ETag`/`If-None-Match` for conditional requests. Use an in-memory or Redis cache for expensive computations — never cache inside route functions with mutable module-level dicts
- For pagination, accept `skip`/`limit` or `page`/`size` query params with sensible defaults and max caps. Return pagination metadata (`total`, `page`, `pages`) in the response body or `Link` headers. Never return unbounded result sets
- Use `APIRouter.dependencies` for route-group-level guards (auth, rate limit). Use `Depends` in individual route signatures for route-specific logic. Layer dependencies — common auth at router level, role checks at route level
