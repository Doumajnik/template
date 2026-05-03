# Research Brief: Quality Automation Tools — Semgrep, mutmut, Hypothesis

**Date:** 2026-05-04  
**Requested by:** User (pre-architecture research — AI agent pipeline integration)

---

## Summary

Three complementary tools form a powerful quality automation layer for an AI coding agent
pipeline. **Semgrep** enforces coding conventions and security rules through AST-aware
pattern matching. **mutmut** validates that test suites actually detect real bugs via
Python mutation testing. **Hypothesis** generates property-based tests that find edge cases
ordinary unit tests miss, with a persistent database of known-bad examples across runs.
Together they create a multi-layer quality gate: *static analysis → test quality → test
breadth*.

---

## Libraries & Dependencies

| Package | Purpose | Version | Notes |
|---|---|---|---|
| `semgrep` | AST-aware static analysis / custom rules | **1.161.0** | Verified from PyPI (Apr 22 2026) |
| `mutmut` | Python mutation testing | **3.5.0** | Verified from PyPI (Feb 22 2026); requires Linux/macOS or WSL — no native Windows fork support |
| `hypothesis` | Property-based testing | **6.152.4** | Verified from PyPI (Apr 27 2026) |

---

## 1. Semgrep

### How Custom Rules Work

Semgrep rules are YAML files that describe **code patterns** resembling the source code they
target — no ASTs, no regexes over raw text. The engine operates semantically: it understands
imports, aliases, constant propagation, and associative operators.

**Minimal rule skeleton:**

```yaml
rules:
  - id: no-raw-sql-string
    languages: [python]
    severity: HIGH
    message: "Avoid raw SQL string formatting — use parameterised queries: $QUERY"
    patterns:
      - pattern: cursor.execute($QUERY % ...)
      - pattern-not: cursor.execute($QUERY, ...)
    fix: "cursor.execute($QUERY, (...))"
```

**Full rule schema — required fields:**

| Field | Type | Purpose |
|---|---|---|
| `id` | string | Unique identifier (used in `# nosemgrep: rule-id` suppressions) |
| `message` | string | Developer-facing description; can embed `$METAVAR` values |
| `severity` | `LOW\|MEDIUM\|HIGH\|CRITICAL` | Criticality rating |
| `languages` | array | `python`, `javascript`, `go`, `java`, etc. |
| `pattern` OR `patterns` OR `pattern-either` OR `pattern-regex` | — | At least one required |

**Optional fields:**

| Field | Purpose |
|---|---|
| `fix` | Auto-fix suggestion applied with `--autofix` |
| `metadata` | Arbitrary tags: `cwe`, `owasp`, `category`, `discovered-by` |
| `paths.include` / `paths.exclude` | Scope a rule to specific file globs |
| `min-version` / `max-version` | Guard rules requiring newer Semgrep features |

### Pattern Operators (composable logic)

```
pattern          → positive match (AND with other patterns)
patterns         → logical AND block
pattern-either   → logical OR block
pattern-not      → logical NOT (remove matching results)
pattern-inside   → keep results inside this context
pattern-not-inside → keep results NOT inside this context
pattern-regex    → PCRE2 regex fallback (use sparingly)
```

**Evaluation order inside `patterns`:** positive → negative → conditionals → focus.

### Metavariables

```yaml
# $X, $FUNC, $ARG2 — match any expression, tracked by name
pattern: db.execute($QUERY)

# ... — ellipsis: zero or more items (args, statements, fields)
pattern: requests.get(..., verify=False, ...)

# $...ARGS — ellipsis metavariable capturing a sequence
pattern: foo($...ARGS, 3, $...ARGS)

# Typed metavariable (Java/Go/TypeScript)
pattern: (java.util.logging.Logger $LOGGER).log(...)
```

Metavariable values must be **identical across sub-patterns** in a `patterns` AND block
(metavariable unification). This is intentionally not enforced in `pattern-either`.

### Advanced Operators for Agent Rules

```yaml
# metavariable-regex — filter match by regex on captured value
- metavariable-regex:
    metavariable: $METHOD
    regex: (insecure1|insecure2)

# metavariable-comparison — numeric/date constraints
- metavariable-comparison:
    metavariable: $PORT
    comparison: $PORT < 1024 and $PORT % 2 == 0

# metavariable-pattern — recurse into a matched value with sub-rules
- metavariable-pattern:
    metavariable: $OPTS
    patterns:
      - pattern-not: {secure: True, ...}

# focus-metavariable — highlight only the relevant node, not the entire match
- focus-metavariable: $ARG

# Deep expression operator — match pattern anywhere in nested expression
pattern: |
  if <... $USER.is_admin() ...>:
    ...
```

### Encoding Coding Conventions as Semgrep Rules

Yes — this is Semgrep's primary use case beyond security. Examples:

```yaml
# Enforce assertEqual over == in tests
rules:
  - id: use-assert-equal
    pattern: self.assertTrue($A == $B)
    fix: self.assertEqual($A, $B)
    languages: [python]
    severity: LOW
    message: "Use assertEqual for equality checks"

# Prevent direct dict access (prefer .get())
  - id: prefer-dict-get
    patterns:
      - pattern: $DICT[$KEY]
      - pattern-not-inside: $DICT[$KEY] = ...
    fix: $DICT.get($KEY)
    languages: [python]
    severity: LOW
    message: "Use .get() to avoid KeyError"

# Ban print() in non-test production code
  - id: no-print-in-src
    pattern: print(...)
    paths:
      exclude: ["tests/**", "scripts/**"]
    languages: [python]
    severity: MEDIUM
    message: "Use logging instead of print()"

# Enforce transaction guard pattern
  - id: db-write-needs-transaction
    patterns:
      - pattern: db.execute($Q, ...)
      - pattern-not-inside: |
          with transaction():
            ...
    languages: [python]
    severity: HIGH
    message: "DB writes must be inside a transaction() context manager"
```

The `fix` key + `--autofix` flag lets the agent automatically apply corrections — critical
for pipeline integration.

### CI Integration Patterns

**GitHub Actions:**

```yaml
# .github/workflows/semgrep.yml
name: Semgrep
on:
  push:
    branches: [main]
  pull_request: {}
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/python
            .semgrep/custom-rules.yml
          # Only report NEW findings on PRs (don't block on pre-existing debt)
          publishToken: ${{ secrets.SEMGREP_APP_TOKEN }}
```

**Local / agent CLI:**

```bash
# Run custom rules + registry pack + emit SARIF
semgrep scan \
  --config .semgrep/ \
  --config p/python \
  --metrics=off \
  --json \
  --output semgrep-results.json \
  src/

# Auto-fix mode (agent applies fixes)
semgrep scan --config .semgrep/conventions.yml --autofix src/

# Diff-aware scan (only changed files on a PR)
semgrep scan --config .semgrep/ --diff-base origin/main src/
```

**MCP Server integration (native AI-agent support):**

```bash
# Start the MCP server — integrates with Cursor, VS Code, Claude Desktop
semgrep mcp

# Built-in MCP prompt to help AI write accurate rules:
# "write_custom_semgrep_rule" — call this to get rule scaffolding
```

**Output parsing for pipeline:**

```python
import subprocess, json

def run_semgrep(config: str, path: str) -> list[dict]:
    result = subprocess.run(
        ["semgrep", "scan", "--config", config, "--json", "--metrics=off", path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data.get("results", [])  # each has: check_id, path, start.line, message, severity
```

**Exit codes:**
- `0` — no findings
- `1` — findings (use to fail CI)
- `2` — parse/config error

---

## 2. mutmut (Python Mutation Testing)

### How Mutation Testing Works in Practice

Mutmut introduces **deliberate small code changes** (mutations), then runs the test suite.
If a test *fails*, the mutant is **killed** (good — test detected the change). If all tests
*pass*, the mutant **survived** (bad — test suite cannot distinguish this code from broken code).

**Mutation categories (actual mutations applied):**

| Original | Mutated | Rationale |
|---|---|---|
| `< ` | `<=` | Boundary condition |
| `== ` | `!=` | Equality inversion |
| `True` | `False` | Boolean flip |
| `break` | `continue` | Loop control |
| `0` | `1`, `5` → `6` | Numeric shift |
| `and` | `or` | Logic operator |
| `+` | `-` | Arithmetic |

### Integration with pytest

```bash
pip install mutmut

# Basic run (auto-detects src/ and tests/)
mutmut run

# Scoped to one module
mutmut run "my_module*"
mutmut run "my_module.my_function*"

# Browse surviving mutants (TUI)
mutmut browse

# Apply a mutant to disk to inspect manually
mutmut apply <mutant-id>  # MUST have file under source control first

# Get results for CI consumption
mutmut results
mutmut show <mutant-id>
```

**pyproject.toml configuration:**

```toml
[tool.mutmut]
source_paths = ["src/"]
pytest_add_cli_args_test_selection = ["tests/"]

# Performance: only mutate lines covered by coverage.py
mutate_only_covered_lines = true

# Exclude generated/boilerplate code
do_not_mutate = ["*migrations*", "*__init__*"]

# Speed: limit stack depth (8 = reasonable balance)
max_stack_depth = 8

# Use mypy to pre-filter type-invalid mutants (reduces noise)
type_check_command = ["mypy", "src/", "--output", "json", "--disable-error-code", "unused-ignore"]

# Timeout: (original_duration + 1.0) * 15.0 seconds per mutant
timeout_constant = 1.0
timeout_multiplier = 15.0

# Suppress patterns that don't need mutation (regex on source)
do_not_mutate_patterns = [
    'logger\.\w+',     # logger calls
    'raise \w+',       # exception raises
]
```

**setup.cfg alternative:**

```ini
[mutmut]
source_paths=src/
pytest_add_cli_args_test_selection=tests/
mutate_only_covered_lines=true
max_stack_depth=8
```

### Skipping Mutations in Code

```python
some_code()  # pragma: no mutate       — single line

def complex_algo():  # pragma: no mutate block
    return some_complex_calculation()  # entire function body excluded

# pragma: no mutate start
b = skip_this()
c = skip_this_too()
# pragma: no mutate end
```

### Kill Rate Metrics and Reporting

```bash
# Summary (surviving / killed / timeout / suspicious)
mutmut results

# Example output:
# 145 out of 160 mutants killed (90.6%)
# 15 survived mutants
```

**Parse for pipeline:**

```python
import subprocess, re

def get_kill_rate() -> float:
    result = subprocess.run(["mutmut", "results"], capture_output=True, text=True)
    m = re.search(r"(\d+) out of (\d+) mutants killed", result.stdout)
    if m:
        return int(m.group(1)) / int(m.group(2))
    return 0.0

# Pipeline gate: require ≥90% kill rate
assert get_kill_rate() >= 0.90, "Mutation kill rate below 90% threshold"
```

**Incrementally resuming runs:** mutmut stores state in `mutants/` directory. Subsequent
`mutmut run` calls continue where they left off. Delete `mutants/` to start fresh.

### Performance Considerations for Large Codebases

| Strategy | Config Key | Effect |
|---|---|---|
| Coverage filtering | `mutate_only_covered_lines=true` | Only mutate lines exercised by tests |
| Stack depth limit | `max_stack_depth=8` | Ignore deeply-nested incidental calls |
| Type-check pre-filter | `type_check_command` | Discard type-invalid mutants before running tests |
| Scope to changed files | `mutmut run "changed_module*"` | Only mutate what changed in a PR |
| Exclude boilerplate | `do_not_mutate` / `do_not_mutate_patterns` | Skip migrations, auto-generated code |
| Parallel execution | Built-in | mutmut runs mutations in parallel by default |

**WSL requirement on Windows:** mutmut uses `fork()` — must run inside WSL on Windows,
which the existing memory notes flag as the environment.

---

## 3. Hypothesis (Property-Based Testing)

### Strategy-Based Test Generation

The `@given` decorator + strategies replace hand-written test data:

```python
from hypothesis import given, settings, assume
import hypothesis.strategies as st

# Core strategies
st.integers(min_value=0, max_value=100)
st.floats(allow_nan=False, allow_infinity=False)
st.text(min_size=1, alphabet=st.characters(whitelist_categories=('Lu', 'Ll')))
st.lists(st.integers(), min_size=1, max_size=50)
st.dictionaries(st.text(), st.integers())
st.one_of(st.integers(), st.text())  # union of strategies
st.sampled_from(["a", "b", "c"])    # pick from known values
st.binary()
st.booleans()
st.none()
st.just(42)                          # always produce 42
st.builds(MyClass, x=st.integers()) # construct an object

# Filter
st.integers().filter(lambda n: n % 2 == 0)

# Map / transform
st.integers().map(lambda n: n * 2)

# Dependent generation with @composite
@st.composite
def ordered_pairs(draw):
    n1 = draw(st.integers())
    n2 = draw(st.integers(min_value=n1))
    return (n1, n2)

@given(ordered_pairs())
def test_ordering(pair):
    n1, n2 = pair
    assert n1 <= n2
```

### Shrinking — Automatic Minimal Failure Reduction

When Hypothesis finds a failing example, it **automatically shrinks** it to the simplest
possible counter-example before reporting:

```
Falsifying example: test_matches_builtin(ls=[0, 0])
```

Instead of reporting the full random input that failed (e.g., `[7, 0, 3, 0, 42, 0]`), it
reduces to the minimal case that still fails. This happens transparently — no configuration
needed. The shrunk example is then **saved to the Hypothesis database** so future runs
reproduce it first.

### Integration with pytest

```python
# Works transparently with pytest — no special runner needed
# pytest discovers @given-decorated functions as normal tests

from hypothesis import given, settings, HealthCheck
import hypothesis.strategies as st
import pytest

# Combined with parametrize
@pytest.mark.parametrize("operation", [reversed, sorted])
@given(st.lists(st.integers()))
def test_length_preserved(operation, lst):
    assert len(lst) == len(list(operation(lst)))

# Combined with fixtures
@pytest.fixture(scope="session")
def db_connection():
    return create_test_db()

@given(st.integers(0, 100))
def test_with_fixture(db_connection, n):
    assert db_connection.lookup(n) is not None

# Settings via decorator
@settings(max_examples=500, deadline=None)
@given(st.text())
def test_heavy(s):
    ...

# Suppress specific health checks (e.g., for slow setups)
@settings(suppress_health_check=[HealthCheck.too_slow])
@given(st.binary(min_size=1000))
def test_large_input(data):
    ...
```

**Settings profiles (for CI vs local):**

```python
from hypothesis import settings, Phase

# Register profiles
settings.register_profile("ci", max_examples=200, deadline=500)
settings.register_profile("dev", max_examples=50, deadline=None)
settings.register_profile("exhaustive", max_examples=10_000, phases=[Phase.explicit, Phase.reuse, Phase.generate, Phase.shrink])

# Activate via env var or code
settings.load_profile("ci")  # or: HYPOTHESIS_PROFILE=ci pytest
```

### Database of Examples Across Runs

Hypothesis maintains a **local SQLite database** (`.hypothesis/` directory) that persists:
- Every failing example found (so they're replayed first on next run)
- Shrunk counter-examples
- Examples found to be "interesting" during shrinking

This means **regressions are automatically checked on every run** — if a bug was found
before, the exact minimal case is replayed even if the random seed changes.

```python
from hypothesis.database import DirectoryBasedExampleDatabase

# Custom database location (useful for CI caching)
settings.register_profile(
    "ci",
    database=DirectoryBasedExampleDatabase(".hypothesis/ci-examples"),
    max_examples=200
)
```

**CI caching pattern (GitHub Actions):**
```yaml
- uses: actions/cache@v4
  with:
    path: .hypothesis/
    key: hypothesis-${{ hashFiles('tests/**/*.py') }}
```

### Stateful Testing Capabilities

`RuleBasedStateMachine` lets Hypothesis generate **entire sequences of operations**, not
just single inputs. It finds bugs that only appear after specific chains of actions:

```python
from hypothesis.stateful import (
    RuleBasedStateMachine, Bundle, rule, initialize, invariant, precondition
)
import hypothesis.strategies as st

class QueueStateMachine(RuleBasedStateMachine):
    """Test a queue implementation against a reference model (list)."""

    def __init__(self):
        super().__init__()
        self.real_queue = MyQueue()
        self.model = []

    items = Bundle("items")

    @initialize(target=items)
    def init_item(self):
        return 0  # Seed the bundle

    @rule(target=items, value=st.integers())
    def enqueue(self, value):
        self.real_queue.push(value)
        self.model.append(value)
        return value

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def dequeue(self):
        expected = self.model.pop(0)
        actual = self.real_queue.pop()
        assert actual == expected

    @invariant()
    def size_matches(self):
        assert len(self.real_queue) == len(self.model)

# Expose as pytest TestCase
TestQueue = QueueStateMachine.TestCase

# Or control settings
QueueStateMachine.TestCase.settings = settings(
    max_examples=100,
    stateful_step_count=50  # max operations per test run
)
```

**Key stateful primitives:**

| Decorator | Purpose |
|---|---|
| `@rule()` | A step Hypothesis can call in any sequence |
| `@initialize()` | Runs exactly once before any `@rule`, guaranteed |
| `@precondition(lambda self: ...)` | Guard: skip rule if condition is False |
| `@invariant()` | Assert checked after EVERY step automatically |
| `Bundle("name")` | Typed collection of values — thread data between rules |
| `consumes(bundle)` | Draw from bundle AND remove the value |

---

## Key Findings for AI Agent Pipeline Integration

### 1. Semgrep as a Continuous Code Convention Gate

```
Agent Worker produces code
    → Semgrep scan with project rules
    → Block if any HIGH/CRITICAL findings
    → Agent applies auto-fixes with --autofix
    → Re-scan to verify clean
```

**Agent-writable rule store:** Keep rules in `.semgrep/` directory. The AI agent (Code Quality
or Security Agent) can write new rules to this directory. Each rule becomes a permanent
guard applied to all future code changes.

**AI rule authoring:** Semgrep has a native MCP prompt `write_custom_semgrep_rule` that
helps AI assistants produce accurate rules. Run `semgrep mcp` to expose this.

**Recommended rule categories to encode as Semgrep:**
- Banned APIs (e.g., `hashlib.md5`, `pickle.loads`, `eval`)
- Required safety patterns (e.g., SQL parameterisation, `with` for resource management)
- Project conventions (naming, assertion style, logging over print)
- Deprecated API migration (old API → new API + `fix` key)

### 2. mutmut as a Test Quality Gate

```
Test Writer Agent produces tests
Worker Agent implements code → tests pass
    → mutmut run on the changed module
    → Compute kill rate
    → If kill rate < 90% → loop back to Test Writer Agent
    → Test Writer Agent writes additional tests targeting surviving mutants
    → Re-run mutmut to verify
```

**Surviving mutant → targeted test:** The pattern is:
```python
# mutmut browse output shows: src/services/payment.py:47 - $ARG > 0  →  $ARG >= 0
# Agent reads the surviving mutant and writes:
def test_payment_rejects_zero_amount():
    with pytest.raises(ValueError):
        process_payment(amount=0)
```

**Performance in agent pipelines:**
- Scope to the changed module only: `mutmut run "module_under_test*"`
- Enable `mutate_only_covered_lines=true` — avoids mutating dead code
- Set `max_stack_depth=8` to avoid testing incidental callers
- Use `type_check_command` with mypy to pre-filter 10–20% of invalid mutants

### 3. Hypothesis as a Test Depth Amplifier

```
Test Writer Agent produces example-based tests
    → Hypothesis @given decorators added to property tests
    → Each test run: 100–500 examples generated
    → Hypothesis database persists failures across CI runs
    → Stateful machines test operation sequences (API, queue, state)
```

**Strategy selection by input type:**

| Code pattern | Hypothesis strategy |
|---|---|
| String input | `st.text()` or `st.from_regex(r'\w+')` |
| Numeric input | `st.integers()`, `st.floats(allow_nan=False)` |
| Collections | `st.lists(...)`, `st.dictionaries(...)` |
| Domain objects | `st.builds(MyClass, ...)` or `@st.composite` |
| File paths | `st.from_regex(r'[a-zA-Z0-9_/]+\.txt')` |
| API payloads | `st.fixed_dictionaries({"id": st.integers(), ...})` |
| Enum values | `st.sampled_from(MyEnum)` |

**Agent-generated property tests pattern:**

```python
# Agent writes: for any valid input, these invariants must hold
@given(st.text(min_size=1))
def test_parse_roundtrip(s):
    """Parsing then serialising is identity."""
    assert deserialize(serialize(s)) == s

@given(st.lists(st.integers(), min_size=1))
def test_sort_idempotent(lst):
    """Sorting an already-sorted list is a no-op."""
    once = sorted(lst)
    twice = sorted(once)
    assert once == twice
```

### 4. Three-Layer Quality Pipeline

```
Phase 1 — STATIC (Semgrep)
  Before code merges: scan for convention violations, security issues
  Exit if HIGH/CRITICAL → apply --autofix → re-scan
  Time: ~seconds

Phase 2 — TEST DEPTH (Hypothesis)  
  During test writing: property-based tests generate edge cases
  Shrunk counter-examples saved to .hypothesis/ and replayed on every CI run
  Time: ~minutes (configurable via max_examples)

Phase 3 — TEST QUALITY (mutmut)
  After tests pass: mutation testing verifies tests are meaningful
  Kill rate < 90% → loop back to Test Writer Agent
  Scope to changed module to keep CI time manageable
  Time: ~10–30 min for a module (parallelised, with coverage filter)
```

### 5. Integration Points for the AGENTS.md Pipeline

| Pipeline Step | Tool | Integration |
|---|---|---|
| Step 17 — Test Writer | Hypothesis | Generate `@given` property tests alongside example-based tests |
| Step 18 — Worker | Semgrep | Post-implementation scan; `--autofix` for convention rules |
| Step 19 — Integration Tester | Hypothesis stateful | `RuleBasedStateMachine` for API sequence testing |
| Step 19a — Mutation Testing | mutmut | `mutmut run "module*"` after tests pass; gate on 90% kill rate |
| Step 21 — Security Agent | Semgrep | `semgrep scan --config p/python --config .semgrep/security.yml` |
| Step 22 — Code Quality | Semgrep | `semgrep scan --config .semgrep/conventions.yml` |
| CI pre-commit hook | Semgrep | `semgrep scan --diff-base origin/main` (diff-aware, fast) |

---

## Pitfalls & Warnings

### Semgrep
- **Community Edition is intra-file only** — cross-function dataflow requires Semgrep Pro/AppSec Platform. For free use, Semgrep CE catches pattern-level and single-function taint issues only.
- **Metavariable names must be `$UPPERCASE` or `$UPPERCASE_2`** — lowercase like `$x` is invalid and silently ignored.
- **`...` ellipsis does not cross scope boundaries** — `foo() ... bar()` will not match if `foo()` is in an inner block and `bar()` is in the outer block.
- **`pattern-not` is evaluated after positives** — ordering of sub-patterns inside `patterns` doesn't change results, but having only negatives without a positive match is an error.
- **Metrics are sent to semgrep.dev when using registry configs** — use `--metrics=off` for air-gapped or privacy-sensitive pipelines.

### mutmut
- **Requires fork() — no native Windows support.** Must run in WSL on the Windows dev machine documented in memory notes.
- **Slow on large codebases without filtering** — always enable `mutate_only_covered_lines=true` and `max_stack_depth` in agent pipelines.
- **mutmut 3.x only mutates code inside functions** — module-level constants, class bodies, and top-level code are NOT mutated. Use mutmut 2.x (different model) if that coverage is needed.
- **Type-checker pre-filter can hide valid mutations** — e.g., `self.x = 123 → self.x = None` in `__init__` may be filtered even when valid. Accept this tradeoff for speed.
- **Surviving mutants on logging/telemetry code** — use `do_not_mutate_patterns` or `# pragma: no mutate` on intentionally untested code paths.

### Hypothesis
- **`max_examples=100` is the default** — sufficient for development, raise to 500+ for CI thoroughness.
- **`assume()` overuse causes `Unsatisfiable` errors** — prefer `st.filter()` or domain-specific strategies over heavy `assume()` usage.
- **`.hypothesis/` directory must be committed or cached** — without it, the database of previously found failures is lost and regressions may not be caught.
- **Stateful tests need `teardown()` for resource cleanup** — always implement `teardown()` in `RuleBasedStateMachine` when using real resources.
- **`deadline` setting triggers flakiness on slow machines** — set `deadline=None` in CI if test infrastructure is slow (common in Docker-in-CI).

---

## Alternative Approaches

### Static Analysis Alternatives to Semgrep
- **pylint / flake8** — rule-based linting but no AST-pattern composition or autofix generation. Cannot match structural patterns like "function calls without a specific keyword argument."
- **Bandit** — Python-specific security scanning only; no custom rules, no polyglot support.
- **Ruff** — fastest Python linter, but limited to predefined rules; no custom AST patterns.
- **Decision:** Semgrep wins for AI pipeline use because of its custom-rule authoring, autofix output, JSON output for parsing, and MCP server.

### Mutation Testing Alternatives to mutmut
- **Cosmic Ray** — older Python mutation tester; less actively maintained than mutmut 3.x.
- **Stryker** — excellent for JavaScript/TypeScript, but not Python.
- **pitest** — Java only.
- **Decision:** mutmut is the only actively maintained Python mutation tester with pytest integration.

### Property Testing Alternatives to Hypothesis
- **Faker** — generates realistic fake data but with no shrinking or falsification feedback loop.
- **factory_boy** — fixtures factory, not property testing.
- **QuickCheck (Haskell/other)** — the original; Hypothesis is its Python port, better integrated.
- **Decision:** Hypothesis is the clear winner for Python property testing.

---

## References

- Semgrep GitHub: https://github.com/semgrep/semgrep
- Semgrep rule writing: https://semgrep.dev/docs/writing-rules/overview/
- Semgrep rule syntax: https://semgrep.dev/docs/writing-rules/rule-syntax/
- Semgrep pattern syntax: https://semgrep.dev/docs/writing-rules/pattern-syntax/
- Semgrep Registry (2000+ community rules): https://semgrep.dev/explore
- Semgrep MCP Server: https://github.com/semgrep/semgrep/tree/develop/cli/src/semgrep/mcp
- mutmut GitHub: https://github.com/boxed/mutmut
- mutmut PyPI: https://pypi.org/project/mutmut/
- Hypothesis GitHub: https://github.com/HypothesisWorks/hypothesis
- Hypothesis docs — quickstart: https://hypothesis.readthedocs.io/en/latest/quickstart.html
- Hypothesis docs — stateful: https://hypothesis.readthedocs.io/en/latest/stateful.html
- Hypothesis PyPI: https://pypi.org/project/hypothesis/
