---
description: Profile and optimize slow code, queries, or endpoints
agent: Performance
---

# Optimize Performance

Profile and optimize the following performance target:

**Performance Target:** ${input:performanceTarget}

## Instructions

1. **Read context files first:**
   - `.ai/PREFERENCES.md` — coding style and project settings
   - `docs/PLAYBOOK.md` — architecture decisions and existing patterns
   - `docs/CODE_INVENTORY.md` — source files and symbol registry

2. **Identify the performance target:**
   - Locate the specific code, endpoint, or query to optimize
   - Read the target source file(s) and understand the current implementation
   - Map the call chain from entry point through all dependencies

3. **Establish a baseline:**
   - Measure current performance (execution time, memory, throughput)
   - Run existing benchmarks or create a simple timing harness
   - Document the baseline metrics for before/after comparison

4. **Profile and find hotspots:**
   - Analyze algorithmic complexity (time and space)
   - Identify N+1 queries, redundant computations, or unnecessary I/O
   - Check for memory leaks, excessive allocations, or large data copies
   - Review database queries with EXPLAIN plans where applicable

5. **Plan optimizations:**
   - Rank hotspots by impact — fix the biggest bottleneck first
   - Consider: caching, batching, lazy loading, algorithm improvements
   - Evaluate trade-offs: readability vs. speed, memory vs. CPU
   - Ensure correctness is never sacrificed for performance

6. **Implement optimizations:**
   - Apply changes incrementally — one optimization at a time
   - Run tests after each change to verify correctness is preserved
   - Keep functions under ~40 lines — extract complex logic into helpers
   - Add comments explaining non-obvious performance decisions

7. **Verify improvement:**
   - Re-measure with the same baseline methodology
   - Compare before/after metrics quantitatively
   - Run the full test suite to confirm no regressions
   - Check for new lint errors or warnings — fix all of them

8. **Report results:**
   - Before/after performance metrics with percentage improvement
   - Summary of each optimization applied and its individual impact
   - Test results confirming no regressions
   - Remaining optimization opportunities (diminishing returns noted)
