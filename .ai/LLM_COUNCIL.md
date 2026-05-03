# LLM Council Protocol

> Reference document for the **LLM Council** meta-pattern used in the Super Greedy Pipeline.
> The Council is NOT a single agent — it's an orchestration pattern where the same task is dispatched to multiple models independently and results are synthesized.

---

## When the Council Runs

The LLM Council pattern is applied during `GREEDY_MODE: ON` sessions at these steps:

| Step | Task | Models Used |
| --- | --- | --- |
| 1 (Prompt Engineer) | Spec synthesis | All Tier 1 |
| 5 (Architect) | Architecture design | All Tier 1 |
| 8 (Innovator) | Creative alternatives | All Tier 1 |
| 10 (Critic) | Full review | 2+ Tier 1 |
| 12 (Plan verification) | Architect verifies plan | 2+ Tier 1 |
| 17 (Test Writer) | Test suite per function | 2 models |
| 18 (Worker) | N-version impl (critical only) | 2–3 models |
| 20 (Reviewer) | Implementation review | All Tier 1 |
| 21 (Security) | Security audit | 2+ models |
| 20a + 24 (Coherence) | Cross-file review | All Tier 1 |
| 25a (Meta-review) | Retrospective findings | All Tier 1 |

---

## Execution Protocol

### Step 1 — Parallel Dispatch

The Orchestrator spawns the same task to N models independently. Each model receives:

- The **same Librarian context brief** (content identical)
- **Different system prompts** tuned to each model's strengths (optional — use the same prompt if models are equivalent)
- **Independent state** — no model sees another model's output during this step

### Step 2 — Collection

All N outputs are collected. The Orchestrator creates a synthesis document containing:

```markdown
## Council Input — {Step Name}

### Model A Output
{full output from Model A}

### Model B Output
{full output from Model B}

### Model C Output (if applicable)
{full output from Model C}
```

### Step 3 — Consensus Analysis

The Orchestrator (or a Tier 1 model designated as "Council Chair") analyzes the collected outputs:

1. **Identify consensus** — areas where ALL models agree → mark as HIGH CONFIDENCE
2. **Identify majority** — areas where most agree, one dissents → mark as MEDIUM CONFIDENCE
3. **Identify disagreement** — areas where models differ significantly → mark as NEEDS DEBATE

### Step 4 — Debate Rounds (if disagreements exist)

For each NEEDS DEBATE area:

1. Each dissenting model receives the other models' reasoning for their position
2. Each model responds: affirm its position, concede, or propose a synthesis
3. Repeat for max 3 rounds or until consensus is reached
4. If no consensus after 3 rounds: the Council Chair decides, and the dissenting opinion is preserved as an `[ALTERNATIVE]` block

### Step 5 — Council Decision Document

The final output is a **Council Decision** written to `.ai/sessions/{date}_council-decision-{step}.md`:

```markdown
# Council Decision — {Step Name}

## Confidence: {unanimous | majority | split}

## Chosen Approach
{the synthesized/chosen output}

## Consensus Points
- {point 1 — all models agreed}
- {point 2 — all models agreed}

## Majority Points (if any)
- {point — N-1 agreed, 1 dissented}: {brief dissent reason}

## [ALTERNATIVE] Blocks (preserved dissenting opinions)
> These are viable alternatives that the Council did not select but may be useful later.

### Alternative 1: {brief name}
{what was proposed and why it was not selected}
```

---

## N-Version Programming Protocol

For **critical functions** (security-sensitive, data-integrity, business-critical):

### Step 1 — Parallel Implementation

Each model independently implements the same function from:
- The same scaffolded stub
- The same test suite (already written)
- The same Librarian brief

### Step 2 — Test All Implementations

Run the FULL test suite against EACH implementation independently. Record:
- Pass/fail count per implementation
- Performance characteristics (execution time, memory)
- Code complexity metrics (cyclomatic, cognitive)

### Step 3 — Behavioral Comparison

For implementations that all pass tests:
- Generate additional random inputs and compare outputs
- Check for edge cases where implementations differ (these reveal spec ambiguity)
- Flag any behavioral divergence for investigation

### Step 4 — Selection

The Council selects the best implementation based on:
1. **Correctness** — passes all tests (mandatory)
2. **Readability** — clearest code wins when correctness is equal
3. **Performance** — better algorithmic complexity
4. **Robustness** — better error handling, edge case coverage
5. **Hybrid** — sometimes the best code takes the structure from one impl and the error handling from another

### Step 5 — Documentation

The selected implementation includes a comment block:

```python
# Council Decision: Selected from N implementations
# Reason: {why this one was chosen}
# Alternatives considered: {brief description of others}
```

---

## Model Tier Assignment

At session start, the Orchestrator writes `.ai/sessions/{date}_available-models.md`:

```markdown
# Available Models — {date}

## Discovery Method
{how models were enumerated — API query, manual config, etc.}

## Tier Assignments

### Tier 1 — Deepest Reasoning
| Model | Provider | Strengths |
| --- | --- | --- |
| Claude Opus 4 | Anthropic | Architecture, security, complex reasoning |
| GPT-4o | OpenAI | Broad knowledge, code generation |
| Gemini 2.5 Pro | Google | Large context, research synthesis |

### Tier 2 — Strong Execution
| Model | Provider | Strengths |
| --- | --- | --- |
| Claude Sonnet 4 | Anthropic | Fast execution, good code |
| GPT-4.1 | OpenAI | Consistent output, good tests |
| Gemini 2.5 Flash | Google | Speed, large context |

### Tier 3 — Fast Validation
| Model | Provider | Strengths |
| --- | --- | --- |
| Claude Haiku | Anthropic | Speed, linting, formatting |
| GPT-4.1 mini | OpenAI | Quick checks, simple tasks |
| Gemini Flash Lite | Google | Fastest, validation only |
```

### Single-Provider Fallback

If only one model is available (e.g., only Claude Sonnet 4), the Council still runs:
- All tiers collapse to that model
- Multi-dispatch uses different **temperatures** (0.0, 0.3, 0.7) and **system prompts** (conservative, balanced, creative) to get diverse outputs
- The synthesis step still applies — different temperatures produce different reasoning paths

---

## Continuous Audit Protocol

After EVERY implementation step (per function), the Orchestrator spawns the mini-audit pack:

1. **Security** (Tier 3 model, fast) — quick OWASP check on the new code
2. **Code Quality** (Tier 3 model, fast) — complexity, duplication, naming
3. **Type Safety** (Tier 3 model, fast) — no `any`, no unsafe casts, schema consistency
4. **Error Handling** (Tier 3 model, fast) — no silent catches, proper context in errors

Each returns a PASS/FAIL with one-line findings. On FAIL:
- The Worker immediately fixes the issue before moving to the next function
- The fix is re-audited (loop until PASS)
- Findings are accumulated for the formal audit steps later

This catches issues at introduction time — far cheaper than finding them at phase boundaries.
