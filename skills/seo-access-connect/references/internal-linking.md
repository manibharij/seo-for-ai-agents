# Internal linking and site architecture

Read this when fixing the link graph and structure. Internal links do two jobs: they help engines **discover** pages, and they distribute **importance and topical relevance** around the site. A page no one links to is a page the site itself is saying doesn't matter.

---

## Real links vs JavaScript navigation — check this first

Engines follow `<a href="...">`. They generally do **not** follow:
- `<button onClick={() => router.push('/page')}>` — no `href`, not a link.
- `<div onClick={...}>` styled to look like a link.
- `<a>` with no `href` (or `href="#"`) wired up purely in JS.

This is a frequent AI-build bug: navigation that works for a mouse user and is invisible to a crawler. **In the served HTML there must be `<a href>` with a real URL.**

- **Next.js:** use `<Link href="/page">` for content navigation — it renders a crawlable `<a href>`. Reserve `router.push` for genuine post-action redirects (after a form submit), not for primary navigation.
- Verify by fetching the page and confirming `<a href>` elements with real URLs are in the served output.

---

## Orphan pages — linked from nowhere

An **orphan** has no internal links pointing to it. It may sit in your sitemap and still be barely discovered and treated as unimportant.

- **Find them:** take the set of real URLs (from routes/sitemap) and subtract the set of URLs linked from other pages. What remains is orphaned or near-orphaned.
- **Fix them:** link each orphan from genuinely relevant pages — its topic hub, related articles, category listings — with descriptive anchors. Don't dump a "links" block of unrelated pages; relevance is the point.

---

## Crawl depth — how far from the homepage

**Crawl depth** = minimum clicks from the homepage to reach a page. Important pages buried deep are crawled less and seen as less important.

- Keep important pages within ~**3 clicks** of the homepage.
- Use hub pages, good navigation, and contextual links to shorten paths to key content.
- Beware deep pagination and faceted navigation that pushes content many clicks down — surface important items via hubs or curated links.

---

## Anchor text — tell engines what the target is about

The clickable text of a link describes its destination to engines and users.

- **Descriptive:** "our pricing for small teams", "the Next.js rendering guide".
- **Avoid:** "click here", "read more", "this page", bare URLs — they waste the signal.
- **Natural, not stuffed:** vary anchors; don't point fifty exact-match keyword anchors at one page. Over-optimised internal anchors look manipulative.
- Anchors should make sense out of context (a screen-reader user tabbing through links should understand each one) — the same discipline that helps engines.

---

## Hub-and-spoke / topic clusters — concentrate authority

The strongest internal-linking pattern for topical authority:

- A **hub (pillar) page** broadly covers a topic and links out to detailed **spoke** pages on sub-topics.
- Each **spoke** links back up to the hub and across to sibling spokes where relevant.
- Result: a tightly interlinked cluster that tells engines "this site is an authority on this topic", with the hub as the consolidating page.

Map your content to topics, identify or create the hub for each, and wire the spokes both ways. This pattern also sets up the Cite rung: clusters of well-linked, well-understood pages are easier for AI engines to navigate and attribute.

---

## Navigation and breadcrumbs

- **Primary navigation** must be in the served HTML (real links). A mega-menu rendered only client-side hides your most important links from crawlers.
- **Breadcrumbs** show hierarchy to users and engines; pair them with `BreadcrumbList` schema (rung 3). They also shorten perceived depth and clarify structure.
- **Footer links** are fine for utility/secondary links but don't rely on a footer link as a page's only internal link — contextual links carry more weight.

---

## Verifying the link graph on the served output

- Fetch key pages; confirm internal links are `<a href>` with real URLs and descriptive anchors **in the served HTML**.
- Re-check former orphans are now linked from relevant pages.
- Trace click-depth to important pages via served links; confirm ≤ ~3 where it matters.
- Confirm primary nav and breadcrumbs are present in the served output, not JS-only.
- If a crawl/render MCP is available, use it to map links at scale; otherwise sample representative templates.
