---
name: 2-read-content
description: >-
  Make sure a reachable page contains real, readable content, correct metadata,
  and a good page experience in the served HTML — a meaningful title, one clear H1,
  a sensible heading structure, substantive body copy, a good meta description,
  image alt text, a language attribute, plus mobile-friendliness and healthy Core
  Web Vitals (page speed). Use this AFTER Reach passes, on any "thin content",
  "missing meta description", "duplicate titles", "page not described well in
  search", "site is slow", "Core Web Vitals", "page speed", "mobile-friendly", page
  copy, or on-page metadata question. Verifies on the rendered HTML, not the source.
---

# Read — Content, Metadata & Page Experience

**Rung 2 of the Visibility Ladder. Do not start here until Reach passes** — there is no point perfecting content an engine cannot fetch. Run the Reach skill first if you have not confirmed the content is in the served HTML.

A page passes Read when the rendered HTML carries enough clear, well-structured, genuine language for an engine to know what the page is *about*, the metadata that controls how it appears in results, and a page experience (speed + mobile) good enough not to hold it back. This is **not** keyword density — that thinking is twenty years stale. It is clarity, substance, correct signals, and a page that's fast and usable.

> These are the timeless on-page fundamentals that drive **classic ranking** — they matter just as much whether you're targeting Google's ten links or an AI answer engine. Content quality, metadata, speed and mobile-friendliness are not "AI SEO" or "old SEO"; they're the foundation both depend on.

> **Same cardinal rule as Reach:** verify on the *served* HTML. A `<title>` set in a component proves nothing until you have fetched the page and seen it in the response. Next.js metadata in particular can be silently overridden by a layout or a missing `generateMetadata` — only the rendered output tells the truth.

Work the four steps: **Diagnose → Fix → Verify → Report.**

---

## Step 1 — Diagnose

Fetch a representative content page's rendered HTML (as in Reach) and assess what an engine actually receives.

### Content substance and structure
- **`<h1>`** — is there exactly one, and does it describe the page (not just the site name)?
- **Heading hierarchy** — do `<h2>`/`<h3>` nest logically, with no skipped levels used purely for visual size? Headings are the page's outline.
- **Body substance** — is there genuine, specific content that answers the page's implied question, or is it thin/boilerplate/placeholder ("Lorem ipsum", "Welcome to our website")?
- **Duplication** — do multiple pages share near-identical body copy or titles? (Thin, templated pages competing with each other.)
- **Semantic HTML** — is content in real elements (`<main>`, `<article>`, `<nav>`, `<h*>`, `<p>`) or a soup of `<div>`s? Semantics help engines parse structure.

### Metadata (controls the search appearance)
- **`<title>`** — present, unique per page, descriptive, front-loaded, roughly ≤ 60 characters before truncation?
- **`<meta name="description">`** — present, unique, an accurate ~150–160 character summary? (Not a ranking factor directly, but it drives click-through and is often the snippet.)
- **`<html lang>`** — set correctly (e.g. `en-GB`)?
- **Image `alt`** — do meaningful images have descriptive alt text? (Decorative images should have empty `alt=""`.)
- **Open Graph / Twitter tags** — present for share previews? (Secondary, but cheap and worth it.)
- **Canonical** — deep canonical strategy is rung 4; here just confirm the title/description aren't being duplicated wholesale across URLs.

### Page experience (speed + mobile — a ranking factor, not just polish)
Unlike the rungs themselves, page experience isn't a hard *dependency* (a slow page still ranks, just lower) — but it's a genuine ranking signal and a build-time fix, so it lives here.
- **Mobile-friendliness** — Google indexes mobile-first, so the *mobile* rendering is the one that counts. Is there a correct `<meta name="viewport">`? Does the layout adapt (no fixed widths forcing horizontal scroll, tap targets not too small, text legible without zoom)?
- **Core Web Vitals** — the three field metrics Google uses: **LCP** (largest content paints quickly), **INP** (the page responds quickly to interaction), **CLS** (layout doesn't jump as it loads). Diagnose with a Lighthouse/PageSpeed run if available, or by inspecting the obvious causes below.
- **Common speed killers in the served page** — unoptimised/oversized images, no lazy-loading of below-the-fold media, render-blocking JS/CSS, heavy client bundles, fonts that block or shift text, missing dimensions on images/embeds (which cause CLS).

See `references/content-and-structure.md`, `references/metadata-titles-descriptions.md`, and `references/page-experience.md` for the standards behind each check.

---

## Step 2 — Fix

Apply safe, clearly-correct fixes autonomously; flag anything that needs the user's voice, facts, or judgement (see Step 4). **You may improve structure and metadata, but you must not invent substance.** If a page is thin because it has nothing to say, that is a content task for the human — surface it, do not pad it with filler.

### Structure and semantics (safe to fix)
- Ensure exactly one descriptive `<h1>`; fix heading levels used only for sizing (use CSS for size, headings for structure).
- Convert `<div>` soup to semantic elements where it is clearly content (`<main>`, `<article>`, `<section>`, `<nav>`, `<p>`).
- Add `lang` to `<html>`.

### Metadata (mostly safe; confirm wording with the user where it's a claim)
- **Next.js App Router (your stack):** set titles and descriptions via the Metadata API — a static `metadata` export for fixed pages, or `generateMetadata` for dynamic routes. Use a title template in the root layout (e.g. `%s | Brand`) so every page gets a unique, branded title. See `references/metadata-titles-descriptions.md` for the patterns.
- Write **unique** titles and descriptions per page; eliminate duplicates.
- Add descriptive `alt` to meaningful images; `alt=""` for decorative ones.
- Add Open Graph/Twitter tags (Next.js: via the same Metadata API) for share previews.

### Content (flag, don't fabricate)
- Where copy is thin, placeholder, or duplicated, **flag it as a human task** with specifics: "This page has two sentences of body text; engines have little to go on. What does this page need to say?" You may restructure and tighten existing real content; you must not manufacture claims, statistics, or expertise.

### Page experience (mostly safe; flag the bigger refactors)
- **Mobile:** ensure a correct viewport meta; fix obvious responsive breakages (fixed-width containers, overflow, tiny tap targets). A full responsive redesign is a human decision — flag it.
- **Images:** serve appropriately sized, modern-format images; lazy-load below-the-fold media; always set width/height (or an aspect ratio) to prevent layout shift. **Next.js:** use `next/image`, which handles sizing, lazy-loading, and modern formats.
- **Fonts:** avoid blocking/shifting text. **Next.js:** use `next/font` (self-hosts and sets `font-display` to avoid layout shift).
- **JavaScript:** reduce render-blocking and oversized client bundles — this overlaps the Reach rung (push `"use client"` down, fetch on the server). Heavy interactivity that tanks INP is a flag-and-discuss, not a silent rewrite.
- Re-using a Lighthouse/PageSpeed MCP here makes the before/after concrete. See `references/page-experience.md` for the per-cause fixes.

---

## Step 3 — Verify (on the rendered output)

Re-fetch the page's served HTML and confirm:
- Exactly one descriptive `<h1>` is present in the rendered HTML.
- The `<title>` and `<meta name="description">` are present, unique, and sensible — **in the served output**, not just in the source component.
- `<html lang>` is set; meaningful images have `alt`.
- Headings form a logical outline; content sits in semantic elements.

- **Page experience:** confirm the viewport meta is present and the page reflows on a narrow viewport; re-run Lighthouse/PageSpeed (or check the specific fixes) to confirm images are sized/lazy-loaded and CLS causes are resolved. Core Web Vitals have a *field-data* side (real users, measured over time) that is **live data you can't fully confirm at build time** — the build fixes the known causes; the live score is on the SearchOps side of the boundary.

Check more than one template type (article, product, listing) — metadata and performance bugs are usually per-template. Verification details are in `references/metadata-titles-descriptions.md` and `references/page-experience.md`.

**If the metadata isn't in the served HTML, it isn't done** — trace the override (often a layout or a client component) and fix it at the source that actually renders.

---

## Step 4 — Report to the user (plain English)

1. **What was wrong** — e.g. "Several of your pages had the same generic title, so in Google's results they were indistinguishable; and three pages were missing the short description that shows under the link."
2. **What I changed and why it matters** — each fix with a one-line reason tied to how the page is understood or how it appears in results.
3. **Proof** — the titles/descriptions/headings now appearing in the served HTML.
4. **What only you can decide** — the content-substance items. Be direct: "These pages are too thin for engines to understand. I won't invent content — here's what each page needs from you." Also flag any metadata wording that makes a factual claim you can't verify.

Then point up the ladder: once Read passes, the next rung is **Understand** (structured data / schema, which describes the content you've just made readable).

---

## Reference files (read when you need them)
- `references/content-and-structure.md` — headings, semantic HTML, content substance, duplication, matching content to search intent, what "thin" means and why it matters.
- `references/metadata-titles-descriptions.md` — title and description standards, the Next.js Metadata API patterns, alt text, Open Graph, and exact verification steps.
- `references/page-experience.md` — mobile-friendliness, Core Web Vitals (LCP/INP/CLS), image/font/JS optimisation, the Next.js tools for each, and what's build-time vs live-data.
