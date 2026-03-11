+++
id = "agents/git-release"
title = "Git Release Agent Rules"
agents = ["git-release"]
technologies = ["all"]
category = "rule"
tags = ["git-release"]
version = 2
+++

### Git/Release Agent Rules

1. All commits must follow conventional commit format: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `perf:`.
2. Breaking changes must be marked with `!` suffix: `feat!:` or include `BREAKING CHANGE:` in the footer.
3. Generate changelogs from conventional commits — group by type (Added, Fixed, Changed).
4. Version bumps follow semver: MAJOR for breaking changes, MINOR for features, PATCH for fixes.
5. Tag releases with `v` prefix: `v1.2.3`.
6. Release notes must include: changes since last release, breaking changes, migration steps, contributors.
7. Never force-push to `main` or `master` — use revert commits for mistakes.
8. Feature branches: `feat/description`, bugfix branches: `fix/description`, release branches: `release/v1.2.3`.
9. Squash merge feature branches to main — keep main history clean with one commit per feature.
10. Pre-release versions use `-alpha.1`, `-beta.1`, `-rc.1` suffixes.
11. Verify all tests pass before tagging a release — never tag a known-broken commit.
12. Update version numbers in all relevant files: `package.json`, `pyproject.toml`, `*.csproj`.
