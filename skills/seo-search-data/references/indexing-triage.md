# Indexing triage

How to turn Search Console's indexing data into causes, owners and fixes. Reason names follow Search Console's Page indexing report (verified 2026-10, https://support.google.com/webmasters/answer/7440203). API fields follow the URL Inspection reference (https://developers.google.com/webmaster-tools/v1/urlInspection.index/UrlInspectionResult).

---

## 1. Build the population

| Source | Gives you | Notes |
|---|---|---|
| A tool exposing the Page indexing report, or the user's export | Counts per reason and example URLs | The aggregate report is **not** in the Search Console API. Treat the example URLs as a sample, not a complete list. |
| Sitemap URLs | What the site wants indexed | Fetch the served sitemap, not the source file. |
| Search Analytics, `page` dimension, last 90 days | Pages with impressions (so almost certainly indexed) | A sitemap URL with zero impressions is a candidate, not proof of non-indexing. |
| Server logs (`seo-log-analysis`) | Whether Googlebot fetches the URL at all | Large sites only. |

Group candidates by **template** (URL pattern). Indexing problems are almost always template problems.

## 2. Sample with URL Inspection

Budget: 2,000 inspections per day per property, 600 per minute. Sample per template and reason (judgement: 5 to 20 each, more where the template is important). Keep, per URL:

```yaml
url: https://example.com/products/blue-widget
inspected: 2026-10-03
verdict: NEUTRAL
coverageState: "Duplicate, Google chose different canonical than user"
indexingState: INDEXING_ALLOWED
robotsTxtState: ALLOWED
pageFetchState: SUCCESSFUL
lastCrawlTime: 2026-09-21T04:12:09Z
crawledAs: MOBILE
userCanonical: https://example.com/products/blue-widget
googleCanonical: https://example.com/products/blue-widget?colour=blue
```

Store conclusions and samples, not full API dumps. If a tool in the environment wraps URL Inspection, its quota is the same.

## 3. Confirm on the served output

For each sampled URL fetch: status code and redirect chain, `X-Robots-Tag` header, raw HTML (meta robots, canonical, main content present?), and rendered HTML if the site renders client-side. The inspection result describes Google's last crawl; if the served page has changed since `lastCrawlTime`, say so and re-check after the next crawl.

## 4. Reason by reason

**Crawled - currently not indexed.** Google fetched the page and chose not to index it, for now. Check: is the main content in the raw HTML (Reach)? Is it thin, templated or near-duplicate of another page (Read)? Does it answer anything better than what is already indexed (Rank)? Fix by improving or consolidating the page, or by removing it from the sitemap and internal links if it should not exist. Resubmitting does not change Google's judgement.

**Discovered - currently not indexed.** Google knows the URL but has not crawled it. Check internal links to it (how many, from where, how deep), whether it is in the sitemap with an accurate `lastmod`, and whether the site generates large numbers of low-value URLs (facets, parameters) that soak up crawling. Owner: Connect; on large sites, log analysis. Google also cites rescheduling to avoid overloading the site: check server response times.

**Duplicate, Google chose different canonical than user.** Compare `googleCanonical` with `userCanonical`. Fetch both. If the content is effectively the same, Google is often right: decide which URL the site really wants and make every signal agree (canonical tag, internal links, sitemap, redirects, hreflang). If the content is meaningfully different, make the difference visible in the served HTML. Owner: Connect, then Read. Treat the existing canonical as possibly intentional and confirm with a person before changing it on a page that earns traffic.

**Duplicate without user-selected canonical.** Declare a canonical on the duplicates, pointing at the preferred URL. Owner: Connect.

**Soft 404.** The page returns 200 but looks empty or "not found" (empty search results, out-of-stock pages with nothing else, expired listings). Either return a real 404 or 410, or give the page substance. Owner: Reach for status, Read for content. For ecommerce, see the profile's out-of-stock guidance.

**URL blocked by robots.txt, URL marked noindex, 401, 403.** Usually deliberate. Confirm intent with the user or the code history before touching. If the page should be indexed, Reach owns the fix. Remember that a robots.txt block stops Google seeing a `noindex`.

**Indexed, though blocked by robots.txt.** The URL is indexed from links without Google reading it. If it should not be indexed, allow crawling and serve `noindex`; Reach.

**Server error (5xx), redirect error, not found (404), other 4xx.** Reach for status and hosting; `seo-migrations` for redirect chains and removed pages that should redirect.

**Alternate page with proper canonical; page with redirect.** Working as designed. Act only if the URL itself should be the canonical.

**Page indexed without content.** Google could not read the content. Check rendering, blocked resources and cloaking-like behaviour; Reach.

## 5. Record

One finding per template and cause, not per URL, in the shared schema:

```yaml
id: data-products-canonical-overruled
skill: seo-search-data
area: connect
target: /products/*?colour=*
severity: high
evidence: "URL Inspection 2026-10-03, 12 of 15 sampled colour variants: googleCanonical is the ?colour= URL, userCanonical the base URL. Served HTML: variants differ only in one image; internal links point to ?colour= URLs."
fix: "Point internal links and sitemap at the base URL; keep the canonical. Owner: 4-connect-architecture."
risk: "Product pages earn 41% of organic clicks: needs sign-off."
status: needs-human
verified: 2026-10-03
notes: "Re-inspect sample after next crawl. data_sources: GSC URL Inspection via MCP tool inspect_url."
```
