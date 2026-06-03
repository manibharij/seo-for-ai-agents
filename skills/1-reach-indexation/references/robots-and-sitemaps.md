# Robots, meta directives, and sitemaps

Read this when the gatekeeper checks (Step 1c) turn up a `robots.txt`, `noindex`, status-code, or sitemap problem. A perfectly rendered page is still unreachable if a rule forbids it or a bad URL hides it.

---

## robots.txt — the crawl gate

`robots.txt` lives at the domain root (`/robots.txt`). It controls **crawling** (whether a bot fetches a URL), not **indexing** directly. Two consequences people get wrong:

- **`Disallow` does not guarantee de-indexing.** A disallowed URL can still appear in results (without a snippet) if other pages link to it. To keep a page *out of the index*, allow crawling and use a `noindex` meta tag/header instead — the crawler must be able to fetch the page to see the `noindex`.
- **Blocking a path you optimise is self-sabotage.** The most common accident is a leftover `Disallow: /` from a staging config, or disallowing a directory that holds real content (`/blog/`, `/products/`).

### What to check
- Is there a stray `Disallow: /` or an over-broad rule blocking real content?
- Are CSS/JS assets blocked that the page needs to render? (Blocking these can stop a crawler rendering the page correctly.)
- Is the sitemap referenced? Add `Sitemap: https://example.com/sitemap.xml`.
- Are you accidentally blocking AI crawlers you *want* (or failing to block ones you don't)? That is a deliberate choice — see the Cite skill's `ai-crawlers-and-llms-txt.md`. Here, just surface it; don't decide it for the user.

### A sane default for a content site
```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```
Add specific `Disallow` rules only for genuinely non-public paths (admin, cart, internal search results, faceted-filter URL explosions). Confirm intent with the user before blocking anything.

---

## Meta robots vs X-Robots-Tag — the silent de-lister

A single stray `noindex` removes a page from search entirely, and it is easy to leave one behind from a template or a "coming soon" phase.

- **`<meta name="robots" content="...">`** — in the page `<head>`. Common values: `index,follow` (default, no tag needed), `noindex` (keep out of index), `nofollow` (don't pass link signals).
- **`X-Robots-Tag` HTTP header** — same directives, but in the response header. Crucial: **you must check the headers, not just the HTML**, because a `noindex` here is invisible in the body. It is also the only way to set directives on non-HTML files (PDFs, images).

### What to check
- Fetch the page and inspect **both** the rendered `<head>` and the response headers for `noindex`.
- In Next.js App Router, `noindex` is usually set via the Metadata API (`robots: { index: false }` in `metadata` or `generateMetadata`). A `noindex` leaking from a shared layout or a default export will silently delist whole sections — trace where it comes from.
- Confirm any `noindex` is intentional before removing it (some pages *should* be noindexed: thank-you pages, internal search results, thin tag archives).

---

## HTTP status codes — reachability at the protocol level

| Code | Meaning | Action |
|---|---|---|
| `200` | OK | Good — content should be present. |
| `301` | Permanent redirect | Fine, but collapse chains (A→B→C should be A→C). |
| `302` | Temporary redirect | Often a mistake where `301` is meant; check intent. |
| `404` | Not found | Correct for missing pages — better than a soft 404. |
| `410` | Gone | Stronger "permanently removed" signal than 404. |
| `5xx` | Server error | Urgent — crawlers back off and can drop pages. |

**Soft 404** — a "page not found" message served with a `200` status. Crawlers may index the error page or waste crawl budget on it. Return a real `404`/`410` for genuinely missing content.

**Redirect chains/loops** — each hop loses a little signal and crawl efficiency; loops are fatal. Flatten to a single hop.

---

## Sitemaps — the URL inventory

An XML sitemap lists the canonical URLs you want crawled and indexed. It does not force indexing, but it helps discovery (especially for large sites or weakly-linked pages) and surfaces issues in Search Console.

### Correctness rules — a sitemap full of bad URLs hurts more than no sitemap
- List **canonical `200` URLs only** — no redirects, no 404s, no `noindex` pages, no parameter duplicates.
- Use the **production host and scheme** — a classic bug is a sitemap full of `http://localhost:3000/...` or a staging domain.
- Keep it current — stale sitemaps that list dead URLs erode trust in the file.
- One sitemap caps at 50,000 URLs / 50 MB uncompressed; beyond that, split and use a sitemap index.
- Reference it from `robots.txt` (a build-time fix). Optionally, once the site is live, the user can also submit it in Search Console to speed discovery — that's a runtime step on the live-data side, not part of the build.

### Framework-native generation (prefer this over hand-maintained XML)
- **Next.js App Router:** add `app/sitemap.ts` exporting a default function returning the URL array (Next serves it at `/sitemap.xml`). For large/dynamic sites, generate entries from your data source. Pair with `app/robots.ts` for `robots.txt`. This keeps the sitemap in sync with real routes automatically — the right answer for this user's stack.
- **Astro:** `@astrojs/sitemap` integration.
- **Nuxt:** `@nuxtjs/sitemap` module.
- **SvelteKit:** generate via an endpoint (`src/routes/sitemap.xml/+server.ts`).
- **Gatsby:** `gatsby-plugin-sitemap`.

Whatever generates it, **verify the output**: fetch `/sitemap.xml` and confirm the URLs are production, canonical, and `200`. A generator pointed at the wrong base URL produces a confidently wrong sitemap.
