# Security Report

> **Persistent security audit trail.** The Security Agent appends findings here after each cycle. Findings are tracked from OPEN → FIXED. This file is append-only — never delete old entries.
>
> **Severity levels:** 🔴 CRITICAL | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW | ℹ️ INFO
>
> **Status values:** 🔧 OPEN | ✅ FIXED | ⚠️ PARTIAL | ❌ NOT FIXED

---

## Summary Dashboard

| Metric | Count |
| --- | --- |
| Total findings | 4 |
| 🔴 Critical open | 0 |
| 🟠 High open | 0 |
| 🟡 Medium open | 0 |
| 🟢 Low open | 0 |
| ℹ️ Info open | 0 |
| ⏸️ N/A | 4 |
| ✅ Fixed (all time) | 0 |

---

## Audit Log

<!-- Security Agent appends new audit entries below this line. -->
<!-- Each entry follows this format:

### Audit — {YYYY-MM-DD} — {cycle description}

| # | Severity | Category | File | Line(s) | Finding | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 🔴 CRITICAL | A04 Crypto | src/config/db.ts | 12 | Hardcoded DB password | Move to .env | 🔧 OPEN |

**Summary:** N findings — X critical, Y high, Z medium

#### Verification — {YYYY-MM-DD}
- Finding #1: ✅ FIXED — password moved to .env
-->

> ⚠️ **PHANTOM AUDIT:** The files referenced in this entry either do not exist on disk or were never persisted (verified 2026-03-15). Findings are not actionable until the files are re-implemented. See Retrospective Report 2026-03-15 for details.

### Audit — 2026-03-11 — RAG Playbook Infrastructure (Initial Full Audit)

**Scope:** Full audit — 6 files (3 library modules, 2 scripts, 1 CI workflow)

| # | Severity | Category | File | Line(s) | Finding | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 🟢 LOW | A03 Supply Chain | .github/workflows/build-knowledge-index.yml | 22-26 | GitHub Actions pinned to major version tags (`@v4`, `@v5`) rather than SHA digests. Tags can be force-moved, introducing a supply-chain risk if upstream is compromised. | Pin to full SHA: e.g. `actions/checkout@<sha>`. Or accept current risk for official actions. | ⏸️ N/A — file does not exist |
| 2 | 🟢 LOW | A02 Misconfiguration | .github/workflows/build-knowledge-index.yml | 37 | `git pull --rebase \|\| true` silently swallows rebase failures. A failed rebase could leave the working tree in a bad state before the push. | Replace with explicit error handling or remove `\|\| true` and let the job fail visibly on conflicts. | ⏸️ N/A — file does not exist |
| 3 | ℹ️ INFO | A05 Injection | src/utils/embedding_client.py | 96-99 | `Retry-After` header parsed as `float()` without upper-bound validation. A malicious or misconfigured upstream could return an extremely large value causing indefinite sleep. Risk is negligible since the API URL is hardcoded to `models.github.ai`. | Add a cap (e.g. `min(float(retry_after), 120)`). Optional — no real attack vector exists because the URL is not user-controllable. | ⏸️ N/A — file does not exist |
| 4 | ℹ️ INFO | — Best Practice | scripts/build-knowledge-index.py, scripts/query-knowledge-index.py | 8 | `sys.path.insert(0, ...)` modifies the Python import path at runtime. Standard for repo scripts but could mask shadowed stdlib modules if a malicious file is placed in the utils directory. | Acceptable for this use case. Consider a proper package install (`pip install -e .`) for production projects. | ⏸️ N/A — file does not exist |

**Summary:** 4 findings — 0 critical, 0 high, 0 medium, 2 low, 2 info

#### Positive Security Patterns Observed

- **Token handling (A04):** API token is passed explicitly as a parameter in library code (`embedding_client.py`), never read from env vars inside libraries. Only entry-point scripts read `GH_MODELS_TOKEN` from the environment. Token is never logged, printed, or included in error messages.
- **Atomic writes (A08):** `knowledge_index.py` uses `os.replace()` via `_atomic_write()` to prevent partial/corrupted index files.
- **Safe deserialization (A08):** Uses `json.load()` and `tomllib.loads()` — no unsafe deserialization (no `pickle`, no `yaml.load()`).
- **SSRF prevention:** API URL is a module-level constant (`https://models.github.ai/inference/embeddings`), not user-controllable.
- **CI secrets (A04):** Workflow uses `${{ secrets.GH_MODELS_TOKEN }}` as an env var (not a CLI argument), keeping it out of process listings.
- **Minimal permissions:** Workflow requests only `contents: write` — the minimum needed for committing the index.
- **`.env` in `.gitignore`:** Confirmed — `.env` and `.env.*` are excluded from version control.
- **No shell injection:** No `os.system()`, `subprocess`, or `exec()` calls anywhere in the codebase. No `${{ github.event.* }}` expressions in workflow `run:` blocks.
- **Content hashing:** Uses SHA-256 for integrity checking — appropriate algorithm choice.
- **Input validation:** Playbook parser validates all required frontmatter fields, types, and category values before processing.
