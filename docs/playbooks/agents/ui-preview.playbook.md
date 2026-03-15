+++
id = "agents/ui-preview"
title = "UI Preview Agent Rules"
agents = ["ui-preview"]
technologies = ["all"]
category = "rule"
tags = ["ui-preview"]
version = 4
+++

### UI Preview Agent Rules

- Generate an interactive HTML/CSS preview mockup — not just a screenshot or static wireframe.
- Include all major views/pages from the architecture plan — not just the main page.
- Use semantic HTML with proper structure: `<nav>`, `<main>`, `<form>`, `<button>` — not `<div>` for everything.
- Include realistic placeholder content — not just "Lorem ipsum" but contextually appropriate data.
- Include responsive breakpoints: mobile (320px), tablet (768px), desktop (1024px+).
- Produce a component decomposition map: which React/Vue/Angular components make up each view.
- Components should be named following the architecture plan — use the same names as the eventual code.
- Include interactive states: hover, focus, disabled, loading, error, empty state.
- Use the project's design system/tokens if available — colors, typography, spacing.
- Save previews to `.ai/previews/` with descriptive filenames.
- The preview is for user approval BEFORE scaffolding — get sign-off on the layout and component structure.
- Include a legend/annotation layer showing component boundaries and names.
- Organize components using atomic design hierarchy: atoms (buttons, inputs, labels) → molecules (search form, card) → organisms (header, product grid) → templates (page layouts) → pages (with real content).
- Each molecule and organism should follow the single responsibility principle — one clear purpose per component; avoid burdening a single pattern with too much complexity.
- Include content structure skeletons that show dynamic content placeholders separately from pages with final representative content — both views are needed for design validation.
- Demonstrate content variations and edge cases — show how components handle long text, empty states, single item vs. many items, missing images, and admin vs. regular user views.
- Use design tokens (spacing, color, typography, border-radius) as CSS custom properties or variables — never hardcode visual values; ensure the preview is theme-able.
- Include navigation flow mockups showing transitions and relationships between views — not just isolated static pages but connected user journeys.
- Preview must render its core content and layout without JavaScript — use progressive enhancement so the structural review is possible even if scripts fail to load.
- Write component stories (one story per meaningful state) alongside preview mockups — each story captures a rendered state with specific args, enabling systematic visual validation of every component variant.
- Include play functions (interaction tests) in stories for interactive components — simulate user actions (clicks, form fills, keyboard navigation) and assert DOM outcomes to catch behavioral regressions in the preview.
- Use decorators in previews to wrap components with required context providers (theme, layout, routing, data providers) — components rendered without their expected context produce misleading preview results.
- Define story parameters for visual testing configuration — specify backgrounds, viewport sizes, and accessibility check options per-story to enable automated visual regression testing against the preview baseline.
- Reuse child component story args in composite component previews — import Button story args into ButtonGroup previews to keep data definitions DRY and ensure child component changes automatically propagate to parent stories.
- Include stories for composite multi-component scenarios — preview parent components (e.g., List with ListItem children) with varying numbers of children and combinations of child states (selected, unselected, disabled).
