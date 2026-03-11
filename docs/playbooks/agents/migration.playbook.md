+++
id = "agents/migration"
title = "Migration Agent Rules"
agents = ["migration"]
technologies = ["all"]
category = "rule"
tags = ["migration"]
version = 2
+++

### Migration Agent Rules

1. Assess the migration scope first: which files, APIs, and dependencies are affected?
2. Create a backward-compatible migration path when possible — avoid big-bang migrations.
3. Write adapter/shim layers for gradual migration between old and new APIs.
4. Update all import paths and references when moving or renaming modules.
5. Run the full test suite after each migration step — never batch migration changes.
6. Update documentation for every changed API: `docs/API_DOCUMENTATION.md`, `docs/CODE_INVENTORY.md`.
7. Handle deprecated API warnings: replace deprecated calls with their modern equivalents.
8. Version bumps in package files must match the actual framework/library version installed.
9. Test with the new version before committing — don't assume backward compatibility.
10. Create rollback instructions in case the migration needs to be reverted.
11. Flag breaking changes that affect downstream consumers — coordinate with affected teams.
12. Verify build, lint, and test all pass with the new version before declaring migration complete.
