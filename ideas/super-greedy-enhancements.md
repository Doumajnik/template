# Super Greedy Pipeline — Additional Ideas & Enhancements

## Novel Agents to Add (research-backed suggestions)

### 1. Formal Verification Agent
- For critical invariants (auth, payments, state machines), generate **Z3/TLA+ specifications** alongside the implementation
- Proves correctness mathematically for the most dangerous code paths
- Only runs on functions flagged as `[formally-verify]` by the Architect

### 2. Regression Oracle Agent
- Captures ALL function I/O pairs during test runs as "golden files"
- On any subsequent change, re-runs the golden file inputs and diffs outputs
- Detects behavioral drift that tests might miss (subtle floating-point changes, ordering changes, etc.)
- Pairs with Mutation Testing to verify the oracle catches mutations too

### 3. Temporal Coherence Agent
- Re-runs the full test suite with the system clock shifted:
  - UTC+14 (Kiribati), UTC-12 (Baker Island)
  - DST transition moments (spring forward, fall back)
  - Leap year edge (Feb 29), year boundary (Dec 31 → Jan 1)
  - Y2038 (Unix timestamp overflow), Y2100 (non-leap century)
- Catches time-sensitive bugs that normal tests miss

### 4. Dependency Future-Proofing Agent
- Runs tests with **next-major versions** of all dependencies
- Identifies upcoming breaking changes before they hit you
- Produces a "future compatibility report" — what will break in 6 months
- Pairs with Dependency Agent (which audits current versions)

### 5. Contract Drift Detector Agent
- For microservice architectures: monitors ALL service contracts
- When one service's API changes, checks if all consumers still work
- Cross-project awareness (needs the centralized hub approach)
- Generates contract tests automatically from OpenAPI specs

### 6. LLM Self-Critique Chain Agent
- After any audit agent (Security, Code Quality, etc.) completes, spawns a second pass:
  - "What did you miss? What false negatives might exist?"
  - Uses a DIFFERENT temperature (creative mode) to catch blind spots
  - Only additions — never removes findings from the first pass
- Turns every audit into a two-pass system

### 7. Chaos Engineering Agent
- Designs failure injection scenarios for the architecture:
  - What happens if this service is down?
  - What happens if the database is slow (5x latency)?
  - What happens if this API returns malformed data?
- Writes test scenarios (not actual infra chaos) that verify graceful degradation
- Pairs with Load Testing and Resilience patterns

### 8. API Fuzzer Agent
- Generates random, malformed, and adversarial inputs for every public API
- Uses property-based testing libraries (Hypothesis, fast-check, QuickCheck)
- Finds crash-inducing inputs that hand-written tests miss
- Runs AFTER the Test Writer's structured tests pass — this is the "break it" layer

### 9. Documentation Accuracy Agent
- Reads code AND docs, checks for drift between them
- Verifies code examples in docs actually compile/run
- Checks that parameter descriptions match actual function signatures
- Different from Consistency Check (which checks plan↔code) — this checks docs↔runtime-behavior

### 10. Multi-Language Coherence Agent
- For polyglot projects: ensures patterns are consistent ACROSS languages
- If Python uses snake_case and TypeScript uses camelCase — fine
- But if Python's `UserService.get_user(id)` returns different fields than TypeScript's `userService.getUser(id)` — that's drift
- Checks shared data models, API contracts, error codes across language boundaries

---

## Enhanced Council Patterns

### Debate Protocol Improvements
1. **Structured disagreement format** — when models disagree, each must state:
   - Their position
   - Their strongest argument
   - What would change their mind (falsifiable criterion)
   - Their confidence level (1–10)
2. **Minority report preservation** — dissenting views are NEVER discarded, only annotated with why the majority won
3. **Retrospective accuracy tracking** — after implementation, check which model's prediction was more accurate. Feed this back into tier assignments

### Temperature Diversity Protocol
When only one model is available (single-provider fallback):
- T=0.0 → conservative, safe implementation
- T=0.3 → balanced (default)
- T=0.7 → creative, unconventional approaches
- T=1.0 → wild exploration (only for Innovator)

The Council then has 3-4 genuinely different perspectives even with one model.

### Quality Gates Escalation
| Gate Result | Standard Pipeline | Super Greedy Pipeline |
| --- | --- | --- |
| All pass | Continue | Continue |
| 1 finding | Fix + continue | Fix + re-run gate + continue |
| 3+ findings | Fix + re-run gate | Fix + re-run gate + spawn a second reviewer model |
| CRITICAL finding | Block + fix + re-run | Block + fix + re-run + Architect re-review + Council vote on whether design is flawed |

---

## Integration with Claude Code Max

### Optimal Model Usage
| Task Type | Model | Reason |
| --- | --- | --- |
| Architecture, Security decisions | Opus (thinking) | Deepest reasoning, catches subtle flaws |
| Implementation, Testing | Sonnet | Fast, high quality, cost-effective |
| Validation, Formatting, Quick checks | Haiku | Instant feedback, cheap |
| Council synthesis | Opus (thinking) | Must reason about trade-offs |
| N-version critical impl | Opus + Sonnet + Sonnet (different temps) | Diversity |

### Session Cost Tracking
Add to Quality Scorecard:
```markdown
## Session Metrics
| Metric | Value |
| --- | --- |
| Total prompts sent | X |
| Opus calls | Y |
| Sonnet calls | Z |
| Haiku calls | W |
| Estimated cost (if metered) | $X.XX |
| Wall-clock time | HH:MM |
| Functions implemented | N |
| Cost per function | $X.XX |
| Tests per dollar | N |
```

This helps users understand what the "greedy" approach actually costs in practice.

---

## Cross-Project Super Greedy (with Centralized Hub)

When the hub manages multiple projects, Super Greedy can do things impossible per-project:

1. **Cross-project API contract verification** — change in Service A → re-test all consumers
2. **Shared security posture** — one vulnerability scan across ALL projects
3. **Pattern propagation** — improvement discovered in Project A → apply to B, C, D
4. **Unified test fixtures** — mock data stays consistent across services
5. **Cross-project retrospective** — patterns that waste time in one project can be pre-empted in others
6. **Shared Playbook evolution** — lessons learned benefit all projects immediately
