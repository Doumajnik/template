# Research Brief: Self-Maintaining AI Agent Systems & Knowledge Base Maintenance

**Date:** 2026-05-04
**Requested by:** Orchestrator (ad-hoc research)

---

## Summary

Four systems were researched for patterns applicable to autonomous maintenance of AI agent instruction files (playbooks, checklists, skills). Renovate Bot offers the most directly transferable patterns — event-driven file scanning, scheduled auto-update, configurable auto-merge, and centralized config inheritance. Trunk.io demonstrates how to maintain a versioned, config-as-code tool registry with partial-override inheritance. Logseq and Obsidian show how graph-linked knowledge with bidirectional references and template enforcement stays coherent at scale. Anthropic's Constitutional AI paper provides the theoretical foundation for agents that self-critique and revise their own outputs against a fixed rule document — directly mapping to playbook files.

---

## 1. Renovate Bot Patterns

**Source:** https://github.com/renovatebot/renovate · https://docs.renovatebot.com/configuration-options/

### 1.1 How automated dependency updating works

Renovate scans repositories for dependency references using **managers** (built-in per ecosystem) and **customManagers** (user-defined regex or JSONata patterns). It then queries registries for newer versions and proposes PRs. The same mechanism can be applied to anything expressed as a version string in any file — including agent model versions in `AGENTS.md`.

Key mechanism:
```json
{
  "customManagers": [{
    "customType": "regex",
    "managerFilePatterns": ["AGENTS.md", ".github/agents/**/*.agent.md"],
    "matchStrings": [
      "model:\\s+(?<currentValue>[\\w\\s.]+)\\s*# (?<datasource>[^/]+)/(?<depName>[^\\n]+)"
    ]
  }]
}
```

This pattern is how Renovate tracks arbitrary version strings. An AI agent maintenance system could use the **same scanning approach** to detect when an agent's `model:` field, a skill's tool version, or a checklist's step count falls out of sync with a source-of-truth registry.

### 1.2 Scheduling patterns (periodic vs event-driven)

Renovate supports two modes, both applicable to agent maintenance:

| Mode | Renovate Config | Agent Maintenance Translation |
|---|---|---|
| **Periodic** | `"schedule": ["before 4am on monday"]` | Weekly playbook audit run (off-hours, low noise) |
| **Event-driven** | Triggered by upstream version changes | Triggered by a merge to `main` that touches `AGENTS.md` |
| **Maintenance window** | `"lockFileMaintenance": { "enabled": true }` | Periodic "refresh all agent instructions from template" job |
| **Release age gate** | `"minimumReleaseAge": "3 days"` | Delay applying AI model upgrades until 3 days of community vetting |

The `lockFileMaintenance` concept maps directly to a **periodic agent instruction refresh** — deleting stale content and regenerating from canonical templates, similar to lock file recreation.

### 1.3 Auto-merge capabilities

Renovate's automerge model is a graduated trust system:

```json
{
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "branch"  // no PR, silent merge
    },
    {
      "matchUpdateTypes": ["minor"],
      "automerge": true,
      "automergeType": "pr"      // create PR, merge after CI green
    },
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true  // human gate required
    }
  ]
}
```

**Agent maintenance translation:**

| Change severity | Auto-merge strategy |
|---|---|
| Typo fix, formatting, dead link removal | `automergeType: "branch"` — silent, no PR |
| New checklist item, playbook clarification | `automergeType: "pr"` — PR + CI green |
| New agent added, pipeline step reordering | `dependencyDashboardApproval: true` — human review |
| Core Rule changes, role separation changes | Block, require explicit approval |

### 1.4 Configuration centralization

Renovate uses a `extends` + `globalExtends` hierarchy for shareable presets:

```json
// org-level preset in github.com/org/renovate-config
{
  "extends": ["config:recommended"],
  "schedule": ["before 4am on weekdays"],
  "automerge": true
}

// per-repo inherits it
{
  "extends": ["local>org/renovate-config"]
}
```

For agent systems, this maps to:

- **Central source of truth** → `AGENTS.md` at repo root
- **Per-tool pointer files** → `.github/copilot-instructions.md`, `CLAUDE.md` point to `AGENTS.md`
- **Inheritance chain** → `globalExtends` (bot admin) → `extends` (org preset) → repo config
- **`inheritConfig`** setting: Renovate can pull an org-wide `renovate-config` from a central repo per org group — equivalent to an AI agent inheriting base rules from a central governance repo

**Key pattern**: The `migratePresets` option renames/removes deprecated presets across all repos without touching each individually. An equivalent `migrateAgentRules` mechanism could replace deprecated playbook references org-wide.

---

## 2. Trunk.io Patterns

**Source:** https://docs.trunk.io/ · https://docs.trunk.io/check/configuration

### 2.1 Centralized config across repos

Trunk uses `.trunk/trunk.yaml` as a single file governing all tool behavior. It is **configuration-as-code** with a versioned schema. Key properties:

- **Pinned versions** for every tool: `- ansible-lint@5.3.2` — no floating versions
- **Merged with defaults**: `trunk print-config` shows the final merged config (repo overrides + shipped defaults). Equivalent to how `AGENTS.md` + agent `.agent.md` files compose behavior.
- **Partial overrides**: Only specify what differs; Trunk merges with defaults. This avoids copy-paste drift.

```yaml
# Only override what you need — Trunk merges the rest from its default definitions
lint:
  definitions:
    - name: clang-tidy
      disable_upstream: false  # flip one boolean, keep everything else
```

**Agent maintenance translation**: Agent `.agent.md` files should be **partial overrides** of base agent behavior defined in a shared defaults section, not full copy-paste specifications. When the base changes, files that only override deltas stay correct automatically.

### 2.2 Plugin/tool management

Trunk's plugin system (`plugins:` in `trunk.yaml`) sources tool definitions from external repos (e.g., `github.com/trunk-io/plugins`). Tool definitions include download URLs, version commands, and command templates.

**Key insight for agent maintenance**: Tool versions in Trunk are:
1. Pinned explicitly in `trunk.yaml`
2. Updated by Trunk's own upgrade notifier (a Renovate-like periodic check)
3. Validated against a schema on load

The same three-layer approach works for agent skills:
1. **Pin skill versions** in a skill registry file (analogous to `trunk.yaml`)
2. **Periodic scanner** checks if a skill's referenced tool (e.g., a Python library) has a newer version
3. **Schema validation** on load ensures skill files conform to `SKILL.md` structure

### 2.3 Upgrade patterns

Trunk notifies about upgrades via:
```yaml
actions:
  disabled:
    - trunk-upgrade-available  # suppress notifications if desired
```

Trunk's upgrade flow:
1. Detects newer Trunk CLI version
2. Proposes a PR bumping the `cli.version` field in `trunk.yaml`
3. CI validates the upgraded version before merge

**Agent maintenance translation**: An autonomous upgrade agent could:
1. Detect that a model version in `AGENTS.md` is no longer the recommended version
2. Open a PR updating the `model:` frontmatter in affected `.agent.md` files
3. Run `validate-playbooks.py` (already in this repo at `scripts/validate-playbooks.py`) as a CI gate
4. Merge automatically if validation passes

---

## 3. Knowledge Management Patterns (Logseq + Obsidian)

**Sources:** https://github.com/logseq/logseq · https://github.com/obsidianmd/obsidian-releases

### 3.1 Graph-based knowledge linking

Logseq uses a **Datalog/DataScript** graph database where every block has properties and can be queried. Key pattern:

- Every page is a node; links between pages are edges
- Queries (`{{query ...}}`) can pull related blocks dynamically: e.g., "show all blocks tagged `#playbook-rule` that reference `#security-agent`"
- The graph auto-updates as content changes — no manual index refresh

**For agent knowledge bases**: If every playbook rule were tagged with which agents it applies to (e.g., `applyTo: [Worker, Reviewer, Security]` in frontmatter), a graph query could produce a per-agent instruction bundle automatically, rather than copy-pasting rules into each `.agent.md` file.

### 3.2 Backlinks and bidirectional references

Obsidian and Logseq both maintain **bidirectional links**: if `AGENTS.md` references `.github/agents/worker.agent.md`, then `worker.agent.md` automatically shows a backlink to `AGENTS.md`.

**For agent maintenance**: Bidirectional indexing immediately surfaces the impact of changes:
- Changing a Core Rule in `AGENTS.md` → backlinks show exactly which `.agent.md` files inherit it
- Deleting a playbook → backlinks reveal which checklists or skills reference it (orphan detection)
- This is the **Reference & Path Integrity** shard of the Consistency Check Agent

Obsidian Bot (the GitHub bot maintaining `obsidian-releases`) runs **daily automated updates** to `community-plugin-stats.json`, committing fresh download counts for every community plugin. The bot is triggered on a schedule and creates direct commits (no PR). This is the exact pattern for a **Stats/Freshness Agent** that periodically updates `docs/CODE_INVENTORY.md` with current file counts, test counts, and coverage metrics.

### 3.3 Template systems for consistent note structure

Obsidian's community plugin submission requires every plugin entry in `community-plugins.json` to have exactly these fields:
```json
{
  "id": "...",
  "name": "...",
  "author": "...",
  "description": "...",
  "repo": "user/repo"
}
```

PRs that omit fields are rejected. This is **schema enforcement at ingest time** — the same approach the `validate-playbooks.py` script uses for playbook files.

**Template-enforced agent files**: Each `.agent.md` should have a mandatory schema (frontmatter fields: `name`, `model`, `responsibility`, `tool-restrictions`). A CI check validates on every PR, and an auto-fixer agent can populate missing fields from defaults when detected.

---

## 4. Self-Improving AI Patterns

**Sources:** Constitutional AI paper (arXiv:2212.08073) · Self-reflection + meta-learning literature

### 4.1 Constitutional AI — Self-correction against a rule document

Anthropic's Constitutional AI (CAI) paper describes a process where a model:

1. **Generates** an initial response
2. **Critiques** its own response against a written constitution (list of principles)
3. **Revises** the response based on that critique
4. **Repeats** until the response satisfies the constitution

The supervised phase produces a dataset of (initial_response, critique, revision) tuples used to finetune the model. The RL phase trains a preference model using AI-generated comparisons, then uses RLAIF.

**Direct mapping to agent playbook maintenance**:

| CAI component | Agent maintenance equivalent |
|---|---|
| Constitution (principles list) | `docs/PLAYBOOK.md` + Core Rules in `AGENTS.md` |
| Initial response | A draft update to a playbook or skill file |
| Self-critique | Retrospective Agent reviews the draft against the Playbook |
| Revision | Updated draft incorporating critique findings |
| Preference model | Consistency Check Agent scoring drift findings |
| RLAIF | Future: using past session retrospectives to tune agent prompts |

**Key insight**: The "constitution" is already present in this template — it's `AGENTS.md` + `docs/PLAYBOOK.md`. An autonomous maintenance agent should:
1. Draft changes to instruction files
2. Run a self-critique pass against `AGENTS.md` Core Rules
3. Revise before committing
4. Log the critique chain in `docs/RETROSPECTIVE_REPORT.md`

### 4.2 Reflection agents that improve their own prompts

The **Reflexion** pattern (Shinn et al., 2023) extends CAI to code agents:
- Agent executes, observes failure
- Stores the failure mode in a scratchpad ("verbal reinforcement")
- On the next attempt, prepends the scratchpad to the prompt

In agent maintenance terms:
- Agent tries to update a playbook → Consistency Check finds residual drift
- Failure is logged to `.ai/lessons.md` with the trigger, pattern, and corrective rule
- On the next maintenance run, the agent reads `.ai/lessons.md` first and avoids the same mistake

This is the **Self-Improvement Loop** already in `AGENTS.md` — the key pattern to automate is reading lessons before every maintenance task.

### 4.3 Meta-learning: using past performance to tune future behavior

Key patterns from the literature:

**Performance metrics for instruction files** (what to measure):
- Consistency Check pass rate after first agent run (fewer fixes = better instructions)
- Number of Retrospective findings flagged as "rule violation" vs. "new pattern"
- Number of times a specific agent needed correction across sessions
- Test pass rate on first Worker attempt (low = unclear instructions)

**Feedback loop structure**:
```
Session → Retrospective Agent → lessons.md → next session (pre-read)
                              → PLAYBOOK.md (rules extracted)
                              → RETROSPECTIVE_REPORT.md (trend analysis)
```

**Decay and staleness detection**: A periodic "freshness agent" could flag any instruction that hasn't been referenced in Retrospective findings for N sessions as potentially stale — analogous to Renovate's `abandonmentThreshold` that flags packages not updated for a period.

### 4.4 Periodic audit/refresh cycles for documentation

The most actionable patterns from all four systems for a periodic audit cycle:

| Phase | Duration | Action | Source pattern |
|---|---|---|---|
| **Scan** | Nightly | Detect mismatches between `AGENTS.md` roster and `.agent.md` files | Renovate customManager scan |
| **Score** | Weekly | Run Consistency Check, produce drift report | Trunk: `trunk check` |
| **Refresh** | Weekly | Regenerate per-agent context briefs from updated docs | Logseq query-based bundle |
| **Self-critique** | Per-session | Retrospective Agent reads transcript, critiques against Playbook | Constitutional AI supervised phase |
| **Promote lessons** | Monthly | Escalate recurring `.ai/lessons.md` entries to Core Rules | CAI RL phase → finetuning |
| **Prune** | Quarterly | Cleanup Agent deduplicates playbooks, removes orphan entries | Obsidian dead-link detection |

---

## Key Findings

1. **Renovate's `customManager` + `schedule` + `automerge` is the most complete automation model.** It separates *detection* (scanning), *proposal* (PR creation), and *approval* (graduated auto-merge by risk level). Apply this trio to instruction file maintenance.

2. **Trunk's partial-override inheritance prevents copy-paste drift.** Agent `.agent.md` files should only declare deltas from a base agent spec, not full copies. Changes to the base propagate automatically.

3. **Bidirectional linking (Logseq/Obsidian) is the correct data model for impact analysis.** Every agent file should be indexable by tag, so "what files are affected by changing this Core Rule?" is answerable without grep.

4. **Constitutional AI's critique-then-revise loop is directly implementable today** using the Retrospective Agent reading draft changes against `AGENTS.md` before committing. No finetuning required — just a structured prompt.

5. **Meta-learning already exists in this repo** via `.ai/lessons.md` and `docs/RETROSPECTIVE_REPORT.md`. The missing piece is *automated reading* of lessons before each maintenance task and *automated promotion* of recurring lessons to Core Rules.

---

## Pitfalls & Warnings

- **Auto-merge of Core Rules without human review is dangerous.** Use the Renovate `major = human gate` pattern: Core Rule changes require explicit user approval.
- **Scheduled runs without observability are black boxes.** Every autonomous maintenance run needs a structured log entry (dispatch log pattern from `AGENTS.md`).
- **Graph-based linking requires discipline at authoring time.** Tags and frontmatter must be consistent for queries to work. Enforce via CI schema validation.
- **Constitutional AI self-critique can produce sycophantic revisions** — the model agrees with its own constitution too readily. Add an adversarial pass ("What would a red team agent say about this change?").
- **Renovate runs Renovate on itself** (the repo has a `renovate.json`). This is the gold standard: any self-maintenance system should maintain its own configuration the same way it maintains everything else.

---

## Alternative Approaches

- **Manual periodic review (no automation):** Simple but doesn't scale past ~20 agent files. Human reviewer fatigue causes drift.
- **Git hooks only (pre-commit validation):** Catches obvious schema errors but doesn't detect semantic drift between files, stale content, or missing cross-references.
- **Full RLAIF pipeline (fine-tuning):** Maximum capability but requires training infrastructure, labeled datasets, and weeks of iteration. Overkill for instruction file maintenance.

---

## Recommended Approach for This Template

1. **Near-term (no new infrastructure):** Add a `Freshness Agent` role (ad-hoc) that runs the Consistency Check Agent on a weekly schedule and auto-creates a GitHub Issue with drift findings. Use the Renovate `schedule` + `dependencyDashboard` Issue pattern.

2. **Medium-term:** Implement a `customManager`-style scanner in `scripts/` that reads all `.agent.md` files, extracts `model:` frontmatter, and opens a PR to bump stale model versions when the `AGENTS.md` roster table changes.

3. **Long-term:** Add a Logseq-style bidirectional index to the Librarian Agent — every knowledge document tags which agents use it, so changes automatically identify affected files without full-repo grep.

---

## References

- Renovate Bot docs: https://docs.renovatebot.com/configuration-options/
- Renovate self-hosted config: https://docs.renovatebot.com/self-hosted-configuration/
- Trunk CLI config docs: https://docs.trunk.io/check/configuration
- Trunk overview: https://docs.trunk.io/
- Logseq GitHub: https://github.com/logseq/logseq
- Obsidian releases & plugin registry: https://github.com/obsidianmd/obsidian-releases
- Constitutional AI paper: https://arxiv.org/abs/2212.08073 (Bai et al., 2022)
- Reflexion paper: https://arxiv.org/abs/2303.11366 (Shinn et al., 2023)
