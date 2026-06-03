# Rendering models: how each stack passes or fails Reach

Read this when the Step 1b fetch shows content missing from the raw served HTML and you need to map the fix to the framework. The single principle underneath all of it:

> **The primary content must be in the HTML the server sends, before any JavaScript runs.** A crawler's first (and sometimes only) view of a page is that raw response. If your content is not in it, you are betting your visibility on the crawler choosing to execute your JavaScript — a bet you will often lose.

---

## The four rendering strategies

| Strategy | Where HTML is built | Content in raw response? | Reach risk |
|---|---|---|---|
| **SSG** (static generation) | Build time, ahead of requests | Yes | Low |
| **SSR** (server-side rendering) | Per request, on the server | Yes | Low |
| **CSR** (client-side rendering) | In the browser, after JS loads | **No** — empty shell | **High** |
| **Hydration** (SSR/SSG + JS) | Server first, JS "wakes it up" | Yes (server part) | Low, if content is in the server part |

The trap is CSR. An SPA (single-page app) ships a near-empty `<div id="root"></div>` and a JavaScript bundle. A human's browser runs the bundle and fills the page. Many crawlers do not run it, run it late, or run it under a budget — so they index the empty shell.

### "But Google renders JavaScript now"
It can, on a deferred second pass, with no guarantee of timeliness or completeness — and many other crawlers (including several AI answer-engine crawlers) render little or no JavaScript at all. Relying on client rendering is relying on the most generous possible crawler behaving perfectly. Server-render the content and the question disappears. Do not let "Google can render JS" become an excuse to ship an empty shell.

---

## Per-framework diagnosis and fix

### Next.js — App Router (`app/` directory) — *the default assumption for this user*
- **Model:** Server Components by default; they render on the server, so content should be in the raw HTML out of the box.
- **How it still fails Reach:**
  - A `"use client"` directive placed at the top of a `page.tsx` or, worse, a `layout.tsx`, turning a whole subtree client-side.
  - Fetching content in a `useEffect`/client hook instead of in a server component or an `async` server fetch — so the data only arrives after hydration.
  - Routes forced dynamic/client in a way that strips content from the initial paint.
- **Fix:**
  - Do data fetching in server components (`async` function components, `fetch`/DB calls server-side). Let the content render on the server.
  - Push `"use client"` down to the smallest interactive leaf components (a button, a form, a carousel) — never on the page/layout wrapper unless genuinely required.
  - Keep above-the-fold, indexable content out of client-only conditional rendering.
- **Verify:** re-fetch the route; the body copy and `<h1>` must be in the raw HTML.

### Next.js — Pages Router (`pages/` directory)
- **Model:** CSR by default unless you export a data function.
- **Fix:** use `getServerSideProps` (per-request data) or `getStaticProps` (build-time data) so the initial HTML carries the content. Replace `useEffect`-based content fetching with these. Use `getStaticPaths` for dynamic static routes.

### Vite SPA (React/Vue/Svelte via Vite) — **high risk**
- **Model:** pure CSR. `index.html` is a shell; everything is rendered client-side. The raw response has no content.
- **Fix (significant — flag as a human decision, present the options):**
  1. **Migrate to a meta-framework** (Next.js, Astro, Remix, SvelteKit, Nuxt). Best long-term answer; largest change.
  2. **Add SSR to the existing Vite app** with `vike` (formerly `vite-plugin-ssr`). Keeps Vite; adds a server render path.
  3. **Pre-render known routes to static HTML** at build time (e.g. a prerender plugin / `vite-plugin-prerender`-style approach, or a headless-browser prerender step). Good for a fixed set of marketing/content routes; weak for highly dynamic ones.
- Do not silently re-architect. Lay out the trade-offs and let the user choose.

### Create React App (CRA) — **high risk**
- Same shape as Vite SPA: empty shell, client-rendered. CRA is effectively unmaintained — the honest recommendation is to migrate to Next.js or Astro. Otherwise add a prerender step. Flag as a human decision.

### Astro
- **Model:** ships zero JS by default; renders to static HTML (SSG) or SSR. Low risk.
- **How it fails Reach:** a component using a client directive (`client:only`) for content that should be static — `client:only` renders nothing on the server. Use `client:load`/`client:visible` for interactivity on top of server-rendered content, and reserve `client:only` for genuinely client-only widgets.

### Nuxt (Vue)
- **Model:** SSR/SSG by default (universal rendering). Low risk.
- **How it fails Reach:** `ssr: false` (SPA mode) in `nuxt.config`, or `<client-only>` wrapping real content. Re-enable SSR or move content out of client-only wrappers.

### SvelteKit
- **Model:** SSR by default. Low risk.
- **How it fails Reach:** `export const ssr = false` on a route, or loading content only in `onMount` (client lifecycle). Use `load` functions (which run on the server for the initial request) and keep `ssr` enabled for content routes.

### Remix / React Router (framework mode)
- **Model:** SSR via route `loader`s. Low risk.
- **How it fails Reach:** fetching in `useEffect` instead of a `loader`. Move data fetching into `loader`s so it is server-rendered.

### Gatsby
- **Model:** SSG. Low risk for static content; data is baked at build time.
- **How it fails Reach:** content that only appears client-side after rehydration, or stale builds. Ensure indexable content comes from the build-time data layer.

### Plain static HTML / SSGs (Hugo, Eleventy, Jekyll)
- **Model:** static HTML. Reach-rendering is fine by construction. Focus diagnosis on robots, sitemap, status codes, and canonicals.

---

## Anti-patterns — never do these
- **Cloaking:** serving crawlers different content than users. Black-hat, against the method, and increasingly detectable.
- **Hidden content for bots:** stuffing text only crawlers see. Same problem.
- **`user-agent` sniffing to server-render only for bots** ("dynamic rendering"): once a stopgap, now discouraged and fragile. Server-render for everyone instead.

The fix is always the same shape: make the real content part of the server response that both users and crawlers receive.
