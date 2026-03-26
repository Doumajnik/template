# HTTP Security Headers Reference

Recommended security headers for web applications. For each header: what it prevents, the recommended value, and common mistakes.

---

## Content-Security-Policy (CSP)

**Prevents:** Cross-site scripting (XSS), data injection, clickjacking, unauthorized resource loading.

**Recommended value:**
```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

**Common mistakes:** Using `'unsafe-inline'` or `'unsafe-eval'` in `script-src` (defeats XSS protection). Setting `default-src *` in production. Forgetting `frame-ancestors` (use instead of X-Frame-Options). Not including `base-uri` (allows `<base>` tag hijacking).

---

## Strict-Transport-Security (HSTS)

**Prevents:** Protocol downgrade attacks, cookie hijacking via HTTP, SSL stripping.

**Recommended value:**
```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

**Common mistakes:** Setting `max-age` too low (use ≥1 year / 31536000). Omitting `includeSubDomains` (leaves subdomains vulnerable). Adding `preload` without submitting to the HSTS preload list. Serving HSTS over HTTP (browsers ignore it — must be over HTTPS).

---

## X-Content-Type-Options

**Prevents:** MIME-type sniffing — stops browsers from interpreting files as a different content type than declared.

**Recommended value:**
```
X-Content-Type-Options: nosniff
```

**Common mistakes:** Not setting it at all (browsers may execute uploaded files as scripts). Only setting it on HTML responses (should be on all responses, especially downloads and API endpoints).

---

## X-Frame-Options

**Prevents:** Clickjacking — stops the page from being embedded in iframes on other origins.

**Recommended value:**
```
X-Frame-Options: DENY
```

Use `SAMEORIGIN` only if the application intentionally uses same-origin iframes.

**Common mistakes:** Using `ALLOW-FROM` (deprecated, not supported by modern browsers — use CSP `frame-ancestors` instead). Not setting it at all on auth-sensitive pages. Note: CSP `frame-ancestors` supersedes this header — set both for backward compatibility.

---

## Referrer-Policy

**Prevents:** Leaking sensitive URL paths and query parameters to external sites via the Referer header.

**Recommended value:**
```
Referrer-Policy: strict-origin-when-cross-origin
```

Use `no-referrer` for maximum privacy if cross-origin referrer data is not needed.

**Common mistakes:** Using `unsafe-url` (sends full URL including path and query to all origins). Not setting it (browser defaults vary). Forgetting that tokens or session IDs in URLs will leak via Referer.

---

## Permissions-Policy

**Prevents:** Unauthorized use of browser features (camera, microphone, geolocation, payment, etc.) by the page or embedded iframes.

**Recommended value:**
```
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()
```

Only enable features the application actually needs: `camera=(self)`.

**Common mistakes:** Not setting it (all features available by default to the page and iframes). Being too permissive — enabling features "just in case." Forgetting to restrict features for embedded third-party content.

---

## Cross-Origin-Embedder-Policy (COEP)

**Prevents:** Loading cross-origin resources that don't explicitly grant permission, enabling `SharedArrayBuffer` and high-resolution timers safely.

**Recommended value:**
```
Cross-Origin-Embedder-Policy: require-corp
```

Use `credentialless` if `require-corp` breaks third-party resources that cannot set CORP.

**Common mistakes:** Setting `require-corp` without ensuring all cross-origin resources have appropriate CORP/CORS headers (breaks images, scripts, fonts from CDNs). Not understanding the relationship with COOP — both are needed for cross-origin isolation.

---

## Cross-Origin-Opener-Policy (COOP)

**Prevents:** Cross-origin window attacks — isolates the browsing context so other origins cannot access `window.opener` or similar references.

**Recommended value:**
```
Cross-Origin-Opener-Policy: same-origin
```

**Common mistakes:** Not setting it (leaves window references accessible to cross-origin openers). Using `same-origin` when the app relies on cross-origin popups (OAuth flows — use `same-origin-allow-popups` instead).

---

## Cross-Origin-Resource-Policy (CORP)

**Prevents:** Other origins from loading your resources (images, scripts, fonts) — a complement to CORS on the response side.

**Recommended value:**
```
Cross-Origin-Resource-Policy: same-origin
```

Use `cross-origin` only for resources intentionally shared with other origins (CDN assets, public APIs).

**Common mistakes:** Setting `same-origin` on resources that need to be loaded cross-origin (breaks CDN assets, embedded widgets). Not setting it at all on sensitive resources (allows cross-origin reads in some scenarios).
