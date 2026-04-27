# Playbooks

Playbooks define behavior rules for agents and shared coding conventions. The Librarian Agent reads the relevant subset of these into every context brief — no agent reads playbooks directly.

## Layout

| Folder | Purpose | Loaded by |
| --- | --- | --- |
| `agents/` | One playbook per agent (`{agent-name}.playbook.md`). File name MUST match `.github/agents/{agent-name}.agent.md`. | Librarian, when serving context to that agent. |
| `shared/` | Cross-cutting rules every agent may need (anti-duplication, code style, naming conventions, markdown formatting, error handling, etc.). | Librarian, when the topic is relevant to the task. |
| `_archive/` | Superseded playbooks kept for historical reference only. **Not parsed by any agent.** Gitignored in this repo. | Nothing. |

Technology-specific conventions (Python, TypeScript, Go, .NET, Rust, Java, Kotlin, Django, FastAPI, Next.js, React) live under `.github/instructions/{lang}.instructions.md` — NOT here. They were migrated out of `playbooks/technologies/` to use Copilot's native `applyTo` mechanism.

## Naming convention (strict)

- **Agent playbooks:** `{agent-name}.playbook.md` — base name must match the corresponding `.github/agents/{agent-name}.agent.md`. The Consistency Check Agent flags any mismatch.
- **Shared playbooks:** descriptive kebab-case (`anti-duplication.playbook.md`, `markdown-formatting.playbook.md`).
- **Templates:** `_TEMPLATE.playbook.md` (single template for new playbooks).

## When to add a playbook

| Situation | Add to |
| --- | --- |
| New agent introduced | `agents/{new-agent}.playbook.md` |
| Cross-agent rule that applies broadly | `shared/{rule-name}.playbook.md` |
| Language/framework convention | `.github/instructions/{lang}.instructions.md` |

## When to archive

Move a playbook to `_archive/` when its rules are superseded by a new one, or when its agent is decommissioned. Never edit archived files; create the replacement in `agents/` or `shared/` instead. The Cleanup Agent periodically prunes `_archive/` per the project's retention policy.

## Validation

`scripts/validate-playbooks.py` checks:

- Every agent in `.github/agents/` has a matching `playbooks/agents/` file (and vice versa).
- All playbook front-matter fields are present.
- No broken references to other playbooks or docs.

Run before committing playbook changes.
