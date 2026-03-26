---
description: "Next.js coding conventions and best practices. Use when working with Next.js App Router projects."
applyTo: "**/*.tsx,**/*.ts"
---

# Next.js Conventions

- Use the App Router (`app/` directory) exclusively. Never use the Pages Router (`pages/`) in new projects — it is legacy and will not receive new features
- All components in the `app/` directory are Server Components by default. Add `"use client"` at the top of a file only when the component uses hooks, browser APIs, event handlers, or React Context
- Keep `"use client"` boundaries as low as possible in the component tree. Wrap only the interactive leaf component, not an entire page or layout
- Fetch data directly in Server Components using `async`/`await` with `fetch()` or database queries. Never use `getServerSideProps`, `getStaticProps`, or `getInitialProps` — they do not exist in the App Router
- Use the extended `fetch()` API with `next` options for caching control: `fetch(url, { next: { revalidate: 3600 } })` for ISR, `{ cache: 'no-store' }` for dynamic data, or `{ cache: 'force-cache' }` for static data
- Define route handlers in `app/api/{route}/route.ts` exporting named functions matching HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. Never use default exports for API routes
- Use `NextRequest` and `NextResponse` from `next/server` in route handlers and middleware. Never use the raw Node.js `req`/`res` objects in App Router code
- Create `loading.tsx` files for route segments to show instant loading UI via React Suspense. Place them at each layout boundary where data fetching occurs
- Create `error.tsx` files (must be a Client Component with `"use client"`) to handle runtime errors in route segments. Always provide a retry mechanism via the `reset` function parameter
- Create `not-found.tsx` files to handle 404 states. Trigger them explicitly with `notFound()` from `next/navigation` when a resource lookup fails
- Use `layout.tsx` for persistent UI that wraps child routes (navigation, sidebars). Layouts preserve state across navigations — never use them for per-page data that should re-fetch
- Use `template.tsx` instead of `layout.tsx` when you need a fresh component instance on every navigation (e.g., enter animations, per-page effects that must re-mount)
- Define page metadata using the `metadata` export (static) or `generateMetadata` function (dynamic) in `page.tsx` and `layout.tsx`. Never use `<Head>` from `next/head` — it does not work in the App Router
- Use `next/image` for all images. Always provide `width` and `height` (or `fill` with a sized container). Set `priority` on above-the-fold images (LCP candidates) to preload them
- Use `next/font` to load fonts. Import and configure fonts in the root layout, then apply the CSS variable to the `<html>` element. Never use `@import` or `<link>` for Google Fonts — it causes layout shift
- Use Server Actions (functions marked with `"use server"`) for form submissions and data mutations. Define them in separate files (`actions.ts`) or inline in Server Components. Always validate input with `zod` or equivalent before processing
- Never expose raw database queries or sensitive logic in Server Actions without authentication and authorization checks — Server Actions are publicly accessible HTTP endpoints
- Use `redirect()` from `next/navigation` for server-side redirects in Server Components and Server Actions. Use `useRouter().push()` only for client-side programmatic navigation
- Use `usePathname()`, `useSearchParams()`, and `useParams()` from `next/navigation` for reading route information in Client Components. Never use `window.location` directly
- Define middleware in `middleware.ts` at the project root. Use it for authentication, redirects, headers, and geolocation — not for data fetching or heavy computation
- Use `matcher` config in middleware to scope it to specific routes. Never let middleware run on static assets (`_next/static`, `_next/image`, `favicon.ico`)
- Prefix environment variables with `NEXT_PUBLIC_` only when they must be available in client-side code. Server-only secrets must never use the `NEXT_PUBLIC_` prefix — they would be bundled into the client
- Use `unstable_cache` or `fetch` caching for expensive server-side computations that can be cached across requests. Always set `revalidate` or `tags` for cache invalidation
- Use `revalidatePath()` and `revalidateTag()` in Server Actions and route handlers to invalidate cached data on mutations. Prefer tag-based revalidation for fine-grained control
- Use parallel routes (`@slot` folders) for simultaneously rendering multiple pages in the same layout (dashboards, modals alongside content). Define `default.tsx` for each slot as a fallback
- Use intercepting routes (`(.)`, `(..)`, `(...)` conventions) for modal patterns where a route can be rendered inline on soft navigation but as a full page on hard navigation
- Use route groups (`(groupName)` folders) to organize routes without affecting the URL structure. Use them to apply different layouts to different sections
- Place shared components in `components/` or `ui/` outside the `app/` directory. Only files named `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`, `route.ts`, and `template.tsx` have special meaning inside `app/`
- Use `generateStaticParams` in dynamic route segments (`[slug]/page.tsx`) to statically generate pages at build time. Return all valid params to enable full static generation
- Use `dynamic = 'force-dynamic'` or `dynamic = 'force-static'` route segment config only when the automatic behavior detection is insufficient. Prefer letting Next.js detect the rendering strategy automatically
- Use `next/link` for all internal navigation. Always use `<Link href="...">` — never `<a>` tags for internal routes. Set `prefetch={false}` only for rarely-visited links to save bandwidth
- Never import server-only modules (database clients, `fs`, Node APIs) in files that have `"use client"`. Use the `server-only` package to poison imports: `import 'server-only'` at the top of server-only modules
- Use `Suspense` boundaries with meaningful fallbacks around async Server Components and `use(promise)` calls. Group related data fetches in the same component to avoid request waterfalls
- Colocate data fetching with the component that uses it. Fetch in the Server Component that renders the data, not in a parent that passes it down. Next.js deduplicates identical `fetch` calls automatically
- Use `cookies()` and `headers()` from `next/headers` to read request data in Server Components. Calling these opts the route into dynamic rendering — only use them when static generation is not needed
