# Profile: e-commerce

Use for sites selling products (Shopify, WooCommerce, custom). The risks concentrate in **Reach** (faceted-URL sprawl, JS-rendered prices), **Understand** (Product/Offer schema), and **Connect** (canonicals across variants). Scale is the enemy — small template issues multiply across thousands of URLs.

## How each rung shifts
- **Reach** — two big risks: (1) **prices/stock rendered client-side** so crawlers see an empty or price-less page; (2) **faceted navigation** (filters/sort) generating near-infinite crawlable URLs that waste crawl budget and create duplicates. Ensure product content (incl. price) is in the served HTML; control facet URLs deliberately.
- **Read** — unique product descriptions, not just manufacturer boilerplate duplicated across the web and across your own variants. Category pages need real introductory content, not just a grid.
- **Understand** — `Product` with `Offer` (`price`, `priceCurrency`, `availability`), `brand`, and `aggregateRating`/`review` **only if real**. `BreadcrumbList`. This drives rich product results — high value here.
- **Connect** — **canonicals across variants** are critical: colour/size variants, query-param and faceted URLs must canonicalise to the right page so equity consolidates. Avoid duplicate product URLs competing.
- **Cite** — buying-intent and comparison queries: clear specs, comparison tables, genuine reviews, and honest answer blocks ("Is X waterproof?") make product content citable.

## Type-specific checks
- **Faceted/filter URLs:** decide per facet — canonical to base, `noindex`, or allow (only genuinely valuable, indexable combinations). Coordinate robots + canonical (see Connect + Reach).
- **Out-of-stock / discontinued:** don't 404 a ranking product abruptly — keep the page (mark unavailable) or `301` to a sensible alternative; map this in `seo-migrations` for bulk changes.
- **Variant duplication:** consolidate variant URLs with canonicals; one indexable product page.
- **Pagination** on category pages: self-canonicalise; ensure products are reachable.
- **Schema honesty:** never fabricate ratings/reviews/stock — a classic and penalised e-comm temptation. Mark up only what's real and shown.
- **Currency/locale:** correct `priceCurrency`; if multi-region, combine with `international.md`.

## Common failures
- Client-rendered prices invisible to crawlers (Reach).
- Faceted-URL explosion diluting crawl budget and creating duplicates.
- Fake `aggregateRating` to chase stars — remove and flag.
- Boilerplate manufacturer descriptions duplicated everywhere (Read).
- Out-of-stock products silently 404ing and losing equity.

## Priority tilt
Weight **Reach** (rendering + facets) and **Understand** (Product schema) highest, then **Connect** (variant canonicals). On hosted carts (Shopify), many fixes are theme/app settings — see the platform adapter.
