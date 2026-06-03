---
name: seo-migrations
description: >-
  Preserve search equity when URLs change — site redesigns, replatforming, domain
  moves, framework migrations, slug changes, HTTPS/www switches, or pruning pages.
  Use on any "migrate", "redesign", "moving to a new domain/CMS", "changed our URLs",
  "404s after relaunch", "redirect", "don't lose rankings when we relaunch", or
  "merge two sites" task. Builds a 1:1 redirect map, applies 301s, updates internal
  links/sitemap/canonicals, and verifies every old URL resolves on the served output.
---

# Migrations & Redirects — preserve equity when URLs change

A specialist skill outside the ladder, for the single most dangerous thing you can do to an existing site: **change its URLs.** A redesign or replatform that drops redirects can erase years of rankings overnight. This skill exists so that doesn't happen. It's the partner of the orchestrator's `seo-orchestrator/references/existing-site-safety.md` — read that too.

> The prime directive: **no ranking URL is ever left to 404.** Every old URL either still works or `301`-redirects to the best equivalent new URL.

Work the four steps: **Diagnose → Plan & Fix → Verify (on served output) → Report.** On large changes, this skill produces a redirect *map* you and the user review before applying.

---

## When this fires
- A site redesign or restructure that changes paths/slugs.
- Replatforming (e.g. WordPress → Next.js, custom → Shopify).
- A domain change or merging/splitting sites.
- HTTP→HTTPS or www↔non-www consolidation (also touched in Reach/Connect).
- Pruning or consolidating pages (removing thin content, merging duplicates).
- Post-relaunch cleanup ("we relaunched and traffic dropped / we have 404s").

---

## Step 1 — Diagnose

- **Establish the old URL inventory.** Get the list of existing indexed/ranking URLs from whatever's available: the current sitemap, server/router config, the CMS, analytics/Search Console exports (the user provides these — they're live data), or a crawl. The goal is to know **which URLs exist and matter** before anything changes.
- **Establish the new URL set** — the post-change paths.
- **Diff them.** Which URLs are unchanged, changed (old→new mapping needed), removed (need a redirect target or deliberate `410`), or new.
- **Find existing breakage** (post-relaunch cases): URLs returning `404`/`5xx` that used to work, redirect **chains** (A→B→C) and **loops**, redirects to `noindex`/404 targets, and internal links still pointing at old URLs.
- **Check the high-value URLs first** — the pages with traffic/links/rankings matter most; prioritise their mapping (the user's analytics/GSC data identifies these — live data, on their side).

---

## Step 2 — Plan & Fix

### Build the redirect map (review before applying)
- Map **old → new 1:1** to the *closest equivalent* page. Don't lazily redirect everything to the homepage — irrelevant redirects lose most of the equity and frustrate users.
- For removed pages with no equivalent: redirect to the most relevant parent/category, or return **`410 Gone`** if truly, permanently removed and you want it de-indexed.
- For consolidations (several old pages → one): `301` all to the survivor.
- Present the map (especially for many URLs) for the user to sanity-check before applying — see `references/redirect-mapping.md`.

### Apply
- Use **`301` (permanent)** for permanent moves — it passes equity and updates the index. Use `302` only for genuinely temporary moves.
- **Single hop:** old → final new URL directly. Collapse any chains so nothing goes A→B→C.
- **Update internal links** to point at the new URLs (don't rely on redirects internally — fix the links).
- **Update the sitemap** to list only new, canonical `200` URLs; remove old ones.
- **Update canonicals** to the new URLs.
- Implement in the right place for the stack/platform (`references/framework-migrations.md`): Next.js `redirects()` in `next.config` with `permanent: true` (which emits a `308` — a permanent redirect equivalent to `301`), or middleware/hosting rules, `.htaccess`/Nginx, CDN/edge rules, or the platform's redirect manager (Shopify/WordPress). On hosted platforms, redirects may live in the platform UI — instruct the user precisely.
- For **domain moves**, also: set up redirects at the old domain, keep it live, update canonicals/sitemap to the new domain, and have the user use Search Console's Change of Address (live step, their side).

> Coordinate with the lifecycle: record the migration in `.seo/log.md`, and add the redirect set as findings to re-verify on future runs (redirects silently get dropped in later deploys).

---

## Step 3 — Verify (on the served output)

A redirect is only real if the server actually serves it. For a representative sample of old URLs (and **all** high-value ones):
- Fetch each old URL and confirm it returns a **permanent redirect — `301` or `308`** (Next.js/Vercel `permanent` rules emit `308`, which passes equity identically; accept either, reject `302`/`307`/`200`/`404`) whose `Location` is the correct new URL, and that the new URL returns **`200`** — in a **single hop**.
- Confirm **no chains or loops** (follow the full redirect path).
- Confirm no redirect points to a `noindex`/`404`/non-canonical target.
- Confirm the **sitemap** lists only new `200` URLs and internal links point to new URLs.
- Spot-check that important old URLs land on a genuinely equivalent new page (not a generic homepage dump).

Exact checks/commands in `references/redirect-mapping.md`. **If an old URL 404s or chains, it isn't done.**

---

## Step 4 — Report (plain English)

1. **What was at risk** — "Your relaunch changed 240 URLs; without redirects, Google would have dropped the rankings tied to the old ones."
2. **What I did** — the redirect map (old→new), 301s applied, internal links/sitemap/canonicals updated, each tied to preserving equity.
3. **Proof** — served-output checks: old URLs now `301` to the right new URLs in one hop; new URLs `200`.
4. **What needs you** — sign-off on the redirect map (especially ambiguous mappings), and the live steps only you can do: submit the new sitemap and (for domain moves) the Change of Address in Search Console.
5. **The boundary** — redirects preserve equity at build time; the actual recovery/movement of rankings is live data you'll watch over the following weeks (point across the boundary).

---

## Reference files
- `references/redirect-mapping.md` — building and reviewing the old→new map, status-code choices, and the exact served-output verification steps.
- `references/framework-migrations.md` — where redirects live per stack/platform (Next.js, Apache/Nginx, CDN, Shopify/WordPress) and replatforming/domain-move specifics.
