+++
id = "agents/git-release"
title = "Git Release Agent Rules"
agents = ["git-release"]
technologies = ["all"]
category = "rule"
tags = ["git-release"]
version = 4
+++

### Git/Release Agent Rules

- All commits must follow conventional commit format: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`.
- Breaking changes must be marked with `!` suffix: `feat!:` or include `BREAKING CHANGE:` in the footer.
- Generate changelogs from conventional commits — group by type (Added, Fixed, Changed).
- Version bumps follow semver: MAJOR for breaking changes, MINOR for features, PATCH for fixes.
- Tag releases with `v` prefix: `v1.2.3`.
- Release notes must include: changes since last release, breaking changes, migration steps, contributors.
- Never force-push to `main` or `master` — use revert commits for mistakes.
- Feature branches: `feat/description`, bugfix branches: `fix/description`, release branches: `release/v1.2.3`.
- Squash merge feature branches to main — keep main history clean with one commit per feature.
- Pre-release versions use `-alpha.1`, `-beta.1`, `-rc.1` suffixes.
- Verify all tests pass before tagging a release — never tag a known-broken commit.
- Update version numbers in all relevant files: `package.json`, `pyproject.toml`, `*.csproj`.
- Major version zero (`0.y.z`) is for initial development — the public API should not be considered stable and may change at any time.
- Once a version is released, its contents must never be modified — any correction, no matter how small, requires a new version number.
- Deprecate functionality in a minor release before removing it in the next major — give consumers at least one minor release to transition.
- Include build metadata using the `+` suffix (e.g., `1.0.0+build.42`) for CI traceability — build metadata must not affect version precedence.
- Automate version bumps from commit history — never manually decide version numbers when conventional commits are in use; let tooling (`standard-version`, `semantic-release`) derive them.
- Sign release tags with GPG or SSH keys to ensure release authenticity and tamper detection.
- Document the public API boundary explicitly — version numbers only have meaning relative to a declared public API; without one, semver is meaningless.
- Commit scopes must be a noun describing a codebase section in parentheses — e.g., `feat(parser):`, `fix(auth):` — use consistent scope names across the project and document allowed scopes in the contributing guide.
- Commit footers must follow git trailer format: `Token: value` or `Token #value` — use hyphens for multi-word tokens (e.g., `Reviewed-by:`, `Refs:`); `BREAKING CHANGE` is the only token that allows a space.
- Multi-paragraph commit bodies must begin one blank line after the description — each paragraph is free-form and newline-separated; use the body for motivation, context, and contrast with previous behavior.
- Enforce conventional commit format with automated tooling (commitlint, commitizen, or git hooks) — reject non-conforming commits at the pre-commit or CI level to maintain parseable commit history.
- Revert commits should use the `revert` type and include a `Refs:` footer with the SHA(s) of the reverted commit(s) — e.g., `revert: undo feature X\n\nRefs: 676104e`.
- Conventional commit types must not be treated as case-sensitive by tooling — `BREAKING CHANGE` (uppercase) and `BREAKING-CHANGE` (hyphenated) are the only tokens with specific casing/format requirements.
- When a commit conforms to more than one type, split it into multiple atomic commits — each commit should have a single purpose to enable accurate changelog generation and version bump calculation.
