# Profile: news / publisher

Use for news sites, magazines, and publishers, anywhere recency and editorial trust drive search. News has its own surfaces (Top Stories, Google News, Discover) and its own signals (freshness, datelines, author authority), which draw across all five systems. Combine with `content-blog.md` for the content fundamentals.

## How the five systems shift

- **Demand** (observed). News demand spikes and decays within hours, so reading it is about which stories this title can credibly own right now, not maintaining a static keyword list.
- **Identity** (built). **Decisive here, not decorative.** Real, credentialled journalists with `Person` schema, a publisher `Organization` with a `logo`, a corrections policy, and visible editorial-standards and about pages. This is where the experience and expertise that news lives on actually sit, and none of it may be fabricated.
- **Substance** (built). Accurate, original reporting with real sourcing, and headlines that match the story rather than baiting the click. Recency counts, so keep evergreen pieces updated, and timestamp honestly: date-bumping without a real update is flagged, never performed.
- **Access** (built). The Visibility Ladder, in dependency order. Speed is the difference here, because a story crawled late is a story wasted.
  1. **Reach.** Crawling and indexing speed matter more than usual, because news is time-sensitive. Ensure new articles are reachable and discoverable fast; a correct, fresh sitemap plus a **Google News sitemap** for recent articles helps. Avoid client-rendered article bodies.
  2. **Read.** A real **headline** (the `<h1>`), **byline** and **dateline**, with visible publish and update timestamps, all present in the served HTML.
  3. **Understand.** `NewsArticle` schema with **true** `datePublished` and `dateModified`, real `author` (`Person`) and `publisher` (`Organization` with `logo`). For subscription content, mark up paywalled sections correctly (`isAccessibleForFree: false` plus `hasPart`/`cssSelector`) so it can be indexed without being treated as cloaking.
  4. **Connect.** Strong section and topic hubs, linked related and follow-up coverage, and a clear canonical for syndicated or wire stories pointing back to the originator.
- **Distribution** (earned, advisory). A news brand's standing is earned off-site: citations by other outlets, wire relationships, and the communities that carry a story. Analyse the gap and advise; never execute outreach.

**On assistant surfaces.** News is heavily surfaced by AI answers, and clear, factual, self-contained reporting with honest attribution raises **eligibility** to be named. Top Stories, Google News and Discover are separate surfaces with their own gates, and Discover in particular is close to unobservable: done right you are eligible, never guaranteed. See `surfaces/` and `seo-surface-assistants`.

## Type-specific checks
- **Top Stories / Discover eligibility:** these need Access and Identity right (fast, valid `NewsArticle`, strong author and publisher signals), but inclusion is Google's call and never guaranteed (see boundary).
- **Google News sitemap:** for articles published in the last ~2 days; keep it current.
- **Timestamps:** accurate, visible `datePublished`/`dateModified`; never fake a "updated" date to look fresh.
- **Paywalled content:** structured-data markup so subscriber content is indexed legitimately (not cloaking).
- **Headlines:** descriptive and accurate; clickbait that mismatches the article hurts trust and performance.
- **Corrections & bylines:** visible author bios, corrections/editorial-standards pages — real E-E-A-T, never fabricated.
- **Avoid duplicate/syndication issues:** canonical wire stories to the originator; don't let republished copies compete.

## The honest news boundary (state it)
- **Google News / Publisher Center inclusion** and **Top Stories/Discover** placement are Google's editorial/algorithmic decisions and policy-gated, you can be *eligible* (technical + E-E-A-T done right) but never *guaranteed* a slot.
- Reputation and authority for a news brand are heavily **off-site/earned** (see `seo-distribution-authority`) and **live** — outside what a build controls.

## Common failures
- Client-rendered article bodies (recency wasted, fails Access at Reach).
- Missing or false `NewsArticle` timestamps; date-bumping without real updates.
- Anonymous articles on topics that demand author authority.
- Clickbait headlines mismatching the story.
- Syndicated copies competing with the original (no canonical to originator).

## Priority tilt
Weight **Access** (fast discovery at Reach, honest `NewsArticle` markup at Understand) and **Identity** (credentialled journalists, corrections policy, editorial standards) highest, with **Substance** close behind. Be explicit early that Top Stories and Google News inclusion is eligibility, not a guarantee.
