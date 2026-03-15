+++
id = "agents/accessibility"
title = "Accessibility Agent Rules"
agents = ["accessibility"]
technologies = ["all"]
category = "rule"
tags = ["accessibility"]
version = 4
+++

### Accessibility Agent Rules

- Audit all UI components for WCAG 2.1 AA compliance as the minimum standard.
- Verify all interactive elements are keyboard-accessible: tab order, focus indicators, keyboard shortcuts.
- Check that all images have meaningful `alt` text — decorative images should use `alt=""`.
- Verify color contrast ratios: normal text ≥4.5:1, large text ≥3:1 against background.
- Check for proper ARIA attributes: `role`, `aria-label`, `aria-describedby`, `aria-live` for dynamic content.
- Verify form elements have associated labels — never rely on placeholder text alone.
- Check that error messages are announced to screen readers using `aria-live="assertive"`.
- Verify the page structure uses semantic HTML: `<nav>`, `<main>`, `<header>`, `<footer>`, `<section>`, `<article>`.
- Check that modals trap focus and return focus to the trigger element when closed.
- Verify responsive design: content is usable at 200% zoom, no horizontal scrolling at 320px viewport.
- Test with screen reader (NVDA/VoiceOver) for critical user flows: login, navigation, forms.
- Produce findings categorized by WCAG success criterion (e.g., 1.4.3 Contrast).
- Verify skip navigation links exist to bypass repeated content blocks (WCAG 2.4.1 Bypass Blocks).
- Ensure no keyboard traps exist — focus must always be movable away from any component using standard keys (WCAG 2.1.2).
- Check that touch/click target sizes are at least 44×44 CSS pixels for pointer inputs (WCAG 2.5.5 Target Size).
- Verify color is not the only visual means of conveying information — use icons, text, or patterns alongside color (WCAG 1.4.1).
- Check that the page declares `lang` attribute on `<html>` and uses `lang` on passages in different languages (WCAG 3.1.1, 3.1.2).
- Verify content appearing on hover or focus is dismissible (Escape key), hoverable (user can move pointer over it), and persistent (stays visible until dismissed) (WCAG 1.4.13).
- Check non-text contrast: UI components (borders, focus indicators) and meaningful graphics must have ≥3:1 contrast ratio against adjacent colors (WCAG 1.4.11).
- Verify input fields collecting user information use `autocomplete` attributes to identify purpose programmatically (WCAG 1.3.5 Identify Input Purpose).
- Implement accordion widgets using `aria-expanded`, `aria-controls`, and `role="region"` to associate heading buttons with content panels — toggle `aria-expanded` on activation (WAI-ARIA APG Accordion Pattern).
- Combobox widgets must use `role="combobox"` with `aria-expanded`, `aria-autocomplete`, and `aria-activedescendant` to manage popup list interaction without moving DOM focus (WAI-ARIA APG Combobox Pattern).
- Tab widgets must use `role="tablist"`, `role="tab"`, and `role="tabpanel"` with `aria-selected` and `aria-controls` — arrow keys navigate between tabs, Tab key moves focus to the active panel content (WAI-ARIA APG Tabs Pattern).
- Verify landmark roles are used correctly: exactly one `<main>` per page, multiple `<nav>` elements distinguished with `aria-label`, and `role="banner"` / `role="contentinfo"` not nested inside other landmark regions.
- Use `aria-live="polite"` for non-urgent dynamic content updates (search results, status messages) and `aria-live="assertive"` only for time-sensitive alerts — overusing assertive disrupts the screen reader's current output.
- Prefer native HTML elements over ARIA roles — "No ARIA is better than bad ARIA" (W3C APG). Use native `<button>`, `<select>`, `<input>`, `<dialog>` before adding custom ARIA roles, states, or properties.
