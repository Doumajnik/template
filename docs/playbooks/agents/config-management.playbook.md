+++
id = "agents/config-management"
title = "Config Management Agent Playbook"
agents = ["config-management"]
technologies = ["env", "config", "feature-flags"]
category = "rule"
tags = ["configuration", "environment", "secrets", "feature-flags"]
version = 1
+++

### Config Sources

- **Catalog every config source** — enumerate all `.env` files, config modules, YAML/JSON/TOML files, hardcoded values, and environment variable reads. No hidden config sources.
- **Enforce a single config entry point** — all configuration must be loaded through a centralized config module (`src/config/`). Direct `process.env` / `os.environ` reads outside this module are violations.
- **Map config flow through the application** — trace how each config value moves from source to point of use. Identify any config that is read but never used, or used but never explicitly configured.
- **Verify `.env.example` exists and is current** — every project must have a `.env.example` listing all required environment variables with placeholder values and comments. No real secrets in the example file.
- **Document every config key** — maintain a config reference (in code comments or docs) listing each key, its type, default value, required/optional status, and which environments use it.

### Validation

- **Validate all config at startup** — parse, type-check, and validate every config value when the application boots. Do not defer validation to the point of use.
- **Fail fast on missing required config** — if a required config value is absent or invalid, the application must crash immediately at startup with a clear error message naming the missing key.
- **Type-safe config loading** — every config value must be parsed to its correct type (number, boolean, URL, enum) at load time. String-typed everything is a code smell.
- **Validate value ranges and formats** — beyond type checking, validate that ports are in range, URLs are well-formed, enums match allowed values, and durations are positive.
- **No implicit defaults for critical config** — database URLs, API keys, and service endpoints must be explicitly provided. Silent fallback to localhost or empty strings masks misconfiguration.

### Secrets

- **Never commit secrets to version control** — API keys, passwords, tokens, connection strings, and private keys must never appear in source code, config files, or git history. Severity: CRITICAL.
- **Verify `.gitignore` covers all secret-bearing files** — `.env`, `*.pem`, `*.key`, `credentials.*`, and any project-specific secret files must be gitignored.
- **Never log secrets** — audit all log statements to ensure secrets, tokens, and credentials are not printed, even in debug mode. Sanitize or redact before logging.
- **Use environment variables or a secrets manager for all secrets** — secrets must come from env vars, a vault (HashiCorp Vault, AWS SSM, Azure Key Vault), or a secrets manager. Never from config files.
- **Recommend secret rotation strategy** — every secret should have a defined rotation schedule. Design config so that rotating a secret requires zero code changes and minimal downtime.
- **Audit CI/CD for secret exposure** — ensure pipelines use protected/masked variables. No secrets in build logs, Dockerfiles, or committed CI config.

### Feature Flags

- **Use a consistent naming convention** — prefix all feature flags with `FEATURE_FLAG_` or equivalent. Use `SCREAMING_SNAKE_CASE` for env-based flags.
- **Track flag lifecycle** — every flag must have a creation date, owner, and intended removal date. Flags older than their intended lifecycle are candidates for cleanup.
- **Clean up shipped flags** — features that have been fully rolled out must have their flags removed. Long-lived flags accumulate dead code paths and testing complexity.
- **Avoid flag dependencies** — flag A should not depend on flag B being enabled. If dependencies exist, document them explicitly and recommend consolidation.
- **Test both flag states** — every feature flag must have tests covering both the enabled and disabled paths. Untested flag states are hidden bugs.

### Multi-Environment

- **Never hardcode environment-specific values** — URLs, database hosts, API endpoints, and service addresses must come from config, not source code. Grep for hardcoded `localhost`, `127.0.0.1`, and production hostnames.
- **Maintain environment parity** — staging must mirror production's config structure. If staging uses different config keys or a different config format than production, drift is inevitable.
- **Detect configuration drift** — recommend tooling or processes to compare config across environments. When environments diverge silently, production incidents follow.
- **Use environment prefixes for clarity** — prefix environment variables with the app name (`APP_DB_HOST`, `APP_REDIS_URL`) to avoid collisions with system or third-party variables.
- **Provide a local development setup** — developers must be able to run the project locally with a single `.env` file copied from `.env.example`. No tribal knowledge required.

### Anti-Patterns

- **Flag scattered env reads** — `process.env.X` or `os.environ["X"]` used outside the config module is a violation. All env reads must be centralized.
- **Flag config duplication** — the same config key read in multiple files with potentially different defaults is a bug waiting to happen. Consolidate to one read.
- **Flag magic strings** — config keys used as raw strings (`"DATABASE_URL"`) instead of constants or typed config objects are fragile and un-greppable.
- **Flag missing error context** — when config validation fails, the error message must name the specific key, expected type/format, and actual value received (redacted if secret).
- **Flag environment-conditional logic in business code** — `if (env === "production")` in business logic is a code smell. Use config values or feature flags instead of environment name checks.
