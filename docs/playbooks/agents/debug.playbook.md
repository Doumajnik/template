+++
id = "agents/debug"
title = "Debug Agent Rules"
agents = ["debug"]
technologies = ["all"]
category = "rule"
tags = ["debug"]
version = 4
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
- Use "divide and conquer" (binary search debugging) — systematically narrow the problem space by halving the code, input, or time range under investigation until the fault is isolated
- Accept that it's probably your code's fault — before blaming libraries, frameworks, or infrastructure, verify your own code first; well-established external tools are rarely the root cause
- Reproduce the bug as quickly as possible — invest time creating a fast reproduction (unit test, script, minimal repro) so each debugging iteration takes seconds, not minutes
- Check your assumptions explicitly — verify that variables hold expected values, code paths are actually executing, the correct file/branch is deployed, and the documentation matches the actual behavior
- Change one thing at a time when testing hypotheses — making multiple simultaneous changes makes it impossible to determine which change had the effect
- Improve debuggability after fixing — add better error messages, input validations, or logging at the failure point so future occurrences are self-explanatory and don't require re-investigation
- Use rubber duck debugging — explain the problem out loud (or in writing) step-by-step to an imaginary listener; the act of articulating the problem forces structured thinking and frequently reveals the bug before finishing the explanation
- Read error messages carefully and completely — parse every part of the error: the error type, message text, file path, line number, and full stack trace (read bottom-to-top for the call chain); most errors tell you exactly what's wrong if you read them thoroughly
- Check environment differences when a bug appears in one environment but not another — compare OS, runtime version, dependency versions, environment variables, configuration files, timezone, locale, file permissions, and available disk/memory between working and broken environments
- Take a deliberate break when stuck beyond 30 minutes on the same hypothesis — step away, context-switch, or sleep on it; continued staring at the same code triggers fixation blindness where you literally cannot see the bug despite it being in front of you
- Use git bisect for regression bugs — when something worked before and now doesn't, use binary search across the commit history to identify the exact commit that introduced the regression; this is faster than reading every change manually
- Keep a debugging log during complex investigations — write down each hypothesis, what you tested, what the result was, and what you concluded; this prevents re-testing the same thing, creates a paper trail if you need to escalate, and often reveals patterns across failed hypotheses
