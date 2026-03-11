+++
id = "shared/extraction-rules"
title = "Extraction Rules"
agents = ["all"]
technologies = ["all"]
category = "strategy"
tags = ["extraction", "refactoring", "shared-code"]
version = 3
+++

### Extraction Rules

- If the same 3+ lines appear in two places, extract into a shared function
- Magic numbers must be extracted into named constants with descriptive names
- String literals used in comparisons must be constants or enums
- Complex regular expressions must be named constants with a comment explaining the pattern
- Configuration values (URLs, timeouts, limits) must be extracted into config, not inline
- If a lambda exceeds one line or 60 characters, convert it to a named function
- SQL queries longer than 2 lines should be stored as named constants or template strings
- Nested function calls deeper than 2 levels should use intermediate variables
- Extract validation logic into dedicated validator functions rather than inline checks
- File paths should be constructed using pathlib, never string concatenation
- HTTP headers, status codes, and content types used in multiple places must be constants
- Error messages displayed to users must be in a centralized i18n/messages module — never inline
- Date/time formatting patterns must be constants — never inline format strings
- API endpoint paths must be defined as constants — never scattered as inline strings
- Environment variable names must be defined as constants with documentation of expected values
- Default values for configuration must be defined alongside the config constant, not at the usage site
- Common validation patterns (email regex, phone regex, URL pattern) must be shared constants
- Retry counts, timeout durations, and backoff multipliers must be named constants, not inline numbers
- If a function signature has more than 2 boolean parameters, extract into an options/config object
- Database table and column names referenced in code must be constants — never inline strings
