---
name: 3-understand-schema
description: >-
  Add correct structured data (schema.org as JSON-LD) so engines can identify the
  entities on a page — articles, products, organisations, FAQs, breadcrumbs,
  local businesses, people. Use this AFTER Read passes, on any "schema", "structured
  data", "JSON-LD", "rich results", "rich snippets", "knowledge panel", or "Google
  doesn't understand my page" question. Marks up only facts already present and true
  on the page; validates against schema.org and verifies on the rendered HTML.
---

# Understand — Structured Data (Schema)

**Rung 3 of the Visibility Ladder. Do not start until Read passes.** Structured data *describes* content that must already exist and already be readable. Marking up a price, author, or rating that is not on the page is at best ignored and at worst a trust violation.

A page passes Understand when its key entities are stated in machine-legible JSON-LD that (a) accurately reflects the visible content, (b) uses the right schema.org types, and (c) validates cleanly. Done well, this is also what makes a page eligible for rich results and easier for AI answer engines to attribute correctly — which is why it sits directly beneath Cite.

> **Cardinal rule, sharpened for schema:** structured data must mirror the **visible, true** content of the page. Never mark up information that is not on the page or is not real. And verify the JSON-LD in the **served HTML** — schema injected only client-side may never be seen.

Work the four steps: **Diagnose → Fix → Verify → Report.**

---

## Step 1 — Diagnose

### Identify what the page actually *is*
Schema follows content. First classify each template by its real entity:
- An article/blog post → `Article` / `BlogPosting`
- A product page → `Product` (with `Offer`)
- The business itself → `Organization` or `LocalBusiness`
- A person → `Person`
- A how-to / recipe → `HowTo` / `Recipe`
- A list of Q&As genuinely on the page → `FAQPage`
- Navigation trail → `BreadcrumbList`
- Site-wide → `WebSite` (optionally with `SearchAction`)

> Rich-result support changes: **`HowTo` rich results were retired** and **`FAQPage` rich results are now restricted to government/health authorities**. On a typical site, add these for entity clarity and AEO — not expecting a Google snippet. Verify current per-type eligibility before promising any rich result (see `references/schema-types-and-jsonld.md`).

### Check what's already there (and whether it's valid)
- Fetch the **served HTML** and look for existing `<script type="application/ld+json">` blocks. Are there any? Are they in the served output or only injected client-side?
- Do existing blocks **match the visible content**, or do they claim things the page doesn't show (a classic AI-build error: copy-pasted schema with placeholder ratings, fake authors, wrong types)?
- Are required/recommended properties present for the type? (See `references/schema-types-and-jsonld.md`.)
- Is the type **appropriate** — not `Product` schema on a blog post, not `FAQPage` where there's no real FAQ?

Record: which templates need schema, which have wrong/invalid/dishonest schema, and which are fine.

---

## Step 2 — Fix

Add or correct JSON-LD, marking up **only what is visibly true on the page.** Prefer JSON-LD in the `<head>` or body of the **server-rendered** output. Use the patterns in `references/schema-types-and-jsonld.md`; validate as you go (`references/validation.md`).

### Principles
- **One source of truth.** The schema values should come from the same data that renders the visible content, so they cannot drift apart. In Next.js, render the JSON-LD from the same props/fetch the page uses (see below).
- **Right type, minimal honesty-safe properties.** Include the properties you can fill truthfully from the page. Don't pad with guessed values.
- **Nest entities properly.** E.g. an `Article` references its `author` (a `Person` or `Organization`) and `publisher` (an `Organization` with a `logo`); a `Product` contains an `Offer` with `price`/`priceCurrency`/`availability`.
- **Connect entities with `@id`** where the same entity recurs (the Organization that is both publisher here and the business elsewhere), so engines resolve them as one thing. This entity consistency pays off again at the Cite rung.

### The white-hat lines you do not cross
- **No fabricated `aggregateRating`/`review`.** Only mark up ratings/reviews that genuinely exist and are shown on the page. Inventing them is a guideline violation and can earn a manual penalty.
- **No fake authors, dates, or credentials.** If authorship/E-E-A-T data is missing, **flag it as a human task** — do not invent a `Person`.
- **No `FAQPage` for marketing Q&As you wrote to game rich results** if they aren't real on-page FAQs. Mark up FAQs that actually serve the user.
- **Don't mark up hidden content.** What's in the schema should be visible to the user.

### Next.js App Router pattern (your stack)
Render JSON-LD from the same data as the page, in a server component, so it lands in the served HTML:
```tsx
// Next.js 15+: params is a Promise — await it (Next 14 passed it synchronously).
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = await getPost(slug)
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    datePublished: post.publishedAt,
    author: { '@type': 'Person', name: post.author.name },   // only if the author is real & shown
    // ...only fields you can fill truthfully from `post`
  }
  return (
    <>
      <script type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <article>{/* the visible content these values mirror */}</article>
    </>
  )
}
```
(`dangerouslySetInnerHTML` is the standard, accepted way to emit JSON-LD in React/Next; the content is your own serialised object, not user input.)

---

## Step 3 — Verify (on the rendered output + validation)

1. **Served HTML:** re-fetch and confirm the `<script type="application/ld+json">` is present in the raw served output, per template.
2. **Validity:** validate the JSON-LD. If a schema-validator MCP is available, use it; otherwise check structure against schema.org and (manually or via the agent) against Google's Rich Results requirements. JSON must parse, `@type` must be valid, required properties present.
3. **Honesty:** re-read the visible page and confirm every schema value appears on the page and is true. This check is as important as validity.

Exact steps and the validation checklist are in `references/validation.md`. **If the JSON-LD isn't in the served HTML, or it claims something the page doesn't show, it isn't done.**

---

## Step 4 — Report to the user (plain English)

1. **What was wrong** — e.g. "Your product pages didn't tell Google in a structured way what the product, price, and availability were, so they couldn't qualify for the richer result format with price and stock shown."
2. **What I added and why it matters** — the types added, each tied to a benefit (eligibility for rich results, clearer entity understanding, better AI attribution).
3. **Proof** — the validated JSON-LD now in the served HTML, and a note that it mirrors the visible page.
4. **What only you can decide / must provide** — missing real trust data: "I did not add author/review schema because there are no real authors/reviews on these pages. If you have genuine ones, add them and I'll mark them up." Be explicit that you refused to invent these *on purpose*.

Then point up the ladder: with entities understood, the next rung is **Connect** (wiring understood pages into a coherent site).

---

## Reference files (read when you need them)
- `references/schema-types-and-jsonld.md` — the common types, their required/recommended properties, ready JSON-LD patterns, and entity-linking with `@id`.
- `references/validation.md` — how to validate (MCP and manual), Rich Results eligibility, and the served-HTML + honesty verification checklist.
