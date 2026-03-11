+++
id = "agents/doc-updater"
title = "Doc Updater Agent Rules"
agents = ["doc-updater"]
technologies = ["all"]
category = "rule"
tags = ["doc-updater"]
version = 2
+++

### Doc Updater Guidelines

- Update `docs/CODE_INVENTORY.md` with any new symbols (functions, classes, constants) added during the session
- Update `docs/files/` with per-file documentation for any new or significantly changed source files
- Write a session summary to `.ai/sessions/` with: what was done, decisions made, issues encountered
- Update `docs/BUSINESS_LOGIC.md` if business logic or data flows changed
- Update `README.md` if new top-level directories, commands, or setup steps were added
- Use conventional commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Never commit generated files (build output, `.pyc`, `node_modules`) — verify `.gitignore` coverage
- Verify all edited documentation follows the `docs/playbooks/shared/markdown-formatting.playbook.md` rules
- Update `docs/API_DOCUMENTATION.md` if any API endpoints changed
- Cross-reference related docs — if a new service is added, link it in BUSINESS_LOGIC, CODE_INVENTORY, and the service's file doc
- Mark all doc-update tasks as ✅ complete in the todo file
