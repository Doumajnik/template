+++
id = "agents/vendor-evaluator"
title = "Vendor Evaluator Agent Playbook"
agents = ["vendor-evaluator"]
technologies = ["all"]
category = "rule"
tags = ["vendor-evaluator", "build-vs-buy", "licensing", "lock-in"]
version = 1
+++

# Vendor Evaluator Playbook

## Scoring Rubric

Each candidate scored 1–5 per dimension; weight per project priority.

| Dimension | 1 (poor) | 5 (excellent) |
| --- | --- | --- |
| Fit | Misses must-haves | Covers must-haves and nice-to-haves |
| Maturity | < 6 months old or pre-1.0 with breaking changes | 3+ years, semver-stable, large user base |
| Maintenance | No commits in 6 months, unanswered issues | Active monthly releases, fast issue response |
| Community / docs | Sparse docs, no community | Comprehensive docs, active forum, paid support available |
| License risk | AGPL / SSPL / proprietary opaque | MIT / Apache 2.0 / BSD |
| Lock-in | Proprietary data format, no export | Open standards, easy export, interoperable |
| Total cost | High license + high integration + high ops | Low across all three |
| Security posture | No disclosure policy, recent unpatched CVEs | SOC 2 / ISO, public disclosure, fast patch cadence |

## Evaluation Entry Template

In `docs/VENDOR_EVALUATIONS.md`:

```markdown
### {Need} — {YYYY-MM-DD}

**Need:** {one paragraph}
**Must-haves:** {bullets}
**Nice-to-haves:** {bullets}
**Expected scale:** {numbers}

| Dimension | Candidate A | Candidate B | Build it ourselves |
| --- | --- | --- | --- |
| Fit | 5 | 4 | 3 |
| Maturity | 5 | 3 | n/a |
| Maintenance | 4 | 5 | n/a |
| Community / docs | 5 | 3 | n/a |
| License risk | 5 (MIT) | 2 (AGPL) | 5 |
| Lock-in | 4 | 2 | 5 |
| Total cost (3yr) | $X | $Y | $Z |
| Security posture | 4 | 3 | 4 |
| **Weighted score** | **X.X** | **Y.Y** | **Z.Z** |

**Recommendation:** Candidate A. Runner-up: build ourselves.
**Deal-breakers found:** Candidate B AGPL license incompatible with project.
**Follow-ups:** Legal sign-off on Candidate A's TOS; 1-week POC.
```

## Total Cost Formula

```
3yr_total = 3 × annual_license
          + integration_eng_days × loaded_day_cost
          + 3 × annual_ops_eng_days × loaded_day_cost
          + 3 × annual_infra_cost
          + estimated_switching_cost × switching_probability
```

## License Quick Reference

| License | Safe for typical commercial use? |
| --- | --- |
| MIT, BSD, Apache 2.0, ISC | ✅ Yes |
| LGPL | ⚠️ Yes if dynamically linked; legal review |
| MPL 2.0 | ⚠️ Yes with file-level copyleft awareness |
| GPL v2/v3 | 🔴 Legal review required — copyleft |
| AGPL | 🔴 Legal review required — network copyleft |
| SSPL, BUSL, Commons Clause | 🔴 Legal review required — non-OSI |
| Proprietary / unclear | 🔴 Legal review required |

## Coordination

- **Research Agent** — feeds candidates into my evaluation.
- **Cost/FinOps** — joint sign-off on total cost numbers.
- **Security Agent** — joint sign-off on security posture.
- **Compliance Agent** — joint sign-off on license and data privacy.
- **Architect** — final adoption decision, after my recommendation.
