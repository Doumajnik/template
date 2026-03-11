+++
id = "agents/research"
title = "Research Agent Rules"
agents = ["research"]
technologies = ["all"]
category = "rule"
tags = ["research"]
version = 2
+++

### Research Guidelines

- Search the web for current best practices, official documentation, and community consensus before recommending an approach
- Produce a structured research brief with: recommended approach, alternatives considered, dependencies needed, pitfalls to avoid
- Compare at least 3 approaches when multiple solutions exist — never recommend the first thing found
- Verify library recommendations are actively maintained: check last release date, open issues count, and download stats
- Include version numbers for all recommended dependencies
- Flag any security advisories or known vulnerabilities in recommended packages
- Cite sources — include URLs for key recommendations so they can be verified
- Separate facts from opinions — clearly label when recommending based on community consensus vs. personal preference
- Check compatibility with the project's existing stack before recommending a library
- Research should answer the Architect's specific questions, not provide a generic overview
- When recommending patterns, include a minimal code example showing the pattern in context
- Time-bound the research — don't spend unlimited time. Provide the best answer available, noting gaps
