+++
id = "agents/planner"
title = "Planner Agent Rules"
agents = ["planner"]
technologies = ["all"]
category = "rule"
tags = ["planner"]
version = 4
+++

### Planner Guidelines

- Read all relevant docs before creating a plan: `docs/PLAYBOOK.md`, `docs/CODE_INVENTORY.md`, `docs/BUSINESS_LOGIC.md`
- Create plans in `.ai/plans/` following the established plan template
- Create todo files in `.ai/todos/` as the living tracker — every task gets a status checkbox
- Plan at the function level when TURBO_MODE is ON — each function is a separate todo item
- Plan at the phase level when TURBO_MODE is OFF — group related functions into phases
- Identify dependencies between tasks — tasks with dependencies must be sequenced, independent tasks can be parallelized
- Estimate complexity for each task: trivial, simple, moderate, complex
- Flag tasks that need user input or decisions with `[ASK USER]`
- Include test tasks for every implementation task — tests come before implementation (TDD)
- Include documentation tasks — doc updates are not optional
- Include review and security audit tasks at the end of every plan
- The plan must cover the full lifecycle: scaffold → test → implement → integrate → review → document
- Apply WIP (Work In Progress) limits — restrict the number of tasks in progress simultaneously to prevent context switching and unfinished work accumulation; no agent should have more than 2 tasks in-progress at once
- Break epics into user stories with clear acceptance criteria — each story should be independently deliverable, testable, and small enough to complete in a single work session
- Define a "Definition of Done" checklist for each task — a task is not done until code is written, tests pass, review is approved, documentation is updated, and the change is merged
- Add spike/research tasks for uncertain areas — before committing to implementation estimates on unfamiliar technology or ambiguous requirements, schedule a time-boxed investigation task
- Plan for continuous improvement — include a retrospective step at the end of every plan to capture what worked, what didn't, and what to change next time
- Prioritize tasks by value and risk — tackle high-risk unknowns and high-value deliverables first; fail fast on uncertainties and deliver visible progress early to maintain momentum
- Size individual tasks to no more than 16 hours of work — larger tasks are harder to estimate accurately, clog the pipeline, and aggravate WIP limits; if a task exceeds 16 hours, decompose it further before scheduling (ref: Atlassian Kanban WIP Limits)
- Map WIP limits to team member skills and specializations — if the team has specialists, set status-specific WIP limits that reflect specialist capacity; use bottlenecks as opportunities to cross-train team members and increase overall flow
- Track lead time (request to delivery) and cycle time (start to delivery) as planning metrics — decreasing cycle time indicates improving efficiency; use these metrics to calibrate future estimates and identify process bottlenecks
- Plan for swarming on bottlenecks — when a workflow stage hits its WIP limit, plan for available team members to assist with the blocked stage rather than starting new work; finishing existing work always takes priority over starting new work
- Resist raising WIP limits just because the team keeps hitting them — consistently hitting a limit signals a process bottleneck to fix, not a limit to raise; investigate root causes (skill gaps, unclear requirements, slow reviews) before adjusting limits
- Include buffer capacity in plans for unplanned work — reserve 10-20% of planned capacity for urgent bugs, production incidents, and ad-hoc requests; plans that assume 100% utilization inevitably slip when reality intervenes
