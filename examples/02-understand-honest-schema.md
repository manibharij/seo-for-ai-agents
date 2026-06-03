# Example 2 — Understand: schema that lies → schema that's honest

An AI agent "added structured data" to a blog. It validates, it's in the served HTML — and it's quietly fabricated. This example shows the white-hat moat: the right move is to **strip the invented signals and flag them**, not to keep convincing-looking lies because they pass a validator.

*Stack: Next.js App Router. Anonymised.*

---

## Diagnose — on the served HTML

The agent fetches a blog post and finds existing JSON-LD in the served output:

```bash
curl -sL https://example.com/blog/seo-tips | grep -i "application/ld+json"
```

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "10 SEO Tips",
  "author": { "@type": "Person", "name": "John Doe" },
  "datePublished": "2024-01-01",
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "127" }
}
```

Cross-checking against the **visible page**:
- There is **no author byline** anywhere on the post. "John Doe" is a placeholder the agent invented.
- There are **no ratings or reviews** on a blog post — `aggregateRating` with "127 reviews" is fabricated to chase a rich result.
- `datePublished` "2024-01-01" doesn't match the post's actual publish date.

It validates. It's in the served HTML. **And it's dishonest** — a guideline violation that risks a manual penalty and undermines the exact trust the Cite rung depends on.

> The lazy version of this skill stops at "valid JSON-LD, present in HTML ✓". This pack's honesty check is what catches it.

---

## Fix

The agent marks up **only what is visibly true**, removes the fabrications, and **flags the gaps** instead of filling them:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "10 SEO Tips",
  "datePublished": "2025-09-14",
  "publisher": {
    "@type": "Organization",
    "@id": "https://example.com/#org",
    "name": "Example",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  },
  "mainEntityOfPage": "https://example.com/blog/seo-tips"
}
```

- `author` **removed** — there's no real author on the page to name.
- `aggregateRating` **removed** — there are no reviews.
- `datePublished` corrected to the real date from the CMS.
- `publisher` added with a consistent `@id` (sets up entity consistency for Connect and Cite).
- Rendered from the same server-component data as the visible post, so values can't drift.

---

## Verify — served HTML + validation + honesty

- **Served:** the corrected block is in the raw served HTML.
- **Valid:** JSON parses, `@type` valid, ISO date, absolute logo URL.
- **Honest (the decisive check):** every remaining value appears on the page and is true. Nothing invented.

---

## Report — plain English

> **What was wrong:** The structured data on your blog posts claimed each one had a "4.9 rating from 127 reviews" and an author called "John Doe" — none of which exist. That was added automatically and it's a problem: Google can hand out manual penalties for fake review markup, and AI answer engines are built to distrust sources that fake credentials. It would have hurt you, not helped.
>
> **What I changed:** I removed the invented author and the fake ratings, corrected the publish date to the real one, and kept the honest, useful markup (what the post is, who published it).
>
> **What only you can provide:** If a real person writes these posts and is happy to be credited, give me their name and genuine credentials and I'll add a visible byline and proper `Person` schema with links to their real profiles. If you collect genuine reviews, I'll mark those up too. **I won't invent either** — fake trust signals do more harm than good.
>
> **Honest limit:** valid, honest schema makes you *eligible* for richer results and easier for AI engines to understand — it doesn't *guarantee* a rich result or a citation; Google and the answer engines decide that per query.

---

**Why this example matters:** anyone can generate schema that validates. The differentiator — the part fifteen years of correctness buys — is knowing that **valid is not the same as honest**, and that the right output when trust data is missing is a flagged human task, not a plausible lie.
