# Deprecation Manager Playbook

## Timeline Defaults

| Surface | Announce | Warn | Remove |
| --- | --- | --- | --- |
| Internal-only utility | Now | Same release | Next minor |
| Internal API used by 2+ teams | Now | Next minor | Minor + 2 |
| Public REST/GraphQL endpoint | Now | Next minor | Major bump |
| SDK / client library | Now | Next minor | Major + 2 minors |
| CLI flag | Now | Next minor | Major bump |

## Warning Mechanism by Language / Surface

| Surface | Mechanism |
| --- | --- |
| Python function | `@deprecated` decorator + `warnings.warn(..., DeprecationWarning)` |
| TypeScript function | JSDoc `@deprecated` + runtime `console.warn` (gated by env) |
| REST endpoint | `Deprecation: true` header, `Sunset: <date>` header per RFC 8594 |
| GraphQL field | `@deprecated(reason: "...")` directive |
| Config key | Read both old and new; log warn when old is used |
| CLI flag | Print warning to stderr when used |

## Deprecation Entry Template

In `docs/DEPRECATION_LOG.md`:

```markdown
### [STATUS] {Surface} — {short name}

- **What:** `module.function_name` / `GET /v1/foo`
- **Status:** ⬜ Announced / 🟡 Warning / 🔴 Removed
- **Reason:** {one sentence}
- **Replacement:** `module.new_function_name` / `GET /v2/foo`
- **Migration guide:** {inline snippet or link}
- **Announce date:** YYYY-MM-DD (release vX.Y.Z)
- **Warn date:** YYYY-MM-DD (release vX.Y.Z)
- **Remove date:** YYYY-MM-DD (release vX.Y.Z)
- **Internal callers:** {count} — see {todo file or list}
- **External consumers notified:** {channels — changelog, email, status page}
```

## Anti-Patterns

- Deprecating without a replacement — leaves users stranded.
- Removing before the announced date — breaks trust.
- Warnings that are too noisy (every call) — turn into ignored noise.
- Warnings that are too quiet (only on rare paths) — miss real users.
- Skipping the migration guide ("just read the new docs").

## Coordination

- **Migration Agent** — when deprecation drives an upgrade, coordinate timelines.
- **Cleanup Agent** — performs the eventual removal once the timeline elapses.
- **Doc Updater** — keeps `docs/API_DOCUMENTATION.md` and CHANGELOG in sync.
- **Git/Release Agent** — aligns deprecation removals with semver major bumps.
