# Schema.org types and JSON-LD patterns

Read this to pick the right type and fill it honestly. Use **JSON-LD** (a `<script type="application/ld+json">` block) — it is Google's preferred format and keeps structured data separate from your markup. Every value below must mirror **visible, true** content on the page.

> Format note: `@context` is always `https://schema.org`. Use one block per primary entity, or a `@graph` array to bundle several connected entities. Dates use ISO 8601 (`2026-06-03` or full timestamps). Link recurring entities with `@id`.

---

## Choosing the type — follow the content

| The page is… | Primary type | Key honest properties |
|---|---|---|
| A blog post / news article | `BlogPosting` / `NewsArticle` (or `Article`) | `headline`, `datePublished`, `author`, `image` |
| A product for sale | `Product` | `name`, `image`, `description`, `offers` (`Offer`) |
| The business | `Organization` or `LocalBusiness` | `name`, `url`, `logo`; local adds `address`, `telephone`, `openingHours` |
| A person | `Person` | `name`, `jobTitle`, `sameAs` (real profiles) |
| Step-by-step instructions | `HowTo` | `name`, `step` (`HowToStep`) — *semantic only; see note* |
| A recipe | `Recipe` | `name`, `recipeIngredient`, `recipeInstructions` |
| Real on-page Q&As | `FAQPage` | `mainEntity` (`Question` → `acceptedAnswer`) — *rich result restricted; see note* |
| A nav trail | `BreadcrumbList` | `itemListElement` (`ListItem`) |
| The site itself | `WebSite` | `name`, `url`, optional `SearchAction` |

Pick the most specific type that fits. Don't force a type for the sake of a rich result.

> **Rich-result currency (verify before promising any rich result).** Google's rich-result support changes; two important shifts:
> - **`HowTo` rich results were retired** (2023) — `HowTo` markup no longer produces a Google rich result on any device. Use it only as optional semantic/entity markup, not to chase a snippet.
> - **`FAQPage` rich results are restricted** (since 2023) to well-known, authoritative **government and health** sites. For a typical business/blog site, `FAQPage` will **not** earn an FAQ rich result — its value now is machine-readability, entity clarity, and AEO extraction (the Cite/AEO layer), which is still worth having.
> Treat the per-type Google docs as the source of truth at the time you work, and report eligibility honestly (see `validation.md`).

---

## Ready patterns (fill only with true, visible values)

### Article / BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Exact visible article title",
  "description": "Short summary matching the page.",
  "image": "https://example.com/cover.jpg",
  "datePublished": "2026-06-03",
  "dateModified": "2026-06-03",
  "author":   { "@type": "Person", "name": "Real Author Name" },
  "publisher": {
    "@type": "Organization",
    "name": "Brand",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  },
  "mainEntityOfPage": "https://example.com/blog/the-post"
}
```
Omit `author` entirely if there is no real, named author shown — do **not** invent one.

### Product with Offer
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Visible product name",
  "image": ["https://example.com/p.jpg"],
  "description": "Matches the on-page description.",
  "brand": { "@type": "Brand", "name": "Brand" },
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  }
}
```
Add `aggregateRating`/`review` **only** if real ratings/reviews are shown on the page. Never fabricate them.

### Organization / LocalBusiness
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://example.com/#business",
  "name": "Business name",
  "url": "https://example.com",
  "telephone": "+44 20 7946 0000",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1 High Street",
    "addressLocality": "London",
    "postalCode": "SW1A 1AA",
    "addressCountry": "GB"
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "09:00", "closes": "17:00"
  }]
}
```
The `@id` lets other blocks reference this same business (see entity linking below). Use `Organization` for non-physical businesses; `LocalBusiness` (or a subtype like `Restaurant`) only for genuine physical locations.

### FAQPage — only for real on-page FAQs
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "A question genuinely answered on the page",
    "acceptedAnswer": { "@type": "Answer", "text": "The answer as shown on the page." }
  }]
}
```
Mark up FAQs that actually exist and serve the reader — never invent Q&As. And note (per the currency box above) that an FAQ *rich result* is now restricted to government/health authorities; on a typical site the payoff is machine-readability and AEO extraction, not a Google snippet — so don't add it expecting one.

### BreadcrumbList
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" },
    { "@type": "ListItem", "position": 3, "name": "The Post", "item": "https://example.com/blog/the-post" }
  ]
}
```

---

## Entity linking with `@id` — the bit most packs miss

Use `@id` so the same real-world entity is recognised as one thing across pages and blocks:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#org", "name": "Brand",
      "logo": "https://example.com/logo.png" },
    { "@type": "WebSite", "@id": "https://example.com/#website",
      "url": "https://example.com", "publisher": { "@id": "https://example.com/#org" } },
    { "@type": "BlogPosting", "headline": "...", "isPartOf": { "@id": "https://example.com/#website" },
      "publisher": { "@id": "https://example.com/#org" } }
  ]
}
```

Consistent `@id`s build a coherent entity graph: the publisher of the article *is* the organisation *is* the business. This is the foundation that the Connect rung (internal linking) and the Cite rung (entity consistency for AI attribution) build on. Keep names, URLs and logos identical wherever the same entity appears.

---

## Common AI-build mistakes to fix
- Copy-pasted schema with placeholder values (`"price": "0.00"`, `"ratingValue": "5"`, `"author": "John Doe"`). Replace with real values or remove the property.
- `@type` mismatch (Product schema on an article; Organization where LocalBusiness is meant, or vice versa).
- Schema describing content that isn't on the page.
- Multiple conflicting blocks (two different Organizations, clashing canonicals-by-`@id`).
- JSON-LD injected only client-side, so it's absent from the served HTML — render it server-side (see the SKILL's Next.js pattern).
