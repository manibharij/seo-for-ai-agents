# Canonicals and duplicate handling

Read this to consolidate duplicate URLs so they reinforce one page instead of competing. A canonical tag tells engines "of these equivalent URLs, *this* is the one to index and credit." Get it wrong and you scatter your signals or hide the wrong page.

---

## What a canonical is (and isn't)

`<link rel="canonical" href="https://example.com/preferred-url">` in the `<head>` declares the preferred URL among duplicates or near-duplicates.

- It is a **strong hint**, not a directive — engines usually honour a sensible one, but a contradictory or nonsensical canonical can be ignored.
- It is **not** a redirect (users still load the URL they requested) and **not** a way to hide a page (use `noindex` for that).
- The canonical version should be **self-referential**: the preferred URL's own canonical points to itself.

---

## The duplicate-URL families to consolidate

One page is often reachable at many URLs. Pick one **preferred** form and point the rest at it (via canonical, and ideally `301` redirects for the host/protocol cases):

- **Protocol:** `http://` vs `https://` → always prefer `https://`.
- **Host:** `www.` vs non-`www.` → pick one, redirect the other.
- **Trailing slash:** `/page` vs `/page/` → pick one consistently.
- **Case:** `/Page` vs `/page` → prefer lowercase; treat URLs as case-sensitive and standardise.
- **Index files:** `/dir/` vs `/dir/index.html` → prefer the clean directory URL.
- **Query parameters:** tracking (`?utm_*`), session IDs, sort/filter params that don't change content → canonical to the clean URL.
- **Faceted/filter URLs:** combinations that produce thin or duplicate content → canonical to the base, or `noindex` the low-value combinations (decide per case).

> Decide the *preferred* form **with the user** when it's ambiguous — it's a one-time decision with site-wide consequences. Then apply it consistently across canonicals, internal links, and the sitemap.

---

## Parameters and pagination

- **Tracking/sort/filter params** that don't change the core content → set the canonical to the parameter-free URL. Keep internal links pointing at clean URLs.
- **Pagination** (`/blog?page=2`): current guidance is to let each page **self-canonicalise** (page 2's canonical is page 2), *not* to canonicalise every page to page 1 (that hides pages 2+). Ensure `rel="next"/"prev"` is not relied upon (deprecated as an indexing signal) — instead make sure paginated items are also reachable via hubs/links. Don't canonicalise a "view all" and the paginated set at cross purposes.
- **Faceted navigation** can explode into millions of URLs; combine canonicals, selective `noindex`, and robots rules deliberately (coordinate with the Reach rung).

---

## Conflicts to catch and resolve

A canonical setup fails silently when signals contradict. Check for:
- Canonical pointing to a URL that is **`noindex`**, **redirected**, or **404** — the canonical target must be a `200`, indexable page.
- **Multiple/conflicting** `<link rel="canonical">` on one page (e.g. one from a layout, one from the page) — there must be exactly one.
- Canonical **disagreeing with the sitemap** (sitemap lists URL A, page canonicalises to URL B) — align them.
- Canonical **disagreeing with internal links** (you link to `/page/` everywhere but canonicalise to `/page`) — align them.
- Cross-domain canonicals pointing off-site by mistake.

---

## Next.js App Router — setting canonicals (your stack)

Set canonicals through the Metadata API so they render into the served HTML and can be derived from the route (preventing drift):

```tsx
// static
export const metadata = { alternates: { canonical: '/about' } }

// dynamic — derive from the same param the route uses
// Next.js 15+: params is a Promise — await it (Next 14 passed it synchronously).
export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params
  return { alternates: { canonical: `/blog/${slug}` } }
}
```

With `metadataBase` set in the root layout, these resolve to absolute URLs. Deriving the canonical from the route parameter is the safest pattern — the canonical and the actual URL cannot disagree. Avoid hand-writing `<link rel="canonical">` in JSX alongside the Metadata API (you'll get duplicates).

Other frameworks: Astro (`<link rel="canonical">` in the layout head from `Astro.url`), Nuxt (`useHead`), SvelteKit (`<svelte:head>` using `$page.url`).

---

## Verifying canonicals & architecture on the served output

```bash
curl -sL https://example.com/page | grep -i "rel=\"canonical\""
```
```powershell
(Invoke-WebRequest -Uri "https://example.com/page" -UseBasicParsing).Content |
  Select-String -Pattern 'rel="canonical"'
```

Confirm in the served HTML, per template:
- [ ] Exactly **one** `<link rel="canonical">`, pointing to the correct preferred URL.
- [ ] The canonical target is a `200`, indexable, non-redirecting page.
- [ ] Variant URLs (slash/case/params/host) resolve to or canonicalise to the preferred URL.
- [ ] Canonical agrees with the **sitemap** and with **internal links**.
- [ ] One preferred host + protocol enforced (https + chosen www/non-www), others `301`-redirected.
- [ ] Important pages are linked (no orphans) and within ~3 clicks; links are real `<a href>` in the served output.

If any box is unchecked, Connect has not passed. Only then climb to rung 5 (Cite).
