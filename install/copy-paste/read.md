# Read — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the Read skill. Run Reach first — there's no point fixing content a crawler can't fetch.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are making sure my pages have real, readable content, correct metadata, and a good page experience (speed + mobile) **in the served HTML**. This is rung 2 of the Visibility Ladder; only do this once you've confirmed crawlers can reach my pages (the Reach step). These are the timeless on-page fundamentals that drive **classic ranking** as much as AI search. Work in four steps and **never invent content** — flag thin pages for me instead of padding them.

**The one rule: verify on what is actually SERVED, not the source.** A title set in a component proves nothing until you've fetched the page and seen it in the HTML.

## Step 1 — Diagnose
Fetch a real content page's HTML and check:
- **Content:** exactly one descriptive `<h1>`? Logical heading order (`<h2>`/`<h3>`, no skipped levels for styling)? Genuine, specific body text — or thin/placeholder/duplicated copy? Real semantic elements (`<main>`, `<article>`, `<p>`) or `<div>` soup?
- **Metadata:** unique, descriptive `<title>` (~≤60 chars, key words first)? Unique `<meta name="description">` (~150–160 chars)? `<html lang>` set? Descriptive `alt` on meaningful images (`alt=""` on decorative ones)?
- **Page experience:** correct `<meta name="viewport">` and a layout that reflows on mobile (Google indexes mobile-first)? Core Web Vitals causes — oversized/unsized images, no lazy-loading, render-blocking or heavy JS, fonts that shift text (LCP/INP/CLS)?
- Check several page types (article, product, listing) — metadata and performance bugs are usually per-template.

## Step 2 — Fix
- **Safe to fix:** one clear `<h1>`; logical headings (use CSS for size, not heading levels); semantic HTML; `<html lang>`; descriptive alt text.
- **Metadata (Next.js App Router):** use the Metadata API — `export const metadata` for fixed pages, `generateMetadata` for dynamic ones, and a `title: { template: '%s | Brand' }` in the root layout so every page gets a unique branded title. Set `metadataBase` for absolute URLs. Don't hand-write `<title>` in JSX alongside the API.
- Make every title and description **unique**. Add Open Graph tags for share previews.
- **Page experience (safe fixes):** correct viewport + obvious responsive breakages; size/lazy-load/modern-format images and always set width/height (Next.js: `next/image`); non-shifting fonts (Next.js: `next/font`); reduce render-blocking/heavy JS. Flag a full responsive redesign or a big interactivity refactor rather than doing it silently.
- **Don't fabricate substance.** If a page is thin, tell me what it's missing and ask what it should say — don't fill it with generic filler, fake stats, or invented testimonials.

## Step 3 — Verify (re-fetch — don't trust the edit)
Re-fetch the page and confirm in the **served HTML**: one descriptive `<h1>`; a unique, sensible `<title>` and `<meta name="description">`; `<html lang>` set; alt text present; viewport meta present and the page reflows on mobile; images sized/lazy-loaded. Re-run Lighthouse/PageSpeed if you can (note: real-user Core Web Vitals are live data that only show after the change is live — the build fixes the causes). If the metadata isn't in the served output, trace what's overriding it (often a layout or a client component) and fix it there. Check more than one template.

## Step 4 — Explain it to me in plain English
1. **What was wrong** (e.g. "several pages shared one generic title, so they looked identical in Google").
2. **What you changed and why it matters.**
3. **Proof** — the titles/descriptions/headings now in the served HTML.
4. **What only I can decide** — which thin pages need real content from me (don't invent it), and any wording that makes a claim you can't verify.

Then tell me the next step is **Understand** (adding structured data / schema that describes this content to engines).
