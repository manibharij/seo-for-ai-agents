# Changelog

All notable changes to this pack. Because search and AI-answer behaviour change quickly, each release notes the date its guidance is **current as of** — check it against primary sources (Google's structured-data/rich-result docs, each AI engine's crawler docs) before relying on time-sensitive advice.

This project aims to follow [Semantic Versioning](https://semver.org/) loosely while it's pre-1.0 and experimental.

## [Unreleased]
*Current as of: 2026-06. Experimental — see [DISCLAIMER.md](DISCLAIMER.md).*

### Added — holistic completeness (closing the off-page and niche gaps)
- **`seo-offsite-authority`** — the off-page half of SEO: audit the backlink profile (via connected Search Console / Ahrefs / DataForSEO), flag toxic links and produce a disavow file, find the competitor authority gap, and recommend strictly white-hat link-building and digital PR. Advisory and audit only — never executes outreach or buys links.
- **Broader schema catalogue** — added `JobPosting`, `Event`, `Course`, `Review`/`AggregateRating`, and `SoftwareApplication` to the Understand skill, with a pointer to the wider schema.org set.
- **News/publisher profile** — `news-publisher.md`: `NewsArticle` + honest timestamps, news sitemaps, Top Stories/Discover eligibility, recency, paywalled-content markup, and the "inclusion is Google's call" boundary.
- **Security headers** — added HSTS / CSP / `X-Content-Type-Options` and mixed-content checks to the Reach rung (previously HTTPS only).

### Changed — the ladder now ends in Rank (SEO-first), plus an autonomy principle
- **Reworked the Visibility Ladder so it names the goal.** The fifth rung is now **Rank** (`5-rank-relevance`): is the page good and relevant enough to actually rank — search intent, quality/depth, E-E-A-T, topical authority. The first four rungs make a page *eligible*; Rank is whether it deserves to win. This makes SEO/ranking the explicit summit.
- **AEO/citation is now the layer *on top* of the ladder, not a rung.** The Cite skill moved from `5-cite-aeo-geo` to **`cite-aeo-geo`** and is framed as additive and secondary: applied after a page can rank, never instead of it.
- **New principle: work it out yourself; don't interrogate the user.** The agent reads the codebase and served pages to infer the site's purpose, audience, stack, platform and sector, and acts on sensible defaults, rather than asking the user to fill in details. Step 0 of the orchestrator is now "understand the site yourself," and "ask the user" prompts are reframed as infer-first.

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

[0.1.0]: https://github.com/manibharij/seo-for-ai-agents/releases/tag/v0.1.0
