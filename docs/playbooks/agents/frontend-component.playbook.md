+++
id = "agents/frontend-component"
title = "Frontend Component Agent Playbook"
agents = ["frontend-component"]
technologies = ["react", "typescript", "css", "html"]
category = "rule"
tags = ["frontend", "components", "ui", "accessibility", "state-management"]
version = 1
+++

### Component Structure

- Name component files `ComponentName.tsx` using PascalCase — one component per file.
- Co-locate tests (`ComponentName.test.tsx`), stories (`ComponentName.stories.tsx`), and styles in the same folder.
- Export components as named exports — use default exports only for lazy-loaded route pages.
- Define a TypeScript `interface` for props named `{ComponentName}Props` — always export it.
- Declare prop interfaces above the component, not inline in the function signature.
- Forward refs on components that wrap native HTML elements using `React.forwardRef`.
- Create an `index.ts` barrel file in each component folder that re-exports the component and its types.

### Accessibility

- Use semantic HTML elements (`<button>`, `<nav>`, `<dialog>`) before adding ARIA roles.
- Add `aria-label` or `aria-labelledby` to every interactive element that lacks visible text.
- Implement keyboard navigation for all custom widgets: Tab, Enter, Space, Escape, Arrow keys.
- Ensure visible focus indicators on all interactive elements — never set `outline: none` without a replacement.
- Maintain color contrast ratios: normal text ≥ 4.5:1, large text ≥ 3:1, UI components ≥ 3:1.
- Announce dynamic content changes with `aria-live` regions — use `polite` for status, `assertive` for errors.
- Trap focus inside modals and dialogs — restore focus to the trigger element on close.

### State Management

- Default to local state (`useState`/`useReducer`) — lift only when siblings share the state.
- Never store derived data in state — compute it during render from existing state or props.
- Use React Context for cross-cutting data (theme, locale, auth) — never for frequently-updating values.
- Separate server state (React Query / SWR) from UI state (open/closed, selected index).
- Keep side effects in `useEffect` with explicit dependency arrays — never suppress the linter.
- Extract complex state logic into custom hooks named `use{Feature}` — components should be thin.

### Styling

- Use the project's established styling approach (CSS Modules, Tailwind, styled-components) — never mix systems.
- Apply design tokens (spacing, color, typography) from the design system — never hardcode raw values.
- Build mobile-first responsive layouts — use `min-width` media queries for progressive enhancement.
- Avoid inline styles for reusable components — reserve inline styles for truly dynamic values only.

### Performance

- Profile before memoizing — add `React.memo`, `useMemo`, `useCallback` only for measurable gains.
- Lazy-load heavy or below-the-fold components with `React.lazy` and `Suspense`.
- Virtualize lists exceeding 100 items using a virtualization library (react-window, TanStack Virtual).
- Import only what you need from libraries — avoid full-library imports that bloat the bundle.
- Optimize images with responsive `srcSet`, `loading="lazy"`, and framework-specific components (`next/image`).

### Testing

- Test user-visible behavior, not implementation details — query by role, label, or text, never by class or test ID.
- Write interaction tests for every clickable, typeable, and navigable element.
- Run automated accessibility checks (`axe-core` / Testing Library `toHaveNoViolations`) in every test file.
- Test all component states: loading, error, empty, populated, disabled.
- Never use snapshot tests — they break on every style change and provide no behavioral coverage.
- Assert that keyboard navigation works: Tab moves focus, Enter/Space activates, Escape dismisses.
