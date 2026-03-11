+++
id = "agents/performance"
title = "Performance Agent Rules"
agents = ["performance"]
technologies = ["all"]
category = "rule"
tags = ["performance"]
version = 2
+++

### Performance Guidelines

- Measure before optimizing — never optimize without profiling data showing an actual bottleneck
- Focus on algorithmic complexity first: O(n²) algorithms with large datasets are the most impactful optimization targets
- Check for N+1 query problems in database access patterns
- Verify caching strategy: are expensive computations cached? Are caches invalidated correctly?
- Check for unnecessary I/O: redundant file reads, repeated API calls, unbatched database queries
- Verify pagination on large collections — never load all records into memory at once
- Check for memory leaks: unclosed resources, growing caches without eviction, circular references
- Profile hot paths — optimize the code that runs most frequently, not the code that looks slow
- Verify async operations are truly concurrent — check for accidental serialization of parallel work
- Check string concatenation in loops — use builders or join patterns for O(n) instead of O(n²)
- Report findings with metrics: before/after measurements, complexity analysis, memory usage
- CRITICAL findings (exponential algorithms, memory leaks) must be fixed — spawn Workers
