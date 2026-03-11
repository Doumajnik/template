+++
id = "agents/debug"
title = "Debug Agent Rules"
agents = ["debug"]
technologies = ["all"]
category = "rule"
tags = ["debug"]
version = 2
+++

### Debug Guidelines

- Start by reading the error message, stack trace, and relevant logs — understand the symptom before investigating
- Reproduce the bug first — if you can't reproduce it, you can't verify the fix
- Check recent changes: what was modified since the last known-good state?
- Read the function where the error occurs AND its callers — the bug may be in the caller
- Check edge cases: null/None inputs, empty collections, boundary values, race conditions
- Verify assumptions: are the inputs what you expect? Add temporary logging if needed
- Fix the root cause, not the symptom — a try/catch around a bug is not a fix
- After fixing, verify the original error is gone AND no new errors are introduced
- Write a regression test that would have caught the bug — prevent it from recurring
- Clean up any temporary debugging code (print statements, logging) before marking complete
- If stuck after 2 attempts, report the failure with: what was tried, what was observed, hypotheses remaining
- Never delete a file to fix a bug — fix the actual problem in place
- Check if the bug exists in similar code elsewhere — fix all instances, not just the reported one
