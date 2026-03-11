+++
id = "agents/dependency"
title = "Dependency Agent Rules"
agents = ["dependency"]
technologies = ["all"]
category = "rule"
tags = ["dependency"]
version = 2
+++

### Dependency Guidelines

1. **Audit all dependencies for known CVEs** — use `pip-audit` (Python), `npm audit` (Node), or equivalent tools for the project's language.
2. **Check for outdated packages** — list current version vs. latest stable version for each dependency. Flag major version gaps.
3. **Flag abandoned packages** — no releases in 12+ months, no response to critical issues, archived repositories. These are risks.
4. **Check license compatibility** — all dependencies must have licenses compatible with the project's license. Flag GPL in MIT projects, etc.
5. **Verify no duplicate dependencies** — check for packages that provide overlapping functionality. Two HTTP clients or two logging libraries is one too many.
6. **Flag transitive dependency risks** — even if the direct dependency is fine, a transitive dependency with known CVEs is still a vulnerability.
7. **Check for pinned versions** — all production dependencies should have exact version pins. Ranges (`^`, `~`, `>=`) are acceptable only for development dependencies.
8. **Verify dependency separation** — development dependencies must be separate from production dependencies. Test frameworks should not ship to production.
9. **Flag dependency bloat** — packages that pull in excessive transitive dependencies (50+ sub-dependencies for a simple utility) should be reconsidered.
10. **Produce a structured report** — for each dependency: package name, current version, latest version, license, CVE count, last release date.
11. **CRITICAL findings trigger immediate action** — known CVEs with public exploits must be updated immediately, not deferred to the next sprint.
12. **Recommend upgrade paths** — which dependencies can be updated with a simple version bump, and which need migration work? Prioritize by risk.
