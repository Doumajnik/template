---
description: "React coding conventions and best practices. Use when writing, reviewing, or refactoring React components."
applyTo: "**/*.tsx,**/*.jsx"
---

# React Conventions

- Use function components exclusively. Never use class components — they cannot use hooks and have a larger API surface
- Name components with PascalCase. Name hook files and utility files with camelCase. Component files must match the component name: `UserProfile.tsx` exports `UserProfile`
- Define props as a `type` or `interface` named `{ComponentName}Props`. Destructure props in the function signature: `function UserCard({ name, role }: UserCardProps)`
- Never mutate state directly. Always use the setter from `useState` or dispatch from `useReducer`. For objects and arrays, spread into a new reference
- Call hooks only at the top level of function components or custom hooks. Never call hooks inside conditions, loops, or nested functions
- Use `useEffect` only for synchronizing with external systems (DOM manipulation, subscriptions, network). Never use it as a "watcher" to derive state from other state — compute it during render instead
- Always provide a dependency array to `useEffect`, `useMemo`, and `useCallback`. Omitting it causes the effect to run on every render. Lint with `react-hooks/exhaustive-deps`
- Clean up side effects in `useEffect` by returning a cleanup function. This prevents memory leaks from subscriptions, timers, and event listeners
- Use `useCallback` only when passing callbacks to memoized child components or when the callback is a dependency of another hook. Do not wrap every function in `useCallback` by default
- Use `useMemo` only when computing values that are expensive (O(n²)+, large list transformations) or when a stable reference is required for a dependency array. Avoid premature memoization
- Wrap components in `React.memo` only when they re-render frequently with the same props and rendering is measurably expensive. Profile before memoizing
- Always provide a stable, unique `key` prop when rendering lists. Never use array index as `key` unless the list is static and never reordered, filtered, or prepended
- Lift state up only as far as the nearest common ancestor that needs it. Prefer colocation — keep state close to where it is used
- Use `useReducer` over `useState` when state has complex update logic, multiple sub-values, or when the next state depends on the previous state
- Create custom hooks (`use{Name}`) to extract reusable stateful logic from components. A custom hook must call at least one other hook — otherwise it is a plain function, not a hook
- Use React Context for low-frequency global state (theme, locale, auth). Never use Context for high-frequency updates (form inputs, animations) — it forces all consumers to re-render
- Split large Context providers by domain. Never create a single "global" Context that holds unrelated state — changes to any field re-render all consumers
- Use controlled components for form inputs: value and onChange managed by React state. Use uncontrolled components with `useRef` only for file inputs or third-party integrations that require DOM access
- Handle form submission with `onSubmit` on the `<form>` element, not `onClick` on the submit button. Always call `event.preventDefault()` in the handler
- Use `React.lazy()` with `<Suspense>` for code-splitting routes and heavy components. Provide a meaningful fallback UI, not an empty fragment
- Use `forwardRef` when creating reusable components that wrap native DOM elements (inputs, buttons) so parent components can attach refs for focus management and measurement
- Use error boundaries to catch rendering errors in subtrees. Create an error boundary component using `class` (the one exception to "no classes") or use `react-error-boundary` library. Place boundaries around route segments and independent widget areas
- Always add `aria-label`, `aria-labelledby`, or visible `<label>` to interactive elements. Use semantic HTML (`<button>`, `<nav>`, `<main>`, `<section>`) instead of `<div>` with click handlers
- Use `onClick` handlers only on interactive elements (`<button>`, `<a>`). Never attach `onClick` to `<div>` or `<span>` — if needed, add `role="button"`, `tabIndex={0}`, and `onKeyDown` for keyboard access
- Colocate component, styles, tests, and types in the same directory. Prefer `components/UserCard/UserCard.tsx` with `UserCard.test.tsx` and `UserCard.module.css` alongside
- Use conditional rendering with early returns or ternaries. Avoid deeply nested `&&` chains — extract conditions into descriptively named variables or early-return patterns
- Avoid inline object and array literals in JSX props (`style={{...}}`, `options={[...]}`). Hoist them to module scope or memoize them to prevent unnecessary child re-renders
- Prefer composition over prop drilling. Use `children` and render props to compose behavior. Pass components as props (`icon={<ChevronIcon />}`) instead of configuration objects
- Never call `setState` during render without a condition guard — it causes infinite re-render loops. If you need derived state, compute it as a `const` during render
- Use `useId()` to generate unique IDs for accessibility attributes (`htmlFor`, `aria-describedby`). Never hardcode IDs — they collide when a component is rendered multiple times
- Use `startTransition` or `useTransition` for non-urgent state updates (search filtering, tab switching) to keep the UI responsive to user input during expensive renders
- Use `useDeferredValue` for deferring expensive re-renders of child trees that depend on fast-changing values (e.g., search input driving a filtered list)
- Use `useRef` for mutable values that do not trigger re-renders (previous values, interval IDs, DOM references). Never use `useRef` as a replacement for state when the UI depends on the value
- Prefer server components for data fetching and static content in frameworks that support them (Next.js). Add `"use client"` only to components that use hooks, browser APIs, or event handlers
- Test components with React Testing Library. Query by accessible role, label, or text — never by class name, test ID (unless no accessible alternative exists), or component internals
- Avoid `dangerouslySetInnerHTML` unless the content is sanitized with DOMPurify or equivalent. Never pass user input directly — this creates XSS vulnerabilities
