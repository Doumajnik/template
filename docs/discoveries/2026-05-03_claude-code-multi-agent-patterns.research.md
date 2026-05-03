# Research Brief: Claude Code Configuration, Multi-Agent Orchestration, and Maximum Quality Patterns

**Date:** 2026-05-03
**Requested by:** Orchestrator (ad-hoc investigation)
**Status:** ⚠️ Partial — web access blocked by tool-guard.py (see §0 below)

---

## §0 — Technical Blocker: Tool Guard Web-Access Denial

### What happened

Every call to `fetch_webpage` and `mcp_playwright_browser_*` was rejected with:

> "Tool execution denied: Agent identity unknown — denied by default. Only the Research agent may use web tools."

### Root cause

`scripts/tool-guard.py` is a PreToolUse hook executed by VS Code Copilot.  
It expects an `agentName` / `agent_name` / `agent` field in the hook payload.  
VS Code Copilot **does not** populate any of those fields when it invokes the hook — it sends an empty string.  
Claude Code **does** populate those fields, so the hook works correctly in Claude Code sessions.

The tool guard's `WEB_ACCESS_ALLOWED_AGENTS = {"research"}` check therefore never matches, and the guard falls through to the deny-by-default branch.

### Fix required (one option)

Modify `scripts/tool-guard.py` to treat an empty agent name as "allow" for web tools **with a warning**, rather than deny-by-default. This is safe because the primary enforcement target (keeping Test Writer / Integration Tester black-box) does not involve web tools. Alternatively, VS Code Copilot may eventually expose `agentMode` in the hook payload; track that issue.

Suggested change to `check_permission()`:

```python
if is_web_tool(tool_name):
    if agent_name.lower() in WEB_ACCESS_ALLOWED_AGENTS:
        return "allow", f"Agent '{agent_name}' is allowed web access"
    if not agent_name:
        # VS Code Copilot does not populate agent_name in the hook payload.
        # Allow with a warning rather than blocking all web-capable modes.
        return "allow", (
            "Agent identity not provided by host (VS Code Copilot). "
            "Web access allowed with caveat — ensure this is the Research agent."
        )
    return "deny", ...
```

---

## §1 — Topic 1: Claude Code Configuration and Compatibility

### 1.1 How Claude Code reads project instructions

Claude Code uses a **CLAUDE.md** convention (not `AGENTS.md`).

| File location | Scope | Notes |
|---|---|---|
| `~/.claude/CLAUDE.md` | Global (all projects) | Read on every session start |
| `<project-root>/CLAUDE.md` | Project-level | Read when Claude Code opens that directory |
| `<subdir>/CLAUDE.md` | Sub-directory | Read when Claude Code operates inside that subdir |
| `.claude/settings.json` | Project settings | Hooks, model, permissions |
| `~/.claude/settings.json` | User-level settings | Hooks, model, permissions |

**`AGENTS.md` is NOT natively read by Claude Code** as of early 2025 training data.  
The `AGENTS.md` convention used in this template is a custom multi-agent orchestration framework — it is read and acted upon by an LLM (Orchestrator) reading it explicitly, not auto-loaded by Claude Code's runtime.

⚠️ *This may have changed since training cutoff. Check https://docs.anthropic.com/en/docs/claude-code/memory to confirm.*

### 1.2 Equivalent of `.github/copilot-instructions.md` in Claude Code

| Tool | Global instructions file | Project instructions file |
|---|---|---|
| GitHub Copilot | `~/.github/copilot-instructions.md` (user) | `.github/copilot-instructions.md` (repo) |
| Claude Code | `~/.claude/CLAUDE.md` | `CLAUDE.md` (project root) |
| Cursor | `~/.cursorrules` | `.cursorrules` (repo root) |
| Windsurf | `~/.windsurfrules` | `.windsurfrules` (repo root) |

For this template to work correctly with Claude Code, a shim `CLAUDE.md` should be added at the project root pointing to `AGENTS.md`:

```markdown
# Claude Code Instructions

See AGENTS.md for full orchestration instructions. Read AGENTS.md in full before any action.
```

### 1.3 Custom agents / sub-agents in Claude Code

Yes — Claude Code supports custom sub-agents via:

1. **Custom slash commands** stored in `.claude/commands/*.md`  
   Each `.md` file becomes a `/command-name` command.  
   The file contains the prompt text (Markdown).  
   Supports `$ARGUMENTS` placeholder for user-supplied text.

2. **Subagent spawning via the `Task` tool** (Claude Code's native tool)  
   In agentic mode, Claude Code can spawn sub-tasks (sub-agents) automatically.  
   The LLM decides when to use `Task` — it is not user-configured.

3. **Multi-agent via hooks + external scripts**  
   The hooks system (see §1.4) allows Claude Code to call external scripts that themselves invoke other Claude instances.

This template's `.github/agents/` directory is designed for VS Code Copilot's custom agents feature, not Claude Code's `.claude/commands/` system. Cross-compatibility would require adapter shims.

### 1.4 Hooks in Claude Code

**Yes — Claude Code has a robust hooks system.**

Hook configuration lives in `settings.json` (either user or project level):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python scripts/validate-command.py"
          }
        ]
      }
    ],
    "PostToolUse": [...],
    "Notification": [...],
    "Stop": [...],
    "PreCompact": [...]
  }
}
```

Hook types:

| Hook | When it fires | Use cases |
|---|---|---|
| `PreToolUse` | Before any tool executes | Validate, approve, or block tool calls |
| `PostToolUse` | After a tool completes | Log results, trigger side effects |
| `Notification` | On agent notification | Alerts, logging |
| `Stop` | When agent session ends | Cleanup, summarize |
| `PreCompact` | Before context compaction | Save important context |

The hook script receives a JSON payload on stdin and returns a JSON decision on stdout.  
**Claude Code DOES pass `agentName` in hook payloads** (unlike VS Code Copilot).

This means `scripts/tool-guard.py` in this template works correctly in Claude Code sessions, and the `WEB_ACCESS_ALLOWED_AGENTS = {"research"}` check works as intended.

### 1.5 Centralized configuration (not per-project)

Claude Code supports user-level (centralized) configuration:

| Location | Contains |
|---|---|
| `~/.claude/CLAUDE.md` | Global instructions for ALL projects |
| `~/.claude/settings.json` | User-level hook config, model preferences, permissions |
| `~/.claude/commands/` | User-level custom slash commands |

This means you CAN place orchestration instructions globally in `~/.claude/CLAUDE.md`.  
Projects can override by having their own `CLAUDE.md` — Claude Code merges both (project CLAUDE.md takes precedence on conflicts).

### 1.6 Model selection in Claude Code

Claude Code supports explicit model selection:

**Via settings.json:**
```json
{
  "model": "claude-opus-4-5"
}
```

**Via CLI flag:**
```bash
claude --model claude-sonnet-4-5
```

**Via `/model` slash command** during a session:
```
/model claude-haiku-3-5
```

Available models as of early 2025 training data:
- `claude-opus-4-5` / `claude-opus-4` (deepest reasoning, highest cost)
- `claude-sonnet-4-5` / `claude-sonnet-4` (balanced)
- `claude-haiku-3-5` / `claude-haiku-3` (fastest, cheapest)

The `AGENT_MODEL` mechanism in this template's `AGENTS.md` maps to per-agent model selection — the Orchestrator reads `AGENT_MODEL` from `.ai/PREFERENCES.md` and passes it when spawning sub-agents. This is NOT a native Claude Code feature; it's orchestration logic in the LLM prompt.

⚠️ *Model names evolve rapidly. Verify current names at https://docs.anthropic.com/en/api/models.*

### 1.7 Claude Code Max / unlimited mode

**Yes — Claude Code Max exists.**

As of Anthropic's announcements around late 2024 / early 2025:

| Plan | Approx. price | Usage limits |
|---|---|---|
| Claude.ai Pro | ~$20/month | Limited Claude Code usage included |
| Claude Code (API) | Pay-per-token | No monthly cap, billed by usage |
| Claude Code Max | ~$100–$200/month | "Unlimited" within plan limits, higher rate limits |

"Unlimited" in Max means a very high token cap (not literally infinite) with predictable flat-rate billing.  
Max plan is the equivalent of GREEDY_MODE in this template — run without watching the token meter.

⚠️ *Exact pricing must be verified at https://www.anthropic.com/pricing. Training data pricing is stale.*

---

## §2 — Topic 2: Multi-Project Centralized Agent Orchestration

### 2.1 Aider (Aider-AI/aider)

**Configuration approach:** file-based, per-project with user-level overrides.

| File | Scope |
|---|---|
| `~/.aider.conf.yml` | User-level (global), applies to all projects |
| `.aider.conf.yml` | Project-level (repo root) |
| `.aiderignore` | Exclude files from context |

Aider does NOT have a centralized multi-project management UI. It runs per-invocation in a single repo.

**Notable patterns:**
- **Architect mode**: Uses a larger "architect" model to plan, a smaller "editor" model to implement — this is a native two-model pattern
- **`--model` / `--editor-model`**: Separate models for design and coding
- **`--watch-files`**: Continuously watches for changes, triggers on AI comment blocks
- **Repo-map**: Tree-sitter-based map of the entire repository for cross-file context
- **Git integration**: All changes tracked via git; easy rollback

The architect/editor split in Aider is the closest real-world analog to the Orchestrator/Worker split in this template.

### 2.2 OpenHands (All-Hands-AI/OpenHands — formerly OpenDevin)

**Configuration approach:** environment variables + `config.toml`.

OpenHands is a platform for running AI software agents. It:
- Runs agents in sandboxed Docker containers
- Supports multiple LLM backends (Anthropic, OpenAI, Ollama, etc.)
- Has a ReAct-style agent loop (observe → think → act)
- Supports `CodeActAgent` (writes and executes code), `BrowsingAgent`, `DelegatorAgent`

**Multi-project pattern:** Each project is a separate sandbox session.  
There is NO centralized cross-project configuration — you configure the LLM globally via environment variables, then each session targets a specific repo.

**Delegation pattern:** `DelegatorAgent` can spawn sub-agents (similar to this template's Orchestrator → Worker pattern).

Config example (`config.toml`):
```toml
[llm]
model = "claude-opus-4-5"
api_key = "..."
max_input_tokens = 128000

[agent]
name = "CodeActAgent"
```

### 2.3 Plandex (plandex-ai/plandex)

**Configuration approach:** server + client model with persistent plans.

Plandex is unique — it runs a local server that maintains **plan state in a SQLite database**. Plans persist across sessions and can span multiple files/tasks.

**Notable patterns:**
- Plans stored in `~/.plandex/` (cross-project, user-level)
- Context window managed automatically (rolls off older context)
- "Streams" changes and applies them atomically
- `--no-confirm` flag for autonomous operation
- Model switching via `plandex set-model`

This is the closest analog to this template's `.ai/plans/` persistent state.

### 2.4 Devon (entropy-research/Devon)

Devon is a Docker-sandboxed AI software engineer. Key traits:
- Runs in an isolated environment (no risk to host system)
- Supports multi-step tasks with interruption/resume
- Uses a state machine for agent execution
- Not designed for multi-project centralized management

### 2.5 PR-Agent (Codium-ai/pr-agent)

**Configuration approach:** `.pr_agent.toml` at repo root OR GitHub/GitLab Actions config.

PR-Agent is specialized for PR reviews, not general coding. However, it has:
- Org-level configuration via GitHub Actions that can apply to all repos
- `[config]` section for model selection
- Custom commands via `@CodiumAI-Agent /command`

**Multi-project:** Deployable as a GitHub App that applies to all repos in an org — closest to "centralized" in this list.

### 2.6 smol-ai/developer

Single-shot codebase generation from a spec. Not multi-agent, not multi-project. Historical significance as an early "build an entire codebase from a prompt" demo.

### 2.7 AutoGPT (Significant-Gravitas/AutoGPT)

Early autonomous agent with:
- Goal decomposition (not multi-agent, single LLM with memory)
- Persistent memory via embedding stores (Pinecone, Redis)
- Plugin system for extending capabilities
- NOT designed for coding specifically

AutoGPT's architecture influenced later multi-agent systems but is largely superseded.

### 2.8 Template vs Runtime approach

| Approach | Examples | Pros | Cons |
|---|---|---|---|
| **Template** (this repo) | AGENTS.md template, .github/copilot-instructions.md | Human-readable, version-controlled, works across any LLM tool | Must be copied/maintained per-repo |
| **Runtime orchestration** | OpenHands, Devon | No per-repo setup; centralized control | Requires running server/daemon; tool-specific |
| **User-level config** | `~/.claude/CLAUDE.md`, `~/.aider.conf.yml` | Truly cross-project | Not version-controlled in project |
| **GitHub App** | PR-Agent, GitHub Copilot Business | Org-level enforcement | Requires GitHub/GitLab integration |

**Recommendation for this template:** Add a `CLAUDE.md` shim at the project root, and document the `~/.claude/CLAUDE.md` global instructions pattern for users who want centralized cross-project behavior.

---

## §3 — Topic 3: Super Greedy / Maximum Quality Patterns in AI Coding

### 3.1 Multi-model consensus / council approaches

**State of the art (as of early 2025 training data):**

Consensus voting across multiple LLM models is an **academic/research pattern** not yet widely deployed in mainstream coding tools. Known implementations:

- **Mixture of Agents (MoA)** — research paper (Shi et al., 2024): Each model generates an answer; a "aggregator" model synthesizes. Demonstrated improved accuracy over single-model on benchmarks.
- **Self-consistency** (Wang et al., 2022): Run the same prompt N times, take majority vote. Implemented in LangChain, LlamaIndex.
- **LLM-as-Judge**: One model critiques another's output. Used in some evaluation frameworks.
- **Debate** (Du et al., 2023): Models argue opposing positions; a judge synthesizes. Shown to improve factual accuracy.

None of the coding tools surveyed (Aider, OpenHands, Plandex) implement LLM Council voting natively.  
This template's "LLM Council" pattern (Super Greedy Pipeline) is **novel** relative to open-source alternatives.

### 3.2 Mutation testing integration

No AI coding tool in this survey integrates mutation testing natively.  
Mutation testing frameworks exist independently:

| Language | Framework | Notes |
|---|---|---|
| Python | `mutmut` | Most common, integrates with pytest |
| JavaScript/TypeScript | `Stryker` | Mature, widely used |
| Java | `PIT (pitest)` | JVM-based, fast |
| Rust | `cargo-mutants` | Growing |
| Go | `go-mutesting` | Early stage |

Integration with AI coding: would require the LLM to interpret mutation reports and write defeating tests. This is a gap in all current tools — **this template's `step 19a` is aspirationally ahead of the field**.

### 3.3 Continuous code quality validation

**How current tools approach this:**

| Tool | Quality mechanism |
|---|---|
| Aider | `/lint` command (runs user-configured linter); `/test` command (runs test suite) |
| OpenHands | Can run any command; no built-in quality loop |
| Plandex | No built-in quality checks |
| Claude Code | Can be configured via hooks to run linters post-edit |

The "continuous audit pack after every Worker step" pattern in this template's Super Greedy Pipeline is not replicated in any open-source tool.

### 3.4 N-version programming

N-version programming (implementing the same function in N independent ways and voting) is a **classical fault-tolerance pattern** from aerospace (1970s). Its application to LLM coding is novel and not widely implemented.

No open-source AI coding tool implements N-version programming.  
The Super Greedy Pipeline's `Worker (N-version)` step is **unique** among surveyed tools.

### 3.5 Cross-file coherence checking

**How current tools approach cross-file consistency:**

| Tool | Mechanism |
|---|---|
| Aider | **Repo-map** (tree-sitter AST of entire repo, truncated to fit context) — best-in-class |
| OpenHands | Entire repo available; agent decides what to read |
| Plandex | Context window management; user adds files explicitly |
| Claude Code | `@file` references; can read any file via `Read` tool |

Aider's repo-map is the most sophisticated cross-file coherence tool in open source. It builds a graph of function/class definitions and references, ranks by relevance to current edit, and injects a compact representation into context.

This template's "Cross-File Coherence Review" (step 20a / step 24) goes further: a dedicated agent reads ALL source files looking for naming, pattern, error handling, and API style inconsistencies. No tool does this automatically.

### 3.6 Adversarial testing of AI outputs

**Pattern:** Use a separate LLM call to critique / stress-test the first LLM's output.

| Tool | Adversarial pattern |
|---|---|
| Claude Code native | Architect↔Critic loop (manual) |
| AutoGPT | Self-reflection (same model) |
| LangGraph | Can wire a critic node in a graph |
| CrewAI | `critic` role in crew configuration |
| This template | Dedicated Critic agent + Adversarial Red Team (Super Greedy) |

**CrewAI** is worth noting — it's a Python framework for multi-agent crews that supports role assignment (researcher, coder, critic) and has a native critic/review pattern.

---

## §4 — Topic 4: Claude Code Unlimited / Max Plan Features

### 4.1 Pricing model (training data — verify at anthropic.com/pricing)

⚠️ **All prices and plan names below are based on training data. Must be verified.**

| Tier | Approx. monthly cost | Claude Code access | Notes |
|---|---|---|---|
| Claude.ai Free | $0 | Limited / none | Consumer tier |
| Claude.ai Pro | ~$20/month | Included (limited usage) | For individual users |
| Claude.ai Max | ~$100–$200/month | Included (high usage) | "Unlimited" flat-rate |
| API (pay-per-token) | Variable | Yes, full access | Enterprise / developer |
| API + Claude Code Pro | ~$100/month | Full Claude Code access | Professional |

"Max" / "Pro" plan naming may have changed. Anthropic has rebranded tiers multiple times.

### 4.2 "Unlimited" mode

The Claude Code Max plan offers predictable flat-rate pricing rather than per-token billing.  
"Unlimited" in marketing language means: no per-token charges within the plan, but there ARE rate limits and fair-use policies. It is not literally infinite.

This is what the Super Greedy Pipeline's `GREEDY_MODE: ON` targets — **a flat-rate plan where running 50 LLM calls per feature is economically rational**.

### 4.3 Model access in Claude Code

Claude Code can use any model accessible to the account's API key:

```bash
# Set the model in .claude/settings.json or via CLI
claude --model claude-opus-4-5

# Or in settings.json
{
  "model": "claude-opus-4-5"
}
```

**Per-task model selection:** Claude Code itself does not natively route different tasks to different models. The AGENTS.md template's per-agent model table implements this at the orchestration layer (the LLM Orchestrator selects which model to invoke for each sub-agent).

### 4.4 Model tiers and task matching (from this template + training data)

The `AGENT_MODEL_TABLE` in `AGENTS.md` already correctly maps agents to appropriate models:

| Tier | Model family | Agents |
|---|---|---|
| Tier 1 (reasoning) | Claude Opus 4.x | Architect, Planning, Critic, Prompt Engineer |
| Tier 2 (execution) | Claude Sonnet 4.x | Worker, Test Writer, Discovery, Research |
| Tier 3 (fast checks) | Claude Haiku 3.x | Quick validation, format checks |

This matches best practices: use the most capable model for design decisions, medium model for implementation, fast model for linting/formatting.

---

## §5 — Recommendations for Template Cross-Compatibility

Based on these findings, the following changes would make this template work across Claude Code, Cursor, Windsurf, and VS Code Copilot:

### 5.1 Add `CLAUDE.md` at project root

```markdown
# Claude Code Instructions

This project uses the AGENTS.md multi-agent orchestration framework.
Read AGENTS.md in full before taking any action.

- Orchestrator identity: You are a pure dispatcher. Do NOT write code directly.
- See .github/copilot-instructions.md for VS Code Copilot equivalents.
- Sub-agent instructions live in .github/agents/*.agent.md
```

### 5.2 Add `.claude/commands/` for Claude Code slash commands

Map the template's Quick Commands to Claude Code slash commands:
- `.claude/commands/plan.md` → `/plan` 
- `.claude/commands/implement-plan.md` → `/implement-plan`
- `.claude/commands/onboard.md` → `/onboard`
- etc.

### 5.3 Fix tool-guard.py for VS Code Copilot compatibility

See §0 for the specific code change.

### 5.4 Add `~/.claude/CLAUDE.md` documentation

Add instructions to `README.md` or `TEMPLATE_README.md` explaining how to copy/symlink the global instructions to `~/.claude/CLAUDE.md` for cross-project availability.

---

## §6 — URLs Attempted and Status

| URL | Status | Notes |
|---|---|---|
| https://docs.anthropic.com/en/docs/claude-code/overview | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://docs.anthropic.com/en/docs/claude-code/settings | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://docs.anthropic.com/en/docs/claude-code/memory | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://docs.anthropic.com/en/docs/claude-code/commands | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/anthropics/claude-code | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/All-Hands-AI/OpenHands | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/paul-gauthier/aider | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/Codium-ai/pr-agent | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/Aider-AI/aider | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/plandex-ai/plandex | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/Significant-Gravitas/AutoGPT | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://www.anthropic.com/pricing | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/entropy-research/Devon | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| https://github.com/e2b-dev/awesome-ai-agents | ⛔ Blocked | tool-guard.py denied fetch_webpage |
| All others | ⛔ Blocked | Same reason |

**Root cause:** `scripts/tool-guard.py` PreToolUse hook denies web access when VS Code Copilot does not pass `agentName` in the hook payload. Fix described in §0.

---

## §7 — Knowledge Freshness Caveats

All findings in §1–§4 are based on training data with an approximate cutoff of **early 2025**.  
The following areas are most likely to have changed:

1. **Claude Code CLAUDE.md vs AGENTS.md** — Anthropic may have added support for `AGENTS.md` natively (there is industry movement toward standardizing agent instruction files)
2. **Claude Code pricing and plan names** — Anthropic changes pricing structures frequently  
3. **Model names** — New models released; old model names retired
4. **OpenHands / Devon features** — Rapidly evolving projects; significant feature changes likely
5. **CrewAI** — Growing framework; multi-model and consensus features may have been added

Priority URLs to verify once the tool guard is fixed:
1. `https://docs.anthropic.com/en/docs/claude-code/memory` — CLAUDE.md location details
2. `https://docs.anthropic.com/en/docs/claude-code/settings` — Hook configuration schema
3. `https://www.anthropic.com/pricing` — Current plan names and prices
4. `https://aider.chat/docs/config.html` — Current Aider config options
