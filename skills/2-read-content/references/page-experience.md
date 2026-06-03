# Page experience: mobile-friendliness & Core Web Vitals

Read this for the speed-and-usability half of Read. Page experience isn't a ladder *dependency* — a slow or clumsy page still gets reached, read, and indexed — but it's a genuine ranking signal and, crucially, a **build-time** problem an agent can fix. It matters identically for classic ranking and for AI search (an answer engine still prefers a fast, usable source). As always, judge it on what's actually **served/rendered**, not on intentions in the source.

> What's build-time vs live: you can fix the **known causes** of poor performance in the code (this file). The **field score** — real users' Core Web Vitals measured over 28 days in the Chrome UX Report — is live data you can't confirm at build time. Fix the causes here; the live score is live data, on the other side of the boundary.

---

## Mobile-friendliness (Google indexes mobile-first)

Google predominantly crawls and indexes the **mobile** version of a page, so the mobile rendering is the one that counts — and content or links present only on desktop can be missed.

Check and fix:
- **Viewport meta** — `<meta name="viewport" content="width=device-width, initial-scale=1">` must be present. Without it, mobile browsers render at desktop width and zoom out.
- **Responsive layout** — the page reflows to narrow screens: no fixed pixel widths forcing horizontal scroll, no content cut off. Test by fetching/rendering at a ~375px width.
- **Legible text** — readable without zooming (don't set tiny base font sizes).
- **Tap targets** — interactive elements large enough and not crammed together.
- **Parity** — the mobile view contains the same primary content and links as desktop (don't hide indexable content behind desktop-only rendering).

A correct viewport and obvious responsive fixes are safe to apply. A full responsive redesign is a human decision — flag it with specifics.

---

## Core Web Vitals — the three metrics

| Metric | Measures | Good | Common build-time causes |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | How fast the main content renders | ≤ 2.5 s | Oversized hero images, render-blocking CSS/JS, slow server/TTFB, client-rendered content (a Reach problem too) |
| **INP** (Interaction to Next Paint) | How fast the page responds to input | ≤ 200 ms | Heavy/long JavaScript tasks, oversized hydration, expensive event handlers |
| **CLS** (Cumulative Layout Shift) | How much the layout jumps while loading | ≤ 0.1 | Images/embeds without dimensions, late-loading fonts, injected banners/ads pushing content |

*(INP replaced FID as the responsiveness metric in 2024.)* Diagnose with a Lighthouse/PageSpeed run if a server is available; otherwise inspect for the causes above directly in the served page.

---

## The fixes (and the Next.js tool for each)

### Images — usually the biggest single win
- Serve **appropriately sized** images (don't ship a 3000px image into a 400px slot) in **modern formats** (WebP/AVIF).
- **Lazy-load** below-the-fold images; eagerly load the LCP image.
- Always set **width/height** (or a reserved aspect ratio) so the browser doesn't reflow when the image arrives — a top CLS cause.
- **Next.js:** `next/image` does sizing, lazy-loading, modern formats, and reserves space automatically. Prefer it over raw `<img>`. Mark the LCP image with `priority`.

### Fonts
- Avoid invisible or shifting text while a web font loads; use `font-display: swap` and preload critical fonts; self-host to avoid a third-party round-trip.
- **Next.js:** `next/font` self-hosts, sets sizing to avoid layout shift, and removes the extra network request.

### JavaScript
- Cut render-blocking and oversized client bundles — the same discipline as Reach: keep work on the server, push `"use client"` down to small interactive leaves, and code-split heavy components (`next/dynamic`) so they don't block first paint or interaction.
- Heavy interactivity that tanks INP is a **flag-and-discuss**, not a silent rewrite — explain the trade-off.

### CSS & layout
- Reserve space for anything that loads late (images, embeds, ads, dynamically injected UI) to keep CLS low.
- Minimise render-blocking CSS; inline only what's needed for first paint where practical.

### Server / delivery
- A slow time-to-first-byte caps LCP regardless of front-end work — note hosting/CDN/caching causes for the user even if they're outside the code you can change.

---

## Verifying page experience on the rendered output
- **Mobile:** confirm the viewport meta is in the served HTML and the page reflows at ~375px without horizontal scroll or clipped content.
- **Images:** spot-check that images are sized, lazy-loaded where appropriate, and carry dimensions (no CLS).
- **Re-run Lighthouse/PageSpeed** (lab data) to confirm the causes you fixed are gone and the lab scores moved.
- **Be honest about field data:** tell the user the lab/build fixes are done, but the *field* Core Web Vitals (real users, over time) show up only after the change is live and traffic accrues — that measurement is live data, not a build-time guarantee.

A page passes the page-experience part of Read when it's mobile-friendly in the served output and the known Core Web Vitals causes are resolved. Then continue up the ladder to **Understand**.
