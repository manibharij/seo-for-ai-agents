# Profile: e-commerce

Use for sites selling products (Shopify, WooCommerce, custom). The risks concentrate in **Reach** (faceted-URL sprawl, JS-rendered prices), **Understand** (Product/Offer schema), and **Connect** (canonicals across variants). Scale is the enemy — small template issues multiply across thousands of URLs.

## How each rung shifts
- **Reach** — two big risks: (1) **prices/stock rendered client-side** so crawlers see an empty or price-less page; (2) **faceted navigation** (filters/sort) generating near-infinite crawlable URLs that waste crawl budget and create duplicates. Ensure product content (incl. price) is in the served HTML; control facet URLs deliberately.
- **Read** — unique product descriptions, not just manufacturer boilerplate duplicated across the web and across your own variants. Category pages need real introductory content, not just a grid.
- **Understand:** `Product` with `Offer` (`price`, `priceCurrency`, `availability`), `brand`, and `aggregateRating`/`review` **only if real**. On pages where people can buy, add the merchant listing fields (shipping, returns, identifiers) and `ProductGroup` for variants; see `3-understand-schema/references/schema-types-and-jsonld.md`. `BreadcrumbList`. High value here.
- **Connect** — **canonicals across variants** are critical: colour/size variants, query-param and faceted URLs must canonicalise to the right page so equity consolidates. Avoid duplicate product URLs competing.
- **Cite** — buying-intent and comparison queries: clear specs, comparison tables, genuine reviews, and honest, direct answers to buyer questions ("Is X waterproof?") in the product copy make product content citable.

## Parity: Merchant Center feed and the served page

Most shops send Google the same facts twice: in a Merchant Center feed and on the product page (visible and in JSON-LD). Google crawls the landing page and compares it with the feed; a price or availability mismatch can get the product disapproved in Merchant Center ("Mismatched value (page crawl)", verified 2026-10 in Merchant Center Help). Fix parity at the data source; patching the markup alone will drift again.
- **Price and currency** in the feed equal the visible price and the JSON-LD `price`, for every variant, including during and after a sale.
- **Availability** agrees in all three. A cached page that still says "In stock" after the feed says out of stock is a mismatch.
- **Identifiers:** the feed's `id`, `gtin` and `mpn` match the markup's `sku` and GTIN for that variant.
- **Links:** each feed item's link opens that exact variant, preselected, with its own price and stock in the served HTML.
- **Shipping and returns** set in Merchant Center or Search Console take precedence over markup. Make the markup agree with them rather than compete.
- **Served, not patched:** the price must be correct in the raw HTML. A placeholder that JavaScript replaces after load fails, even if shoppers see the right number.

Run the parity checklist in `3-understand-schema/references/validation.md` on a sample (a simple product, a variant, a sale item, an out-of-stock item). Reading the Merchant Center account itself needs the owner's access; without it, list the feed comparison as `needs-human`.

## Variant URLs

Google's ecommerce URL guidance (verified 2026-10) accepts a variant as a path segment (`/t-shirt/green`) or a query parameter (`/t-shirt?color=green`). What matters:
- **Every variant you want shown in Google has its own URL** that loads with that variant selected, so the price, stock and image in the served HTML match the variant. A picker that changes the variant only in client state, at one URL, gives Google one variant at most.
- **Single-page design** (one page, a picker, `?size=large` preselects): the page canonicalises to the URL without variant parameters, and `ProductGroup` markup lists each variant with its own `offers.url`.
- **Multi-page design** (each variant its own page): each page self-canonicalises and carries full markup for its variant.
- Do not let sort, tracking or session parameters create further copies of variant URLs; canonicalise those to the clean URL.
- On an existing shop, treat the current variant URL scheme as intentional. Changing it is a migration (`seo-migrations`), with redirects and sign-off.

## Faceted navigation

Follow Google's faceted navigation guidance (https://developers.google.com/crawling/docs/faceted-navigation, verified 2026-10). Decide per facet whether its URLs should be indexed at all.
- **Facets you do not need in Search** (sort orders, price sliders, most multi-filter combinations): stop the crawling. Google's options are to disallow those URL patterns in `robots.txt`, or to implement filtering with URL fragments (`#`), which Google generally ignores for crawling and indexing. A `noindex` alone still lets Google crawl every combination.
- **Facets that deserve to rank** (for example "women's running shoes" as a real category with demand): give them clean, stable URLs, real introductory content, internal links and a self-canonical. These are categories, and belong in the sitemap.
- **If facet URLs stay crawlable:** use the standard `&` separator (not commas, semicolons or brackets), keep filters in a consistent order, return `404` when a combination has no results, and point filtered URLs at the unfiltered page with `rel="canonical"`.
- **Coordinate robots and canonical.** A URL disallowed in `robots.txt` cannot have its canonical or `noindex` read. Do not combine them on the same URL and expect both to work.
- On an existing shop, check Search Console and logs before blocking a facet pattern: some facet URLs may already rank. Flag the change for sign-off (see `existing-site-safety.md`).

## Out-of-stock and discontinued products

- **Temporarily out of stock:** keep the page live with `200`, keep the price, show the status clearly, and set `availability` to `https://schema.org/OutOfStock` (or `BackOrder` or `PreOrder` where true) in both markup and feed. Offer alternatives on the page. Do not `noindex` or remove it: it keeps its rankings for when stock returns.
- **Discontinued with a real replacement:** `301` to the successor or the closest equivalent product, and say so on the target page. Redirecting everything to the homepage or a loosely related category is a judgement call Google may treat as a soft 404; prefer a genuinely equivalent target.
- **Discontinued with no replacement:** keep a useful page (specs, support, alternatives) if people still search for it; otherwise return `404` or `410`. Remove it from the feed and the sitemap either way.
- **Empty categories:** Google's guidance is to `noindex` them, or return `404` if the category is removed from the site's navigation.
- Bulk changes (a range withdrawn, a season rolled over) go through `seo-migrations` for the redirect map.

## Type-specific checks
- **Faceted/filter URLs:** decide per facet, as above. Coordinate robots + canonical (see Connect + Reach).
- **Variant duplication:** one URL per variant that matters, consolidated with canonicals as above.
- **Pagination** on category pages: self-canonicalise; ensure products are reachable.
- **Schema honesty:** never fabricate ratings/reviews/stock — a classic and penalised e-comm temptation. Mark up only what's real and shown.
- **Feed parity:** feed, visible page and JSON-LD agree on price, currency, availability and identifiers.
- **Currency/locale:** correct `priceCurrency`; if multi-region, combine with `international.md`. Google asks for a distinct URL per currency offering.

## Common failures
- Client-rendered prices invisible to crawlers (Reach).
- Faceted-URL explosion diluting crawl budget and creating duplicates.
- Feed price and page price out of step after a sale ends or stock changes.
- Variants selectable only in client state, all sharing one URL.
- Fake `aggregateRating` to chase stars — remove and flag.
- Boilerplate manufacturer descriptions duplicated everywhere (Read).
- Out-of-stock products silently 404ing and losing equity.

## Priority tilt
Weight **Reach** (rendering + facets) and **Understand** (Product schema and feed parity) highest, then **Connect** (variant canonicals). On hosted carts, many fixes are theme or app settings: see `platforms/shopify.md` and `platforms/wordpress.md` (WooCommerce).
