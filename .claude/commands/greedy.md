Run the Super Greedy Pipeline with maximum quality. This is for unlimited LLM resource sessions.

First, read AGENTS.md fully — specifically the "Super Greedy Pipeline (GREEDY_MODE: ON)" section and .ai/LLM_COUNCIL.md for the Council protocol.

Then execute:
1. Model Discovery — enumerate available models, assign to Tier 1/2/3
2. For EVERY critical decision, dispatch to ALL Tier 1 models independently and synthesize via LLM Council
3. Run continuous Security + Code Quality + Type Safety audits after every implementation step
4. Use N-version programming for critical functions (2–3 models implement, Council selects best)
5. Run Cross-File Coherence Review twice (after impl + final)
6. Run Mutation Testing — verify ≥90% kill rate
7. Produce Quality Scorecard at the end

Set GREEDY_MODE: ON for this session. Follow the checklist in .ai/checklists/greedy.checklist.md step by step.

User's request: $ARGUMENTS
