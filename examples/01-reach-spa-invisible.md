# Example 1 — Reach: a beautiful site Google can't see → indexed

**The hero demo.** An AI agent built a slick marketing site. It looks perfect in the browser. The owner can't understand why it's been live for two months with zero search traffic. The answer is the single most common failure of AI-built sites: it's a client-rendered SPA, and to a crawler the pages are nearly empty.

*Stack: Vite + React SPA. Anonymised.*

---

## Diagnose — on the served HTML

The agent fetches a real content page the way a crawler first sees it — raw HTML, no JavaScript executed:

```bash
curl -sL https://example.com/services/web-design -o raw.html
```

What's in `raw.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <title>My Company</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/assets/index-a1b2c3.js"></script>
  </body>
</html>
```

The diagnosis writes itself:
- The page's content — the `<h1>`, the body copy, everything — is **not in the served HTML**. There's an empty `<div id="root">` and a script bundle.
- A crawler that doesn't execute that bundle sees a blank page with one generic title. **Every page shares the same `<title>` ("My Company").**
- Searching for a distinctive sentence of the visible copy confirms it: `grep -i "award-winning web design" raw.html` → no match.

> **Floor identified: Reach.** No point touching content, schema, or anything above — the content isn't reaching crawlers at all. This is exactly why the ladder says start at the bottom.

---

## Fix

The honest fix for a pure SPA is to render the content on the server. That's an architectural change, so the agent **flags it as a human decision** and presents the options (per the Reach skill):

> "Your site is a single-page app: the server sends an empty shell and the browser builds the page with JavaScript. Crawlers often don't run that JavaScript, so they see blank pages — that's why you're not in search. To fix it, the content needs to be in the HTML the server sends. Options:
> 1. **Migrate to a meta-framework** (Next.js / Astro) — best long-term, biggest change.
> 2. **Add server-side rendering to your Vite app** (via `vike`) — keeps Vite.
> 3. **Pre-render your known pages to static HTML at build time** — simplest if your routes are a fixed set of marketing pages.
> Which fits your plans?"

The owner picks **option 3** (a fixed set of marketing pages). The agent adds a build-time pre-render step so each route is emitted as static HTML with its content baked in, and along the way fixes the shared title (a per-page `<title>`/description — a Read-rung win that came for free once pages were real).

---

## Verify — on the served HTML

Re-fetch the same URL, raw, no JS:

```bash
curl -sL https://example.com/services/web-design -o raw-after.html
grep -i "award-winning web design" raw-after.html   # now matches
grep -i "<h1" raw-after.html                          # real heading present
curl -sIL https://example.com/services/web-design     # 200, no redirect chain
```

`raw-after.html` now contains:

```html
<html lang="en-GB">
<head>
  <title>Web Design Services | My Company</title>
  <meta name="description" content="Award-winning web design for small businesses…" />
</head>
<body>
  <main>
    <h1>Web design that turns visitors into customers</h1>
    <p>Award-winning web design for small businesses across the UK…</p>
    …
  </main>
</body>
</html>
```

Checklist (from `references/verification.md`):
- [x] Primary content present in **raw** served HTML, before JS.
- [x] `200`, no redirect chain, no stray `noindex`.
- [x] Per-page `<title>` (no longer all "My Company").
- [x] `robots.txt` allows the path; sitemap lists production `200` URLs.

The build-time fixes were now done. As an optional live follow-up, the owner submitted the sitemap in Search Console (a runtime step on the live-data side, not part of the build); over the following crawls the pages were indexed.

---

## Report — plain English

> **What was wrong:** Your site was built as a single-page app. Your pages looked fine to you because your browser runs the JavaScript that loads the content — but search engine crawlers often don't, so to Google your pages looked nearly empty, and every page even shared the same title. That's why two months in, you had no search traffic.
>
> **What I changed:** I added a step to your build that produces a real HTML version of each page with the content already in it, and gave each page its own title and description. Crawlers now receive your actual content.
>
> **Proof:** Before, the served HTML was an empty shell. After, here's your real heading and copy in the raw HTML a crawler sees (shown above).
>
> **What only you could decide:** moving away from a pure single-page app — you chose pre-rendering, which suited your fixed set of pages.
>
> **Honest limit:** this makes your pages *findable and readable*. It can't tell you whether you now *rank* for anything, or how you compare to competitors — that's live ranking data, a separate thing. Next rung up is **Read** (we already improved your titles; there's more to do on content depth).

---

**Why this is the hero demo:** the before/after is visceral — an empty `<div id="root">` versus a page full of real content — and it's verified on the *served HTML*, not on a source edit. It's the failure most AI-built sites share and the fix with the biggest payoff. The before/after of those two `curl` outputs is the screenshot pair worth leading a launch with.
