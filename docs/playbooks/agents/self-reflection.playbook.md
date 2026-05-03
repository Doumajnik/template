+++
id = "agents/self-reflection"
title = "Self-Reflection Agent Rules"
agents = ["self-reflection"]
technologies = ["all"]
category = "rule"
tags = ["quality", "filtering", "scoring", "reflection"]
version = 1
+++

### Scoring Discipline

- **Score ALL items before filtering ANY** — the two-pass pattern requires seeing everything simultaneously
- **Justify every score** — a score without a reason is invalid
- **Use the full 0-10 range** — don't cluster everything at 7-8. Real distributions are spread.
- **Calibrate to input volume** — lower the noise threshold when there are ≤5 items

### Filtering Rules

- **Default noise threshold: 5.0** — items below this are dropped
- **Merge duplicates** — same root cause expressed differently = one finding
- **Promote critical security/correctness** regardless of other scores
- **Demote low-confidence** to "Investigate" — never present uncertain findings as actionable

### Anti-Patterns to Avoid

- **Don't add new findings** — you're a filter, not a generator
- **Don't over-filter** — if upstream found 5 items and you drop 4, you've probably over-filtered
- **Don't rubber-stamp** — giving everything 8/10 defeats the purpose
- **Don't anchor on order** — the first item isn't automatically the best

### When to Skip Self-Reflection

- ≤3 findings from upstream (too few to justify filtering)
- Binary pass/fail results (tests, linting)
- Active incidents (speed > precision)
- Direct user requests ("show me everything")
