# Changelog

All notable changes to this pack. Because search and AI-answer behaviour change quickly, each release notes the date its guidance is **current as of** — check it against primary sources (Google's structured-data/rich-result docs, each AI engine's crawler docs) before relying on time-sensitive advice.

This project aims to follow [Semantic Versioning](https://semver.org/) loosely while it's pre-1.0 and experimental.

## [Unreleased]

### Changed: the method is now the Visibility Model (five systems), not a single ladder

The ladder's dependency insight was right and too small: it assumed one engine, one
asset, one moment and one kind of work. The method is now **five systems** separated by
your relationship to control, plus an **Operations loop**, judged across many
**surfaces**. See [METHOD.md](METHOD.md) and [`model/`](model/).

- **Demand** (observed), **Identity**, **Substance**, **Access** (built),
  **Distribution** (earned, advisory). Operations keeps all of it true.
- **The Visibility Ladder is now the Access system**, and keeps four rungs: Reach, Read,
  Understand, Connect. Diagnose top to bottom, fix bottom to top, unchanged.
- **Rank is no longer a rung.** It is the outcome the whole model produces. Its old
  contents moved to Substance (intent, quality) and Identity (experience, expertise,
  authorship), which is where the work actually happens.
- **AEO is no longer "the layer on top".** An assistant is a **surface**, not a layer.
  Being named draws on all five systems and is verified far more weakly than a ranking,
  so eligibility remains the only claimable outcome.

### Added: the agentic structure

- **[`model/`](model/)** the canonical method: `systems.md`, `surfaces.md`,
  `invariants.md`.
- **[`contracts/`](contracts/)** four machine-readable schemas so findings can be
  stored, diffed and rendered rather than only read: `finding`, `context-fact`,
  `work-item`, `evidence`. `finding.verify.method` deliberately has no `source` option,
  so "verify on served output" is enforced by the schema rather than by good intentions.
- **[`surfaces/`](surfaces/)** per-surface profiles stating what weighs there, how it is
  verified, and what is unknowable. **All 16 surfaces in the model are now profiled**,
  indexed in [`surfaces/README.md`](surfaces/README.md).
- **[`roles/`](roles/)** role definitions: what a role owns, which tools it may use,
  what it must ask before doing, its budget, and what finishing means. **Six roles**, one
  per system plus the Account Reporter, indexed in [`roles/README.md`](roles/README.md).
- **[`jobs/`](jobs/)** the situation a user actually arrives with, which scopes the model
  and activates roles. **All nine jobs** in the `work-item` contract are now written,
  indexed in [`jobs/README.md`](jobs/README.md).
- **`scripts/check-links.py`** checks every relative link, that each skill's `name:`
  matches its directory, and that no skill is nested, because a nested skill would not
  survive the flat copy into `~/.claude/skills/`.

### Breaking: every skill has been renamed

Skills are now named for the system they belong to. The numeric prefixes encoded the old
five-rung model and had become actively misleading. Update any saved prompts and
installs.

| Old | New |
|---|---|
| `1-reach-indexation` | `seo-access-reach` |
| `2-read-content` | `seo-access-read` |
| `3-understand-schema` | `seo-access-understand` |
| `4-connect-architecture` | `seo-access-connect` |
| `5-rank-relevance` | `seo-substance-quality` |
| `cite-aeo-geo` | `seo-surface-assistants` |
| `seo-performance` | `seo-access-performance` |
| `seo-migrations` | `seo-access-migrations` |
| `seo-log-analysis` | `seo-access-logs` |
| `seo-search-data` | `seo-demand-search-data` |
| `seo-context-gathering` | `seo-identity-context` |
| `seo-positioning-strategy` | `seo-identity-positioning` |
| `seo-content-audit` | `seo-substance-content-audit` |
| `seo-content-editing` | `seo-substance-content-editing` |
| `seo-media` | `seo-substance-media` |
| `seo-programmatic` | `seo-substance-at-scale` |
| `seo-offsite-authority` | `seo-distribution-authority` |
| `seo-measurement-setup` | `seo-operations-measurement` |
| `seo-launch-qa` | `seo-operations-launch-qa` |
| `seo-automations` | `seo-operations-automation` |
| `seo-proposal-roadmap` | `seo-operations-reporting` |

`seo-orchestrator` keeps its name.

Two copy-paste minis were renamed too, because their old names were the two concepts the
model removed:

| Old | New |
|---|---|
| `install/copy-paste/rank.md` | `install/copy-paste/quality.md` |
| `install/copy-paste/cite.md` | `install/copy-paste/assistants.md` |

Every other mini filename in `install/copy-paste/` is unchanged.

### Added: named DataForSEO workflows, so three described analyses become executable

`live-data-integrations.md` already said "think in capabilities, not products", and
`third-party-mcps.md` already covered how to connect DataForSEO, Ahrefs, Semrush and
OpenSEO. What was missing was the step after connecting: **what to actually call, with which
filter, to perform a named analysis.**

New: [`data/dataforseo.md`](skills/seo-orchestrator/references/data/dataforseo.md), verified
against DataForSEO's documentation 2026-11. Six workflows, each with the endpoint, the
request shape, the fields to read and what it cannot tell you.

Three of them were analyses the library described and had no mechanism for:

1. **Cannibalisation without Search Console.** `ranked_keywords/live` returns
   `keyword_data.keyword` and `ranked_serp_element.serp_item.url` per item, so grouping by
   keyword finds any query with two of the site's own URLs. This is the path for
   `client-audit`, which by definition never has the owner's Search Console. Confirmed by
   re-running the SERP on a schedule: a winner that **flips between two of your own pages**
   is confirmed cannibalisation, which is a stronger signal than any single snapshot.
2. **Intent-shift detection.** `search-intent.md` said the result shape changing over time is
   the clearest evidence of an intent shift and gave no way to see it. Snapshot the `type` of
   every SERP element, re-run, diff the mix. A stable mix with you falling is decay; a changed
   mix is an intent shift; an `ai_overview` appearing explains falling clicks on flat
   impressions. `content-decay.md` separates four causes that look identical in a traffic
   graph, and two of them can now be told apart with evidence.
3. **AI Overview references.** `item_types: ["ai_overview_reference"]` returns which pages
   were cited, for which keywords, and the `text` snippet used to generate the overview.
   That last field says which passage was extractable enough to lift, which is the most
   actionable signal available on a surface where the honest alternative is sampled prompts.
   It does not move the claimable outcome: vendor observation, confidence `inferred`,
   eligibility only.

Plus striking distance on a site you do not own (a `rank_group` filter), and page-level
competitor comparison via `relevant_pages/live`.

Wired into `decay-cannibalisation-actions.md` (as a third data path, between the Search
Console method and the title-overlap fallback), `search-intent.md`, `content-decay.md`,
`seo-surface-assistants` and `live-data-integrations.md`.

Honest about its own edges: DataForSEO's Backlinks, OnPage, Business Data, Domain Analytics
and Content Analysis modules are reachable through capability detection and have **no
verified recipe in that file yet**, and it says so rather than implying coverage.

### Added: Ahrefs and Semrush, and a table of which tool can do which workflow

[`data/ahrefs-semrush.md`](skills/seo-orchestrator/references/data/ahrefs-semrush.md),
verified 2026-11. The most useful part is the comparison at the top, because **these tools
are not interchangeable** and choosing by habit is how an analysis becomes impossible
halfway through.

- **Ahrefs Brand Radar** is the only multi-engine AI citation source verified in this pack:
  `chatgpt`, `google_ai_overviews`, `google_ai_mode`, `gemini`, `perplexity`, `copilot`,
  `claude` and `grok`. Two limits shape its use, and both are stated: the response returns
  the cited page and a response count but **not the prompt and not the engine**, so
  attributing by engine means one call per `data_source`; and `claude` supports custom
  prompts only. Requests limited to your own custom prompts are free, which makes a tracked
  prompt set the habit to build. `volume` and `mentions` are deprecated.
- **Ahrefs cannot do the cannibalisation analysis.** `organic-keywords` returns
  `best_position_url`, one ranking URL per keyword, so two of your own pages competing for
  one query never appears. The file says to use DataForSEO for it or to report that it was
  not performed, rather than approximating it by inference.
- **Ahrefs `date_compared`** returns a period-over-period comparison in one call, which
  feeds the progress half of the Operations loop.
- **Semrush `domain_organic_organic`** discovers who actually competes. Wired into
  `earning-angles.md`, because the competitors a business names in a meeting are frequently
  not the ones holding its search demand, and a plan built against the wrong set is wasted.
- **Semrush `backlinks_overview`**: `domains_num` is the number that matters, not `total`,
  which is the same sitewide-footer-link trap called out for DataForSEO.
- Practical traps recorded: Semrush uses **two different base URLs** (domain reports and
  backlinks are not the same host), bills **per line returned** so `display_limit` is never
  optional in practice, and returns CSV with a header row you should confirm columns
  against. Ahrefs documents API v3 from the Lite plan while separately stating that new
  applications require Enterprise activation, so an existing key and a new key are not the
  same situation. Check access before designing a workflow around either.

Throughout, "not verified here" is used rather than asserting a tool cannot do something.

### Added: the rest of the DataForSEO modules, as workflows 7 to 14

[`data/dataforseo-modules.md`](skills/seo-orchestrator/references/data/dataforseo-modules.md),
verified 2026-11. Backlinks, OnPage, Content Analysis and the local endpoints, each as a
named analysis rather than an endpoint list. Four of them give a mechanism to something the
library previously only described:

- **Render-gap detection at scale (10).** `on_page/instant_pages` defaults to
  `enable_javascript: false`, so calling the same URL twice and diffing `checks` finds pages
  whose title, `h1` or description exist only after scripts run. That is the pack's
  number-one finding, across hundreds of URLs instead of one at a time. The finding stays
  `inferred` and the fix is still proven with your own fetch: invariant 1 does not bend for
  a vendor's score.
- **The geo-grid (13).** `surfaces/google-maps.md` said there is no such thing as your
  position "in a town", only positions at points, and that a grid is the only honest report.
  The Maps endpoint takes `location_coordinate` as `"latitude,longitude,zoom"`, so a lattice
  of coordinates produces one. Priced explicitly, because a 7x7 grid is 49 calls per keyword
  per run and that surprises people.
- **Unlinked mentions by subtraction (12).** Content Analysis gives everyone who mentions
  the brand; Backlinks gives everyone who links. The difference is the list `earning-angles.md`
  calls the highest hit rate available and nobody looks at.
- **Google listing consistency (14).** `profiles/local-business.md` began "ask the owner for
  the GBP values (or a screenshot)". `my_business_info` observes `title`, `address_info`,
  `phone`, `category`, the hours timetable and `is_claimed` directly, so the diff runs
  without waiting. The listing side stays `needs-human`, because only the owner can edit it.

Plus the authority gap quantified against named competitors (7), lost links (8), broken
backlinks (9, which is a redirect job rather than a campaign and belongs to
`seo-access-migrations`), and on-page triage on a site you cannot crawl (11).

One trap is called out in both the recipe and `earning-angles.md`: compare **referring root
domains, never total backlinks**. A single partner with a sitewide footer link produces
thousands of backlinks from one domain, and a comparison on the raw count can say the
opposite of the truth.

Still not covered, and stated as such: Domain Analytics, and the task-based full-site OnPage
crawl.

### Added: four more site-type profiles, and depth where the model said it was missing

**Four new profiles**, bringing the set to eleven. They are deliberately *modalities* rather
than sector playbooks, which is why there is no `healthcare.md`: what those sectors share is
that a wrong answer harms somebody, and that is `ymyl-regulated.md`.

| Profile | For | What shifts |
|---|---|---|
| `marketplace-directory` | Marketplaces, job boards, property portals, directories | Access dominates: faceted sprawl and an explicit expiry policy |
| `affiliate-comparison` | "Best X", versus pages, referral-monetised content | Identity and Substance are the constraint: who tested it, and disclosure |
| `portfolio-personal-brand` | One person or a very small studio | Identity, after the client-rendered-portfolio rendering failure |
| `ymyl-regulated` *(modifier)* | Health, legal, finance, safety, gambling, childcare | Identity stops being a weighting and becomes a **gate** |

**Depth added where the audit of the library said the mass was in the wrong place.** The
re-work moved the method's centre of gravity to Substance, Identity and Distribution, but
`skills/` was still distributed the way the old ladder was, with Access holding seven skills and
the deepest references while `seo-substance-quality` had one reference file of 54 lines.

- `seo-substance-quality/references/search-intent.md` — reading intent off the SERP rather than
  from a tool's label, the four distinct mismatch patterns and how to tell them apart (they have
  four different fixes and get reported as one), and intent against the audience's real
  vocabulary.
- `seo-substance-quality/references/information-gain.md` — the test that actually decides
  whether a page wins: does it contain anything the results above it do not? Why word count and
  competitor keyword coverage are not that test, what genuine gain looks like, and what to do
  when the honest answer is that none is available.
- `seo-substance-quality/references/content-decay.md` — telling decay apart from a technical
  cliff, an intent shift and a SERP-feature change, since all four look like "traffic is down".
  Includes the honest-freshness rule, which refuses date-bumping at any autonomy rung.
- `seo-distribution-authority/references/earning-angles.md` — establishing whether authority is
  actually the constraint before recommending a campaign, what a genuinely citable asset looks
  like (proprietary data first), and why drafting outreach "for the human to send" is not a
  loophole in the advisory boundary.

### Fixed: more stale framing, found by a broader sweep

The first pass caught "the Cite rung". A wider sweep found the same problem in other phrasings:
`seo-access-connect` still pointed "up the ladder" to Rank as a final rung with Cite above it,
`prioritisation.md` still sorted by "ladder order" across all systems rather than by the Access
dependency alone, `seo-substance-quality` still described itself as "the top of the ladder" and
recorded findings as `area: rank`, and two `seo-surface-assistants` references still called the
surface a rung. All corrected.

### Added: the agentic layer is filled in, not sketched

The re-work created `jobs/`, `surfaces/` and `roles/` and shipped one example of each. The
model named nine jobs, sixteen surfaces and a department of roles, so a reader arriving at
the repo found a shape that promised far more than the contents delivered. That gap is
closed.

**Nine jobs** (`jobs/`), one per situation in the `work-item` contract's `job` enum, each
with its leading system, its order of work, what it must never do, and what the honest
negative answer looks like:

| Job | They arrive saying | Leading system | Autonomy |
|---|---|---|---|
| `new-site` | "I have an idea and I am about to build it" | Demand | 4 |
| `launch` | "We are going live this week" | Access | 3 |
| `rescue` | "Something is wrong and I do not know why" | Operations, then Access | 2 |
| `grow` | "It works, I want more of it" | Demand, Substance, Distribution | 2 |
| `migrate` | "The URLs are changing" | Access | 2 |
| `scale` | "I need a lot of pages" | Substance, as a gate | 2 |
| `ai-visible` | "I want AI assistants to recommend me" | Identity | 2 |
| `client-audit` | "I need to audit a site I do not control" | The constraint | 1 |
| `maintain` | "Keep it from breaking" | Operations | 4 |

Autonomy tracks what is **at risk**, not difficulty, which is why `new-site` and
`maintain` sit highest and `migrate` and `grow` sit low.

**Sixteen surface profiles** (`surfaces/`), each stating its weighting, how it can be
verified, what is unknowable, and what may never be claimed. `google-web`, `google-maps`,
`google-ai-mode`, `google-shopping`, `google-images`, `google-news-discover`,
`bing-copilot`, `perplexity`, `chatgpt`, `claude`, `gemini`, `youtube`,
`reddit-communities`, `app-store`, `marketplace`, `agent-mcp`. `model/surfaces.md` now
links to each one.

The leading system differs per surface, which is the main practical use of these files:
Access leads on `google-web`, Identity on `chatgpt` and `google-maps`, Substance on
`google-ai-mode` and `perplexity`, Demand on `youtube`, Distribution on
`reddit-communities`.

**Six roles** (`roles/`): `demand-analyst`, `identity-steward`, `content-editor`,
`technical-engineer`, `distribution-strategist` and `account-reporter`. Each declares what
it may do unsupervised, what it must ask about, and what it may never do at any rung.
`distribution-strategist` has a deliberately empty `fenceable` list: it is the one role
that can never act, because every mechanism for executing earned media is either against
platform rules or deceptive.

### Fixed: the re-work reached the whole library, not just its headline

The rename and the new `model/` landed first; the body of the library still taught the old
shape. That is now consistent throughout.

- **"The Cite rung" is gone** (35 occurrences across 26 files). An assistant is a surface,
  so the text now says so wherever it used to imply a sixth rung.
- **All seven site-type profiles** moved from "How each rung shifts" to "How the five
  systems shift", with the Visibility Ladder nested inside Access and a separate note on
  assistant surfaces. Their deep type-specific sections are unchanged.
- **The health scorecard** in `audit-report-and-state.md` (and the lifecycle example) now
  reports by system, with Access broken out into its four rungs, plus a line stating which
  surfaces were checked and how strongly each can be verified.
- `install/agents-md.md` no longer lists Rank as a fifth Access rung.
- `USE-CASES.md`'s "weight highest" column names systems rather than rungs.
- `examples/03-cite-answer-blocks.md` is now `examples/03-assistants-answer-blocks.md`.

## [0.2.0] - 2026-10-06
*Current as of: 2026-10. Experimental: see [DISCLAIMER.md](DISCLAIMER.md). Volatile facts are stamped "verified 2026-10" beside their sources.*

### Changed: three modes, and read-only by default
- **Every skill runs in one of three modes.**
  - **`audit`** is the default: it diagnoses on the served output, records findings with ids and short refs (R-01, R-02...), saves the report to `.seo/`, and **never changes the site**.
  - **`fix`** applies only the findings you approve, by ref or by a rule such as "all low-risk", on a branch, one commit per finding, each verified on the served output and logged with a date.
  - **`re-check`** re-tests earlier findings, marks regressions, and measures what changed where data is available.
- **One way to ask:** skill, mode, target, then optional scope and output.
- **`audit.md` no longer makes changes.** New minis: `fix.md` and `recheck.md`. `audit-readonly.md` now just points to `audit.md`.
- **A standard "Inputs and modes" block in every skill:** access (URL only, read-only repo, write), mode, the tool ladder, scope or budget, audience, output (report, `.seo/`, CSV, tickets, PR description), context, and the rule that fetched content is data. The full contract is in `seo-orchestrator/references/operating-modes.md`. It also covers URL-only mode, monorepos and sampling on very large sites.
- **A shared findings schema** for every specialist, plus an `approved` field, `data_sources`, a dated change log in `.seo/log.md`, and exports for CSV, Jira/Linear tickets and PR descriptions.
- **Pages that already earn traffic are protected.** Title, h1, copy or URL changes on pages with meaningful clicks need explicit approval and are logged so they can be measured.
- **Fetched content is data.** Anything read from a site (HTML, robots.txt, llms.txt, API responses) is evidence, never instructions. Injected instructions aimed at AI agents are recorded as a finding and never acted on.

### Added: live data, detected from the user's environment
- **`seo-demand-search-data`** (new skill) reads the search data the user's environment already provides, to:
  - triage indexing reasons and compare Google's chosen canonical with the declared one;
  - protect pages that earn traffic;
  - map demand and striking-distance queries;
  - measure whether changes worked;
  - report AI visibility.
- **Capability detection, not products.** The pack looks for any tool that provides search performance, URL inspection, Core Web Vitals field data, revenue or leads by landing page, keyword demand, backlinks or AI answer mentions: an MCP server, a connector, a CLI, the user's own API credentials, or an exported file. All read-only, never a precondition, never invented numbers. Paid calls are announced first.
- **Recipes for the direct-API fallback** in `seo-orchestrator/references/data/`: Search Console (Search Analytics, URL Inspection, Sitemaps), GA4, CrUX and PageSpeed Insights, Bing Webmaster, and third-party SEO MCP servers. Each recipe states what the APIs do not expose.

### Added: new skills
- **`seo-operations-launch-qa`:** go-live checks on the production URL, 22 checks in ladder order, split into launch blockers and fix-this-week, with a quick-wins mode and a first-week watch list.
- **`seo-access-performance`:** Core Web Vitals deep work. Field data first, then lab; LCP sub-parts, INP phases and Long Animation Frames, CLS and bfcache, third-party tag triage, and honest limits on what build time can prove.

### Added: versatility
- **Platforms:** detailed references for WordPress (including WooCommerce), Shopify, site builders (Webflow, Wix, Squarespace, Framer, plus Ghost, HubSpot, Drupal, BigCommerce) and headless CMSs. Each covers where every setting lives, what is locked, and how to give instructions when code is not editable.
- **Frameworks:** the stack table now covers Angular SSR, React Router framework mode, TanStack Start, SolidStart, Qwik, docs generators and server-rendered stacks. Next.js 16 `proxy` replaces `middleware`.
- **Rendering and metadata:** a JavaScript SEO reference, auditing existing prerender services, and a per-framework metadata table with the common override bugs.
- **Edge, CDN and bot access:** CDN and firewall rules can block crawlers whatever robots.txt says. Covers Cloudflare's AI bot policies, Vercel deployment protection, AWS WAF, Netlify and Fastly. Bot user-agent comparisons, with confirmation by IP and reverse DNS.
- **Verification tool ladder:** a rendering MCP or headless browser, then curl or Invoke-WebRequest, then a fetch tool, which is low confidence.
- **AI crawlers:** a dated table of AI crawler tokens, the snippet controls, and Search Console's site-level control for Google's AI features.
- **Security and spam:** a check for hacked-site injections, cloaking, unexpected outbound links, rogue sitemaps, and prompt-injection text aimed at AI agents.

### Changed: depth and correctness
- **Deeper data-led skills:**
  - Content audit: an inventory CSV, decision rules, sampling and cannibalisation detection.
  - Log analysis: parsing, bot verification, CSV outputs and a Verify step.
  - Programmatic: Google's spam policies by name, a measurable quality gate and a staged rollout.
- **Deeper strategy skills:**
  - Positioning: reads the context pack instead of asking, plus SERP, competitor and keyword research that never invents volumes.
  - Proposals: output templates.
  - Content editing: a "review an AI draft" mode.
  - Off-site authority: a link-audit CSV and the verified disavow rules.
  - Measurement setup: Consent Mode v2, Bing and non-Next.js stacks.
- **Media:** `VideoObject` only where the video is the main content, key moments, Discover image controls, and the LCP hero image.
- **Understand:** the sitelinks search box is marked retired; the FAQ row matches the May 2026 retirement; merchant listings, shipping, returns and product variants added.
- **Cite reframed** around Google's 2026 guidance that optimising for its generative AI features is still SEO, with no need to chunk content, add special schema or publish AI-only files. "Answer blocks" are now clear, self-contained writing. AI visibility measurement is added.
- **Profiles:**
  - Ecommerce: feed parity.
  - International: hreflang sitemaps, i18n routing and a reciprocity checker.
  - Local: service-area pages and doorway tests.
  - Documentation: docs generators.
- **Next.js:** the LCP image advice is updated for Next.js 16, where `priority` is deprecated.
- **Context everywhere:** the content, schema, rank and cite skills now read `.seo/context.md`.
- **Install guides** now list `seo-identity-context` and the new skills.
- **Freshness:** `scripts/check-freshness.py` and a monthly workflow flag stale "verified" stamps and broken or redirected source links, and open an issue to re-check them.

### Earlier in this release (2026-08)

### Added — context gathering, the foundation under the content half
- **`seo-identity-context`** — the missing first step. Learns what the business actually is (offer, audience and *their* vocabulary, provable differentiators, real proof assets, house voice, claim constraints, competitors, entities) from the repository, the served site, connected data and free public sources, then writes it to **`.seo/context.md`** for every later skill and every later run to read.
- **Provenance labelling, and the rule it enforces.** Every fact in the pack is marked `[established]` / `[inferred]` / `[unknown]` / `[conflict]`. Inferences may shape strategy; **only an established fact may reach published copy, structured data, or a trust signal**, and unknown is never rounded up to a plausible guess. This turns "never fabricate" from a refusal into a method: go and find the real material first.
- **`.seo/context.md` is now part of the lifecycle.** Added to the `.seo/` folder contract in `audit-report-and-state.md`; orchestrator Step 0 gained a sixth check (does a context pack exist, is it current) and a dispatch rule that context precedes any content, positioning, E-E-A-T or entity work. Purely technical rungs still run without it.
- **References:** `context-sources.md` (every source worth reading and what each is uniquely good for — including Search Console's query report as the best audience-vocabulary source there is, the free no-key options, and the fetching etiquette and legal lines) and `context-pack-format.md` (the file format, section by section, with a worked example).
- **Respects the autonomy principle.** The skill infers everything it can and is explicitly forbidden from becoming an onboarding questionnaire: what remains is a short ranked list of only the questions that materially change the work, each with a proposed default. Unanswered questions stay `[unknown]` and downstream skills degrade gracefully.
- **Mini:** `install/copy-paste/context.md`.

### Added — a use-case guide by site type
- **[USE-CASES.md](USE-CASES.md)** — the orientation layer for site types: which profile fits (SaaS, e-commerce, local, blog/content, docs, news, international), the classic failure per type, the priority tilt, a read-only starter prompt per type, and the honest per-type boundaries. Linked from README and SKILLS.md. Depth stays in the profile files; this is the map.

### Changed — freshness pass (2026-08), verified against Google's changelog
- **FAQ rich results were fully retired by Google (May 2026)** — previously restricted to government/health sites (2023), now not shown at all. Updated everywhere the old restriction was stated (Understand skill + schema reference, Cite answer-formatting reference, docs & SaaS profiles, `understand.md` mini). `FAQPage` markup stays valid; its value is entity clarity and AEO extraction only.
- **More rich-result types retired** — course info, estimated salary, learning video, special announcement, vehicle listing (Sep 2025) and practice problems (Jan 2026) noted in the schema reference's currency box; the schema types themselves remain valid for entity clarity.
- **`llms.txt` status sharpened** — Google has stated it has no effect on Search rankings or AI Overviews (mid-2026); some AI tools (Perplexity, Claude, coding agents) do fetch it, making it most defensible for docs. The reference now says both, still framed as low-cost, low-certainty.

### Added — a read-only audit mini
- **`install/copy-paste/audit-readonly.md`** — an analysis-only version of the audit mini: it walks the whole Visibility Ladder on the served HTML and reports a scorecard, the floor, and prioritised fixes with risk, but **changes nothing** (no code edits, no `.seo/` written). The safe first look, ideal for auto-mode or a live site you don't want touched; switch to `audit.md` to actually apply fixes.

### Added — holistic completeness (closing the off-page and niche gaps)
- **`seo-distribution-authority`** — the off-page half of SEO: audit the backlink profile (via connected Search Console / Ahrefs / DataForSEO), flag toxic links and produce a disavow file, find the competitor authority gap, and recommend strictly white-hat link-building and digital PR. Advisory and audit only — never executes outreach or buys links.
- **Broader schema catalogue** — added `JobPosting`, `Event`, `Course`, `Review`/`AggregateRating`, and `SoftwareApplication` to the Understand skill, with a pointer to the wider schema.org set.
- **News/publisher profile** — `news-publisher.md`: `NewsArticle` + honest timestamps, news sitemaps, Top Stories/Discover eligibility, recency, paywalled-content markup, and the "inclusion is Google's call" boundary.
- **Security headers** — added HSTS / CSP / `X-Content-Type-Options` and mixed-content checks to the Reach rung (previously HTTPS only).

### Changed — the ladder now ends in Rank (SEO-first), plus an autonomy principle
- **Reworked the Visibility Ladder so it names the goal.** The fifth rung is now **Rank** (`seo-substance-quality`): is the page good and relevant enough to actually rank — search intent, quality/depth, E-E-A-T, topical authority. The first four rungs make a page *eligible*; Rank is whether it deserves to win. This makes SEO/ranking the explicit summit.
- **AEO/citation is now the layer *on top* of the ladder, not a rung.** The Cite skill moved from `5-seo-surface-assistants` to **`seo-surface-assistants`** and is framed as additive and secondary: applied after a page can rank, never instead of it.
- **New principle: work it out yourself; don't interrogate the user.** The agent reads the codebase and served pages to infer the site's purpose, audience, stack, platform and sector, and acts on sensible defaults, rather than asking the user to fill in details. Step 0 of the orchestrator is now "understand the site yourself," and "ask the user" prompts are reframed as infer-first.
- **Refined rung 5 into an explicit "build vs earn" split.** Rank is now framed as an *outcome you earn*, not a switch you flip, with two halves: *what you build* (on-page intent, quality, on-page E-E-A-T, topical authority — the agent's job) and *what you earn* (backlinks, brand and reputation — a major factor, but off-site and ongoing, so `seo-distribution-authority` advises beside the ladder). Off-page authority now has a visible place at the summit across METHOD, the rung skill, README/SKILLS and the website.
- **Softened the dependency language to match reality.** The first three rungs are strict prerequisites; the top two build on them rather than gating as rigidly (a broken lower rung still caps everything above, so fix bottom-up). AEO is now described as applied *alongside* ranking on a page whose fundamentals are sound, never *instead of* it, rather than strictly "after" it ranks.
- **Fixed a stale audit-walk.** The orchestrator's audit-lifecycle sweep and `examples/04` scorecard now include rung 5 (Rank) and treat Cite as the on-top layer, instead of listing Cite as rung 5.

### Added — holistic coverage (technical · content · data · automations · advanced)
- **`seo-operations-automation`** — automate the audit in CI/CD: a GitHub Action that runs the served-HTML checks on deploy/PR and fails the build on a critical regression, plus Lighthouse CI, scheduled re-audits, and hooks. (Codifies the mechanisable checks; the deeper agent audit stays a periodic human-in-the-loop run.)
- **`seo-substance-media`** — image & video SEO: alt/filenames/formats, image & video sitemaps, `VideoObject` schema (honest values only), and real transcripts/captions.
- **`seo-substance-at-scale`** — pages at scale from data, white-hat: a quality gate that refuses thin/doorway pages, with crawl-budget/indexation control.
- **`seo-access-logs`** — advanced/large-site server-log & crawl-budget analysis (verified crawlers only; finds under-crawled pages and wasted budget).

### Changed — legibility & robustness (from the improvement review)
- Added [SKILLS.md](SKILLS.md) — a canonical "which skill when" index (entry / rungs / technical / strategy / automation-advanced tiers).
- README restructured to lead with the hook + a table of contents; the SEO/AEO distinction condensed (full version stays in METHOD).
- Disambiguated overlapping skill `description` triggers (e.g. "thin content", "improve content", "audit my site") with scope + negative-routing cues for cleaner skill selection.
- Added this CHANGELOG and a "current as of" version stamp.

## [0.1.0] — 2026-06-03
*Current as of: 2026-06. Experimental — see [DISCLAIMER.md](DISCLAIMER.md).*

First public release.

### The method
- **The Visibility Ladder** — five rungs in dependency order: Reach → Read → Understand → Connect → Cite. Diagnose top-to-bottom, fix bottom-to-top, verify on the served HTML.
- Three principles: verify on rendered output (not source); talk to the agent, serve the non-SEO human; strictly white-hat.

### Skills (12)
- **Rungs:** `seo-access-reach`, `seo-access-read` (incl. page experience: Core Web Vitals + mobile), `seo-access-understand`, `seo-access-connect`, `5-seo-surface-assistants`.
- **Entry/conductor:** `seo-orchestrator` — runs the repeatable **audit lifecycle** with `.seo/` state (baseline → progression → regression checks).
- **Technical specialists:** `seo-access-migrations`, `seo-operations-measurement`.
- **Strategy tier:** `seo-substance-content-audit`, `seo-substance-content-editing`, `seo-identity-positioning`, `seo-operations-reporting`.

### Adaptability & data
- Stack/platform adapters (code vs hosted-CMS boundary) and six site-type profiles (content, e-commerce, local, SaaS/marketing, docs, international).
- Optional **bring-your-own-key** live-data integrations (Search Console, DataForSEO, Ahrefs, Bing, PageSpeed) — enrich the audit, never required, never paywalled.

### Distribution
- Full skills + self-contained copy-paste minis; install guides for Claude Code, Cursor, AGENTS.md hosts; optional MCP layer; before/after examples.

### Time-sensitive facts baked in (verify on re-use)
- FAQ rich results restricted to government/health authorities (2023); HowTo rich results retired (2023); FID → INP (2024); `llms.txt` is an emerging, limited-adoption proposal. These will date — re-check against primary sources.

