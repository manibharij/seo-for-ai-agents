---
name: 1-reach-indexation
description: >-
  Make sure search engines and AI crawlers can actually reach a page and see its
  content in the served HTML. Use this FIRST on any SEO, indexing, "Google can't
  find my site", "not showing up in search", "is my site crawlable", SSR/CSR, or
  rendering question — and before any other SEO work, because nothing else counts
  if the page can't be reached. Diagnoses client-rendering blind spots, robots and
  sitemap problems, and bad status codes; verifies on the rendered HTML, not the source.
---

# Reach — Indexation & Rendering

**Rung 1 of the Visibility Ladder. The foundation. If this fails, nothing above it matters.**

A page is "reachable" when a crawler can fetch its URL *and* the response contains the page's real content. The number one failure of AI-built sites is that they pass the first test and fail the second: the page looks perfect in a browser (which runs JavaScript) and is nearly empty to a crawler (which often does not). Your job is to catch that and fix it.

> **The cardinal rule of this skill:** verify on the *rendered output*, not the source. Editing code and declaring success proves nothing. You must confirm the content is present in what is actually *served*. Assume content is client-rendered and invisible until you have proven otherwise by fetching it.

Work the four steps in order: **Diagnose → Fix → Verify → Report.**

---

## Step 1 — Diagnose

The goal is to find the *lowest* thing that is broken. Do not jump to fixes. Gather evidence first.

### 1a. Identify the stack
Look for the framework so you can reason about how it renders:
- `next.config.*` → **Next.js** (check App Router `app/` vs Pages Router `pages/`; default assumption for this user is App Router).
- `vite.config.*` + `index.html` with a single `<div id="root">` → **Vite SPA** (high risk: client-rendered by default).
- `astro.config.*` → **Astro** (SSG/SSR by default — usually low risk).
- `nuxt.config.*` → **Nuxt**, `svelte.config.*` → **SvelteKit**, `gatsby-config.*` → **Gatsby**, `remix`/`react-router` → **Remix/React Router**.
- A `create-react-app` / plain CRA `react-scripts` setup → **CRA SPA** (high risk).
- Plain static `.html` files or a static-site generator output → usually fine for Reach; focus on robots/sitemap.

Work the stack out from the dependencies and config yourself; if it's genuinely undeterminable, assume the most likely and proceed, noting the assumption. Don't make the user tell you the framework.

### 1b. Fetch a real URL and look at the SERVED HTML
This is the heart of the diagnosis. Pick a representative content page (not just the homepage — an article, a product, a deep page). Fetch the **raw, un-executed** HTML the way a crawler first sees it.

- If a render/fetch MCP server is available (see `install/mcp.md`), use it to get both the raw HTML and the JS-rendered HTML so you can compare.
- Otherwise use the agent's built-in fetch/HTTP capability to retrieve the raw response body.

Then check: **is the page's primary content actually in that HTML?** Search the served markup for a distinctive sentence of body copy, the real `<h1>`, the `<title>`. See `references/verification.md` for the exact checks and commands.

The decisive comparison:
- Content present in raw served HTML → **Reach for rendering is OK.** Move to robots/sitemap/status checks.
- Content absent from raw HTML but present after JS executes → **client-rendering blind spot.** This is the primary failure. Go to Fix.
- Content absent in both → a data/build problem, not just rendering. Investigate before "fixing" rendering.

### 1c. Check the gatekeepers
Even a perfectly rendered page is unreachable if something forbids it:
- **`robots.txt`** — is it accidentally `Disallow:`-ing real content, or blocking the crawlers you want? (See `references/robots-and-sitemaps.md`.)
- **`<meta name="robots">` / `X-Robots-Tag`** — a stray `noindex` will silently delist a page. Check the served HTML *and* response headers.
- **HTTP status** — does the URL return `200`? Watch for soft 404s (a "not found" page served with `200`), redirect chains, and `4xx/5xx`.
- **HTTPS** — is the site served over HTTPS with a valid certificate, and does `http://` redirect to `https://` (a single hop)? HTTPS is a baseline trust/ranking signal and a prerequisite for many browser features; mixed content (HTTPS page loading `http://` assets) can break rendering and trust. Deep host/protocol canonicalisation is rung 4 — here, just confirm the secure version is the one served and reachable.
- **Sitemap** — does one exist, is it referenced from `robots.txt`, does it list correct canonical URLs (not dev/staging hosts, not redirects, not 404s)?
- **Canonical sanity** — does the page point its canonical at itself or somewhere sensible? (Deep canonical strategy is rung 4; here, only catch the gross errors that block indexation.)

Record what is broken and what is fine. The lowest broken item drives the fix order.

---

## Step 2 — Fix

Fix from the lowest problem upward. Apply safe fixes autonomously; flag anything that changes site behaviour or needs a human decision (see Step 4). For full per-stack detail and trade-offs, read `references/rendering-ssr-csr.md`.

### Rendering (the high-value fix)
The principle: **the primary content must be in the HTML the server sends, before any JavaScript runs.** Map the fix to the stack:

- **Next.js App Router** — Server Components render on the server by default; content should already be in the HTML. If it is not, the usual cause is a `"use client"` boundary placed too high (an entire page or layout marked client-side), or content fetched in a `useEffect` instead of in a server component / `async` server fetch. Pull data fetching server-side; push `"use client"` down to the smallest interactive leaves. Confirm the route is not opted into purely dynamic client rendering.
- **Next.js Pages Router** — use `getServerSideProps` (per-request) or `getStaticProps` (build-time) so content is in the initial HTML, instead of fetching in `useEffect`.
- **Vite / CRA SPA** — the honest fix is to introduce server-side rendering or pre-rendering, because an SPA serves an empty shell by default. Options, in rough order of preference: migrate to a meta-framework (Next/Astro/Remix), add SSR (e.g. `vite-plugin-ssr`/`vike`), or pre-render known routes to static HTML at build time. This is a significant change — **flag it as a human decision** with the options and trade-offs; do not silently re-architect their app.
- **Astro / Nuxt / SvelteKit / Remix** — these render server-side by default; if content is missing, find the specific component or route that opted into client-only rendering and move its data fetching to the server-rendered path.

> Never "fix" rendering by stuffing hidden content for crawlers or serving crawlers different HTML than users (cloaking). That is black-hat and breaks the method. The content a crawler sees must be the content a user sees.

### Robots, sitemap, status, HTTPS
- Remove erroneous `Disallow` rules and stray `noindex` directives on pages that should be indexed. Infer intent yourself: admin, cart, account, and internal-search paths are almost always meant to stay private, so leave those; only flag a genuinely ambiguous case rather than asking about every path.
- Ensure a valid sitemap exists, lists canonical `200` URLs only, and is referenced from `robots.txt`. For framework-native sitemap generation (e.g. Next.js `app/sitemap.ts`), see `references/robots-and-sitemaps.md`.
- Fix soft 404s (return a real `404`), collapse redirect chains, and resolve `5xx`.
- Ensure `http://` redirects to `https://` (single hop) and fix mixed-content references (assets loaded over `http://` on an HTTPS page). Certificate provisioning is usually a host/platform setting — flag it for the user if it's missing rather than assuming you can issue one. Picking the single preferred host+protocol site-wide is finished at rung 4.

---

## Step 3 — Verify (on the rendered output)

A fix is not done until you have re-fetched and seen the content with your own eyes. **Re-run the Step 1b fetch** and confirm:
- The previously-missing content is now present in the **raw served HTML**.
- The page returns `200`, with no stray `noindex` in body or headers.
- `robots.txt` allows the path; the sitemap lists the correct canonical URL.

If a Lighthouse / PageSpeed or render MCP is available, use it to confirm crawlability and that the rendered content matches the raw content. Exact verification steps and the "definition of done" checklist are in `references/verification.md`.

**If verification fails, you are not finished.** Return to Diagnose. Do not report success on the strength of a source edit.

---

## Step 4 — Report to the user (plain English)

The user does not know SEO. Tell them, in plain language:

1. **What was wrong** — e.g. "Your site is built as a single-page app. Your pages look fine in a browser because the browser runs the JavaScript that loads the content — but search engine crawlers often don't run that JavaScript, so to Google your pages looked nearly empty. That's why you weren't showing up."
2. **What I changed, and why it matters** — the specific fixes, each with a one-line reason tied to being found in search.
3. **Proof** — "Here's the content now appearing in the raw HTML that crawlers see," with the before/after.
4. **What only you can decide** — the human-judgement items, called out clearly. Examples:
   - "Switching your SPA to server-side rendering is a meaningful architectural change. Here are the options and trade-offs — which do you want?"
   - "These paths are currently blocked from search — are any of them meant to be private?"
   - "I can't tell you whether you now actually *rank* for anything — that needs live ranking data, which is outside what a build can check." (The honest boundary; see the Cite skill's closing note.)

Then point up the ladder: once Reach passes, the next rung is **Read** (real, readable content, correct metadata, and a fast, mobile-friendly page experience).

---

## Reference files (read when you need them)
- `references/rendering-ssr-csr.md` — per-framework rendering models, how each fails Reach, and the concrete fix for each.
- `references/robots-and-sitemaps.md` — robots.txt rules, meta robots vs X-Robots-Tag, sitemap correctness, framework-native generation.
- `references/verification.md` — exact fetch/inspection steps and commands, MCP-assisted checks, and the definition-of-done checklist.
