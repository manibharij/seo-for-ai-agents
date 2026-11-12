# Building and verifying the redirect map

Read this to produce a correct old→new redirect map and prove it on the served output. The map is the heart of a safe migration; get it reviewed before applying, and verified after.

---

## Status codes — choose deliberately

| Code | Use for | Effect |
|---|---|---|
| **301** Moved Permanently | Permanent moves (the default for migrations) | Passes equity; index updates to the new URL |
| **302** Found (temporary) | Genuinely temporary moves only | Does **not** pass equity / consolidate; index keeps the old URL |
| **410** Gone | Pages permanently removed with no equivalent | Stronger de-index signal than 404 |
| **404** Not Found | Genuinely missing (avoid for URLs that had value) | Eventually dropped; equity lost |

Default to **301** for moved content. Use **410** for deliberate permanent removals. Reserve **302** for the rare true-temporary case (don't use it for a permanent move — a common, costly mistake).

> **301 vs 308:** `308` is also a *permanent* redirect and passes equity exactly like `301` — it just additionally preserves the HTTP method. Next.js `redirects({ permanent: true })` and Vercel/Netlify `permanent` rules emit `308`. So when you verify, **accept `301` or `308`**; both are correct for a permanent move. (`307` is the temporary equivalent of `308` — treat it like `302`.)

---

## Mapping rules

- **1:1 to the closest equivalent.** Each old URL → the new page that best matches what the old page was about. A blog post → its new URL; a product → the new product page; a category → the new category.
- **Don't bulk-redirect to the homepage.** Redirecting many unrelated URLs to `/` ("soft 404" behaviour) wastes most of the equity and is a known anti-pattern. Only the homepage's own old URL maps to the homepage.
- **Consolidations:** several old pages that now live as one → all `301` to the survivor.
- **Removals with a near-match:** redirect to the most relevant parent/category.
- **Removals with no match, permanent:** `410` (or `404`) — deliberately, not by neglect.
- **Single hop:** if old URLs already redirect somewhere, point them at the *final* destination so you don't create chains during the migration.
- **Preserve query/anchor semantics** where they matter; strip tracking params in the target.

## Review before applying
For anything beyond a handful of URLs, present the map for human review — a table is ideal:

```
| Old URL                    | New URL                      | Code | Note                |
|----------------------------|------------------------------|------|---------------------|
| /old-blog/seo-tips         | /blog/seo-tips               | 301  | direct match        |
| /services/web-design-2019  | /services/web-design         | 301  | renamed             |
| /products/old-widget       | /products/widget-v2          | 301  | replaced            |
| /landing/promo-expired     | /offers                      | 301  | no equivalent → parent |
| /temp/internal-test        | —                            | 410  | permanently removed |
```

High-value URLs (traffic/links/rankings — from the user's analytics/GSC) **must** be mapped explicitly and reviewed, not left to a catch-all rule.

---

## Verifying on the served output

For a representative sample, and **every high-value URL**:

```bash
# Follow the full redirect chain and show each hop's status + location
curl -sIL https://example.com/old-blog/seo-tips | grep -iE "^HTTP|^location"
```
```powershell
# PowerShell: inspect the redirect without auto-following, then confirm the target
$r = Invoke-WebRequest "https://example.com/old-blog/seo-tips" -MaximumRedirection 0 -SkipHttpErrorCheck
$r.StatusCode; $r.Headers.Location
```

Confirm:
- [ ] Old URL returns a **permanent redirect — `301` or `308`** (not `302`/`307`, not `200`, not `404`). Next.js `redirects({ permanent: true })` and Vercel/Netlify `permanent` rules emit **`308`**, which passes equity identically to `301` — accept it.
- [ ] `Location` is the **correct** new URL.
- [ ] The new URL returns **`200`** — and it's the **single** hop (no A→B→C chain, no loop).
- [ ] The target is **canonical and indexable** (not `noindex`/redirected/404).
- [ ] **Internal links** point at the new URL (not the old one relying on the redirect).
- [ ] The **sitemap** lists only new `200` URLs.
- [ ] Important old URLs land on a genuinely equivalent page (manual spot-check).

Record the verified redirect set in `.seo/` so future progression runs re-check it — redirects are routinely lost in later deploys/refactors, and that's a classic silent regression.
