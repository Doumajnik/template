+++
id = "agents/accessibility"
title = "Accessibility Agent Rules"
agents = ["accessibility"]
technologies = ["all"]
category = "rule"
tags = ["accessibility"]
version = 2
+++

### Accessibility Agent Rules

1. Audit all UI components for WCAG 2.1 AA compliance as the minimum standard.
2. Verify all interactive elements are keyboard-accessible: tab order, focus indicators, keyboard shortcuts.
3. Check that all images have meaningful `alt` text — decorative images should use `alt=""`.
4. Verify color contrast ratios: normal text ≥4.5:1, large text ≥3:1 against background.
5. Check for proper ARIA attributes: `role`, `aria-label`, `aria-describedby`, `aria-live` for dynamic content.
6. Verify form elements have associated labels — never rely on placeholder text alone.
7. Check that error messages are announced to screen readers using `aria-live="assertive"`.
8. Verify the page structure uses semantic HTML: `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>`.
9. Check that modals trap focus and return focus to the trigger element when closed.
10. Verify responsive design: content is usable at 200% zoom, no horizontal scrolling at 320px viewport.
11. Test with screen reader (NVDA/VoiceOver) for critical user flows: login, navigation, forms.
12. Produce findings categorized by WCAG success criterion (e.g., 1.4.3 Contrast).
