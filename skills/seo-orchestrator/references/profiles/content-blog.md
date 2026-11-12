# Profile: content / blog / news

Use for blogs, news, magazines, and content/affiliate sites. The product *is* the content, so the value concentrates in **Substance** (depth and originality), **Identity** (a real, resolvable author), and the Connect rung of **Access** (topic clusters).

## How the five systems shift

- **Demand** (observed). Question and comparison demand, and the seasonality behind it. Reading it properly is what stops a content site writing twenty posts into one intent and splitting its own signals.
- **Identity** (built). Real, consistent author pages with `Person` schema and `sameAs` to genuine profiles. Experience and expertise are Identity work, and they are what an answer engine checks before quoting anyone. Never fabricated: a missing author is a job for a human, not a field to fill in.
- **Substance** (built). **The heaviest system here.** Depth, originality and information gain decide everything, and thin or templated posts are the main failure. Match content to **search intent** precisely. Honest freshness too: genuinely update and re-date cornerstone posts rather than bumping dates, and merge or re-target posts that compete with each other.
- **Access** (built). The Visibility Ladder, in dependency order. Usually healthier on a content CMS than on an app, but two failures here are common and both are silent.
  1. **Reach.** Mostly fine on a content CMS, but watch client-rendered article bodies and infinite-scroll or "load more" archives that hide posts from crawlers. Ensure paginated archives are crawlable.
  2. **Read.** Strong heading outlines, real author bylines, accurate visible dates, and body copy that is genuinely in the served HTML.
  3. **Understand.** `Article`/`BlogPosting` (or `NewsArticle`) with real `author` (`Person`) and `publisher`; `datePublished`/`dateModified` that are true. `BreadcrumbList`.
  4. **Connect.** **Topic clusters** are the signature move: pillar and hub pages linking to detailed posts and back. Hunt **orphan posts** and fix **cannibalisation** (multiple posts targeting the same intent: consolidate or differentiate). `noindex` thin auto-generated archives while keeping useful hubs.
- **Distribution** (earned, advisory). Mentions, syndication and the communities the readers actually use. Find the gap and write the angle. Earning the link is real work done by people over time, and the agent refuses to fake it.

**On assistant surfaces.** Content sites are among the strongest candidates to be named, so headings that say what the section answers, self-contained answers, definitions and comparison tables pay off most here. Do not fragment pages into FAQ chunks. This raises **eligibility**, which is the only honest claim: an engine synthesises from many sources and may cite nobody, and presence can only be sampled. See `surfaces/` and `seo-surface-assistants`.

## Type-specific checks
- **Content freshness:** genuinely update and re-date cornerstone posts; don't just bump dates.
- **Author entities:** real, consistent author pages with `Person` schema and `sameAs` to genuine profiles — strong for both ranking and AI attribution.
- **Cannibalisation:** two posts competing for one query split signals — merge or re-target.
- **Tag/category archives:** thin auto-generated archives can bloat the index; `noindex` the low-value ones, keep useful hubs.
- **Pagination:** archive pages self-canonicalise; ensure older posts remain reachable via hubs.

## Common failures
- Thin, AI-spun posts with no real expertise (fails Substance, and with it eligibility anywhere).
- Dozens of near-duplicate posts cannibalising each other.
- Orphan posts linked from nowhere.
- Fabricated authors/dates — **never** do this; flag for a real byline instead.

## Priority tilt
Weight **Substance** and **Identity** highest, with the **Connect** rung of Access (clusters) close behind. Quick wins: fix orphans, add real author schema, surface buried answers.
