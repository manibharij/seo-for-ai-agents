# Connect — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the Connect skill. Run Reach, Read, and Understand first.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are wiring my pages into a coherent site so engines understand importance and topical relationships — internal links, architecture, anchor text, and canonical tags. This is rung 4 of the Visibility Ladder. Work in four steps.

**Verify on what is actually SERVED.** Links injected only client-side, or a canonical overridden at render, will mislead you — crawl the served HTML.

## Step 1 — Diagnose
- **Links:** Are internal links real `<a href>` elements in the served HTML, or JS-only click handlers/buttons a crawler can't follow? Any **orphan pages** (no internal links pointing to them)? Are important pages within ~3 clicks of the homepage? Is anchor text descriptive or generic ("click here")?
- **Architecture:** Is there a logical hierarchy (home → hub → detail)? Do related pages link to each other and to a hub? Is primary nav in the served HTML?
- **Canonicals:** Does each page have exactly one `<link rel="canonical">` pointing to the correct preferred URL? Any duplicate URL variants (http/https, www/non-www, trailing slash, case, tracking params) splitting signals? Any canonical pointing at a noindexed/redirected/404 page?

## Step 2 — Fix
- Use real `<a href>` links (Next.js: `<Link href>`, not `router.push` for navigation). Link orphans from relevant pages with **descriptive anchors**. Build hub-and-spoke topic clusters (hub links to details, details link back).
- Add **self-referential canonicals** to preferred pages; point variant URLs at the preferred one. Enforce one host+protocol with `301`s. **Next.js:** set canonicals via the Metadata API (`alternates: { canonical }`), derived from the route so they can't drift.
- Add breadcrumbs (mirrored by `BreadcrumbList` schema).
- **Propose, don't silently make,** big navigation/URL-structure changes — those affect users and existing links. Ask me which duplicate URL is the *preferred* one when it's ambiguous.
- Don't misuse canonicals to hide pages (use `noindex`) or point unrelated pages at each other.

## Step 3 — Verify (re-fetch)
Confirm in the **served HTML**: internal links are real `<a href>` with descriptive anchors; former orphans are now linked; important pages reachable within ~3 clicks; exactly one correct `<link rel="canonical">` per page pointing to a 200/indexable URL; canonical agrees with sitemap and internal links.

## Step 4 — Explain it to me in plain English
1. **What was wrong** (e.g. "12 pages had no links pointing to them; your menu used buttons crawlers can't follow").
2. **What you changed and why it matters.**
3. **Proof** — now-linked pages and correct canonicals in the served HTML.
4. **What only I can decide** — information-architecture/navigation changes, and which duplicate URL is preferred.

Then tell me the final step is **Cite** (formatting pages to be quoted by AI answer engines like Google's AI Overviews, ChatGPT, and Perplexity).
