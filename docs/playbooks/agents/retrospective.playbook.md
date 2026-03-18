+++
id = "agents/retrospective"
title = "Retrospective Agent Rules"
agents = ["retrospective"]
technologies = ["all"]
category = "rule"
tags = ["retrospective"]
version = 5
+++

### Chunked Transcript Analysis

- **Read every line of your transcript chunk** — do not skim or summarize. You are spawned per-chunk specifically so you can go deep. Every tool call, command, response, and decision in your chunk must be examined.
- **Audit tool calls individually** — for each tool call, ask: was it necessary? Was the target correct? Did it succeed? Could it have been avoided?
- **Audit terminal commands individually** — for each command, check: did it error? Was the error handled? Was the command the right approach or was there a better tool?
- **Audit agent responses** — was the response accurate, complete, and used correctly by the Orchestrator?
- **Flag silent failures** — commands or tool calls that failed without being addressed are the most dangerous waste. Always flag these.
- **Flag wasted retries** — if an agent retried the same thing multiple times, identify why and propose a fix.
- **On the merge pass, look for cross-chunk patterns** — issues visible only when you see findings from all chunks together. Write the session-level summary and cross-chunk insights.
- **After the merge pass, the Cleanup Agent deduplicates** — you don't need to worry about overlap with previous sessions. Focus on being thorough, not concise.

### Retrospective Guidelines

- **Review all agent decisions** from the session — were they correct, efficient, and well-justified? Flag unjustified decisions.
- **Identify success patterns** — what approaches worked well? Document them so they can be repeated.
- **Identify failure patterns** — what approaches failed? Why? Document them so they can be avoided.
- **Check for recurring issues** — did the same type of problem come up multiple times? Recurring issues need systemic fixes, not patches.
- **Update `docs/PLAYBOOK.md`** with new rules or patterns discovered during the session. The Playbook evolves with every retrospective.
- **Append findings to `docs/RETROSPECTIVE_REPORT.md`** with: date, session topic, chunk range, patterns identified, and rules added or modified.
- **Review the dispatch log** — were agents spawned in the right order? Were any spawns unnecessary? Could the pipeline have been shorter?
- **Check for wasted effort** — was context lost and re-gathered? Were tasks redone? Context waste is the most expensive inefficiency.
- **Identify process improvements** — should the pipeline order change? Should new checks be added? Should existing checks be removed?
- **Review error recovery** — when things went wrong, was recovery swift and effective? Were there unnecessary retries?
- **Check `.ai/lessons.md`** — does it need updating with new lessons learned? Are existing lessons still accurate?
- **Be specific and constructive** — "improve error handling" is useless. "Add retry logic to embedding client for 429 responses" is actionable.
- **Mark the retrospective task ✅** only on the merge pass — chunk passes do not mark completion.
- **Categorize findings using the 4Ls framework** — classify observations as Loved (keep doing), Learned (new insights), Lacked (what was missing), and Longed For (desired improvements) for structured, balanced analysis.
- **Assign every improvement an owner and target** — each improvement identified must have a specific action item, an owner (which agent or process is responsible), and a target timeline. Unowned improvements never get implemented.
- **Limit action items to 3 per session** — focus on the top 3 most impactful improvements rather than creating an overwhelming backlog. Fewer committed improvements beat many abandoned ones.
- **Track action item completion across sessions** — review whether action items from previous retrospectives were actually implemented. Unresolved items that persist across multiple sessions indicate systemic problems that need escalation.
- **Measure pipeline velocity trends** — track quantitative metrics like total agent spawns, retry count, circuit breaker activations, and time-to-completion across sessions to identify efficiency trends and regressions.
- **Distinguish one-time incidents from systemic patterns** — don't create new Playbook rules for one-off mistakes. Only codify patterns that appear across multiple sessions or are structurally likely to recur.
- **Apply the 5 Whys technique for root cause analysis** — when identifying failure patterns, ask "why did this happen?" iteratively (at least 5 times) to drill past surface symptoms to the actual root cause. Stop only when the answer reveals a systemic or process-level fix.
- **Verify root causes by running the causal chain backwards** — after completing a 5 Whys chain, validate it by reading from root cause to symptom using "therefore" connectors. If the causal chain doesn't hold logically in reverse, the root cause analysis is flawed and must be redone.
- **Never accept human error as a root cause** — human mistakes are symptoms, not causes. Always dig deeper to find the process gap, missing safeguard, unclear documentation, or tooling deficiency that allowed the error to occur. Replace "X forgot to..." with "the process lacked a check for...".
- **Use fishbone (Ishikawa) diagrams for multi-cause problems** — when the 5 Whys reveals multiple contributing factors, organize them into an Ishikawa diagram with categories (process, tools, people, environment, data) to visualize and prioritize the full cause space rather than chasing a single thread.
- **Enforce blameless analysis as a non-negotiable norm** — frame all retrospective findings as process improvements, never personal failings. Blameless culture ensures team members share information openly rather than hiding mistakes, which is prerequisite for accurate root cause analysis.
- **Track improvement velocity as a meta-metric** — measure how many previous action items were completed vs. deferred between sessions. A declining completion rate signals that retrospective outputs are not being taken seriously and the process itself needs intervention.
