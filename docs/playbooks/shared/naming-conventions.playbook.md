+++
id = "shared/naming-conventions"
title = "Naming Conventions"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["naming", "style", "readability"]
version = 3
+++

### Naming Conventions

- Files: `lower_snake_case.py`, `lower-kebab-case.ts` — never mixed case or spaces
- Classes: `PascalCase` (e.g., `UserService`, `HttpClient`)
- Functions/methods: `lower_snake_case` (Python), `camelCase` (JS/TS)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `API_URL`)
- Private/internal: prefix with underscore `_` (Python), no I-prefix for interfaces (TS)
- Boolean variables/functions: use `is_`, `has_`, `can_`, `should_` prefixes
- Test files: `test_<module>.py` (Python), `<module>.test.ts` (TypeScript)
- Test functions: `test_<function>_<scenario>` — descriptive of what's being tested
- Avoid generic names: `data`, `info`, `temp`, `result`, `thing` — be specific
- Acronyms in names: treat as words — `HttpClient` not `HTTPClient`, `getUrl` not `getURL`
- Event handlers: `on_<event>` or `handle_<event>` — be consistent per project
- Factory functions: `create_<thing>()` or `make_<thing>()` — be consistent per project
- Conversion functions: `to_<target_type>()` (e.g., `to_dict()`, `to_json()`, `toString()`)
- Predicate functions: `is_<condition>()`, `has_<property>()`, `can_<action>()` — must return boolean
- Collection variables: use plural nouns (`users`, `items`, `records`) — never `user_list` or `userArray`
- Iterators/loop variables: `for user in users`, `for item in items` — singular of the collection name
- Environment variables: `UPPER_SNAKE_CASE` with project prefix (e.g., `APP_DATABASE_URL`, `APP_LOG_LEVEL`)
- Config files: `lower-kebab-case.json` or `lower_snake_case.toml` — match the ecosystem convention
- Database tables: `plural_snake_case` (e.g., `user_accounts`, `order_items`)
- API endpoints: plural nouns, kebab-case (`/api/v1/user-accounts`) — never camelCase or PascalCase in URLs
- Callback/handler parameters: use descriptive names (`onUserCreated`, `handleSubmit`) — never `cb`, `fn`, or `handler`
- Type parameters/generics: single uppercase for simple (`T`, `K`, `V`), descriptive for complex (`TResponse`, `TConfig`)
