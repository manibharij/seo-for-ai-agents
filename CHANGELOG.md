# Changelog

All notable changes to this pack. Because search and AI-answer behaviour change quickly, each release notes the date its guidance is **current as of** — check it against primary sources (Google's structured-data/rich-result docs, each AI engine's crawler docs) before relying on time-sensitive advice.

This project aims to follow [Semantic Versioning](https://semver.org/) loosely while it's pre-1.0 and experimental.

## [Unreleased]

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
- **`seo-search-data`** (new skill) reads the search data the user's environment already provides, to:
  - triage indexing reasons and compare Google's chosen canonical with the declared one;
  - protect pages that earn traffic;
  - map demand and striking-distance queries;
  - measure whether changes worked;
  - report AI visibility.
- **Capability detection, not products.** The pack looks for any tool that provides search performance, URL inspection, Core Web Vitals field data, revenue or leads by landing page, keyword demand, backlinks or AI answer mentions: an MCP server, a connector, a CLI, the user's own API credentials, or an exported file. All read-only, never a precondition, never invented numbers. Paid calls are announced first.
- **Recipes for the direct-API fallback** in `seo-orchestrator/references/data/`: Search Console (Search Analytics, URL Inspection, Sitemaps), GA4, CrUX and PageSpeed Insights, Bing Webmaster, and third-party SEO MCP servers. Each recipe states what the APIs do not expose.

### Added: new skills
- **`seo-launch-qa`:** go-live checks on the production URL, 22 checks in ladder order, split into launch blockers and fix-this-week, with a quick-wins mode and a first-week watch list.
- **`seo-performance`:** Core Web Vitals deep work. Field data first, then lab; LCP sub-parts, INP phases and Long Animation Frames, CLS and bfcache, third-party tag triage, and honest limits on what build time can prove.

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
- **Install guides** now list `seo-context-gathering` and the new skills.
- **Freshness:** `scripts/check-freshness.py` and a monthly workflow flag stale "verified" stamps and broken or redirected source links, and open an issue to re-check them.

### Earlier in this release (2026-08)

### Added — context gathering, the foundation under the content half
- **`seo-context-gathering`** — the missing first step. Learns what the business actually is (offer, audience and *their* vocabulary, provable differentiators, real proof assets, house voice, claim constraints, competitors, entities) from the repository, the served site, connected data and free public sources, then writes it to **`.seo/context.md`** for every later skill and every later run to read.
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
- **`seo-offsite-authority`** — the off-page half of SEO: audit the backlink profile (via connected Search Console / Ahrefs / DataForSEO), flag toxic links and produce a disavow file, find the competitor authority gap, and recommend strictly white-hat link-building and digital PR. Advisory and audit only — never executes outreach or buys links.
- **Broader schema catalogue** — added `JobPosting`, `Event`, `Course`, `Review`/`AggregateRating`, and `SoftwareApplication` to the Understand skill, with a pointer to the wider schema.org set.
- **News/publisher profile** — `news-publisher.md`: `NewsArticle` + honest timestamps, news sitemaps, Top Stories/Discover eligibility, recency, paywalled-content markup, and the "inclusion is Google's call" boundary.
- **Security headers** — added HSTS / CSP / `X-Content-Type-Options` and mixed-content checks to the Reach rung (previously HTTPS only).

### Changed — the ladder now ends in Rank (SEO-first), plus an autonomy principle
- **Reworked the Visibility Ladder so it names the goal.** The fifth rung is now **Rank** (`5-rank-relevance`): is the page good and relevant enough to actually rank — search intent, quality/depth, E-E-A-T, topical authority. The first four rungs make a page *eligible*; Rank is whether it deserves to win. This makes SEO/ranking the explicit summit.
- **AEO/citation is now the layer *on top* of the ladder, not a rung.** The Cite skill moved from `5-cite-aeo-geo` to **`cite-aeo-geo`** and is framed as additive and secondary: applied after a page can rank, never instead of it.
- **New principle: work it out yourself; don't interrogate the user.** The agent reads the codebase and served pages to infer the site's purpose, audience, stack, platform and sector, and acts on sensible defaults, rather than asking the user to fill in details. Step 0 of the orchestrator is now "understand the site yourself," and "ask the user" prompts are reframed as infer-first.
- **Refined rung 5 into an explicit "build vs earn" split.** Rank is now framed as an *outcome you earn*, not a switch you flip, with two halves: *what you build* (on-page intent, quality, on-page E-E-A-T, topical authority — the agent's job) and *what you earn* (backlinks, brand and reputation — a major factor, but off-site and ongoing, so `seo-offsite-authority` advises beside the ladder). Off-page authority now has a visible place at the summit across METHOD, the rung skill, README/SKILLS and the website.
- **Softened the dependency language to match reality.** The first three rungs are strict prerequisites; the top two build on them rather than gating as rigidly (a broken lower rung still caps everything above, so fix bottom-up). AEO is now described as applied *alongside* ranking on a page whose fundamentals are sound, never *instead of* it, rather than strictly "after" it ranks.
- **Fixed a stale audit-walk.** The orchestrator's audit-lifecycle sweep and `examples/04` scorecard now include rung 5 (Rank) and treat Cite as the on-top layer, instead of listing Cite as rung 5.

### Added — holistic coverage (technical · content · data · automations · advanced)
- **`seo-automations`** — automate the audit in CI/CD: a GitHub Action that runs the served-HTML checks on deploy/PR and fails the build on a critical regression, plus Lighthouse CI, scheduled re-audits, and hooks. (Codifies the mechanisable checks; the deeper agent audit stays a periodic human-in-the-loop run.)
- **`seo-media`** — image & video SEO: alt/filenames/formats, image & video sitemaps, `VideoObject` schema (honest values only), and real transcripts/captions.
- **`seo-programmatic`** — pages at scale from data, white-hat: a quality gate that refuses thin/doorway pages, with crawl-budget/indexation control.
- **`seo-log-analysis`** — advanced/large-site server-log & crawl-budget analysis (verified crawlers only; finds under-crawled pages and wasted budget).

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
- **Rungs:** `1-reach-indexation`, `2-read-content` (incl. page experience: Core Web Vitals + mobile), `3-understand-schema`, `4-connect-architecture`, `5-cite-aeo-geo`.
- **Entry/conductor:** `seo-orchestrator` — runs the repeatable **audit lifecycle** with `.seo/` state (baseline → progression → regression checks).
- **Technical specialists:** `seo-migrations`, `seo-measurement-setup`.
- **Strategy tier:** `seo-content-audit`, `seo-content-editing`, `seo-positioning-strategy`, `seo-proposal-roadmap`.

### Adaptability & data
- Stack/platform adapters (code vs hosted-CMS boundary) and six site-type profiles (content, e-commerce, local, SaaS/marketing, docs, international).
- Optional **bring-your-own-key** live-data integrations (Search Console, DataForSEO, Ahrefs, Bing, PageSpeed) — enrich the audit, never required, never paywalled.

### Distribution
- Full skills + self-contained copy-paste minis; install guides for Claude Code, Cursor, AGENTS.md hosts; optional MCP layer; before/after examples.

### Time-sensitive facts baked in (verify on re-use)
- FAQ rich results restricted to government/health authorities (2023); HowTo rich results retired (2023); FID → INP (2024); `llms.txt` is an emerging, limited-adoption proposal. These will date — re-check against primary sources.

