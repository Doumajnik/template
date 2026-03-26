# Profiling Tools by Language/Platform

Quick reference for selecting the right profiling tool. Prefer language-native tools first, then reach for general-purpose tools for cross-cutting analysis.

---

## Python

| Tool | Type | Use Case |
|------|------|----------|
| **cProfile** | CPU (built-in) | First-pass profiling. Low overhead. Use `python -m cProfile -o prof.out script.py`, visualize with `snakeviz`. |
| **py-spy** | CPU (sampling) | Production-safe sampling profiler. No code changes needed. Generates flame graphs: `py-spy record -o flame.svg -- python script.py`. |
| **line_profiler** | CPU (line-level) | Precise line-by-line timing. Decorate with `@profile`, run with `kernprof -l -v script.py`. Use after cProfile narrows the hotspot. |
| **tracemalloc** | Memory (built-in) | Track memory allocations by source line. `tracemalloc.start()` at entry, snapshot and compare. Good for finding allocation hotspots. |
| **memory_profiler** | Memory (line-level) | Line-by-line memory usage. Decorate with `@profile`, run with `python -m memory_profiler script.py`. |
| **objgraph** | Memory (object graph) | Visualize object reference chains. Useful for diagnosing why objects are not garbage collected. |
| **scalene** | CPU + Memory + GPU | All-in-one profiler with low overhead. Separates Python time from C extension time. `scalene script.py`. |

**Recommended workflow:** cProfile → py-spy flame graph → line_profiler on hotspot → tracemalloc for memory.

---

## Node.js / TypeScript

| Tool | Type | Use Case |
|------|------|----------|
| **--inspect + Chrome DevTools** | CPU + Memory | Built-in V8 profiler. Start with `node --inspect script.js`, open `chrome://inspect`. Take CPU profiles and heap snapshots interactively. |
| **clinic.js** | CPU + Event Loop | Three tools: `clinic doctor` (event loop), `clinic flame` (flamegraph), `clinic bubbleprof` (async). Best first-pass tool. |
| **0x** | CPU (flame graph) | Fast flame graph generation. `0x script.js` produces an interactive SVG. Lower setup than clinic. |
| **v8-profiler-next** | CPU + Memory (programmatic) | Embed profiling in code for targeted snapshots. Useful in test harnesses. |
| **heapdump** | Memory (heap snapshot) | `require('heapdump').writeSnapshot()` to capture heap on demand. Analyze in Chrome DevTools. |
| **--max-old-space-size** | Memory (limit) | Set heap limit to surface leaks faster: `node --max-old-space-size=256 script.js`. |

**Recommended workflow:** clinic doctor → clinic flame on hotspot → Chrome DevTools heap snapshot for memory.

---

## Go

| Tool | Type | Use Case |
|------|------|----------|
| **pprof (CPU)** | CPU | Import `net/http/pprof`, hit `/debug/pprof/profile?seconds=30`. Analyze with `go tool pprof`. |
| **pprof (heap)** | Memory | Hit `/debug/pprof/heap`. Shows live allocations. Use `--alloc_space` for cumulative, `--inuse_space` for current. |
| **pprof (goroutine)** | Concurrency | Hit `/debug/pprof/goroutine?debug=2`. Detects goroutine leaks — count should be stable, not growing. |
| **trace** | Execution trace | `go tool trace trace.out` for event-level execution timeline. Shows goroutine scheduling, GC events, syscalls. |
| **benchstat** | Benchmarks | Compare benchmark runs statistically: `benchstat old.txt new.txt`. Detects significant changes. |
| **-gcflags=-m** | Escape analysis | `go build -gcflags='-m'` shows which allocations escape to heap. Reduce escapes to reduce GC pressure. |

**Recommended workflow:** pprof CPU profile → flame graph → pprof heap for memory → benchstat for before/after.

---

## Rust

| Tool | Type | Use Case |
|------|------|----------|
| **cargo flamegraph** | CPU (flame graph) | `cargo flamegraph -- args` produces a flame graph from perf data. Requires Release build with debug info. |
| **perf** | CPU (Linux) | `perf record --call-graph dwarf ./target/release/binary` → `perf report`. Low-level, high-precision. |
| **criterion** | Benchmarks | Statistical benchmarking framework. Detects regressions automatically. Add to `[dev-dependencies]`. |
| **valgrind (DHAT)** | Memory (heap) | `valgrind --tool=dhat ./target/release/binary`. Shows allocation sites, lifetimes, and access patterns. |
| **cargo-instruments** | CPU + Memory (macOS) | Uses Xcode Instruments on macOS. `cargo instruments -t time` for CPU, `-t alloc` for memory. |
| **tracing + tracy** | Instrumented | Add `tracing` spans to code, visualize with Tracy profiler. Best for complex async workflows. |

**Recommended workflow:** criterion benchmarks → cargo flamegraph → perf for deep-dive → DHAT for allocation analysis.

---

## Java / Kotlin

| Tool | Type | Use Case |
|------|------|----------|
| **Java Flight Recorder (JFR)** | CPU + Memory + I/O | Built into JDK 11+. `java -XX:StartFlightRecording=duration=60s,filename=rec.jfr App`. Analyze with JDK Mission Control. |
| **async-profiler** | CPU + Allocation | Low-overhead sampling profiler. `-e cpu` for CPU, `-e alloc` for allocations. Produces flame graphs. Production-safe. |
| **VisualVM** | CPU + Memory (interactive) | GUI tool. Attach to running JVM, take snapshots, analyze heap. Good for development-time profiling. |
| **JMH** | Benchmarks | Java Microbenchmark Harness. Use `@Benchmark` annotation. Handles JIT warmup, dead-code elimination. The standard for JVM benchmarks. |
| **jstat** | GC monitoring | `jstat -gcutil PID 1000` for per-second GC stats. Quick check for GC pressure without full profiling. |
| **MAT (Memory Analyzer)** | Memory (heap dump) | Analyze heap dumps (`-XX:+HeapDumpOnOutOfMemoryError`). Finds leak suspects and dominator trees. |

**Recommended workflow:** JFR recording → async-profiler flame graph on hotspots → JMH for before/after benchmarks → MAT for heap analysis.

---

## General / Cross-Platform

| Tool | Type | Use Case |
|------|------|----------|
| **Flame graphs** | Visualization | Universal visualization for profiling data. Wide bars = hotspots. Generate from any profiler's stack trace output. |
| **perf (Linux)** | CPU + System | `perf stat`, `perf record`, `perf report`. Works with any compiled language. Requires Linux. |
| **dtrace (macOS/Solaris)** | System tracing | Dynamic tracing of kernel and user-space. Powerful but complex. Use for system-level bottlenecks. |
| **strace / ltrace** | Syscall tracing | `strace -c program` for syscall summary. Quick check for I/O-bound programs — shows where time goes in the kernel. |
| **Wireshark / tcpdump** | Network | Capture and analyze network traffic. Use when profiling reveals time spent in network calls. |
| **wrk / hey / k6** | Load testing | Generate HTTP load for benchmarking. `wrk -t4 -c100 -d30s URL`. Essential for measuring throughput and latency under load. |
