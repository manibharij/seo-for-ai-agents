# JavaScript SEO: what happens after the server response

Read this when a site uses a JavaScript framework and the raw HTML looks right but something is still wrong: content or links missing for some crawlers, the wrong status code, a `noindex` or canonical that changes after load. `rendering-ssr-csr.md` covers which rendering model each stack uses. This file covers the behaviours on top of it.

The primary source is Google's [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) (last updated 2026-03-04, checked 2026-10), with Google's pagination and lazy-loading guides and the Next.js docs where noted.

---

## How Google handles JavaScript

Google works in three phases: crawl, render, index. It queues every page that returns `200` for rendering, unless a robots meta tag or header tells it not to index the page. A page can wait in that queue for seconds or longer. Two consequences matter for every section below:
- **The raw response is read first.** Status codes, robots directives and canonicals in the raw HTML are acted on before any JavaScript runs.
- **Other crawlers may never render.** Treat the raw response as the only view you can rely on for crawlers other than Google. This is judgement, not a measured figure, and it is why the pack verifies on the raw HTML first.

### The test: raw against rendered

```bash
URL="https://example.com/page"
PHRASE="a sentence from the main content"
curl -sL "$URL" > raw.html
google-chrome --headless --dump-dom "$URL" > rendered.html
for f in raw.html rendered.html; do printf "%s: " "$f"; grep -c "$PHRASE" "$f"; done
```
```powershell
$URL = "https://example.com/page"
$PHRASE = "a sentence from the main content"
(Invoke-WebRequest -Uri $URL -UseBasicParsing).Content | Out-File raw.html -Encoding utf8
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --dump-dom $URL | Out-File rendered.html -Encoding utf8
foreach ($f in "raw.html", "rendered.html") { "$f`: " + (Select-String -Path $f -Pattern $PHRASE -SimpleMatch).Count }
```

Present in rendered, absent in raw: the content depends on JavaScript. Run the same comparison for the title, canonical, robots meta, `<h1>` and internal links. Use a rendering MCP or Search Console's URL Inspection live test if you have one; adjust the Chrome path for your machine.

---

## Hydration

Hydration is the browser attaching JavaScript to server-rendered HTML. It is fine for SEO when the server HTML already holds the content. Problems:
- **Content that appears only after hydration.** Anything rendered in `useEffect`, `onMount`, Angular's `afterNextRender`, Qwik's `useVisibleTask$` or Solid's client-only resources is missing from the raw HTML. Move it to the server data path (server component, `loader`, `load`, `routeLoader$`).
- **Hydration mismatches.** When the server HTML and the first client render differ (dates, random IDs, `window` checks, locale formatting), frameworks patch or re-render on the client. The served HTML may then disagree with what users see, which is a quiet parity problem. Fix mismatch warnings in the browser console; they are not cosmetic.
- **Client errors that blank the page.** A JavaScript error during hydration can replace good server HTML with an error state for users and for rendering crawlers. Check the console on each template.

---

## Streaming and Suspense: what is in the initial HTML

Streaming frameworks (Next.js App Router, React Router, TanStack Start, SolidStart, Nuxt and others) send the page in chunks over one response.
- **The first chunk** holds the shell: layouts, anything outside a `<Suspense>` boundary, and the fallbacks (`loading.tsx` skeletons).
- **Later chunks** in the same response carry the resolved content, plus inline scripts that move it into place.

The Next.js docs state that streaming is server-rendered and does not affect SEO, and suggest Google's Rich Results Test to see the HTML Google receives. The risk is for crawlers that read the HTML without running scripts: the content arrives at the end of the document, outside its intended place, and the fallback text sits where the content should be. That is judgement, so design for it:
- Keep the `<h1>`, the primary copy and the main internal links **outside** Suspense boundaries, or in data that resolves before the first flush.
- Use `loading.tsx` and Suspense for secondary, slow or personalised parts.
- **Status codes are fixed once streaming starts.** In Next.js, a `notFound()` called after the response has begun streaming still returns `200`, with a `<meta name="robots" content="noindex">` added to the streamed HTML. Call `notFound()` before any Suspense boundary or `await` that may suspend, or check in `proxy.ts`, if you need a real `404`.
- **Streaming metadata** (Next.js 15.2 and later): for clients that run JavaScript, `generateMetadata` output may be appended to `<body>` instead of `<head>`. HTML-only bots (Next.js keeps a list, configurable with `htmlLimitedBots`) still get it in `<head>`. Setting `htmlLimitedBots: /.*/` in `next.config` turns streaming metadata off.
- **Not in the initial HTML at all:** Astro `server:defer` islands (fetched after load) and Angular `@defer` blocks during SSR (placeholder only, unless incremental hydration with `hydrate` triggers is enabled).

---

## Links: client-router links against real `<a href>`

Google can only discover links that are `<a>` elements with an `href`. Links injected by JavaScript are fine if they follow that rule.

| Crawlable | Not crawlable |
|---|---|
| `<a href="/pricing">Pricing</a>` | `<span onClick={() => router.push('/pricing')}>` |
| Next.js `<Link href>`, React Router `<Link to>`, `<NuxtLink to>`, SvelteKit `<a href>`, Angular `routerLink` **on an `<a>`** | `<button>` that navigates; Angular `routerLink` on a `<div>` or `<button>` (no `href` is rendered) |
| `<a href="/products?page=2">` | `<a href="#" onClick=...>`, `<a href="javascript:void(0)">` |

Check the served HTML: count `<a href` pointing at internal URLs per template and compare with the navigation a user sees.

---

## Infinite scroll and pagination

Googlebot does not scroll or click. Content that loads on scroll or behind a "Load more" button is invisible unless it also has its own URL. Following Google's pagination guidance (updated 2025-12):
- Give each page of results a unique URL, for example `?page=2`. Do not use fragments (`#page=2`) for page numbers; Google ignores fragments.
- Link pages in sequence with `<a href>` (next, previous, or numbered links), even if users mostly scroll.
- Give each page its own canonical. Do not canonicalise page 2 onward to page 1.
- When infinite scroll loads a new chunk, update the address bar with the History API so each chunk has a persistent URL.
- Google no longer uses `rel="next"` and `rel="prev"`. They do no harm, but they are not the fix.

---

## Hash routes

URLs like `https://example.com/#/products/blue` route on the fragment. Google cannot reliably resolve fragment URLs, so every "page" collapses into the home page. Google's guidance is to use the History API for client-side routing.

Fix by switching the router to history mode: Vue Router `createWebHistory` instead of `createWebHashHistory`; React Router `createBrowserRouter` instead of `createHashRouter` / `HashRouter`; Angular without `withHashLocation()` / `useHash: true`. The server must then return the app for every deep URL (and a `404` for unknown ones). Old hash URLs cannot be redirected server-side, because the fragment never reaches the server: map them in client code once, with `location.replace`. Treat this as a URL migration (`seo-migrations`).

---

## Soft 404s in single-page apps

An SPA served from one `index.html` returns `200` for every path, including ones that do not exist. Google reports these as soft 404s, and junk URLs can get indexed.

**Best fix, server-side:** return a real `404` (or `410`) from the server or the framework's data layer.
- Next.js: `notFound()` in the page or `generateMetadata`, called before streaming starts (see above).
- SvelteKit: `error(404, 'Not found')` in a `load` function.
- React Router: throw `data(null, { status: 404 })` from a `loader`.
- Nuxt: throw `createError` with a 404 status.
- Angular SSR: a `status` on the server route or `RESPONSE_INIT`.

**If the app is client-rendered and cannot change yet,** Google gives two options:
1. Use a JavaScript redirect to a URL for which the server responds with `404` (for example `/not-found`).
2. Add `<meta name="robots" content="noindex">` to error pages with JavaScript.

Both only work for crawlers that render. Record them as interim fixes, not final ones.

---

## Lazy-loaded content

Google's lazy-loading guidance (updated 2025-12): load content when it becomes visible in the viewport, using native `loading="lazy"` for images and iframes, or `IntersectionObserver`. Do not depend on user actions such as scrolling or clicking, because Google Search does not interact with the page.
- Content behind tabs and accordions is fine if it is in the DOM. Content fetched only when a tab is clicked is not seen.
- Do not lazy-load the main image above the fold; it delays Largest Contentful Paint (`2-read-content/references/page-experience.md`).
- Verify lazy-loaded images in the rendered HTML: the real URL must be in `src` (or `srcset`), not only in a `data-src` that a script swaps in.

---

## `noindex` set by JavaScript

- If the raw HTML contains `noindex`, **Google may skip rendering and JavaScript execution**, so using JavaScript to remove or change a `noindex` may not work. A staging `noindex` in the base HTML template that JavaScript "removes" in production is a classic launch failure: the page stays out of the index.
- Adding `noindex` with JavaScript works for Google only if the page is rendered, and does nothing for crawlers that do not render.

Put robots directives in the server response: a `<meta name="robots">` in the raw HTML or an `X-Robots-Tag` header. Check both on every template.

---

## Canonical swapped by JavaScript

Google advises against using JavaScript to change the canonical to something other than the URL in the original HTML. If you must set it with JavaScript, set it to the same value as the original HTML. Typical bugs:
- An SPA `index.html` ships `<link rel="canonical" href="https://example.com/">`, and a head manager changes it per route on the client. The raw HTML says every page is the home page.
- A static canonical in the base template plus one added by a head library, giving two canonicals.

Render the canonical on the server, once per page. See `2-read-content/references/metadata-titles-descriptions.md` for the per-framework pattern and `4-connect-architecture/references/canonicals-and-architecture.md` for canonical strategy.

---

## Titles and descriptions set by JavaScript

Google can use a `<title>` or meta description set by JavaScript. HTML-only crawlers and social preview bots cannot, and a client-set title appears late. Server-render them.

---

## Resources and caching

- Do not block the JavaScript, CSS or API endpoints a page needs to render in `robots.txt`; Google cannot render what it cannot fetch (`robots-and-sitemaps.md`).
- Googlebot caches aggressively and may use stale JavaScript or CSS. Fingerprint asset filenames (`main.2bb85551.js`) so a deploy changes the URL. Most frameworks do this by default; check a custom build.

---

## Verify and report

For each template, record in the findings: what the raw HTML holds, what the rendered DOM holds, the status code, and which behaviour above explains the difference. Evidence is the two outputs side by side. Fixes that move content, links, status codes or directives into the server response are the durable ones. JavaScript-only workarounds are `open` until replaced.
