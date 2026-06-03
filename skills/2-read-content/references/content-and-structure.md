# Content substance, headings, and semantic structure

Read this when diagnosing or fixing the *content* half of Read (the metadata half is in `metadata-titles-descriptions.md`). The aim is a page whose rendered HTML makes its subject and structure unmistakable to an engine — and genuinely useful to a human, because the two goals have converged.

---

## What "readable content" actually means now

Forget keyword density, exact-match phrases, and word-count targets. Modern engines (and AI answer engines especially) assess whether a page **comprehensively and clearly addresses the topic a user came for.** The practical test: *if a knowledgeable human read only the rendered text, would they understand what this page is about and find it useful?* If yes, you are most of the way there.

This means the failure mode is not "too few keywords" — it is **thinness**: pages with nothing specific to say, padded with generalities, or templated so heavily that every page reads the same.

### Search intent — the part of "keywords" that still matters
Keyword *density* is dead, but **search intent** is not. A page should clearly address the question or need a user actually has when they land on it, in the language they'd recognise. Two build-time checks:
- **Intent match:** does the page's main content answer what someone arriving here actually wants — informational ("what is X"), commercial ("best X"), transactional ("buy X"), or navigational? A pricing page should talk price; a guide should teach. A mismatch between the page's purpose and its content is a real problem no amount of formatting fixes.
- **Recognisable language:** use the terms your audience uses for the thing (naturally, in headings and body), rather than internal jargon — so both readers and engines connect the page to the query. This is *not* an invitation to keyword-stuff.

Note the boundary: which queries to target, their search volume, and how competitive they are is **keyword research — live data** on the SearchOps side. The build-time job is making each existing page genuinely match the intent it's meant to serve.

---

## Headings — the page's outline

Engines use the heading structure as a machine-readable table of contents.

- **Exactly one `<h1>`**, describing the page's specific subject — not the site name, not a tagline. The `<h1>` and `<title>` should agree on what the page is about (they need not be identical).
- **Logical nesting:** `<h2>` for major sections, `<h3>` for sub-points, no skipped levels. A page that jumps `<h1>` → `<h4>` because `<h4>` "looked the right size" is using headings for styling — fix the CSS, not the semantics.
- **Descriptive, not cute:** "Pricing for small teams" beats "The fun part". For the Cite rung later, question-shaped headings ("How much does X cost?") become valuable; even here, descriptive headings help.
- Don't wrap non-heading text in heading tags for emphasis, and don't demote real headings to styled `<div>`s.

---

## Semantic HTML — structure engines can parse

A page built from meaningful elements is easier to parse than a wall of `<div>`s:

- `<main>` — the primary content of the page (one per page).
- `<article>` — a self-contained piece (a blog post, a product, a news item).
- `<section>` — a thematic grouping, usually with a heading.
- `<nav>` — navigation blocks.
- `<header>` / `<footer>` — page or section chrome.
- `<p>`, `<ul>`/`<ol>`, `<table>`, `<figure>`/`<figcaption>` — for the content itself.

Semantic markup also improves accessibility, which overlaps heavily with how engines and assistive technology both consume the page. You rarely need to rewrite everything — target the main content region first.

---

## Content substance — the part you must not fake

This is where the white-hat rule bites hardest. You may **restructure, tighten, and clarify content that genuinely exists.** You may **not** manufacture substance that does not.

### Signs of a thin or low-value page
- Placeholder text ("Lorem ipsum", "Welcome to our website", "Content coming soon").
- A handful of generic sentences that could describe any company in the sector.
- Heavy templating: dozens of pages identical but for a swapped name or city.
- An obvious mismatch between the page's promise (title) and its delivery (body).

### What to do
- **Restructure and tighten** real content: clearer headings, shorter paragraphs, lists where appropriate, front-loaded key points.
- **Flag thinness as a human task**, specifically: name the page, say what's missing, and ask what it should contain. "This service page is three generic sentences. What makes your version of this service specific — process, scope, who it's for?"
- **Never** invent statistics, claims, testimonials, case studies, or credentials to bulk a page out. Fabricated substance is both a trust violation and, increasingly, something answer engines are built to discount.

---

## Duplication — pages competing with themselves

Near-identical pages split signals and confuse engines about which to show.

- **Duplicate titles/descriptions** across many URLs → make them unique (see the metadata reference).
- **Boilerplate bodies** across templated pages → differentiate with genuinely page-specific content, or consolidate the thin pages into fewer strong ones.
- **True duplicates at multiple URLs** (e.g. with/without trailing slash, query-param variants) → this is a canonicalisation problem; note it and hand it to rung 4 (Connect), which owns canonical strategy.

---

## Verifying content and structure on the rendered output

As always, check what is *served*:
- Fetch the rendered HTML and read the actual text — is the real content present (this also re-confirms Reach) and is it substantive?
- Confirm exactly one `<h1>` and a sensible heading outline in the served markup.
- Confirm the main content sits in semantic elements, not just nested `<div>`s.
- Spot-check several templates; thinness and duplication are usually systemic, not per-page.
