+++
id = "shared/extraction-rules"
title = "Extraction Rules"
agents = ["all"]
technologies = ["all"]
category = "strategy"
tags = ["extraction", "refactoring", "shared-code"]
version = 1
+++

### Extraction Rules

When the same logic appears in 2+ places, extract it into a shared utility in `src/utils/`. Plan shared utilities before feature-specific code.
