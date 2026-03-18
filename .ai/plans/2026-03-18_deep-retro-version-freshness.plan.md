# Plan: Deep Retrospective + Version Freshness

**Date:** 2026-03-18
**Status:** 🟡 Draft

## Objective

Two enhancements to the agent pipeline:

1. **Deep Retrospective** — The Retrospective Agent currently reviews only the dispatch log, session summary, and report files. It should instead reconstruct the **entire conversation**: every tool call, every command, every agent response, every decision point. To avoid missing details due to context limits, the Orchestrator spawns the Retrospective **in parts** — one per phase/chunk of the session — then spawns a Cleanup Agent pass to deduplicate the accumulated report content.

2. **Version Freshness** — Every agent that introduces or references a dependency, library, tool, or framework must check the web for the current latest stable version. This applies at Research time, Worker time, and any ad-hoc agent that adds a dependency.

---

## Feature 1: Deep Retrospective

### Problem

The Retrospective Agent only sees high-level summaries (dispatch log, session summary, reports). It misses:
- Individual tool call results (errors, retries, unexpected output)
- Commands that failed silently or needed workarounds
- Agent reasoning that wasn't captured in reports
- The full back-and-forth of Architect↔Critic loops
- Worker red-green cycles (which tests failed, how many retries)

### Solution

**A. Expand what gets passed to the Retrospective Agent**

Currently the Orchestrator passes:
1. Dispatch log
2. Session summary
3. Report files (REVIEW, SECURITY, QUALITY)
4. Current PLAYBOOK
5. Todo file

**Add:**
6. The **full session trace** — every agent spawn prompt and its complete response
7. All **terminal command outputs** from Worker/Debug agents (captured in session)
8. All **test results** (pass/fail details per test)
9. Any **error logs** or **retry records** from the session

The Orchestrator already mediates all agent calls. It needs to **accumulate a session transcript** — a running log of every sub-agent call (prompt sent + response received) — and pass it to the Retrospective Agent.

**B. New session transcript file**

Create `.ai/sessions/{date}_{topic}.transcript.md` during the session. The Orchestrator appends to it after every sub-agent completes:

```markdown
## Dispatch #{N} — {Agent Name}

### Prompt Sent
{the prompt the Orchestrator sent to the sub-agent, truncated to key parts}

### Response Received
{the sub-agent's full response}

### Tool Calls Made
{list of tools the agent called and their results, if available}

### Terminal Commands
{any commands run and their output}
```

**C. Chunked Retrospective — spawn in parts, not all at once**

The Orchestrator does NOT spawn one giant Retrospective at the end. Instead:

1. **Partition the transcript** by phase or by dispatch ranges (e.g., dispatches #1–#5, #6–#10, etc.)
2. **Spawn one Retrospective instance per chunk** — each gets only its slice of the transcript + the relevant reports. Each instance appends its findings to `docs/RETROSPECTIVE_REPORT.md` and `docs/PLAYBOOK.md`.
3. **Fresh context per chunk** — each spawn starts clean, so nothing is glossed over or lost to context window limits.
4. **Final merge spawn** — after all chunks are done, spawn one last Retrospective instance with only the newly-appended entries to write a session-level summary and cross-chunk patterns.

Each chunk's audit covers:
- Every tool call: was it necessary? Did it succeed?
- Every command: did it produce errors? Were errors handled?
- Every agent answer: was it accurate? Was it used correctly?
- Every decision point: what alternatives existed?

**D. Post-Retrospective deduplication**

After the Retrospective Agent generates/appends to reports, spawn the Cleanup Agent (or the Reviewer Agent in dedup-audit mode) to:
1. Read `docs/RETROSPECTIVE_REPORT.md` — find duplicate entries, overlapping patterns, or redundant rules
2. Read `docs/PLAYBOOK.md` — find rules that say the same thing in different words
3. Read `.ai/lessons.md` — find duplicate or superseded lessons
4. Consolidate duplicates, remove superseded entries, merge overlapping rules
5. Report what was consolidated

### Files to Change

| File | Change |
|------|--------|
| `AGENTS.md` | Update Retrospective description: "Reviews **entire session transcript** including all tool calls, commands, and responses" |
| `.github/copilot-instructions.md` | Same update to Retrospective description |
| `.github/agents/retrospective.agent.md` | Add transcript reading step, expand audit scope to cover tool calls/commands/responses |
| `docs/playbooks/agents/retrospective.playbook.md` | Add rules for transcript-level analysis and dedup pass |
| `AGENTS.md` (Planning Sequence) | Add step 20.5: "Cleanup Agent — deduplicates accumulated report content" |
| `.github/copilot-instructions.md` (Planning Sequence) | Same addition |

### New File

| File | Purpose |
|------|---------|
| `.ai/SESSION_TRANSCRIPT_TEMPLATE.md` | Template for the session transcript file |

---

## Feature 2: Version Freshness

### Problem

Agents sometimes reference or install dependencies without verifying the current latest version. The PREFERENCES already say "Always use the latest versions" and "the Research Agent MUST check the web," but:
- Workers might install a package without checking
- The Research Agent might rely on cached knowledge instead of actually fetching
- No enforcement mechanism exists

### Solution

**A. Strengthen the Research Agent instructions (sole owner of version checking)**

The Research Agent is the **only** agent responsible for version freshness. Add an explicit mandatory step: "For EVERY dependency listed in the research brief, you MUST fetch the package registry page (PyPI, npm, crates.io, NuGet, etc.) and confirm the latest stable version. Never rely on training data for version numbers."

Other agents (Worker, Dependency, etc.) trust the Research Agent's verified versions — they don't need to re-check.

**B. Add a version check rule to shared playbook**

A new shared playbook rule that directs all agents to the Research Agent: "When any agent needs a dependency version, it MUST come from a Research Agent brief with web-verified versions. Never guess or use training data for version numbers."

### Files to Change

| File | Change |
|------|--------|
| `.github/agents/research.agent.md` | Add mandatory registry fetch step for every dependency |
| `docs/playbooks/shared/` | New file: `version-freshness.playbook.md` — shared rule directing to Research Agent |
| `docs/playbooks/agents/research.playbook.md` | Add version verification rules |

---

## Phases

- [ ] **Phase 1: Session Transcript Infrastructure** `[delegatable]`
  - Create `.ai/SESSION_TRANSCRIPT_TEMPLATE.md`
  - Update orchestrator instructions (AGENTS.md, copilot-instructions.md) to accumulate transcript
  - Impl plan: `.ai/plans/impl/deep-retro-versions_phase-1.impl.md`

- [ ] **Phase 2: Chunked Retrospective Agent** `[delegatable]`
  - Update `retrospective.agent.md` with chunked transcript analysis workflow
  - Update `retrospective.playbook.md` with chunked analysis rules
  - Update AGENTS.md and copilot-instructions.md: Orchestrator partitions transcript, spawns retro per chunk, then dedup pass
  - Impl plan: `.ai/plans/impl/deep-retro-versions_phase-2.impl.md`

- [ ] **Phase 3: Version Freshness Rules** `[delegatable]`
  - Update `research.agent.md` with mandatory registry fetch (sole owner)
  - Create `docs/playbooks/shared/version-freshness.playbook.md`
  - Update `docs/playbooks/agents/research.playbook.md`
  - Impl plan: `.ai/plans/impl/deep-retro-versions_phase-3.impl.md`

---

## Post-Implementation Checklist

- [ ] All agent .md files updated
- [ ] All playbook files updated
- [ ] AGENTS.md and copilot-instructions.md pipeline steps updated
- [ ] Template files created
- [ ] No duplication between agent instructions and playbook rules
- [ ] README unchanged (no new top-level dirs)
