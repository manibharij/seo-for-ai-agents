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

For what happens after the server response (hydration, streaming, client-side links, soft 404s, `noindex` or canonicals changed by JavaScript), read `javascript-seo.md` in this folder. This file covers which rendering model each stack uses and how to move content into the server response. Framework facts below verified 2026-10 against each framework's docs.

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
- **Server islands** (`server:defer`) are also missing from the initial HTML. Astro leaves the fallback slot and a script in their place, and the browser fetches the island's HTML after load. Use them for personalised or slow fragments (a basket count, a greeting), never for the primary copy.

### Nuxt (Vue)
- **Model:** SSR/SSG by default (universal rendering). Low risk.
- **How it fails Reach:** `ssr: false` (SPA mode) in `nuxt.config`, or `<client-only>` wrapping real content. Re-enable SSR or move content out of client-only wrappers.

### SvelteKit
- **Model:** SSR by default. Low risk.
- **How it fails Reach:** `export const ssr = false` on a route, or loading content only in `onMount` (client lifecycle). Use `load` functions (which run on the server for the initial request) and keep `ssr` enabled for content routes.

### React Router, framework mode (v7 onward) and Remix v2
- **Model:** SSR through route `loader`s. `ssr` defaults to `true` in `react-router.config.ts`. Low risk. React Router v8 is current (verified 2026-10); Remix v2 apps follow the same model.
- **How it fails Reach:**
  - Fetching in `useEffect` instead of a `loader`. Move data fetching into `loader`s so it is server-rendered.
  - `ssr: false` without `prerender` is **SPA mode**: only the root route is rendered into a single HTML file, and every other route is rendered in the browser. Medium to high risk for content routes.
  - `ssr: false` with `prerender: [...]` prerenders the listed paths and serves an SPA fallback for everything else. Check that every indexable route is in the prerender list.
- **Fix:** keep `ssr: true` for content, or prerender every content path (`prerender` accepts an array or an async function that returns paths).

### Angular (with `@angular/ssr`)
- **Model:** a plain Angular app renders **client-side** only. `ng add @angular/ssr` (or `ng new --ssr`) adds server rendering, with a render mode per route in `app.routes.server.ts`: `RenderMode.Server` (SSR per request), `RenderMode.Prerender` (static at build time) or `RenderMode.Client`.
- **Detect:** the served root element carries `ng-version`. A server-rendered or prerendered page also has `ng-server-context="ssr"` or `"ssg"`; if that attribute is missing, the page was rendered in the browser.
- **How it fails Reach:**
  - No `@angular/ssr` at all: an empty `<app-root>` in the raw HTML. High risk; flag as a human decision.
  - Content routes set to `RenderMode.Client`.
  - `@defer` blocks: during SSR and prerendering they render only their `@placeholder` (or nothing). Enable incremental hydration and give the block `hydrate` triggers if its content must be in the server HTML, or move primary content out of `@defer`.
  - Prerendered parameterised routes set to `fallback: PrerenderFallback.Client`: any path not returned by `getPrerenderParams` is rendered in the browser.
- **Fix:** add `@angular/ssr`, set content routes to `Server` or `Prerender`, and use `provideClientHydration()` so the client reuses the server DOM. Set real status codes per route (a `status` on the server route, or `RESPONSE_INIT`) so missing pages return `404`.

### TanStack Start
- **Model:** SSR by default, with route-level `ssr` options and static prerendering. Status: Release Candidate, described by its docs as feature-complete with a stable API (verified 2026-10). Low risk.
- **How it fails Reach:** content routes marked `ssr: false`, or data fetched in components instead of route loaders.
- **Fix:** keep SSR on for indexable routes; load data in the route `loader`.

### SolidStart
- **Model:** SSR by default. Head tags through `@solidjs/meta`. Low risk.
- **How it fails Reach:** client-only rendering configured for the app, or content fetched only in the browser.
- **Fix:** keep SSR on and load data through the router's server-side data functions.

### Qwik City
- **Model:** SSR, then **resumability**: the browser picks up where the server stopped instead of re-running the app to hydrate. Content is in the raw HTML by default. Low risk.
- **How it fails Reach:** content produced only inside `useVisibleTask$`, which runs in the browser.
- **Fix:** load data with `routeLoader$` so it renders on the server.

### Gatsby
- **Model:** SSG. Low risk for static content; data is baked at build time.
- **How it fails Reach:** content that only appears client-side after rehydration, or stale builds. Ensure indexable content comes from the build-time data layer.

### Plain static HTML / SSGs (Hugo, Eleventy, Jekyll)
- **Model:** static HTML. Reach-rendering is fine by construction. Focus diagnosis on robots, sitemap, status codes, and canonicals.

### Docs generators (Docusaurus, VitePress, Starlight, Mintlify)
- **Model:** Docusaurus, VitePress and Starlight build static HTML for every route. Mintlify is hosted and renders pages for you. Low risk.
- **How they fail Reach:** interactive components (API playgrounds, tabs that fetch content, embedded widgets) that load their content in the browser; versioned docs that leave old versions indexable and competing; a missing sitemap because the site URL is not configured (VitePress needs `sitemap.hostname`; Starlight and `@astrojs/sitemap` need `site`).
- **Fix:** keep reference content in Markdown or MDX rather than fetched at runtime; `noindex` or canonical old doc versions deliberately (a person decides which).

### Server-rendered stacks (Rails, Django, Laravel, plain PHP)
- **Model:** HTML rendered on the server for every request. Reach-rendering is fine by construction.
- **How they fail Reach:** a JavaScript front end bolted on. Laravel with **Inertia** renders pages in the browser unless Inertia's SSR server is set up and running; Rails **Turbo Frames** with a lazy `src` load their content after the page. Also check error handling: a custom error page that returns `200` is a soft 404.
- **Fix:** enable Inertia SSR (or render the content in Blade); keep primary content out of lazy frames; return real `404` and `410` statuses.

---

## Auditing an existing prerender service

Many SPAs already sit behind a prerender service: Prerender.io, a self-hosted Rendertron, or an edge function that detects bots and serves a headless-browser snapshot. This is **dynamic rendering**. Google calls it "a workaround and not a recommended solution", and recommends server-side rendering, static rendering or hydration instead (Search Central, updated 2025-12). Rendertron itself is deprecated and its repository was archived on 2022-10-06. Do not rip a working service out in an audit, and do not add one. Audit it, then plan the move to real SSR or SSG.

### 1. Find it
- **Repo or infrastructure:** `prerender-node` or other prerender middleware, a Rendertron URL in server config, an nginx `map` on `$http_user_agent`, a Cloudflare Worker or other edge function that branches on user agent, or a service token such as `X-Prerender-Token`.
- **Served output:** the same URL returns very different HTML for a crawler user agent and a browser user agent (step 2). For the edge and CDN side of bot handling, see `edge-cdn-and-bot-access.md` in this folder.

### 2. Compare the bot response with what users see
The raw browser response of an SPA is a shell, so compare the **bot snapshot** with the **rendered page a user sees**.

```bash
URL="https://example.com/products/blue-widget"
BOT="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
curl -sL -A "$BOT" -D bot.h -o bot.html "$URL"
google-chrome --headless --dump-dom "$URL" > user.html   # the DOM after JavaScript runs
grep -i "^HTTP/" bot.h                                    # status the bot gets
for f in bot.html user.html; do
  echo "== $f"
  grep -oiE '<title>[^<]*</title>|<h1[^>]*>[^<]*|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>' "$f"
  echo "links: $(grep -oi '<a [^>]*href=' "$f" | wc -l)  words: $(sed -e 's/<[^>]*>/ /g' "$f" | wc -w)"
done
```
```powershell
$URL = "https://example.com/products/blue-widget"
$BOT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
$bot = Invoke-WebRequest -Uri $URL -UserAgent $BOT -UseBasicParsing
$bot.StatusCode
$bot.Content | Out-File bot.html -Encoding utf8
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --dump-dom $URL | Out-File user.html -Encoding utf8
foreach ($f in "bot.html", "user.html") {
  $c = Get-Content $f -Raw
  "== $f"
  [regex]::Matches($c, '<title>[^<]*</title>|<h1[^>]*>[^<]*|<link[^>]+rel=.canonical.[^>]*>|<meta[^>]+name="robots"[^>]*>') | ForEach-Object Value
  "links: " + [regex]::Matches($c, '(?i)<a [^>]*href=').Count + "  words: " + (($c -replace '<[^>]*>', ' ') -split '\s+' | Where-Object { $_ }).Count
}
```

Adjust the Chrome path for your machine; a rendering MCP or any headless browser can replace the Chrome command. Word counts include inline scripts, so use them to spot large gaps, not small ones. Some setups verify Googlebot by reverse DNS, so a spoofed user agent may get the browser response. If so, use Search Console's URL Inspection (live test, then view the crawled HTML) as the bot view.

### 3. Check parity, because a difference is a cloaking risk
Google does not generally treat dynamic rendering as cloaking **when the content is similar**; serving crawlers materially different content is cloaking. Compare, per template:
- title, meta description, `<h1>`, primary copy (read both; the word counts only point you at large gaps);
- canonical, robots meta, `hreflang`;
- internal links (the snapshot should not drop navigation or add links users never see);
- structured data (same entities and values as the visible page, especially prices and ratings);
- status code (a removed product must return `404` or `410` to bots as well as users, not a cached `200`).

Record any material difference as `high` severity with both versions as evidence. Treat added bot-only text or links as urgent, because they are the cloaking pattern.

### 4. Check cache staleness
- Compare a fast-changing value (price, stock, date, headline) between the snapshot and the live page.
- Look at `Date`, `Age` and `Last-Modified` on the bot response, and the service's cache settings (recache interval, recache on deploy, recache on content publish).
- Look for cached failures: snapshots of an error page, a cookie banner, a loading spinner or a half-rendered shell, often caused by a render timeout or blocked API calls.

### 5. Plan the move to real SSR or SSG
Present this as a human decision with options (`seo-migrations/references/framework-migrations.md` covers the migration itself):
1. **Prerender the content routes at build time** (static generation) if the set of URLs is known and changes slowly.
2. **Move to a framework with SSR** (Next.js, React Router framework mode, Nuxt, SvelteKit, Angular with `@angular/ssr`, Astro), template by template, starting with the highest-traffic templates.
3. **Keep the prerender service in place** until each migrated template is verified on the served HTML, then remove the user-agent branch for that template. Remove the service only when no template depends on it.

---

## Anti-patterns — never do these
- **Cloaking:** serving crawlers different content than users. Black-hat, against the method, and increasingly detectable.
- **Hidden content for bots:** stuffing text only crawlers see. Same problem.
- **Adding `user-agent` sniffing to server-render only for bots** ("dynamic rendering"): Google describes it as a workaround, not a recommended solution. Server-render for everyone instead. If a site already has it, audit it as described above.

The fix is always the same shape: make the real content part of the server response that both users and crawlers receive.
