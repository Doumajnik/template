+++
id = "shared/code-style"
title = "Code Style Convention"
agents = ["all"]
technologies = ["all"]
category = "convention"
tags = ["style", "readability", "formatting"]
version = 1
+++

### Code Style

Readable over clever. Doc comments on all exports. No hardcoded secrets — use env vars or `.env` (must be in `.gitignore`). Structure: `src/utils/`, `src/services/`, `src/models/`, `src/config/`.
