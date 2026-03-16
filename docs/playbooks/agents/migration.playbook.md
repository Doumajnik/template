+++
id = "agents/migration"
title = "Migration Agent Rules"
agents = ["migration"]
technologies = ["all"]
category = "rule"
tags = ["migration"]
version = 4
+++

### Migration Agent Rules

- Assess the migration scope first: which files, APIs, and dependencies are affected?
- Create a backward-compatible migration path when possible — avoid big-bang migrations.
- Write adapter/shim layers for gradual migration between old and new APIs.
- Update all import paths and references when moving or renaming modules.
- Run the full test suite after each migration step — never batch migration changes.
- Update documentation for every changed API: `docs/API_DOCUMENTATION.md`, `docs/CODE_INVENTORY.md`.
- Handle deprecated API warnings: replace deprecated calls with their modern equivalents.
- Version bumps in package files must match the actual framework/library version installed.
- Test with the new version before committing — don't assume backward compatibility.
- Create rollback instructions in case the migration needs to be reverted.
- Flag breaking changes that affect downstream consumers — coordinate with affected teams.
- Verify build, lint, and test all pass with the new version before declaring migration complete.
- Use the Strangler Fig pattern for large migrations — introduce a façade/proxy that incrementally routes traffic from legacy to new system without disrupting clients.
- Run old and new systems in parallel and compare outputs before full cutover — validate data consistency and behavioral equivalence.
- Use feature flags to control migration rollout — enable instant rollback to the legacy path if the new implementation shows issues.
- Decouple database migrations from application migrations — schema changes should be backward-compatible and deployed independently.
- Monitor and compare key metrics (latency, error rates, throughput) between old and new systems throughout the migration period.
- Ensure the migration façade/proxy does not become a single point of failure or performance bottleneck — design it for high availability.
- Decommission legacy components only after verifying zero remaining dependencies and zero traffic — maintain a quiet period before final removal.
- Use the Deployment Stamp pattern for large-scale migrations — deploy new versions as isolated stamps (scale units) serving a subset of tenants, enabling incremental migration without affecting existing stamps.
- Implement blue-green deployments for cutover migrations: maintain two identical production environments, deploy the new version to the idle environment, run validation, then switch traffic — keep the old environment ready for instant rollback.
- Use canary releases for high-risk migrations — route a small percentage of traffic (1–5%) to the new version first, monitor error rates and latency, and gradually increase traffic only when metrics confirm stability.
- Lock database migrations with advisory locks or migration state tables to prevent concurrent migration execution in multi-instance deployments — never rely on application-level locking alone.
- Define all migration environments as infrastructure as code (IaC) using Bicep, Terraform, or ARM templates — ensure deployment configurations are predictable, repeatable, and auditable across stamps.
- Perform capacity planning before migration cutover — load-test each deployment stamp to determine its tenant and traffic threshold and deploy additional stamps proactively to absorb demand.
