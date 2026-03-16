+++
id = "shared/naming-conventions"
title = "Naming Conventions"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["naming", "style", "readability"]
version = 5
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
- Avoid single-character names except for well-established conventions: `i`, `j`, `k` for iterators, `e` for exceptions in `except`, `f` for file handles in `with` — descriptiveness should be proportional to scope (Google Python Style Guide, §3.16.1)
- Never encode the type in the variable name — avoid `id_to_name_dict` or `user_list`; use `id_to_name` or `users` instead (Google Python Style Guide, §3.16.1, Names to Avoid)
- Exception classes must end in `Error` (e.g., `ValidationError`, `ConnectionError`) — never use suffixes like `Exception`, `Fault`, or plain nouns (Google Python Style Guide, §2.4)
- Module filenames must be `lower_snake_case` and must not contain dashes — this ensures they are importable (Google Python Style Guide, §3.16.3)
- Avoid double-underscore name mangling (`__var`) for internal attributes — prefer single underscore (`_var`), which is more readable and testable (Google Python Style Guide, §3.16.2)
- Descriptiveness scales with scope: a loop variable `i` in a 3-line loop is fine, but a module-level variable must have a fully descriptive name that communicates intent without reading surrounding code (Clean Code, Meaningful Names)
- Async function names should indicate their asynchronous nature when the sync counterpart also exists — use a consistent prefix/suffix convention per project (e.g., `fetch_user` vs `fetch_user_async`)
- Never prefix interfaces with `I` (e.g., use `UserService` not `IUserService`) — give interfaces names that express why the interface exists (e.g., `UserStorage` for a storage contract, `Serializable` for a capability) (Google TypeScript Style Guide, §5.1.1)
- Do not use trailing or leading underscores for private properties or methods in TypeScript — use the `private` visibility modifier instead, which is enforced at compile time (Google TypeScript Style Guide, §5.2.3)
- Use `lowerCamelCase` for module namespace imports in TypeScript (e.g., `import * as fooBar from './foo_bar'`) — the namespace name follows variable conventions, not the file's snake_case (Google TypeScript Style Guide, §5.2.4)
- Do not create container classes with only static members for namespacing — export individual constants and functions at module level instead of wrapping them in a class (Google TypeScript Style Guide, §3.4.3)
- Type aliases must use `UpperCamelCase` (e.g., `type UserConfig = {...}`) — treat them like classes and interfaces since they represent named types in the type system (Google TypeScript Style Guide, §5.2)
- Name test files and test methods to read as behavior specifications: `test_transfer_funds_fails_when_insufficient_balance` tells the story without reading the test body — avoid opaque names like `test_case_1` or `test_happy_path` (Google Testing Blog, Code Health — Identifier Naming)
- Decorator names follow `UpperCamelCase` convention (e.g., `@Component`, `@Injectable`) — when creating custom decorators, name them as nouns or adjectives describing the capability they provide, not verbs (Google TypeScript Style Guide, §5.2)
