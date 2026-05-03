# Research Brief: Aider and Plandex — Architecture, Agent Patterns, and Quality Mechanisms

**Date:** 2026-05-03
**Requested by:** Orchestrator (ad-hoc investigation)
**Sources:** github.com/Aider-AI/aider, aider.chat/docs/, github.com/plandex-ai/plandex, docs.plandex.ai/

---

## §0 — Executive Summary

Both tools are open-source AI coding assistants that solve the same core problem (providing LLM-driven edits to existing codebases) using radically different design philosophies.

| Dimension | Aider | Plandex |
|---|---|---|
| Language | Python | Go |
| Stars | ~44k | ~15k |
| Latest release | v0.86.0 | cli/v2.2.1 |
| Context strategy | Repo-map (graph-ranked AST) | Project map (tree-sitter) + smart sliding window |
| Change delivery | Edits files directly; auto-commits | Sandbox until `apply`; version-controlled diffs |
| Planning/implementation split | Architect/Editor mode (two models per request) | Ask/implement flow; multi-step plans |
| Multi-model | Main model + editor model (per request) | Model packs; mix providers per plan |
| Lint/test integration | Auto-lint + auto-test with auto-fix | `plandex debug <cmd>` with auto-retry + rollback |
| Watch/background | `--watch-files` with AI comments | Background tasks (v2) |
| Cloud status | N/A (CLI tool, no cloud) | Plandex Cloud **wound down 10/3/2025**; self-hosted only |

---

## §1 — Aider

### 1.1 Repo Map (cross-file awareness)

**How it works:**

1. **Tree-sitter AST extraction** — for every file in the git repo, Aider uses `tree-sitter` (via `py-tree-sitter-languages`) to parse the source into an Abstract Syntax Tree. From the AST, it extracts all symbol *definitions* (functions, classes, variables, types) AND all *references* to those symbols from other files.

2. **Graph construction** — a directed graph is built where each source file is a node. Edges connect files that have dependency relationships (i.e., file A references a symbol defined in file B → edge A→B).

3. **Graph ranking** — a PageRank-style algorithm runs on this dependency graph to score each symbol by how frequently it is referenced. The most-referenced symbols across the codebase get the highest scores.

4. **Budget-aware trimming** — the map is trimmed to fit a configurable token budget (`--map-tokens`, default: **1024 tokens**). Only the top-ranked symbols survive. The budget expands automatically when no files are in the active chat (Aider needs maximum codebase awareness).

5. **What's in the map** — for each surviving symbol, the map includes the critical lines of the definition (function signature, class header, method signatures) but **not** the full implementation body. Example:

   ```
   aider/coders/base_coder.py:
   ⋮...
   │class Coder:
   │    abs_fnames = None
   ⋮...
   │    @classmethod
   │    def create(self, main_model, edit_format, io, ...):
   ⋮...
   │    def run(self, with_message=None):
   ⋮...
   ```

6. **LLM-driven expansion** — if the LLM needs more detail on a symbol, it can request the full file from the map, and Aider adds it to the chat context. The map is the navigation layer; full files are the deep-dive layer.

**Key property:** The repo map is always sent with every request, regardless of which files are in the chat. It gives the LLM global awareness of the codebase structure without requiring all files to be in context.

**Language support:** 30+ languages (Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, PHP, etc.) via `py-tree-sitter-languages`.

**What replaced:** An older `ctags`-based map, which required manual installation of `universal-ctags` and produced less rich output.

---

### 1.2 Architect Mode (planning vs. implementation)

**The fundamental insight:** Some models (especially reasoning models like `o1`, `o3`) excel at *thinking through* a problem but produce poorly-formatted structured output. Other models are strong at *executing* structured file-edit instructions but weaker at deep reasoning. Architect mode separates these concerns.

**Two-request flow (per user message):**

```
User message
     │
     ▼
┌────────────┐   Describes solution   ┌────────────┐
│ Architect  │ ──────────────────────▶│  Editor    │
│ (main model│                        │  model     │
│ --model)   │  No format constraint  │            │
└────────────┘                        └─────┬──────┘
                                            │ Structured file edit instructions
                                            ▼
                                    Local source files
```

- **Architect** receives the user's request + repo map + any added files. It is free to describe the solution in prose, pseudocode, or any form it prefers. **No edit format constraints** are imposed.
- **Editor** receives the architect's proposal and must translate it into one of Aider's structured edit formats (`editor-diff` or `editor-whole`). It focuses entirely on formatting — not on solving the problem again.

**Configuration:**
```bash
aider --architect                    # enables architect mode; auto-selects editor model
aider --architect --editor-model sonnet  # custom editor
aider --editor-edit-format editor-diff  # force diff format for editor
```

**Benchmark impact (aider's code editing benchmark):**

| Architect | Editor | Format | Score |
|---|---|---|---|
| o1-preview | o1-mini | whole | **85.0%** (SOTA) |
| o1-preview | deepseek | whole | 85.0% |
| o1-preview | claude-3.5-sonnet | diff | 82.7% |
| claude-3.5-sonnet | claude-3.5-sonnet | diff | 80.5% |
| claude-3.5-sonnet | Baseline (solo) | diff | 77.4% |
| gpt-4o | gpt-4o | diff | 75.2% |
| gpt-4o | Baseline (solo) | diff | 71.4% |

**Key observation:** Using the *same* model as both architect and editor still improves scores vs. solo mode — two passes is better than one even with identical models.

**Fluent alternative (single model):** The `ask`/`code` workflow. Use `/ask` to reason through a plan, then say "go ahead" in `/code` mode. Less structured than architect mode but requires only one model.

**Chat modes:**
- `code` — default; edits files directly
- `ask` — discussion only; never edits
- `architect` — two-model split as described above
- `help` — answers questions about Aider itself

---

### 1.3 Multi-Model Setups

```bash
# Main model (also acts as Architect in architect mode)
aider --model claude-sonnet-4-5

# Editor model (architect mode only)
aider --architect --editor-model gpt-4o

# Switch model mid-session
/model gpt-4o

# Same model for both roles (still benefits from two passes)
aider --sonnet --architect
```

**Supported providers:** Anthropic, OpenAI, Google Gemini, DeepSeek, OpenRouter, Ollama (local), and essentially any provider via LiteLLM (which Aider uses under the hood).

**Practical multi-model pairings:**
- Reasoning model as architect + fast model as editor (e.g., o1 + Sonnet) — best quality, higher cost
- Same strong model as both (e.g., Sonnet + Sonnet) — good quality, moderate cost
- Budget pair (e.g., GPT-4o-mini + GPT-4o-mini) — acceptable for simple tasks

**No agent-to-agent communication:** Aider is a single-process tool. "Multi-model" means sequentially calling two models per turn, not parallel agents.

---

### 1.4 Lint and Test Integration (auto-fix loop)

**Linting:**
- Built-in linters for popular languages; auto-lints every edited file by default
- `--lint-cmd <cmd>` — plug in any linter (e.g., `eslint`, `ruff`, `golangci-lint`)
- `--no-auto-lint` — disable
- Per-language: `--lint "python: ruff check" --lint "go: golangci-lint run"`
- If linter returns non-zero → Aider automatically requests a fix from the LLM

**Testing:**
- `--test-cmd <cmd>` — auto-run tests after each AI edit
- `--auto-test` — enable automatic testing
- `/test <cmd>` — run tests manually from chat
- If tests fail → Aider tries to fix the failures

**Auto-fix loop:**
```
AI edits file
     │
     ▼
Run linter/tests
     │
  Pass? ──Yes──▶ Done ✅
     │
    No
     │
     ▼
LLM analyzes error output
     │
     ▼
LLM applies fix
     │
     ▼
Run linter/tests again...  (loops)
```

**Manual equivalent:** `/run python myscript.py` — run any command and paste output to LLM for analysis.

**Compiled languages:** Use `--lint-cmd` to trigger per-file compilation checks; use `--test-cmd` to trigger full project builds.

---

### 1.5 Context Management Across Long Sessions

**Core challenge:** LLM context windows fill up; relevant files change as work progresses.

**Mechanisms:**

| Mechanism | What it does |
|---|---|
| Repo map | Always-on global codebase index (fits in ~1k tokens) |
| `/add <file>` | Bring a file into the active chat context |
| `/drop <file>` | Remove a file from context |
| `/clear` | Discard all chat history; keep repo map + added files |
| `/reset` | Clear history AND remove all added files |
| `/tokens` | Show current token usage breakdown |
| `CONVENTIONS.md` | Read-only file loaded once, cached; survives `/clear` |
| `--read <file>` | Load any file as read-only; ideal for docs/conventions |

**CONVENTIONS.md pattern:**
```yaml
# .aider.conf.yml — auto-load conventions on every session
read: CONVENTIONS.md
```
This is equivalent to the template's `docs/PLAYBOOK.md` — a persistent instruction file that shapes all LLM output. The `read:` config auto-includes it in every session without polluting the editable file list.

**Session continuity:** Aider auto-commits every change to git with a descriptive message. History is recoverable via `git log` and `git diff`. No native "resume session" — each new `aider` invocation is fresh, but git provides the persistent audit trail.

**Context window management strategy (from official tips):**
1. Add only files that *need to change* (not all relevant files — the repo map handles global awareness)
2. Drop files once their changes are complete
3. Use `/ask` for planning (low-token mode) before switching to `/code`
4. Use `/clear` when the model gets confused; it retains the files but drops the confusion

---

### 1.6 Watch Mode (continuous integration)

**`--watch-files` mode:**

Aider watches all repo files for AI trigger comments. This enables use from any IDE without switching to a terminal.

**Trigger syntax:**
```python
# Regular annotation (accumulates, waits for trigger)
# AI: Refactor this...

# Trigger: make changes
def factorial(n):  # Implement this. AI!

# Trigger: answer question
# What is the purpose of this method? AI?
```

**How it works:**
1. User adds `# AI: ...` comments in code using their IDE
2. When a comment ending with `AI!` or `AI?` is saved, Aider wakes up
3. Aider collects ALL `AI` comments across ALL files, presents them to the LLM with repo map context
4. Changes are made (or question answered); Aider strips the AI comments from the code

**Multi-file coordination:**
```python
# file1.py
# AI: Add logging here...

# file2.py
# AI: ... and also here
def something():  # trigger! AI!
```

**Integration with terminal chat:** The watch session and terminal chat share conversation history; you can start with AI comments and continue in the terminal for complex follow-up.

---

## §2 — Plandex

### 2.1 Persistent Plans Across Sessions

**A "plan" = conversation + context + pending changes**, all stored in a `.plandex/` directory in the project root. Analogous to a long-lived ChatGPT thread but with version control baked in.

**Plan components:**
- **Context:** all loaded files, directories, URLs, images, notes
- **Conversation:** full prompt/response history
- **Pending changes:** AI-generated file edits not yet applied

**Cross-session persistence:**
```bash
plandex new -n my-feature     # named plan
plandex                       # REPL opens existing current plan
plandex plans                 # list all plans
plandex cd my-feature         # switch to a plan
plandex archive my-feature    # archive without deleting
```

**Plan discovery:** Running `plandex plans` shows plans in the current directory AND nearby parent/child directories, helping navigate complex project structures.

**Every action is versioned** — adding context, sending a prompt, model responses, building changes, applying changes, changing models. All create a new entry in plan history. This is Plandex's primary differentiator: a full audit trail of everything the AI did.

---

### 2.2 The Sandbox Concept

**Core design principle:** AI changes do NOT touch project files until you explicitly approve. All changes accumulate in an internal, version-controlled sandbox.

```
User prompt
     │
     ▼
LLM generates proposed changes
     │
     ▼
Changes accumulated in sandbox ──▶ plandex diff (review)
(version-controlled)               plandex diff --ui (browser view)
     │
     ▼
plandex apply ──▶ Changes written to project files
     │
     ▼
Auto-execute _apply.sh (if enabled)
     │
     ▼
Auto-commit to git (if enabled)
```

**Sandbox contains:**
- File edits (accumulated as "pending changes")
- Shell commands in a special `_apply.sh` path (for installs, builds, server starts, etc.)

**Review options:**
- `plandex diff` — git-style diff
- `plandex diff --ui` — browser-based side-by-side or line-by-line diff viewer
- `plandex reject file1.ts` — reject specific files
- `plandex reject --all` — reject everything

**Applying:**
- `plandex apply` — apply and prompt before commands
- `plandex apply --full` — apply + auto-execute commands + auto-debug failures

**After apply:** Rollback is possible via `plandex rewind` (default v2 behavior: also reverts project files).

---

### 2.3 Version Control of AI-Generated Changes

**Plan-level version control** (separate from, but integrated with, git):

Everything creates a new plan version:
- Loading or removing context
- Each prompt sent
- Each model response
- Building proposed file changes
- Rejecting changes
- Applying changes
- Model or model-settings changes

**Commands:**
```bash
plandex log                    # view plan history
plandex rewind                 # interactive: pick a state to rewind to
plandex rewind 3               # rewind 3 steps
plandex rewind a7c8d66         # rewind to specific step hash
plandex convo                  # view full conversation text
```

**Branches:**
```bash
plandex checkout new-branch    # create new branch at current state
plandex branches               # list branches
plandex checkout main          # switch back

# Safe rewind pattern:
plandex checkout experimental  # create branch
plandex rewind 5               # rewind on branch (main retains history)
```

**Branch use cases:**
- Try different prompting strategies and compare
- Compare results with different model packs
- Compare different files in context
- Safe rewind without losing history

**Git integration:**
- `auto-commit` config: commits project files to git after `apply` (enabled by default in `plus`+ autonomy levels)
- `auto-revert-on-rewind`: when rewinding after an apply, also reverts project files (v2 default: on)

---

### 2.4 Multi-Agent / Multi-Model Capabilities

**Internal architecture (not directly user-configurable):**
Plandex uses multiple specialized model roles internally:
- **Planner** — creates multi-step plans, decides what needs to happen
- **Navigator** — determines which context to load per step
- **Executor/Builder** — generates actual file edits

**User-facing multi-model:**
- **Model packs** — pre-configured combinations of models for different roles and tradeoffs
- Mix providers: Anthropic, OpenAI, Google, open-source models
- Use OpenRouter.ai as a universal gateway for model access
- Claude Pro/Max subscription can be connected for Anthropic models

**Effective context window:** 2M tokens with default model pack (achieved through smart context loading — only loads what's needed per step, not everything at once).

**Model configuration:**
```bash
plandex set-model                    # interactive model selection
plandex set-model default sonnet     # set default model for all new plans
```

**Note:** The `plandex.ai/docs/models` and `docs/core-concepts/model-packs` pages returned 404 at time of research — detailed model pack documentation may have moved. The README confirms multi-provider mixing and curated model packs with capability/cost/speed tradeoffs.

---

### 2.5 Context Management

**Automatic context loading (v2 default — `semi` and `full` autonomy):**

1. **Project map** generated using tree-sitter (30+ languages supported)
2. Map is loaded into context along with the user's prompt
3. LLM uses map to **select relevant files** for the planning phase
4. **Smart context window management:** for multi-step plans, only files relevant to *each specific step* are loaded into context during implementation
5. Context auto-updates when files change outside Plandex

This creates an effective "sliding context window" — the full context is never all loaded at once, but each step has exactly what it needs.

**Autonomy matrix for context:**

| Feature | none | basic | plus | semi | full |
|---|:---:|:---:|:---:|:---:|:---:|
| auto-load-context | ❌ | ❌ | ❌ | ✅ | ✅ |
| smart-context | ❌ | ❌ | ✅ | ✅ | ✅ |
| auto-update-context | ❌ | ❌ | ✅ | ✅ | ✅ |

**Manual context loading:**
```bash
plandex load file.ts                      # single file
plandex load tests/**/*.ts                # glob pattern
plandex load lib -r                       # recursive directory
plandex load . --tree                     # directory layout only (names, no content)
plandex load . --map                      # tree-sitter project map
plandex load https://docs.example.com/    # URL content
plandex load ui-mockup.png                # image
plandex load -n 'use httpx not requests'  # sticky note (won't be summarized away)
npm test | plandex load                   # piped command output

# REPL shortcut
@component.ts   # load file
@lib            # load directory
```

**Sticky notes:** Load instructions as notes with `plandex load -n`. Unlike prompts, notes are NOT summarized during long conversations — they persist as permanent instructions throughout the plan.

**Respects:** `.gitignore`, `.plandexignore`. Force-load ignored files with `--force`.

---

### 2.6 Quality Gates and Review Mechanisms

**Layer 1 — Sandbox (primary gate):**
All changes accumulate in the sandbox. No files are touched until `plandex apply`. This is the foundational quality control: nothing lands in your project without an explicit human decision (unless you set `auto-apply`).

**Layer 2 — Diff review:**
```bash
plandex diff                    # git-diff format in terminal
plandex diff --ui               # browser UI with side-by-side view
plandex diff --ui --side-by-side
```

**Layer 3 — Automated debugging (`plandex debug`):**
```bash
plandex debug 'npm test'         # retry up to 5 times (default)
plandex debug 10 'pytest'        # retry up to 10 times
plandex debug 'go build'         # fix build errors
plandex debug 'npm run lint'     # fix lint errors
plandex debug 'tsc --noEmit'     # fix type errors
```

The debug loop:
1. Run command → check exit code
2. If fail → send output to LLM → generate fixes → tentatively apply to project files
3. Re-run command
4. If success → commit (if auto-commit enabled)
5. If fail → roll back → repeat (up to `auto-debug-tries`, default 5)

**Layer 4 — Syntax + logic validation:**
Plandex validates file edits for syntax and logic correctness. Multiple fallback layers when initial edits have problems. This is done before edits enter the sandbox.

**Layer 5 — Command execution safety:**
Commands accumulate in `_apply.sh` in the sandbox (not executed). User reviews + approves before execution. If execution fails → rollback available.

**Layer 6 — Browser debugging (Chrome integration):**
For browser applications: Chrome is launched automatically when the plan calls for a browser app. Console errors are caught and fed back to the LLM.

**Layer 7 — Autonomy levels:**
```bash
plandex set-auto none    # maximum control: nothing automatic
plandex set-auto basic   # auto-continue plans only
plandex set-auto plus    # smart context + auto-commit
plandex set-auto semi    # auto-load context (default for fresh v2 install)
plandex set-auto full    # full automation (apply, exec, debug, commit)
```

---

## §3 — Patterns Adoptable by This Template

### From Aider

| Pattern | Aider Mechanism | Template Analogue / Adoption |
|---|---|---|
| **Graph-ranked repo map** | `--map-tokens` + tree-sitter AST + PageRank | The Librarian Agent's `CODE_INVENTORY.md` serves this purpose, but manually. Could generate an AST-based index for freshness. |
| **Architect/Editor split** | `--architect` + `--editor-model` | Maps directly to the template's Architect → Worker split. The key insight: Architect should NOT be forced to produce code diffs — it should propose solutions in prose, and Worker converts to actual edits. |
| **CONVENTIONS.md as read-only context** | `--read CONVENTIONS.md` auto-loaded | Template already uses `docs/PLAYBOOK.md` similarly. Enhancement: mark PLAYBOOK as a `read`-mode context (never editable, always cached). |
| **Auto-lint + auto-test loop** | `--lint-cmd` + `--test-cmd` + `--auto-test` | Maps to the Worker's red-green loop. Extend: configure per-language linters in the Worker's context brief. |
| **Watch mode AI comments** | `--watch-files` + `# AI!` comments | Useful inspiration: annotate stubs with `# TODO: implement AI!` to trigger implementation in watch mode. |
| **`/ask` before `/code`** | `/ask` mode → planning → "go ahead" | This is exactly the template's Architect→Worker handoff. The value of explicit mode-switching (planning vs. implementing) is validated by Aider's benchmark data. |

### From Plandex

| Pattern | Plandex Mechanism | Template Analogue / Adoption |
|---|---|---|
| **Sandbox before apply** | Changes in pending diff until `apply` | Template's workers write to files directly. Consider: staging all AI-generated files in a review directory before Worker marks them final. |
| **Plan version control** | Every action creates a new version | Maps to the template's `.ai/plans/` + `.ai/todos/` + dispatch logs. Plandex's approach: version EVERYTHING in a plan (context, conversation, changes) — much richer than logs alone. |
| **Branches for AI exploration** | `plandex checkout` + multiple branches | Template could adopt: when the Innovator produces alternatives, create separate todo branches for each approach rather than embedding all as sub-items. |
| **`plandex debug` loop** | Debug command with rollback-on-failure | The Worker's red-green loop already does this conceptually. Add explicit rollback: if Worker fails N times, revert the file to its pre-Worker state before retrying. |
| **Autonomy levels** | none/basic/plus/semi/full spectrum | Template has BUDGET_MODE vs. DEEP_MODE binary. Plandex's granular levels are more practical: let users choose how much automation they want per session. |
| **Sticky notes** | `plandex load -n 'instruction'` | Addresses a real gap: in long conversations, early instructions get summarized away. The template's conventions/playbook in the context brief should be marked as "sticky" — never compress or summarize. |
| **Smart context per step** | Only loads files relevant to each implementation step | Template's Librarian already does this conceptually. Explicit "smart context" enforcement: each Worker spawn gets only its function's relevant context, not the entire codebase brief. |
| **Diff UI review** | `plandex diff --ui` — browser side-by-side | Before Gate 2 (Consistency Check after Worker), present a diff summary to the user rather than just running Consistency Check silently. |

---

## §4 — Dependency Versions (verified)

| Package | Registry | Latest Stable Version | Verified URL |
|---|---|---|---|
| `aider-chat` | PyPI | **0.86.0** | https://pypi.org/project/aider-chat/ (inferred from GitHub v0.86.0 release tag, 2025-08-09) |
| `plandex` (CLI) | GitHub releases | **cli/v2.2.1** | https://github.com/plandex-ai/plandex/releases (2025-07-16) |

⚠️ PyPI registry was not directly fetched for `aider-chat` — version inferred from GitHub release tag. Recommend verifying at https://pypi.org/project/aider-chat/ before pinning.

---

## §5 — References

- https://github.com/Aider-AI/aider
- https://aider.chat/docs/repomap.html
- https://aider.chat/docs/usage/modes.html
- https://aider.chat/docs/usage/lint-test.html
- https://aider.chat/docs/usage/watch.html
- https://aider.chat/docs/usage/conventions.html
- https://aider.chat/docs/usage/tips.html
- https://aider.chat/2024/09/26/architect.html
- https://aider.chat/2023/10/22/repomap.html
- https://github.com/plandex-ai/plandex
- https://docs.plandex.ai/core-concepts/plans
- https://docs.plandex.ai/core-concepts/context-management
- https://docs.plandex.ai/core-concepts/reviewing-changes
- https://docs.plandex.ai/core-concepts/execution-and-debugging
- https://docs.plandex.ai/core-concepts/version-control
- https://docs.plandex.ai/core-concepts/branches
- https://docs.plandex.ai/core-concepts/autonomy
- https://docs.plandex.ai/core-concepts/configuration
