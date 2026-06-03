---
name: 4-connect-architecture
description: >-
  Wire pages into a coherent site so engines understand importance and topical
  relationships — internal linking, site architecture, descriptive anchor text,
  and correct canonical tags so duplicates consolidate instead of competing. Use
  this AFTER Understand passes, on any "internal linking", "site structure", "site
  architecture", "canonical", "duplicate content", "orphan pages", "anchor text",
  or "how should I organise my pages" question. Verifies link graph and canonicals
  on the rendered HTML.
---

# Connect — Internal Links, Architecture & Canonicals

**Rung 4 of the Visibility Ladder. Do not start until Understand passes.** Internal linking is most powerful once engines already know what each page is and which entities it covers — wire *understood* pages together and the whole site reinforces itself.

A page passes Connect when it is reachable through a sensible internal link graph with descriptive anchors, sits in a clear hierarchy that signals topical authority, and has correct canonicals so duplicates consolidate rather than compete.

> **Cardinal rule here:** verify the link graph and canonicals on the **served HTML**. Links injected only client-side, or a canonical set in a component but overridden at render, mislead you. Crawl what is actually served.

Work the four steps: **Diagnose → Fix → Verify → Report.**

---

## Step 1 — Diagnose

### Internal link graph
- **Orphan pages** — pages with no internal links pointing to them. An orphan is hard to discover and signals low importance. Compare your set of real URLs (from the sitemap/routes) against the set actually linked from other pages.
- **Crawl depth** — how many clicks from the homepage to reach important pages? Anything important buried more than ~3 clicks deep is being under-served.
- **Anchor text** — are links descriptive ("our pricing for small teams") or generic ("click here", "read more", bare URLs)? Anchors tell engines what the target is about.
- **Link rendering** — are internal links real `<a href>` elements in the served HTML, or JavaScript click handlers / buttons that a crawler can't follow? (A common AI-build bug: `onClick={() => router.push(...)}` with no `href`.)

### Architecture
- **Hierarchy** — is there a logical structure (home → category/hub → detail) that groups related content? Flat sites with hundreds of equal pages give engines no sense of what matters.
- **Topical clustering** — do related pages link to each other and up to a hub page (the "hub-and-spoke" / topic-cluster pattern)? This concentrates topical authority.
- **Navigation & breadcrumbs** — is primary navigation in the served HTML? Are breadcrumbs present (and matched by `BreadcrumbList` schema from rung 3)?

### Canonicals & duplication
- **Canonical tags** — does each page declare a `<link rel="canonical">`? Does it point to the correct, single preferred URL (self-referential for the canonical version)?
- **Duplicate URLs for one page** — trailing-slash variants, `http`/`https`, `www`/non-`www`, query-parameter and tracking variants, uppercase/lowercase, pagination. These split signals unless canonicalised.
- **Conflicts** — canonical pointing somewhere that's `noindex`ed, redirected, or 404; multiple conflicting canonicals; canonical fighting the sitemap.

See `references/internal-linking.md` and `references/canonicals-and-architecture.md` for the standards.

---

## Step 2 — Fix

Apply structural fixes that are clearly correct; flag changes to site navigation or information architecture that are editorial/business decisions (see Step 4).

### Internal linking (mostly safe)
- **Use real `<a href>` links** for navigation, not JS-only click handlers. In Next.js, use `<Link href>` (it renders an `<a href>` in the served HTML) rather than programmatic `router.push` for content navigation.
- **Connect orphans** by linking them from relevant hub/related pages with descriptive anchors.
- **Improve anchor text** — replace "click here"/"read more" with text describing the destination. Keep it natural, not stuffed.
- **Add contextual and related links** between topically related pages, and up to their hub.

### Architecture (propose; let the user approve big moves)
- **Establish hubs** for topic clusters: a hub page linking to its detail pages and vice versa.
- **Flatten excessive depth** so important pages are within ~3 clicks of the homepage.
- **Add breadcrumbs** in the served HTML, mirrored by `BreadcrumbList` schema.
- Reorganising primary navigation or URL structure affects users and existing links — **propose and explain; don't silently restructure.**

### Canonicals & duplication (safe once intent is confirmed)
- Add **self-referential canonicals** to the preferred version of each page.
- Point duplicate/variant URLs' canonicals at the single preferred URL.
- Resolve **one preferred host/protocol** (https + one of www/non-www) and redirect the rest with `301`s (coordinate with the Reach rung's redirect work).
- Handle parameters and pagination per `references/canonicals-and-architecture.md`.
- **Next.js:** set canonicals via the Metadata API (`alternates: { canonical }`) consistently, ideally derived from the route so they can't drift.

> Don't use canonicals to "hide" pages (that's what `noindex` is for) or to point unrelated pages at each other. A canonical asserts "these are the same page"; misusing it confuses engines.

---

## Step 3 — Verify (on the rendered output)

- **Links are real and served:** fetch key pages and confirm internal links are `<a href>` elements in the served HTML, with descriptive anchors. Spot-check that important pages are now linked (no longer orphaned).
- **Depth:** confirm important pages are reachable within ~3 clicks from the homepage via served links.
- **Canonicals:** fetch each template and confirm a single, correct `<link rel="canonical">` in the served HTML, pointing to a `200`, indexable, non-redirecting URL — and that variants point to the preferred URL.
- **Consistency:** canonical, sitemap, and internal links should all agree on the preferred URL.

Exact crawl/inspection steps and the checklist are in `references/canonicals-and-architecture.md`. **If links or canonicals aren't right in the served output, it isn't done.**

---

## Step 4 — Report to the user (plain English)

1. **What was wrong** — e.g. "Twelve of your pages had no links pointing to them, so they were nearly invisible to search engines — and your menu used buttons instead of real links, which crawlers can't follow."
2. **What I changed and why it matters** — links added, anchors improved, canonicals set, each tied to discoverability or signal consolidation.
3. **Proof** — the now-linked pages and correct canonicals in the served HTML.
4. **What only you can decide** — information-architecture and navigation choices: "I recommend grouping these ten articles under a 'Guides' hub — shall I? It changes your menu." Plus which of any duplicate URLs is the *preferred* one.

Then point up the ladder: with the site connected, the final rung is **Rank** (`5-rank-relevance`) — making the page good and relevant enough to actually rank (intent, quality, E-E-A-T, topical authority). Above the ladder, once it ranks, the optional **Cite (AEO)** layer formats it to be quoted by AI answer engines.

---

## Reference files (read when you need them)
- `references/internal-linking.md` — link graph, orphans, crawl depth, anchor text, hub-and-spoke topic clusters, real-vs-JS links.
- `references/canonicals-and-architecture.md` — canonical rules, duplicate/variant handling, parameters & pagination, host/protocol consolidation, and verification.
