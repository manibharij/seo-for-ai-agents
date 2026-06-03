# Profile: content / blog / news

Use for blogs, news, magazines, and content/affiliate sites. The product *is* the content, so the value concentrates in **Read**, **Understand** (Article), **Connect** (topic clusters), and **Cite** (these sites are prime AI-citation candidates).

## How each rung shifts
- **Reach** — usually fine on a content CMS, but watch client-rendered article bodies and infinite-scroll/"load more" archives that hide posts from crawlers. Ensure paginated archives are crawlable.
- **Read** — the heaviest rung here. Depth, originality, and genuine expertise matter most; thin/templated posts are the main failure. Strong heading outlines, real author bylines, accurate dates. Match content to **search intent** precisely.
- **Understand** — `Article`/`BlogPosting` (or `NewsArticle`) with real `author` (`Person`) and `publisher`; `datePublished`/`dateModified` that are true. `BreadcrumbList`.
- **Connect** — **topic clusters** are the signature move: pillar/hub pages linking to detailed posts and back. Hunt **orphan posts** and fix **cannibalisation** (multiple posts targeting the same intent — consolidate or differentiate).
- **Cite** — answer-block formatting pays off most here: question-shaped headings, self-contained answers, definitions, comparison tables. Real author E-E-A-T is a major citation signal.

## Type-specific checks
- **Content freshness:** genuinely update and re-date cornerstone posts; don't just bump dates.
- **Author entities:** real, consistent author pages with `Person` schema and `sameAs` to genuine profiles — strong for both ranking and AI attribution.
- **Cannibalisation:** two posts competing for one query split signals — merge or re-target.
- **Tag/category archives:** thin auto-generated archives can bloat the index; `noindex` the low-value ones, keep useful hubs.
- **Pagination:** archive pages self-canonicalise; ensure older posts remain reachable via hubs.

## Common failures
- Thin, AI-spun posts with no real expertise (fails Read and Cite).
- Dozens of near-duplicate posts cannibalising each other.
- Orphan posts linked from nowhere.
- Fabricated authors/dates — **never** do this; flag for a real byline instead.

## Priority tilt
Weight **Read** and **Cite** highest, with **Connect** (clusters) close behind. Quick wins: fix orphans, add real author schema, surface buried answers.
