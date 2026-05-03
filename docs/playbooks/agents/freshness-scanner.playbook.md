+++
id = "agents/freshness-scanner"
title = "Freshness Scanner Agent Rules"
agents = ["freshness-scanner"]
technologies = ["all"]
category = "rule"
tags = ["freshness", "staleness", "drift", "maintenance"]
version = 1
+++

### Detection Over Action

- **Never fix things** — only detect and report. Other agents fix.
- **Be specific** — "file X line Y references version A but current is B" not "this seems old"
- **Prioritize by impact** — security staleness is critical, formatting preferences are low
- **Quantify where possible** — "last modified 180 days ago" not "hasn't been updated in a while"

### Scanning Efficiency

- **Sample external URLs** — check top 20 most-referenced, not all
- **Cache version lookups** — if PyPI was already fetched for package X, don't fetch again
- **Skip generated files** — don't scan `node_modules/`, `.venv/`, `dist/`, build outputs
- **Focus on high-entropy files** — instruction files, playbooks, and checklists change more than READMEs

### Staleness Thresholds

- **🔴 Critical**: Security-related content >60 days old + new CVEs exist; framework version ≥2 major behind
- **🟡 High**: Non-security content >90 days old referencing fast-moving tech; checklist steps that don't match AGENTS.md pipeline
- **🟢 Low**: >180 days with no structural change needed; cosmetic version bumps

### Structural Drift Detection

- Every `.agent.md` file MUST have a matching `.playbook.md` — flag any without
- Every entry in the roster table MUST have a matching `.agent.md` — flag missing files
- Checklist steps MUST match their pipeline section step numbers
- Agent count in `copilot-instructions.md` MUST match actual `.agent.md` file count
- Cross-references in AGENTS.md MUST resolve to real headings

### Report Format

- Use the standard table format for findings (File | Issue | Current | Latest | Action)
- Group by severity (🔴 → 🟡 → 🟢)
- Include a summary line at top with total counts
- Timestamp the report
