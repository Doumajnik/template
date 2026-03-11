+++
id = "agents/planner"
title = "Planner Agent Rules"
agents = ["planner"]
technologies = ["all"]
category = "rule"
tags = ["planner"]
version = 2
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
