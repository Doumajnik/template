# Lessons Learned

> **Self-Improvement Loop.** After ANY correction from the user, the Orchestrator immediately records the pattern here.
> This file is read at session start. Agents use these lessons to avoid repeating mistakes.

---

## Format

Each lesson follows this structure:

```
### {date} — {short description}
**Trigger:** What went wrong / what the user corrected
**Pattern:** The underlying mistake pattern
**Rule:** The rule to prevent recurrence
**Applies to:** Which agents should follow this rule
```

---

## Lessons

### 2026-03-15 — Reports must not reference non-existent files
**Trigger:** Review, Security, and Code Quality reports referenced 6 files (`embedding_client.py`, `knowledge_index.py`, `build-knowledge-index.py`, `query-knowledge-index.py`, and their test files) that do not exist on disk. CODE_INVENTORY also lists symbols from these phantom files.
**Pattern:** Reports were generated based on code that existed in an agent's context window but was never persisted to disk — or was lost between sessions. No verification step confirmed the files actually existed before auditing them.
**Rule:** Before generating any Review, Security, or Quality report, the agent MUST verify every referenced file exists on disk (read the file or list the directory). If a file does not exist, the report MUST flag it as missing and NOT audit phantom code.
**Applies to:** Reviewer, Security Agent, Code Quality Agent, Doc Updater

### 2026-03-15 — Dispatch log must cover the full session lifecycle
**Trigger:** The dispatch log only recorded 9 planning-phase dispatches. All implementation dispatches (Scaffolder, Test Writer, Worker, Integration Tester, Reviewer, Security, Code Quality, Doc Updater) were missing. This made it impossible to reconstruct the implementation timeline.
**Pattern:** When implementation spans multiple chat sessions, dispatch logging is forgotten or the new session starts a fresh log without linking to the original.
**Rule:** Every sub-agent spawn MUST be logged in the dispatch log — no exceptions. When continuing work in a new session, the Orchestrator MUST either continue the existing dispatch log or create a new one that references the original. The dispatch log entry count should match the todo completion count.
**Applies to:** Orchestrator

### 2026-03-15 — Todo tasks must be marked as they complete
**Trigger:** All ~90 todo tasks remained ⬜ unchecked despite partial implementation being present on disk (`playbook_parser.py` with 74 tests). The todo file's Progress Log only has one entry from the Planning Agent.
**Pattern:** Agents completed work without updating the todo tracker. The todo became stale and useless as a progress indicator.
**Rule:** Every agent MUST mark its todo task(s) 🔵 in-progress before starting and ✅ done upon completion. The Orchestrator MUST verify todo updates after each agent reports back. If a todo task is not updated, the Orchestrator blocks the next dispatch until it is.
**Applies to:** All agents, Orchestrator (enforcement)

### 2026-03-15 — Critic rejections should generate lessons immediately
**Trigger:** The Critic rejected the architecture in dispatch #6 with 3 critical and 6 additional issues. No lesson was recorded in `.ai/lessons.md` despite the rejection being a significant learning moment.
**Pattern:** Lessons are only recorded when the user corrects the agent, not when internal quality gates (Critic, Reviewer) catch problems.
**Rule:** When the Critic rejects an architecture or the Reviewer rejects an implementation, the Orchestrator MUST immediately record the root cause pattern in `.ai/lessons.md` — even before the fix is applied. Internal rejections are learning opportunities, not just workflow steps.
**Applies to:** Orchestrator

### 2026-03-15 — Plan status must be updated after approval
**Trigger:** The plan status remained 🟡 Draft even after the Critic approved the architecture in dispatch #8 and the Planning Agent created the full implementation plan in dispatch #9.
**Pattern:** The plan status field was set during creation and never updated as the plan progressed through the pipeline.
**Rule:** The Orchestrator MUST update the plan status to 🟢 Approved after Critic approval, to 🔵 In Progress during implementation, and to ✅ Complete or 🟡 Paused at session end.
**Applies to:** Orchestrator, Planning Agent
