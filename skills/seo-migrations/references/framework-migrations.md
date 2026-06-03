# Where redirects live, per stack — and replatform/domain specifics

Read this to implement the redirect map in the right place for the site, and to handle the bigger cases (replatforming, domain moves). The map (`redirect-mapping.md`) is *what*; this is *where and how*.

---

## Where to implement redirects

### Next.js
- **`redirects()` in `next.config.js`** — best for a known, static list: returns `{ source, destination, permanent: true }` (permanent → 308/301-equivalent). Good for bounded maps.
- **`middleware.ts`** — for dynamic/large or pattern-based redirects (e.g. look up old→new in a map/edge KV). Use when the list is big or data-driven.
- **Hosting-level** (Vercel `vercel.json` `redirects`, Netlify `_redirects`) — also valid and fast (edge).
- Note: Next's `permanent: true` emits `308` (which preserves method and is treated like a permanent redirect); a plain `301` is also fine. Either passes equity.

### Apache
- **`.htaccess`**: `Redirect 301 /old /new` or `RewriteRule` for patterns. Order matters; avoid chains.

### Nginx
- `return 301 https://example.com/new;` in a `location` block, or a `map` for many URLs.

### CDN / edge (Cloudflare, Fastly, etc.)
- Bulk/redirect rules at the edge — fast and centralised; good for large maps and domain moves.

### Hosted platforms (fixes live in the platform, not your repo)
- **WordPress:** a redirect plugin (e.g. Redirection) or server `.htaccess`. Instruct the user where to add entries.
- **Shopify:** **URL Redirects** in the admin (Online Store → Navigation → URL Redirects), or bulk CSV import. Some paths are platform-locked.
- **Wix/Squarespace/Webflow:** the builder's redirect manager / 301 settings panel.
- On these, the agent produces the **map** and tells the user exactly where to enter it.

> Whatever the mechanism, **verify on the served output** (`redirect-mapping.md`) — the implementation isn't trusted until the server returns the right `301` in one hop.

---

## Replatforming (e.g. WordPress → Next.js, custom → Shopify)

The URL structure almost always changes. Sequence:
1. **Inventory** the old URLs (sitemap, CMS export, crawl, the user's analytics/GSC for the high-value ones).
2. **Map** old → new against the new platform's URL scheme (`redirect-mapping.md`).
3. **Rebuild equity-bearing on-page elements** in the new platform: titles, descriptions, headings, canonicals, schema, internal links (run the relevant rungs).
4. **Implement redirects** in the new platform/hosting.
5. **Match or improve** content — don't quietly drop pages that ranked; carry their content over.
6. **Launch, then verify** every high-value old URL `301`s correctly and the new pages are reachable and in the sitemap.
7. **Re-audit** with the orchestrator post-launch to catch anything the move broke (relaunches are a classic source of Reach regressions — e.g. the new platform ships client-rendered).

## Domain moves (example.com → newsite.com)

1. Map every old URL to its new-domain equivalent (path usually preserved → `https://old/x` → `https://new/x`).
2. Implement site-wide `301`s at the **old** domain to the new domain, per URL (not all to the new homepage).
3. **Keep the old domain live** and redirecting for a long time (rankings migrate gradually).
4. Update canonicals, internal links, and the sitemap to the new domain.
5. **Live steps the user does:** verify both properties in Search Console and submit a **Change of Address**; monitor the migration in GSC over the following weeks (live data).

## HTTPS / www consolidation
- Pick one canonical host+protocol (https + one of www/non-www). `301` all other variants to it (single hop), fix mixed content, align canonicals and sitemap. (Also covered in Reach/Connect — coordinate so you don't create chains.)

## The recurring risk
Every one of these can **silently regress** later — a deploy drops the redirect config, a refactor reverts canonicals, a CMS update clears the redirect plugin. Record the redirect set and canonical strategy in `.seo/` so the orchestrator's progression runs re-verify them. A migration isn't "done" the day it launches; it's done when it still verifies weeks later.
