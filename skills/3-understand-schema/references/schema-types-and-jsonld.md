# Schema.org types and JSON-LD patterns

Read this to pick the right type and fill it honestly. Use **JSON-LD** (a `<script type="application/ld+json">` block) — it is Google's preferred format and keeps structured data separate from your markup. Every value below must mirror **visible, true** content on the page.

> Format note: `@context` is always `https://schema.org`. Use one block per primary entity, or a `@graph` array to bundle several connected entities. Dates use ISO 8601 (`2026-06-03` or full timestamps). Link recurring entities with `@id`.

---

## Choosing the type — follow the content

| The page is… | Primary type | Key honest properties |
|---|---|---|
| A blog post / news article | `BlogPosting` / `NewsArticle` (or `Article`) | `headline`, `datePublished`, `author`, `image` |
| A product for sale | `Product` | `name`, `image`, `description`, `offers` (`Offer`); on a page where people can buy, the merchant listing fields below |
| A product sold in sizes, colours or materials | `ProductGroup` + variant `Product`s | `productGroupID`, `variesBy`, `hasVariant` (see Product variants below) |
| The business | `Organization` or `LocalBusiness` | `name`, `url`, `logo`; local adds `address`, `telephone`, `openingHours` |
| A person | `Person` | `name`, `jobTitle`, `sameAs` (real profiles) |
| Step-by-step instructions | `HowTo` | `name`, `step` (`HowToStep`) — *semantic only; see note* |
| A recipe | `Recipe` | `name`, `recipeIngredient`, `recipeInstructions` |
| A job opening | `JobPosting` | `title`, `description`, `datePosted`, `hiringOrganization`, `jobLocation`, `validThrough` |
| An event | `Event` | `name`, `startDate`, `endDate`, `eventStatus`, `location` (or `VirtualLocation`), `offers` |
| A course | `Course` | `name`, `description`, `provider` (`Organization`) |
| A genuine review / rating | `Review` / `AggregateRating` | only if real reviews are shown on the page — `reviewRating`/`author`, or `ratingValue`/`reviewCount`. Never fabricate. |
| Software / an app | `SoftwareApplication` | `name`, `applicationCategory`, `operatingSystem`, `offers` |
| Real on-page Q&As | `FAQPage` | `mainEntity` (`Question` → `acceptedAnswer`). *No Google rich result since May 2026; entity clarity and AEO only. See note.* |
| A nav trail | `BreadcrumbList` | `itemListElement` (`ListItem`) |
| The site itself | `WebSite` | `name`, `url`, `alternateName` on the home page (Google uses it for the site name shown in results). Skip `SearchAction`: the sitelinks search box it powered was retired in November 2024. |

Pick the most specific type that fits. Don't force a type for the sake of a rich result. This is the common set; schema.org has many more (e.g. `Service`, `QAPage`, `Dataset`) — choose the most specific *real* one. Media types (`VideoObject`, `ImageObject`) are handled by the `seo-media` skill.

> **Rich-result currency (verify before promising any rich result).** Google keeps narrowing which types produce rich results; the important shifts:
> - **`HowTo` rich results were retired** (2023) — `HowTo` markup no longer produces a Google rich result on any device. Use it only as optional semantic/entity markup, not to chase a snippet.
> - **`FAQPage` rich results were fully retired (May 2026).** Google stopped showing them from 2026-05-07 and removed the documentation in June 2026 (verified 2026-10 against Google's Search documentation updates). They were restricted to government/health sites in 2023 and are now **no longer shown in Google Search at all**. `FAQPage` remains valid schema.org markup. Its value now is machine-readability, entity clarity, and AEO extraction (the Cite/AEO layer), which is still worth having. Never add it expecting a SERP feature.
> - **The sitelinks search box was retired (November 2024).** Google stopped showing it globally from 2024-11-21 and removed its documentation on 2024-11-29. `WebSite` + `SearchAction` markup no longer does anything in Google Search. Google says existing markup causes no issues or Search Console errors, so there is no need to remove it, but do not add it as a recommendation.
> - **More types retired in 2025–26:** course info, estimated salary, learning video, special announcement and vehicle listing (Sep 2025), and practice problems (Jan 2026) no longer produce rich results. The underlying schema types stay valid for entity clarity.
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

### Merchant listings: shipping, returns and identifiers

A page where people can buy the product is eligible for Google's merchant listing experiences, which read more of the `Offer` (verified 2026-10 against Google's merchant listing docs). Required: `name`, `image`, and `offers` with `price` (above zero) and `priceCurrency`. Recommended, and worth filling truthfully: `availability`, `itemCondition`, `priceValidUntil` (sale prices only), `url`, `shippingDetails`, `hasMerchantReturnPolicy`, plus `brand`, `description`, `sku` and a GTIN (`gtin8`, `gtin12`, `gtin13` or `gtin14`).

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Oak chopping board, large",
  "image": ["https://example.com/img/oak-board-large.jpg"],
  "description": "Matches the on-page description.",
  "sku": "OAK-BRD-L",
  "gtin13": "5012345678900",
  "brand": { "@type": "Brand", "name": "Brand" },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/oak-board?size=large",
    "price": 45.00,
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": { "@type": "MonetaryAmount", "value": 4.95, "currency": "GBP" },
      "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "GB" },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY" },
        "transitTime":  { "@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY" }
      }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "GB",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }
  }
}
```
- Every value must match the visible page and the checkout: the price shown, the stock status shown, the shipping rate the basket charges, the return window in the published returns policy. A GTIN must be the real barcode; leave it out if you do not have one.
- Offer-level return policies support only a subset of properties: `applicableCountry`, `returnPolicyCategory`, `merchantReturnDays`, `returnMethod`, `returnFees` and `returnShippingFeesAmount`.
- **Out of stock:** keep the `Offer` and set `availability` to `https://schema.org/OutOfStock` (or `PreOrder` or `BackOrder` where true). Do not drop the price to hide it.

### Organization-level shipping and return policies

Google recommends one store-wide return policy under `Organization` rather than repeating it on every offer, and supports store-wide shipping the same way. Google added Organization return policies in June 2025 and shipping policies in July 2025 (verified 2026-10). Put this block on the homepage or the policy page, using the same `Organization` `@id` as everywhere else.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#org",
  "name": "Brand",
  "url": "https://example.com",
  "hasMerchantReturnPolicy": {
    "@type": "MerchantReturnPolicy",
    "applicableCountry": "GB",
    "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
    "merchantReturnDays": 30,
    "returnMethod": "https://schema.org/ReturnByMail",
    "returnFees": "https://schema.org/FreeReturn",
    "refundType": "https://schema.org/FullRefund"
  },
  "hasShippingService": {
    "@type": "ShippingService",
    "name": "Standard UK delivery",
    "fulfillmentType": "FulfillmentTypeDelivery",
    "handlingTime": {
      "@type": "ServicePeriod",
      "cutoffTime": "14:00:00+01:00",
      "duration": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY" },
      "businessDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    },
    "shippingConditions": [{
      "@type": "ShippingConditions",
      "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "GB" },
      "orderValue": { "@type": "MonetaryAmount", "minValue": 0, "maxValue": 49.99, "currency": "GBP" },
      "shippingRate": { "@type": "MonetaryAmount", "value": 4.95, "currency": "GBP" },
      "transitTime": {
        "@type": "ServicePeriod",
        "duration": { "@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY" }
      }
    }]
  }
}
```
- A return policy needs either `applicableCountry` plus `returnPolicyCategory` (with `merchantReturnDays` for a finite window), or a `merchantReturnLink` to the policy page.
- `ShippingService` requires `shippingConditions`. When several conditions apply to one product, Google uses the lowest cost.
- **Precedence, strongest first:** Content API for Shopping settings; Merchant Center or Search Console shipping and return settings; product-level markup; Organization-level markup. If the shop already set policies in Merchant Center, those win. Make the markup agree with them and ask the owner which is current.
- Return windows, fees and rates are business facts. Take them from the published policy page or `[established]` context; if they are missing, raise `needs-human`.

### Product variants (`ProductGroup`)

For a product sold in variants, Google supports a `ProductGroup` that holds the shared details and lists each variant as a `Product` (verified 2026-10). Required on the group: `productGroupID` (the parent SKU), `variesBy` (values such as `https://schema.org/size`, `color`, `material`, `pattern`, `suggestedAge`, `suggestedGender`) and `hasVariant`, or `isVariantOf` on each variant.

```json
{
  "@context": "https://schema.org",
  "@type": "ProductGroup",
  "@id": "https://example.com/products/oak-board#group",
  "name": "Oak chopping board",
  "productGroupID": "OAK-BRD",
  "brand": { "@type": "Brand", "name": "Brand" },
  "variesBy": ["https://schema.org/size"],
  "hasVariant": [
    {
      "@type": "Product", "name": "Oak chopping board, medium", "sku": "OAK-BRD-M", "size": "Medium",
      "image": "https://example.com/img/oak-board-medium.jpg",
      "offers": { "@type": "Offer", "url": "https://example.com/products/oak-board?size=medium",
        "price": 35.00, "priceCurrency": "GBP", "availability": "https://schema.org/InStock" }
    },
    {
      "@type": "Product", "name": "Oak chopping board, large", "sku": "OAK-BRD-L", "size": "Large",
      "image": "https://example.com/img/oak-board-large.jpg",
      "offers": { "@type": "Offer", "url": "https://example.com/products/oak-board?size=large",
        "price": 45.00, "priceCurrency": "GBP", "availability": "https://schema.org/OutOfStock" }
    }
  ]
}
```
- **Single-page design:** one page with a variant picker. Give each variant its own URL (a query parameter such as `?size=large` that preselects it); the page canonicalises to the URL without variant parameters.
- **Multi-page design:** each variant has its own page. Repeat the `ProductGroup` on each page with full markup for that page's variant, and reference the other variants by URL.
- Variant names are specific ("Oak chopping board, large"); the group name is general.
- Variant URLs and canonicals are covered in `seo-orchestrator/references/profiles/ecommerce.md`.

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
Mark up FAQs that actually exist and serve the reader — never invent Q&As. And note (per the currency box above) that FAQ *rich results* were fully retired in May 2026; the payoff is machine-readability and AEO extraction, not a Google snippet — so don't add it expecting one.

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
