+++
id = "agents/doc-updater"
title = "Doc Updater Agent Rules"
agents = ["doc-updater"]
technologies = ["all"]
category = "rule"
tags = ["doc-updater"]
version = 4
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
- Classify documentation into four Diátaxis categories: tutorials (learning-oriented), how-to guides (task-oriented), reference (information-oriented), explanation (understanding-oriented) — never mix categories in a single document (source: Diátaxis framework)
- Commit messages must include a scope when the change affects a specific module, e.g., `feat(auth): add token refresh` — bare types without scope are only for cross-cutting changes (source: Conventional Commits 1.0.0)
- Each commit must contain exactly one logical change — never combine a feature, a fix, and a refactor in a single commit (source: Conventional Commits FAQ)
- When deleting code or deprecating features, update or remove associated documentation in the same commit — stale documentation is worse than missing documentation
- Reference documentation must stay synchronized with code — when a function signature, API endpoint, or configuration option changes, the corresponding docs must be updated in the same session
- Session summaries must include a "Decisions Made" section listing each decision with its rationale, so future sessions can trace why choices were made
- Tutorials must be learning-oriented and guide the reader through concrete steps toward an achievable goal — minimize explanation, focus on doing, show expected output at each step, and aspire to perfect reliability so every user succeeds (source: Diátaxis framework, "Tutorials")
- How-to guides must be goal-oriented and address real-world problems — assume the reader already knows what they want to achieve, provide actionable steps focused on the task, and omit teaching or background discussion (source: Diátaxis framework, "How-to guides")
- Reference documentation must be information-oriented — describe the machinery (APIs, classes, functions, configuration) austerely and completely, structured to mirror the code itself, with no instruction or opinion mixed in (source: Diátaxis framework, "Reference")
- Explanation documentation must be understanding-oriented — provide context, background, design rationale, and alternative perspectives; explanation is the only documentation type meant to be read away from the product (source: Diátaxis framework, "Explanation")
- Never mix Diátaxis quadrants in a single document — link from tutorials to reference instead of embedding API details inline; link from how-to guides to explanation instead of digressing into background (source: Diátaxis framework, "Applying Diátaxis")
- How-to guide titles must state the goal explicitly using the format "How to {verb} {object}" — vague titles like "Authentication" or "Database Setup" fail to communicate what the reader will accomplish (source: Diátaxis framework, "Pay attention to naming")
