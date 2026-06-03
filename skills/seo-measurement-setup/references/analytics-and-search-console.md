# Analytics, Search Console & web-vitals — install patterns

Read this to install measurement plumbing correctly and verify it on the served output. Scope reminder: this is **setup only**. Interpreting the data is live-data work, outside the build.

---

## GA4 (Google Analytics 4)

Universal Analytics (the old `analytics.js`/`ga()`) is **defunct** — if you find a UA tag, remove it. Use **GA4** (`gtag.js` with a `G-XXXXXXX` Measurement ID), installed **once**.

### Next.js (App Router) — preferred
Use `@next/third-parties` (official, optimised):
```tsx
// app/layout.tsx
import { GoogleAnalytics } from '@next/third-parties/google'

export default function RootLayout({ children }) {
  return (
    <html lang="en-GB">
      <body>{children}</body>
      <GoogleAnalytics gaId="G-XXXXXXX" />
    </html>
  )
}
```
Or with `next/script` if you prefer manual control:
```tsx
import Script from 'next/script'
// in the root layout, once:
<Script src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX" strategy="afterInteractive" />
<Script id="ga4" strategy="afterInteractive">{`
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
`}</Script>
```
Place it **once** in the root layout — not per page (which double-counts).

### Generic (any site)
The standard `gtag.js` snippet in `<head>`, once, site-wide. On hosted platforms, use the platform's analytics field or a tag-manager integration rather than editing code.

### The common failures
- **Two tags** (e.g. one in the theme + one via a plugin/tag manager) → every event double-counted. Find and remove the duplicate.
- **Legacy UA tag** still present → remove.
- **Client-only injection that never loads** (or is blocked before consent) → confirm it actually fires.
- **Wrong Measurement ID** (a staging/other-project ID) → confirm the right `G-` ID.

---

## Google Search Console verification

GSC is where the user sees real indexing/performance data. Verification proves they own the site. Methods:
- **HTML meta tag** — easiest for a code site. Next.js via the Metadata API:
  ```tsx
  export const metadata = { verification: { google: 'your-verification-token' } }
  ```
  (renders `<meta name="google-site-verification" content="…">`).
- **HTML file** — upload the provided file to the site root.
- **DNS record** — a TXT record (verifies the whole domain; good for domain-wide).
- **Via GA4** — if analytics is already installed and the user has access.

The agent puts the **token/method in place**; the **user completes verification** in their GSC account (a live step) and then submits the sitemap there.

---

## Core Web Vitals (field) reporting — optional

Real-user CWV (the field score Google uses) only exists once real users hit the live site. You can wire reporting so the user sees it over time:
- **Next.js:** `useReportWebVitals` (from `next/web-vitals`) to forward LCP/INP/CLS to GA4.
- **Generic:** the `web-vitals` library reporting to your analytics endpoint.

Be explicit: this *enables* the user to see field CWV accruing; it does not produce a score at build time. Lab CWV (Lighthouse) is the build-time proxy (see the Read rung's `page-experience.md`).

---

## Verifying setup on the served output

```bash
# exactly one GA4 tag?
curl -sL https://example.com | grep -o "G-[A-Z0-9]\{6,\}" | sort -u
# search-console verification token present?
curl -sL https://example.com | grep -i "google-site-verification"
```
```powershell
(Invoke-WebRequest "https://example.com" -UseBasicParsing).Content |
  Select-String -Pattern "G-[A-Z0-9]{6,}|google-site-verification"
```

Confirm:
- [ ] Exactly **one** GA4 snippet with the correct `G-` ID (no duplicates, no legacy UA).
- [ ] If a network/browser MCP is available: the analytics request **fires once** on load.
- [ ] GSC verification token/method in place (the user then verifies in GSC).
- [ ] Sitemap reachable and referenced in `robots.txt`, ready to submit.
- [ ] No tracking added that bypasses a required consent mechanism (flag consent gaps to the user).

Record what's set up in `.seo/` so progression runs confirm the tags didn't regress (a redeploy dropping analytics is common). Then hand off: the instruments are in; **reading them is the live-data discipline, not the build.**
