# Plan: Integrating This Template into an Existing Project

## Overview

This document provides a detailed plan for integrating the `Doumajnik/template` repository into an already-existing project. The goal is to retrofit the conventions, tooling, folder structure, and workflows defined in this template without disrupting what is already working in the target project. Three concrete strategies are outlined below, ranging from the least invasive (cherry-picking individual pieces) to the most thorough (full structural migration).

---

## Strategy 1: Selective File Cherry-Pick

**Goal:** Adopt only the specific template assets your project needs, without restructuring anything.

### When to Use
- The existing project already has a well-established structure that you do not want to disturb.
- You only need one or two pieces of the template (e.g., CI/CD pipeline, `.env` conventions, or the feedback folder).

### Steps

1. **Audit the template.** Review every folder and file in this repository:
   - `.github/` — workflow YAML files, agent instructions, prompt templates.
   - `scripts/` — build and automation helpers.
   - `docs/` — playbook, code inventory, business logic docs.
   - `ideas/` and `feedback/` — structured brainstorming and feedback tracking.
   - `.env.example` — environment variable conventions.
   - `AGENTS.md` and `README.md` — project-level documentation standards.

2. **Identify what you need.** Create a checklist of which files add value to the existing project. For example:
   - [ ] `.github/workflows/*.yml` → replace or merge with existing CI/CD.
   - [ ] `.env.example` → merge with existing environment variable list.
   - [ ] `docs/PLAYBOOK.md` → adopt coding conventions.
   - [ ] `scripts/` → evaluate each script for relevance.

3. **Copy files one at a time.**
   - For each selected file, manually copy it into the existing project at the same relative path.
   - If a file already exists (e.g., `.github/workflows/ci.yml`), perform a careful diff and merge the two files line by line. Preserve existing logic and layer in the template's additions.

4. **Verify after each file.** After copying each file:
   - Run the existing test suite to confirm nothing broke.
   - Run any linter or formatter the existing project uses.
   - Commit the change with a message like `chore: adopt template <filename>`.

5. **Update references.** If copied scripts or workflow files reference paths or names specific to the template repo (e.g., `template` as the project name), find and replace them with the existing project's name.

6. **Document what was adopted.** Add a short section to the existing project's README or CHANGELOG listing which template files were brought in and why, so future contributors know the origin.

### Risks & Mitigations
- **Conflict with existing CI:** Always diff before overwriting. Keep a backup branch.
- **Stale template files:** Pin the template version you cherry-picked from (the commit SHA) so you know when to re-sync.

---

## Strategy 2: Parallel Branch Merge

**Goal:** Bring in the full template structure by merging it as a separate branch, resolving conflicts deliberately.

### When to Use
- You want a more comprehensive adoption of the template conventions.
- The existing project is in a state where a larger structural change is acceptable (e.g., early in development, between major releases, or during a planned refactor sprint).

### Steps

1. **Create a dedicated integration branch** in the existing project:
   ```bash
   git checkout -b integrate/template-conventions
   ```

2. **Add this template as a remote** in the existing project:
   ```bash
   git remote add template https://github.com/Doumajnik/template.git
   git fetch template
   ```

3. **Merge the template's main branch** using the `--allow-unrelated-histories` flag (since the two repos have separate git histories):
   ```bash
   git merge template/main --allow-unrelated-histories --no-commit --no-ff
   ```
   The `--no-commit` flag stages all changes but does not auto-commit, giving you full control over conflict resolution before anything is finalized.

4. **Resolve conflicts systematically.** Go through each conflict:
   - **Template wins:** For new files that only exist in the template (e.g., `ideas/`, `feedback/`, `.github/agents/`), accept them as-is.
   - **Existing project wins:** For project-specific files like `src/`, `package.json`, or `README.md`, keep the existing project's version as the base and selectively paste in relevant template additions.
   - **True merges:** For files like `.gitignore`, `.env.example`, and CI YAML, merge both sets of entries carefully to produce a unified version.

5. **Run the full test suite** after resolving all conflicts:
   ```bash
   # Example for a Node.js project
   npm install && npm test
   ```
   Fix any failures before committing.

6. **Commit the merge:**
   ```bash
   git add .
   git commit -m "feat: integrate Doumajnik/template conventions and tooling"
   ```

7. **Open a pull request** from `integrate/template-conventions` into the existing project's main branch. Include in the PR description:
   - A list of every file that was added, modified, or removed.
   - The rationale for each significant decision made during conflict resolution.
   - Links to relevant template docs (e.g., `docs/PLAYBOOK.md`) so reviewers understand the conventions being introduced.

8. **Remove the remote** after the merge is complete to keep the existing project's remote list clean:
   ```bash
   git remote remove template
   ```

### Risks & Mitigations
- **Large conflict surface:** If the existing project is large, the merge will produce many conflicts. Mitigate by doing the merge in sub-batches: merge only `.github/` first, then `docs/`, then scripts.
- **History pollution:** The merge will import the template's full commit history. If this is undesirable, use `git merge --squash` to collapse the template history into a single commit.

---

## Strategy 3: Incremental Folder-by-Folder Adoption Over Multiple Sprints

**Goal:** Gradually adopt the template's conventions over time, integrating one folder or concern per sprint, allowing the team to learn and adapt at a sustainable pace.

### When to Use
- The existing project is large and mature, with many contributors.
- A big-bang merge would be too disruptive or risky.
- The team needs time to understand each template convention before it is enforced.

### Phase Plan

#### Phase 1 — Environment & Secrets (Sprint 1)
1. Copy `.env.example` into the existing project.
2. Compare against the existing project's own `.env.example` (or equivalent). Merge entries, adding any missing variables defined by the template.
3. Update `.gitignore` to match the template's entries (add any missing patterns).
4. Communicate the updated environment variable list to all contributors.
5. **Acceptance criteria:** Every developer can run the project locally using only variables documented in `.env.example`.

#### Phase 2 — Documentation & Conventions (Sprint 2)
1. Copy `docs/PLAYBOOK.md` and adapt it to the existing project's stack (replace language-specific rules as needed).
2. Copy `docs/CODE_INVENTORY.md` and populate it with the existing project's top-level modules.
3. Introduce `ideas/` and `feedback/` folders with their README files so the team has a structured place for async input.
4. Update the main `README.md` to match the template's structure (sections: Overview, Setup, Usage, Contributing).
5. **Acceptance criteria:** A new contributor can onboard using only the README and PLAYBOOK with no verbal guidance.

#### Phase 3 — CI/CD & Automation (Sprint 3)
1. Review `.github/workflows/` in the template. For each workflow:
   - Determine whether the existing project already has an equivalent.
   - If not, copy and adapt the workflow (update language versions, dependency commands, etc.).
   - If yes, diff the two and merge improvements (e.g., caching steps, matrix builds, security scanning).
2. Copy relevant `scripts/` utilities. Update any hardcoded project names or paths.
3. Run a full CI pipeline on a test branch to verify all workflows pass before merging to main.
4. **Acceptance criteria:** All existing CI checks continue to pass, and any new checks added from the template also pass.

#### Phase 4 — Agent & AI Tooling (Sprint 4, Optional)
1. Copy `.github/agents/` and `.github/prompts/` into the existing project.
2. Review `AGENTS.md` and adapt the sub-agent roster to reflect the existing project's tech stack.
3. Copy `.ai/PREFERENCES.md` and customize it for the team's preferences.
4. Brief the team on how to use the agent pipeline for new features.
5. **Acceptance criteria:** At least one new feature is planned and scaffolded using the agent pipeline defined in `AGENTS.md`.

### Tracking Progress
Create a tracking issue in the existing project with the following checklist:
```
- [ ] Phase 1: Environment & Secrets
- [ ] Phase 2: Documentation & Conventions
- [ ] Phase 3: CI/CD & Automation
- [ ] Phase 4: Agent & AI Tooling (Optional)
```
Link each phase to its corresponding PR so the history is traceable.

### Risks & Mitigations
- **Team resistance to new conventions:** Introduce each phase with a short team demo or written summary of what changed and why. The `docs/PLAYBOOK.md` should serve as the canonical reference.
- **Drift over time:** After completing all phases, add a quarterly calendar reminder to diff the existing project against the latest template commit and pull in any improvements.
- **Inconsistent adoption across branches:** Enforce template conventions via automated checks (linters, required CI status checks) rather than relying solely on code review.

---

## Choosing the Right Strategy

| Situation | Recommended Strategy |
|---|---|
| Project is mature; only a few template assets are needed | Strategy 1 — Selective File Cherry-Pick |
| Project is in early/mid stage; team wants full adoption quickly | Strategy 2 — Parallel Branch Merge |
| Large team; risk-averse; prefer incremental change | Strategy 3 — Incremental Folder-by-Folder Adoption |

---

## Next Steps

1. Share this document with the team and agree on which strategy fits the project.
2. Create a tracking issue or ticket for the chosen strategy.
3. Assign an owner per phase (or per cherry-pick batch).
4. Schedule a retrospective after the first phase to evaluate whether the integration is delivering value and adjust the approach if needed.
