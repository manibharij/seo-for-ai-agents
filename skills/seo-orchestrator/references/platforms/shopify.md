# Platform: Shopify

Read this when Step 0 detects Shopify. Diagnose the served HTML exactly as on any site. This file covers where each fix lives in a Shopify store, what Shopify fixes in place, and the failures that recur. Platform facts verified 2026-10 against Shopify's help centre and developer docs, and by fetching Shopify's public Dawn demo store.

---

## Detection

- **Served output:** a `powered-by: Shopify` response header, assets on `cdn.shopify.com`, and `window.Shopify` / `Shopify.theme` in inline scripts.
- **Theme code access:** the theme is editable in Online Store > Themes > Edit code, or locally with Shopify CLI. The files that matter most are `layout/theme.liquid`, `templates/robots.txt.liquid` (if it exists), the product and collection templates and sections, and any `snippets/` that print meta tags.
- **Headless Shopify** (Hydrogen or another front end on the Storefront API) is a code-editable app. Treat the front end as its framework and read [headless-cms.md](headless-cms.md) for the publish-to-live gap.

---

## Where each setting lives

| Setting | Where | Notes |
|---|---|---|
| Title and meta description | Each product, collection, page and blog post: the **Search engine listing** section in the admin. Output by the theme from `page_title` and `page_description` in `layout/theme.liquid` | If the listing fields are empty, Shopify falls back to the resource title and content |
| Canonical | `<link rel="canonical" href="{{ canonical_url }}">` in `layout/theme.liquid` | Theme Store themes include it. Check custom themes for a missing or hard-coded canonical |
| Open Graph and social tags | A theme snippet (in Dawn, `snippets/meta-tags.liquid`) | |
| Structured data | The theme (product JSON-LD) and apps | Apps and themes often both add `Product`. Keep one complete graph |
| `robots.txt` | `templates/robots.txt.liquid`. Adding the template replaces Shopify's generated file | Edit with the `robots` Liquid object so the default rules stay. See below |
| Sitemap | Automatic at `/sitemap.xml`, linking product, collection, page and blog sitemaps | Not editable. If theme code sets `noindex` on a resource, check whether the sitemap still lists it, and treat a mismatch as a finding |
| Redirects | Content > Menus > **View URL redirects** (bulk CSV import is available) | Limits below |
| URL handle | Each resource's search engine listing. Changing a handle offers a **Create a URL redirect** option | Leave it ticked unless a person decides otherwise |
| Agent and LLM files | `/agents.md` is managed by Shopify for every store; an `agents.md.liquid` template can override it, and it also serves `/llms.txt` and `/llms-full.txt` unless those have their own templates | Verified 2026-10. See `cite-aeo-geo` before changing it |

### `robots.txt.liquid`

Shopify's default `robots.txt` already blocks cart, checkout, account and admin paths, sorted collection URLs (`sort_by`), tag combinations (`+`) and multi-filter URLs. Do not replace it with plain text. Keep the default groups and add or remove single rules:

```liquid
{% for group in robots.default_groups %}
  {{- group.user_agent }}
  {%- for rule in group.rules -%}
    {{ rule }}
  {%- endfor -%}
  {%- if group.user_agent.value == '*' -%}
    {{ 'Disallow: /*?q=*' }}
  {%- endif -%}
  {%- if group.sitemap != blank -%}
    {{ group.sitemap }}
  {%- endif -%}
{% endfor %}
```

Before publishing, save the current `/robots.txt` output and compare it with the new one. Shopify's docs give the same advice, because a broken template can block the whole store.

### URL redirects: limits

- Up to **100,000** redirects per store (Shopify Plus: 20,000,000).
- A redirect fires **only when the old URL is broken** (returns "Page not found"). If a live product or page still exists at the old path, the redirect is ignored. Delete or rename the old resource first.
- You **cannot redirect from fixed Shopify paths**: `/products`, `/collections`, `/collections/all`, nor from paths starting `/apps`, `/application`, `/cart`, `/carts`, `/orders`, `/services` or `/shop`.
- URLs with query strings may not redirect as expected, and collection tag-filter URLs cannot be redirected.
- Stores with international market subfolders need a redirect per locale path.

---

## Fixed URL structure

Shopify's URL prefixes are not configurable: products live at `/products/<handle>`, collections at `/collections/<handle>`, pages at `/pages/<handle>`, blog posts at `/blogs/<blog>/<handle>`. A migration into Shopify must map every old URL onto these prefixes (`seo-migrations/references/redirect-mapping.md`). Never promise a client that `/shoes/red-runner` will survive a move to Shopify: it becomes `/products/red-runner` plus a redirect.

---

## The `/collections/x/products/y` duplicate

A product can be reached at `/products/<handle>` and, when a theme links to it with the Liquid `within` filter, at `/collections/<collection>/products/<handle>` for every collection it belongs to. Shopify's docs note that these are the same content on separate URLs and tell theme developers to consider the SEO implications of `within`.

What Shopify does about it: with the standard `{{ canonical_url }}` tag, the collection-path URL canonicalises to `/products/<handle>`. Fetching Shopify's Dawn demo store (2026-10) showed `/collections/bags/products/puff-olive-leaf` and `/products/puff-olive-leaf?variant=123` both serving `<link rel="canonical" href=".../products/puff-olive-leaf">`, while paginated collection pages keep their own canonical (`/collections/bags?page=2`).

What to check and fix:
1. **The canonical on a collection-path product URL** in the served HTML. If it is missing or self-referencing, the theme has replaced `canonical_url`. Restore it.
2. **Internal links.** If product cards use `product.url | within: collection`, every collection creates more crawlable duplicate paths. The canonical consolidates them, but links to the canonical URL are cleaner. Prefer `{{ product.url }}` in product cards and keep collection context through breadcrumbs, unless a person wants collection-aware URLs for navigation reasons.
3. **Variant URLs** (`?variant=`) canonicalise to the product. Do not add separate canonicals per variant unless variants are genuinely distinct products.

---

## What is locked

- The URL prefixes above, and redirects from them.
- The sitemap's existence and structure.
- Checkout markup and most of `/account`.
- Server and CDN behaviour: headers, caching, HTTP status codes for most resource types.
- Apps inject their own markup and scripts. You change those in the app's settings or by removing the app.

---

## Known failure patterns

1. **Password page left on.** A store in "password protection" mode serves a password page to crawlers and Google cannot read the sitemap. Check the home page's served HTML.
2. **Duplicate `Product` schema** from the theme and one or more review or SEO apps, often with conflicting prices or ratings. Keep one source. Never let an app output ratings that are not real reviews shown on the page.
3. **Redirects that never fire** because the old product was archived but still exists at the old handle. Delete or rename it, then test the redirect.
4. **A custom `robots.txt.liquid`** written as plain text that dropped Shopify's default `sort_by` and filter rules, letting faceted URLs flood the crawl.
5. **Missing or hard-coded canonical** in a custom or heavily edited theme (`theme.liquid` no longer prints `canonical_url`, or prints the home URL).
6. **Thin tag and filter pages indexed:** `/collections/x/tag` URLs with near-empty content. The default rules block combinations; single tags may still need a `noindex` from the theme if they add nothing.
7. **Apps that render content client-side** (reviews, FAQs, size guides) so the text is missing from the raw HTML. Check whether the app offers a server-rendered or theme-block option.
8. **International markets** without correct `hreflang` or with redirects set only for the primary locale.

---

## Giving instructions when you cannot edit code

```text
Finding: /collections/bags/products/puff-olive-leaf serves a self-referencing canonical,
         so each collection path competes with /products/puff-olive-leaf.
Where: Online Store > Themes > (live theme) > Edit code > layout/theme.liquid
Change: inside <head>, make sure this line exists exactly once:
        <link rel="canonical" href="{{ canonical_url }}">
        and remove any other <link rel="canonical"> printed by snippets or apps.
Check: open the collection-path URL, view source, and confirm the canonical points to
       /products/puff-olive-leaf. Tell me and I will re-fetch it to verify.
```

For admin-only changes, give the menu path (for example, Products > [product] > Search engine listing > Edit), the field, the exact value, and the live URL to check. Theme code edits are safer on a duplicate theme that is previewed, then published. Record anything Shopify will not allow as `needs-human` or `wont-fix` with the reason.

---

## Verify

Fetch the live URLs after the theme is published and caches have cleared: one product (at both its `/products/` and a collection path), one collection, one page and one blog post. Confirm the title, description, canonical, robots meta, and that `/robots.txt` still contains Shopify's default rules plus your change.
