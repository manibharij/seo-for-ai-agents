# Profile: news / publisher

Use for news sites, magazines, and publishers, anywhere recency and editorial trust drive search. News has its own surfaces (Top Stories, Google News, Discover) and its own signals (freshness, datelines, author authority), on top of the normal ladder. Combine with `content-blog.md` for the content fundamentals.

## How each rung shifts
- **Reach** — speed of crawling/indexing matters more than usual (news is time-sensitive). Ensure new articles are reachable and discoverable fast; a correct, fresh sitemap (plus a **Google News sitemap** for recent articles) helps. Avoid client-rendered article bodies (recency is wasted if the article is an empty shell).
- **Read** — accurate, original reporting; a real **headline** (the `<h1>`), **byline**, and **dateline** (visible publish + update timestamps). Clear, non-clickbait titles that match the story.
- **Understand** — `NewsArticle` schema with **true** `datePublished` and `dateModified`, real `author` (`Person`) and `publisher` (`Organization` with `logo`). For subscription content, mark up paywalled sections correctly (`isAccessibleForFree: false` + `hasPart`/`cssSelector`) so it can be indexed without being treated as cloaking.
- **Connect** — strong section/topic hubs; link related and follow-up coverage; clear canonical for syndicated/wire stories (the originator should be canonical).
- **Rank** — E-E-A-T is paramount for news (and YMYL-adjacent): real, credentialled journalists, sourcing, corrections policy, an about/editorial-standards page. Recency is a ranking signal for news queries, keep evergreen pieces updated, and timestamp honestly.
- **Cite (AEO, on top)** — news is heavily surfaced and cited by AI answers; clear, factual, self-contained reporting with honest attribution is highly citable.

## Type-specific checks
- **Top Stories / Discover eligibility:** these need the technical + E-E-A-T basics right (fast, valid `NewsArticle`, strong author/publisher signals) — but inclusion is Google's call, not guaranteed (see boundary).
- **Google News sitemap:** for articles published in the last ~2 days; keep it current.
- **Timestamps:** accurate, visible `datePublished`/`dateModified`; never fake a "updated" date to look fresh.
- **Paywalled content:** structured-data markup so subscriber content is indexed legitimately (not cloaking).
- **Headlines:** descriptive and accurate; clickbait that mismatches the article hurts trust and performance.
- **Corrections & bylines:** visible author bios, corrections/editorial-standards pages — real E-E-A-T, never fabricated.
- **Avoid duplicate/syndication issues:** canonical wire stories to the originator; don't let republished copies compete.

## The honest news boundary (state it)
- **Google News / Publisher Center inclusion** and **Top Stories/Discover** placement are Google's editorial/algorithmic decisions and policy-gated, you can be *eligible* (technical + E-E-A-T done right) but never *guaranteed* a slot.
- Reputation and authority for a news brand are heavily **off-site/earned** (see `seo-offsite-authority`) and **live** — outside what a build controls.

## Common failures
- Client-rendered article bodies (recency wasted, fails Reach).
- Missing or false `NewsArticle` timestamps; date-bumping without real updates.
- Anonymous articles on topics that demand author authority.
- Clickbait headlines mismatching the story.
- Syndicated copies competing with the original (no canonical to originator).

## Priority tilt
Weight **Reach** (fast indexing), **Understand** (`NewsArticle` + timestamps), and **Rank** (E-E-A-T + recency) highest; be explicit early that Top Stories/Google News inclusion is eligibility, not a guarantee.
