# Localization Playbook

## Externalization Rules

- Every string visible to a human end-user lives in the catalog (`locales/en.json`, `messages/en.po`, etc.).
- Keys are namespaced by feature: `checkout.button.submit`, not `submit`.
- Default locale is `en` (or project-defined); all other locales are translations of `en`.

## Format Anti-Patterns (forbid)

| Bad | Good |
| --- | --- |
| `"Hello " + name` | `t("greeting", { name })` |
| `n === 1 ? "1 item" : n + " items"` | `t("cart.items", { count: n })` with ICU plural |
| `date.toLocaleDateString("en-US")` hardcoded | `Intl.DateTimeFormat(currentLocale).format(date)` |
| `"$" + amount` | `Intl.NumberFormat(locale, { style: "currency", currency: ccy }).format(amount)` |
| `margin-left: 8px` (in RTL contexts) | `margin-inline-start: 8px` |
| `<img src="arrow-right.svg">` | direction-aware: flip in RTL or use logical name |

## ICU Plural Example

```json
{
  "cart.items": "{count, plural, =0 {Your cart is empty} one {# item} other {# items}}"
}
```

## Translator Context Comments

Every key gets a comment for translators:

```json
{
  "// checkout.button.submit": "Primary CTA on checkout page. Max 18 chars on mobile.",
  "checkout.button.submit": "Place order"
}
```

## Text Expansion Budget

- Plan for ~30% growth from English to most European languages.
- Critical CTAs / labels: test against German and Russian.
- Truncation policy documented per component (ellipsis, wrap, scale).

## RTL Checklist

- All directional CSS uses logical properties.
- Icons that imply direction (arrows, undo) flip or have RTL variants.
- Numerals: decide upfront — Latin or Arabic-Indic — and document.
- Bidi text edge cases: usernames, mixed-script content.

## Coordination

- **Frontend Component Agent** — components ship i18n-ready by default.
- **Accessibility Agent** — screen reader announcements also use the catalog.
- **UX Research** — locale-specific usability concerns surface here.
- **Doc Updater** — maintains the catalog inventory in `docs/I18N_REPORT.md`.
