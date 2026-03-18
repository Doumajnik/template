+++
id = "shared/version-freshness"
title = "Version Freshness Rules"
agents = ["all"]
technologies = ["all"]
category = "rule"
tags = ["dependencies", "versions"]
version = 1
+++

### Version Freshness

- **The Research Agent is the sole owner of version verification.** All dependency versions in the project must come from a Research Agent brief where the version was fetched from the package registry.
- **Never guess or use training data for version numbers.** Training data is always stale. If you need a version and no Research Agent brief exists, ask the Orchestrator to spawn the Research Agent first.
- **Workers install what the Research Agent verified.** When a Worker installs a dependency, it uses the exact version from the research brief. No ad-hoc version picking.
- **If a dependency is added without a Research Agent brief**, the Retrospective Agent flags it as a process violation.
- **Pin to exact versions.** Use `4.2.1`, not `^4.2.1`, `~4.2`, or `latest`. Exact pins prevent silent upgrades.
