+++
id = "agents/dependency"
title = "Dependency Agent Rules"
agents = ["dependency"]
technologies = ["all"]
category = "rule"
tags = ["dependency"]
version = 4
+++

### Dependency Guidelines

- **Audit all dependencies for known CVEs** — use `pip-audit` (Python), `npm audit` (Node), or equivalent tools for the project's language.
- **Check for outdated packages** — list current version vs. latest stable version for each dependency. Flag major version gaps.
- **Flag abandoned packages** — no releases in 12+ months, no response to critical issues, archived repositories. These are risks.
- **Check license compatibility** — all dependencies must have licenses compatible with the project's license. Flag GPL in MIT projects, etc.
- **Verify no duplicate dependencies** — check for packages that provide overlapping functionality. Two HTTP clients or two logging libraries is one too many.
- **Flag transitive dependency risks** — even if the direct dependency is fine, a transitive dependency with known CVEs is still a vulnerability.
- **Check for pinned versions** — all production dependencies should have exact version pins. Ranges (`^`, `~`, `>=`) are acceptable only for development dependencies.
- **Verify dependency separation** — development dependencies must be separate from production dependencies. Test frameworks should not ship to production.
- **Flag dependency bloat** — packages that pull in excessive transitive dependencies (50+ sub-dependencies for a simple utility) should be reconsidered.
- **Produce a structured report** — for each dependency: package name, current version, latest version, license, CVE count, last release date.
- **CRITICAL findings trigger immediate action** — known CVEs with public exploits must be updated immediately, not deferred to the next sprint.
- **Recommend upgrade paths** — which dependencies can be updated with a simple version bump, and which need migration work? Prioritize by risk.
- **Generate and maintain a Software Bill of Materials (SBOM)** — produce an SBOM in CycloneDX or SPDX format for every release. SBOMs enable rapid vulnerability response when new CVEs are disclosed against any component in your dependency tree.
- **Integrate dependency scanning into CI/CD** — run dependency checks (OWASP Dependency-Check, Snyk, pip-audit, npm audit) on every pull request. Don't rely on periodic manual audits; vulnerabilities can be introduced with any commit.
- **Verify dependency integrity with lock files and checksums** — ensure lock files (package-lock.json, poetry.lock, Cargo.lock) are committed to version control and checksums are verified on install to prevent supply chain tampering.
- **Monitor for dependency confusion attacks** — verify that private package names cannot be hijacked via public registries. Use namespaced/scoped packages and configure registry scoping to prevent substitution attacks.
- **Require justification for new dependencies** — new dependencies must be justified (why not use stdlib or existing deps?) and reviewed for security posture, license, maintenance status, and transitive dependency impact before adoption.
- **Track CPE identifiers for automated CVE correlation** — map dependencies to their Common Platform Enumeration (CPE) identifiers to enable automated vulnerability correlation against NVD data feeds, as used by OWASP Dependency-Check.
- **Set maximum age thresholds for dependency releases** — flag dependencies whose latest release is older than a configurable threshold (e.g., 18 months). Aging releases indicate potential abandonment before the repository is officially archived.
- **Guard against typosquatting attacks** — verify package names character-by-character before adding new dependencies. Attackers publish malicious packages with names nearly identical to popular ones (e.g., `lodahs` vs `lodash`). Use scoped registries and organization-verified publishers to reduce typosquatting risk.
- **Require build provenance verification for critical dependencies** — adopt SLSA provenance verification to confirm that a package was built from the expected source repository using the expected build process. Provenance attestations detect supply chain tampering that code review alone cannot catch.
- **Defend against dependency confusion and namespace substitution attacks** — configure package managers to scope private package names to internal registries explicitly. Without registry scoping, attackers can publish a higher-version public package with the same name, causing builds to silently pull the malicious public version.
- **Audit lock file integrity in code review** — treat lock file changes as security-critical diffs. Verify that lock file updates match expected dependency additions and that no unexpected transitive dependencies or registry URL changes were introduced. Lock file poisoning is a stealthy and effective attack vector.
- **Sign and verify packages using Sigstore or equivalent keyless signing** — use keyless signing (Sigstore/cosign) to create verifiable signatures for artifacts you produce, and verify signatures on artifacts you consume. Signature verification proves artifact authenticity and build provenance without managing long-lived cryptographic keys.
- **Pin dependencies to exact versions AND verified checksums** — version pins alone are insufficient because a package registry can serve different content for the same version after publication. Always verify checksums from lock files on every install to detect post-publication package tampering.
