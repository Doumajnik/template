+++
id = "agents/ui-preview"
title = "UI Preview Agent Rules"
agents = ["ui-preview"]
technologies = ["all"]
category = "rule"
tags = ["ui-preview"]
version = 2
+++

### UI Preview Agent Rules

1. Generate an interactive HTML/CSS preview mockup — not just a screenshot or static wireframe.
2. Include all major views/pages from the architecture plan — not just the main page.
3. Use semantic HTML with proper structure: `<nav>`, `<main>`, `<form>`, `<button>` — not `<div>` for everything.
4. Include realistic placeholder content — not just "Lorem ipsum" but contextually appropriate data.
5. Include responsive breakpoints: mobile (320px), tablet (768px), desktop (1024px+).
6. Produce a component decomposition map: which React/Vue/Angular components make up each view.
7. Components should be named following the architecture plan — use the same names as the eventual code.
8. Include interactive states: hover, focus, disabled, loading, error, empty state.
9. Use the project's design system/tokens if available — colors, typography, spacing.
10. Save previews to `.ai/previews/` with descriptive filenames.
11. The preview is for user approval BEFORE scaffolding — get sign-off on the layout and component structure.
12. Include a legend/annotation layer showing component boundaries and names.
