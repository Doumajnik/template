# Code Quality Report

> **Persistent code quality audit trail.** The Code Quality Agent appends findings here after each cycle. Findings are tracked from OPEN → FIXED. This file is append-only — never delete old entries.
>
> **Severity levels:** 🔴 CRITICAL | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW | ℹ️ INFO
>
> **Status values:** 🔧 OPEN | ✅ FIXED | ⚠️ PARTIAL | ❌ NOT FIXED

---

## Summary Dashboard

| Metric | Count |
| --- | --- |
| Total findings | 9 |
| 🔴 Critical open | 0 |
| 🟠 High open | 0 |
| 🟡 Medium open | 1 |
| 🟢 Low open | 0 |
| ℹ️ Info open | 0 |
| ⏸️ N/A | 8 |
| ✅ Fixed (all time) | 0 |

---

## Audit Log

<!-- Code Quality Agent appends new audit entries below this line. -->
<!-- Each entry follows this format:

### Audit — {YYYY-MM-DD} — {cycle description}

| # | Severity | Category | File | Line(s) | Finding | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 🔴 CRITICAL | Duplication | src/services/user.ts, src/services/admin.ts | 20-35 | validateEmail() duplicated | Extract to src/utils/validation.ts | 🔧 OPEN |

**Summary:** N findings — X critical, Y high, Z medium

#### Verification — {YYYY-MM-DD}
- Finding #1: ✅ FIXED — extracted to shared utility
-->

> ⚠️ **PHANTOM AUDIT:** The files referenced in this entry either do not exist on disk or were never persisted (verified 2026-03-15). Findings are not actionable until the files are re-implemented. See Retrospective Report 2026-03-15 for details.

### Audit — 2026-03-11 — RAG Playbook Infrastructure (Initial)

| # | Severity | Category | File | Line(s) | Finding | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 🟡 MEDIUM | Duplication | src/utils/embedding_client.py, src/utils/knowledge_index.py | 13-14, 8-9 | `DIMENSIONS = 1536` and model name (`"openai/text-embedding-3-small"`) are defined in both modules. If these drift out of sync, the index becomes inconsistent. | Extract shared constants to a single `src/utils/constants.py` (or `src/config/`) and import from there. | ⏸️ N/A — file does not exist |
| 2 | 🟡 MEDIUM | Duplication | src/utils/playbook_parser.py | 37-47 | Three nearly identical `isinstance(meta[field], list)` validation blocks for `agents`, `technologies`, and `tags`. Copy-paste pattern. | Consolidate into a loop: `for field in ("agents", "technologies", "tags"): if not isinstance(meta[field], list): raise ...` | 🔧 OPEN |
| 3 | 🟡 MEDIUM | Code Smell | scripts/query-knowledge-index.py | 73 | `except Exception as exc:` in `run_query()` catches all exceptions including programming errors (e.g., `TypeError`, `KeyError`). Could mask bugs silently. | Catch specific exceptions (`ValueError`, `urllib.error.URLError`, `FileNotFoundError`). Let unexpected errors propagate. | ⏸️ N/A — file does not exist |
| 4 | 🟡 MEDIUM | Code Smell | scripts/build-knowledge-index.py | 48-51 | `validate_environment()` calls `sys.exit(1)` directly. Mixes validation with flow control, making the function untestable without mocking `sys.exit`. | Raise a custom exception (e.g., `ConfigError`) and let `main()` handle the exit. | ⏸️ N/A — file does not exist |
| 5 | 🟢 LOW | Magic Number | scripts/query-knowledge-index.py | 95 | Content preview truncation uses hardcoded `200` (`content[:200]`). No named constant or docstring explaining the choice. | Extract to `PREVIEW_MAX_CHARS = 200` at module level. | ⏸️ N/A — file does not exist |
| 6 | 🟢 LOW | Duplication | src/utils/embedding_client.py | 101-124 | `_retry_with_backoff`: the `except urllib.error.HTTPError` and `except urllib.error.URLError` branches share identical retry logic (compute delay, check max_retries, print message, sleep). Only the delay source differs. | Extract the shared retry tail into a helper or combine the except clauses using a shared code path. | ⏸️ N/A — file does not exist |
| 7 | 🟢 LOW | Naming | src/utils/embedding_client.py, src/utils/knowledge_index.py | 13, 8 | Inconsistent constant naming: `MODEL` in embedding_client.py vs `MODEL_NAME` in knowledge_index.py for the same value. | Use a single canonical name (either `MODEL` or `MODEL_NAME`) — ideally in the shared constants file from finding #1. | ⏸️ N/A — file does not exist |
| 8 | ℹ️ INFO | Structure | scripts/build-knowledge-index.py, scripts/query-knowledge-index.py | 8-9, 9-10 | Both scripts use `sys.path.insert(0, ...)` to import from `src/utils/`. Standard pattern for flat-layout scripts, but fragile if directory structure changes. | Acceptable for now. Consider adding a `pyproject.toml` with installable package in the future. | ⏸️ N/A — file does not exist |
| 9 | ℹ️ INFO | Performance | src/utils/knowledge_index.py | 67-69 | `_dot_product` uses pure Python `sum(a * b for ...)`. Adequate for current scale (~50 chunks) but would bottleneck at thousands of chunks. | No action needed now. If index grows to 500+ chunks, consider `numpy.dot()` or a vector DB. | ⏸️ N/A — file does not exist |

**Summary:** 9 findings — 0 critical, 0 high, 4 medium, 3 low, 2 info

**Positive observations:**

- All functions in `playbook_parser.py` are under 40 lines
- Test coverage for `playbook_parser.py` is excellent: 74 tests covering all 8 functions
- Constants are well-extracted (e.g., `VALID_CATEGORIES`, `REQUIRED_FIELDS`)
- No dead code, no commented-out blocks, no unused imports in `playbook_parser.py`
