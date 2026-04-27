+++
id = "agents/ux-research"
title = "UX Research Agent Playbook"
agents = ["ux-research"]
technologies = ["all"]
category = "rule"
tags = ["ux-research", "usability", "personas"]
version = 1
+++

# UX Research Playbook

## Method Selection

| Question type | Recommended method | Sample size |
| --- | --- | --- |
| Can users complete this task? | Moderated usability test | 5–8 users |
| Where do users drop off? | Funnel analytics + unmoderated test | Analytics: all; test: 10+ |
| What do users think about X? | Semi-structured interview | 6–10 users |
| Which of A or B works better? | A/B test (if traffic) or unmoderated comparative | Quant: power-calc; qual: 10+ |
| How do users behave over time? | Diary study | 8–12 users, 1–4 weeks |
| What features do users want? | Open-ended survey + interviews | Survey: 100+; interviews: 8–12 |

Avoid surveys for "would you use X?" — stated preference is poor predictor of behavior.

## Question Anti-Patterns (forbid)

| Bad (leading) | Good (open) |
| --- | --- |
| "Was that confusing?" | "Tell me what you were thinking there." |
| "Do you like this design?" | "What would you do next on this screen?" |
| "Would you pay for this?" | "When did you last pay for something similar? Why?" |
| "How often do you use X?" (no anchor) | "Tell me about the last time you used X." |

## Synthesis Format

For `docs/UX_RESEARCH_NOTES.md`:

```markdown
### {Study name} — {YYYY-MM-DD}

- **Question:** {one sentence}
- **Method:** {method}
- **Participants:** {count and recruitment criteria}
- **Materials:** {protocol link, prototype version}

#### Findings (ranked by severity × frequency)

##### F1 — [HIGH] Users miss the primary CTA on mobile

- **Frequency:** 6 of 8 participants
- **Severity:** Blocks task completion
- **Evidence:** {paraphrased + 1–2 anonymized quotes}
- **Design implication:** Primary CTA needs higher visual weight or placement above the fold on mobile breakpoints.

##### F2 — [MEDIUM] Confusion about pricing tiers
- ...

#### Persona updates

- {bullet}

#### Follow-up research needed

- {bullet}
```

## Severity × Frequency Rubric

| | Low frequency (< 25%) | Medium (25–60%) | High (> 60%) |
| --- | --- | --- | --- |
| **Catastrophic** (blocks task) | HIGH | CRITICAL | CRITICAL |
| **Major** (workaround needed) | MEDIUM | HIGH | HIGH |
| **Minor** (friction) | LOW | MEDIUM | MEDIUM |

## Coordination

- **Prompt Engineer** — I feed user-centric requirements into the enriched spec.
- **Architect** — I provide constraints; Architect designs the response.
- **Accessibility** — WCAG ≠ usability; coordinate to cover both.
- **Localization** — locale-specific usability concerns route here.
- **Frontend Component** — implements the design that addresses the findings.
