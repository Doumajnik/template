# Research Brief: AutoGPT, OpenHands, and PR-Agent

**Date:** 2026-05-04
**Requested by:** Orchestrator (pre-architecture research)
**Scope:** Architecture patterns, agent/workflow design, quality mechanisms, and maintenance/self-improvement patterns

---

## 1. AutoGPT (Significant-Gravitas/AutoGPT)

### Architecture Pattern: Visual Block Graph

AutoGPT's platform architecture is built around a **low-code visual graph** in which every unit of work is a "Block" — a typed, self-contained function with structured input and output schemas. Users wire blocks together in a directed graph to build autonomous agents.

```
Graph (agent workflow)
  └── Node (block instance)
        ├── Input  (BlockSchemaInput — typed Pydantic model)
        └── Output (BlockSchemaOutput — typed Pydantic model, multiple output pins)
```

**Backend stack:** FastAPI + Prisma (PostgreSQL) + Redis + RabbitMQ  
**Frontend stack:** Next.js + TypeScript  
**Execution infrastructure:** Docker-compose services; executor can be scaled horizontally (`docker compose up --scale executor=3`)

### Block Taxonomy

The `backend/blocks/` directory exposes ~60+ block files grouped by domain:

| Category | Examples |
| --- | --- |
| **AI / LLM** | `llm.py`, `ai_condition.py`, `ai_image_generator_block.py`, `text_to_speech_block.py` |
| **Code execution** | `code_executor.py` (E2B sandbox), `claude_code.py`, `codex.py` |
| **Integrations** | GitHub, Discord, Notion, Airtable, HubSpot, Linear, Jira, Slack, Telegram, Twitter |
| **Control flow** | `branching.py`, `iteration.py`, `sampling.py` |
| **Data** | `data_manipulation.py`, `sql_query_block.py`, `persistence.py`, `mem0.py` |
| **Special** | `human_in_the_loop.py`, `orchestrator.py`, `agent.py`, `autopilot.py` |

Each block declares:
- A stable UUID `id`
- `block_type` enum (`STANDARD`, `HUMAN_IN_THE_LOOP`, `AGENT`)
- `categories` set for UI filtering
- `test_input` / `test_output` / `test_mock` for built-in unit testing

### Multi-Agent Orchestration Pattern

Three dedicated blocks enable multi-agent composition:

1. **`agent.py`** — Embeds a saved agent graph as a block inside another graph. The host graph can pass inputs and receive outputs, enabling **recursive nesting**: an agent can call another agent.
2. **`orchestrator.py`** — Coordinates parallel or sequential spawning of sub-agents with shared context.
3. **`autopilot.py`** — Fully autonomous execution mode that bypasses HITL gates.

The **executor** (`backend/executor/manager.py`) is responsible for:
- Pulling graph execution jobs from RabbitMQ
- Resolving block dependencies and scheduling in topological order
- Tracking execution cost per block call (`cost_tracking.py`, `billing.py`)
- Redis cluster locking for distributed safety
- Scheduler for cron-style triggered executions

### Human-in-the-Loop (HITL) — First-Class Block

`HumanInTheLoopBlock` is a native block type that **pauses the graph** and creates a `ReviewStatus.PENDING` entry. Execution resumes only when a human approves or rejects via the UI.

- **Dual output pins:** `approved_data` and `rejected_data` — downstream blocks simply connect to the relevant pin; they never inspect a status string.
- **Editable flag:** the reviewer can modify the data before approving.
- **Auto-approve mode:** a "safe mode disabled" path bypasses HITL for fully automated runs.

This is a clean architectural pattern: safety gating expressed as graph topology, not as runtime flags.

### Quality Mechanisms

| Mechanism | Details |
| --- | --- |
| **Testing** | Integration tests (Vitest + RTL + MSW, ~90% coverage), Playwright E2E for critical flows, Storybook for UI components |
| **CI** | Codecov, conventional commits, pre-commit hooks (gitleaks secret scanning) |
| **Cost auditing** | `billing_reconciliation_test.py`, `block_usage_cost_test.py` — dynamic cost tracking, automated audits prevent "cost leaks" |
| **Activity scoring** | `activity_status_generator.py` computes a **correctness score** for each graph execution — a live quality signal without human review |

### Self-Improvement and Maintenance Patterns

- **AI-readable instructions:** Both `AGENTS.md` and `CLAUDE.md` at repo root and in `autogpt_platform/` are explicitly formatted for AI coding agents (Claude, Codex). The project maintains parallel instruction files so agents can contribute to the codebase.
- **Dogfooding:** AutoGPT agents are used to develop AutoGPT — the `claude` GitHub user is listed as an active contributor.
- **Consistent commit scopes:** Conventional commit types `feat/fix/refactor/ci/dx` with mandatory scopes (`backend`, `frontend`, `blocks`, `executor`) make automated changelog generation reliable.
- **Model cost config:** A dedicated audit test (`fix(block_cost_config): audit + correct stale LLM/block rates`) shows a practice of regularly verifying and updating LLM cost configurations.

---

## 2. OpenHands (All-Hands-AI/OpenHands)

### Architecture Pattern: Layered SDK + App Server

OpenHands is structured in **three clean layers**:

```
Frontend (React SPA)
  └── App Server (FastAPI — openhands/app_server/)
        ├── Sandbox management       (Docker / Remote / Kubernetes / Local)
        ├── Conversation lifecycle   (create → run → pause → archive)
        ├── Event streaming          (WebSocket)
        ├── Integrations             (GitHub, GitLab, Jira, Linear, Slack)
        └── SDK (Python library — software-agent-sdk repo)
              ├── Agent core
              ├── Tool definitions
              └── LLM abstraction (via LiteLLM)
```

The SDK is intentionally **model-agnostic**: it runs with any LLM by routing through LiteLLM.

### Agent Sandboxing Approach

Each conversation runs inside a **fully isolated sandbox**. Multiple backends are supported through a common `SandboxService` interface:

| Backend | Use case |
| --- | --- |
| `DockerSandboxService` | Default local/self-hosted |
| `RemoteSandboxService` | Cloud-hosted (OpenHands Cloud) |
| `ProcessSandboxService` | Local process (lightweight, no Docker) |
| Kubernetes (via `kind/`) | Enterprise large-scale deployments |

**Security design principles:**
- Session API key (`X-Session-API-Key`) is **invalidated on pause** — no stale keys can resume a paused sandbox.
- Secrets flow **server → sandbox only**, never through the SDK client (no raw secrets in API responses by default; `expose_secrets=true` requires both Bearer + session API key).
- Sandbox scoped secrets endpoints: `/sandboxes/{id}/settings/secrets/{name}` — secret values accessible only from within the running sandbox.
- `sandbox_status === "MISSING"` renders conversations as read-only archived state.

### Tool Restriction Pattern

OpenHands enforces tool restrictions via:
1. Pre-commit hooks that MUST pass before pushing (mypy type checking + Ruff formatting).
2. An `AGENTS.md` file that specifies pre-commit hook installation as a **mandatory first step** before any code changes.
3. The `tool-guard.py` hook pattern (mirrored in this template) — a pre-tool-use hook that blocks specific tool calls.

The instruction files use **truthy value convention** for feature flags: both `'true'` and `'1'` are accepted (important for Helm chart compatibility — pure `== 'true'` checks silently break when values are `'1'`).

### Multi-Model Support

OpenHands maintains explicit **capability arrays** per model:

```python
FUNCTION_CALLING_SUPPORTED_MODELS    # models with structured function calling
REASONING_EFFORT_SUPPORTED_MODELS    # o1, o3, etc. with reasoning budget params
CACHE_PROMPT_SUPPORTED_MODELS        # models supporting prompt caching
MODELS_WITHOUT_STOP_WORDS            # models that don't support stop word params
```

Models are organized into provider groups (`VERIFIED_OPENAI_MODELS`, `VERIFIED_ANTHROPIC_MODELS`, `VERIFIED_MISTRAL_MODELS`, `VERIFIED_OPENHANDS_MODELS`). The CLI and frontend both derive from the same arrays — a single source of truth for model discovery.

### Microagents Pattern

**Microagents** are Markdown files injected into the agent's context window to provide domain-specific knowledge:

```yaml
---
triggers:
  - "docker"
  - "kubernetes"
---
# Docker Specialist Microagent
When the user mentions Docker or Kubernetes, apply these specialized instructions...
```

- **Without frontmatter** → always loaded (permanent system prompt additions)
- **With `triggers`** → loaded only when user message matches keywords

Two scopes:
- **Public microagents** (`microagents/` in the OpenHands repo) — shared across all users
- **Repository microagents** (`.openhands/microagents/` in any repo) — project-specific knowledge injected per workspace

This is a clean pattern for **contextual knowledge injection without permanent prompt bloat**.

### Quality Validation Mechanisms

| Mechanism | Details |
| --- | --- |
| **Mandatory pre-commit** | `make install-pre-commit-hooks` is the first step; hooks MUST pass before any push |
| **Type safety** | Mypy, with `PYTHONPATH=".:$PYTHONPATH"` for correct import resolution |
| **Ruff formatting** | Consistent code style, run `--show-diff-on-failure` to match CI exactly |
| **90%+ coverage target** | Enterprise modules aim for 90%+ coverage on critical business logic |
| **In-memory DB for unit tests** | `sqlite:///:memory:` prevents unit tests from depending on real PostgreSQL |
| **PR artifacts** (`.pr/`) | Temporary design docs committed per-PR, auto-deleted when PR is approved (via GitHub Actions workflow) |
| **Benchmark tracking** | SWE-bench, SWT-bench, multi-SWE-bench — quantitative agent performance tracking |

### Maintenance / Self-Improvement Patterns

- **The agent contributes:** `openhands-agent` (GitHub user) is an active contributor with real commits — the system genuinely uses itself.
- **Automatic context compression:** SDK feature for handling tasks that exceed context windows without manual chunking.
- **Theory-of-Mind module:** Separate repo (`OpenHands/ToM-SWE`) for agent-to-agent communication reasoning.
- **Enterprise extension pattern:** Core is MIT-licensed; enterprise features extend via dynamic imports — open core with commercial layer, same codebase.
- **Lockfile preservation:** Explicit instructions to use the EXACT same tool version that generated the lockfile (to avoid noisy diffs from tool version migrations).

---

## 3. PR-Agent (Codium-ai/pr-agent)

### Architecture Pattern: Command-Based Tool Orchestration

PR-Agent uses a **command dispatcher pattern**:

```
pr_agent/agent/pr_agent.py    ← dispatches commands
  └── pr_agent/tools/         ← individual capabilities
        ├── review.py
        ├── describe.py
        ├── improve.py (code suggestions)
        ├── add_docs.py
        ├── test.py
        └── update_changelog.py
pr_agent/git_providers/        ← platform adapters (GitHub, GitLab, Bitbucket, Azure DevOps, Gitea)
pr_agent/settings/             ← Dynaconf configuration
```

Each command is an independent tool that can be triggered manually (comment on PR) or automatically (GitHub Action, webhook, push trigger).

### Org-Level Centralized Configuration

PR-Agent uses a **three-tier configuration hierarchy** via Dynaconf:

```
Tier 1 (defaults):   pr_agent/settings/configuration.toml
Tier 2 (repo-level): .pr_agent.toml in repo root
Tier 3 (org-level):  Wiki-based settings (use_wiki_settings_file=true)
```

Key org-level patterns:
- `ignore_pr_authors`, `ignore_pr_labels`, `ignore_pr_target_branches`, `ignore_repositories` — regex-based ignore rules
- `best_practices.md` in repo root — feeds the AI model organization-specific coding standards
- Per-provider command lists: `[github_app].pr_commands`, `[gitlab].pr_commands`, `[bitbucket_app].pr_commands` — different defaults per platform
- `push_commands` — separate commands triggered on push (distinct from PR-open commands)
- `response_language` — localize AI output to any locale (e.g., `"zh-CN"`)
- `reasoning_effort` — control model compute budget: `"low"`, `"medium"`, `"high"`

The `.pr_agent.toml` in PR-Agent's own repo is committed to the repository — **the tool reviews itself using its own configuration**.

### Review Automation Patterns

The `/review` tool produces structured sections, each individually toggleable:

| Section | Config flag | Default |
| --- | --- | --- |
| Tests review | `require_tests_review` | `true` |
| Security review | `require_security_review` | `true` |
| Effort estimate | `require_estimate_effort_to_review` | `true` |
| Score | `require_score_review` | `false` |
| Ticket compliance | `require_ticket_analysis_review` | `true` |
| Can be split | `require_can_be_split_review` | `false` |
| TODO scan | `require_todo_scan` | `false` |

**Auto-labels** are applied directly to the PR:
- `possible security issue` — triggers CI blocks
- `Review effort [x/5]` — visibility into review complexity
- `Fully compliant` / `Partially compliant` / `Not compliant` — ticket compliance

**Label-based merge blocking:** Standard CI/CD actions check for `possible security issue` label and block merge — AI review as a mandatory gate.

### Self-Reflection Mechanism (Two-Pass Review)

The `/improve` (code suggestions) tool uses an explicit **two-pass self-reflection** pattern:

```
Pass 1: Generate N suggestions (scored by generation order)
Pass 2: Present all N suggestions back to the model simultaneously
        → Model scores each 0-10 with rationale
        → Re-rank by score
        → Filter out score=0 (incorrect/irrelevant)
        → Apply user threshold (suggestions_score_threshold)
```

Key insight: **presenting all suggestions simultaneously** provides cross-suggestion context that per-suggestion evaluation lacks. The model can compare suggestions against each other, identify contradictions, and make more calibrated importance judgments.

The self-reflection output is hierarchically presented:
```
Category (e.g., "Security")
  └── One-liner summary        ← always visible (5-10 sec review)
        └── Full description   ← expandable
              └── Before/after diff
```

**Self-review checkbox:** `demand_code_suggestions_self_review=true` adds a PR author checkbox. Checking it can optionally auto-approve the PR (`approve_pr_on_self_review=true`) — enforcing that authors acknowledge AI feedback before merge.

### Code Suggestion Mechanisms

- **Chunked processing:** Large PRs split into chunks of `max_model_tokens` (default 32k). Each chunk independently generates `num_code_suggestions_per_chunk` suggestions (default 3). Scales linearly with PR size.
- **Parallel chunk calls:** `parallel_calls=true` — chunks processed concurrently.
- **Dual publishing mode:** Table view (low noise, default) + committable inline comments for high-score suggestions (`dual_publishing_score_threshold`).
- **Extended mode** (`/improve --extended`): multiple parallel AI calls on the same PR with a final clip factor to deduplicate.
- **Custom prompt:** `/custom_prompt` tool with `self_reflect_on_custom_suggestions=true` — applies self-reflection to user-defined review criteria.
- **Best practices file:** `best_practices.md` at repo root feeds organization guidelines into every suggestion call — persistent, versionable coding standards as AI context.

### Dynamic Context Strategy

PR-Agent uses **asymmetric, structure-aware context expansion**:

- **Asymmetric:** More context before a change (preceding lines) than after (following lines) — recognizing that setup/signature matters more than teardown.
- **Dynamic:** Context expands to the enclosing function or class boundary, not a fixed number of lines (`max_extra_lines_before_dynamic_context=8`).
- **Token-aware compression** for large PRs:
  1. Language prioritization (code files before docs)
  2. Additions-first (deletion-only hunks are batched separately)
  3. tiktoken-based token counting (accurate, not estimated)
  4. Adaptive fitting: fill to token budget, then degrade gracefully to `other modified files` list

### Multi-Stage Metadata (Chain-of-Thought Without Extra API Calls)

PR-Agent chains commands to build richer context across tools:

1. `/describe` runs first → produces PR type, bullet summary, per-file change walkthrough
2. That AI-generated output is stored as PR metadata
3. Subsequent `/review` and `/improve` calls receive the `/describe` output as context — **no additional API calls needed**

This is an elegant chain-of-thought pattern: intermediate AI outputs become structured context for downstream AI calls.

### Continuous Maintenance Patterns

- **Self-dogfooding:** `.pr_agent.toml` committed in the PR-Agent repo — every PR is auto-reviewed by the tool.
- **Health test:** `tests/health_test/main.py` exercises `/describe`, `/review`, `/improve` against expected artifacts — a canary for prompt regressions.
- **Release drafter:** Automated changelog generation from conventional commit messages.
- **CodeQL:** Static security analysis via GitHub Actions workflow.
- **Ticket context extraction from branch names:** `extract_issue_from_branch=true` — automatically links PRs to issues via branch naming convention (e.g., `feature/123-auth-google` → issue #123).

---

## Cross-Cutting Patterns and Inspiration for This Template

### Pattern 1: Two-Pass Self-Reflection (from PR-Agent)

**What it is:** Generate → score → re-rank → filter.  
**Template application:** Apply to Reviewer and Code Quality agents. After generating findings, present all findings back to the model simultaneously for scoring 0-10, re-ranking, and removing false positives. This is better than asking the model to self-rank during generation.

### Pattern 2: Block-as-Agent with Typed I/O (from AutoGPT)

**What it is:** Every unit of work has a declared, typed schema with named output pins. Different outputs route to different downstream agents.  
**Template application:** Agent outputs should be structured (not free-text). Define a standard `AgentOutput` schema with named sections (findings, severity, recommendations). Downstream agents consume named fields, not raw text.

### Pattern 3: HITL as First-Class Gate (from AutoGPT)

**What it is:** Human-in-the-Loop is a proper block type, not a manual step. It pauses execution, presents data, and routes based on approval/rejection to different downstream paths.  
**Template application:** The User Approval gate in the pipeline could be formalized: "approved_path" → Scaffolder, "rejected_path" → Prompt Engineer with feedback. Currently this is described in prose; making it a typed gate with explicit routing would be cleaner.

### Pattern 4: Microagents for Domain Expertise (from OpenHands)

**What it is:** Small Markdown files with `triggers` frontmatter that inject domain-specific knowledge only when relevant keywords appear.  
**Template application:** The playbook files in `docs/playbooks/` could have a trigger frontmatter. The Librarian could load only triggered playbooks into agent briefs, reducing context window usage and improving relevance.

### Pattern 5: Multi-Stage Metadata Reuse (from PR-Agent)

**What it is:** Earlier agent outputs become context for later agents — no extra API calls, stored as metadata.  
**Template application:** The Planning Agent's output (function signatures, module boundaries) should be explicitly passed as pre-built context to the Test Writer and Worker, not re-fetched via the Librarian each time. The Librarian's brief for downstream agents should include a structured summary from the Planning Agent.

### Pattern 6: Capability Arrays per Model (from OpenHands)

**What it is:** Explicit lists of which models support which features (`FUNCTION_CALLING_SUPPORTED_MODELS`, `REASONING_EFFORT_SUPPORTED_MODELS`).  
**Template application:** The Super Greedy Pipeline's "Model Discovery" step (step 0) should maintain explicit capability arrays. When assigning models to tiers, document which features each model supports — this prevents sending stop-word parameters to models that don't support them.

### Pattern 7: Asymmetric Dynamic Context (from PR-Agent)

**What it is:** Provide more context before a change than after; expand to structural boundaries (function/class), not fixed lines.  
**Template application:** When the Worker reads a file to implement a function, it should expand context to the enclosing function/class, not just N lines. The Reviewer should have the full function context for changed functions, not just the diff hunk.

### Pattern 8: Activity Scoring / Correctness Signal (from AutoGPT)

**What it is:** `activity_status_generator.py` computes a correctness score for each graph execution — a live quality metric without requiring human review.  
**Template application:** The Retrospective Agent should emit a session quality score (0-10) based on: checklist completion rate, findings per gate, agent retry count, and circuit breaker triggers. This becomes the "correctness score" for the session, stored in `.ai/sessions/` for trend analysis.

### Pattern 9: Tool Self-Dogfooding (from PR-Agent)

**What it is:** PR-Agent runs itself on its own PRs via `.pr_agent.toml` committed to the repo.  
**Template application:** This template's own `.github/copilot-instructions.md` and `AGENTS.md` could be reviewed by the pipeline itself on every PR. Add a self-review step where the Reviewer agent reads the agent instruction files and checks for internal consistency, dangling references, and rule contradictions.

### Pattern 10: Lockfile Version Pinning (from OpenHands)

**What it is:** Explicit instructions to extract the tool version from the lockfile header and reinstall that exact version before regenerating — prevents noisy diffs from tool upgrades.  
**Template application:** Add to the Research Agent's dependency verification step: after confirming the latest stable version from the registry, also check if the lockfile already pins a version, and prefer the lockfile version unless explicitly upgrading.

---

## References

- AutoGPT repo: https://github.com/Significant-Gravitas/AutoGPT
- AutoGPT AGENTS.md: https://raw.githubusercontent.com/Significant-Gravitas/AutoGPT/master/AGENTS.md
- AutoGPT blocks directory: https://github.com/Significant-Gravitas/AutoGPT/tree/master/autogpt_platform/backend/backend/blocks
- AutoGPT executor: https://github.com/Significant-Gravitas/AutoGPT/tree/master/autogpt_platform/backend/backend/executor
- AutoGPT HITL block: https://github.com/Significant-Gravitas/AutoGPT/blob/master/autogpt_platform/backend/backend/blocks/human_in_the_loop.py
- OpenHands repo: https://github.com/All-Hands-AI/OpenHands
- OpenHands AGENTS.md: https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/AGENTS.md
- OpenHands sandbox: https://github.com/All-Hands-AI/OpenHands/tree/main/openhands/app_server/sandbox
- OpenHands SDK docs: https://docs.openhands.dev/sdk
- PR-Agent repo: https://github.com/The-PR-Agent/pr-agent
- PR-Agent AGENTS.md: https://raw.githubusercontent.com/Codium-ai/pr-agent/main/AGENTS.md
- PR-Agent configuration.toml: https://github.com/Codium-ai/pr-agent/blob/main/pr_agent/settings/configuration.toml
- PR-Agent self-reflection docs: https://docs.pr-agent.ai/core-abilities/self_reflection/
- PR-Agent dynamic context docs: https://docs.pr-agent.ai/core-abilities/dynamic_context/
- PR-Agent compression strategy: https://docs.pr-agent.ai/core-abilities/compression_strategy/
- PR-Agent metadata docs: https://docs.pr-agent.ai/core-abilities/metadata/
- PR-Agent improve tool: https://docs.pr-agent.ai/tools/improve/
- PR-Agent review tool: https://docs.pr-agent.ai/tools/review/
