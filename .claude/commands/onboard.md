Run the Onboarding Pipeline for an existing project. Read AGENTS.md "Onboarding Pipeline" section.

Execute all 7 phases (read-only until user approves):
1. Discovery — map the codebase → docs/discoveries/
2. Documentation — fill BUSINESS_LOGIC, CODE_INVENTORY, API docs, per-file docs
3. Audits (parallel) — Security, Code Quality, Dependency, Error Handling, Type Safety, Monitoring
4. Structure & Cleanup analysis — Architect (structure review) + Cleanup (audit-only)
5. Test harness — Test Writer + Integration Tester (black-box, ≥12/function)
6. Improvement plan — Planning Agent synthesizes all reports
7. Present to user — show findings, ask for approval before fixes

Follow .ai/checklists/onboarding.checklist.md.

User's request: $ARGUMENTS
