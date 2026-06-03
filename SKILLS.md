# Which skill do I use when?

The pack has three tiers. **Start with the orchestrator** for anything broad — it routes to the rest and runs the audit lifecycle. Reach for a specific skill only when your request is already scoped.

| Skill | What it does | Reach for it when you say… | Tier |
|---|---|---|---|
| [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) | **Entry point.** Detects stack/site-type, runs the whole Visibility Ladder as a repeatable audit, routes to every other skill. | "audit my SEO", "improve my rankings", "why isn't my site showing up" | **Entry** |
| [`1-reach-indexation`](skills/1-reach-indexation/SKILL.md) | Crawlable + rendered in served HTML + HTTPS + indexable | "Google can't find my site", "is it crawlable", SSR/CSR | Rung 1 |
| [`2-read-content`](skills/2-read-content/SKILL.md) | Real content + metadata + page experience (speed/mobile) on a page | "missing meta description", "duplicate titles", "site is slow", "mobile-friendly" | Rung 2 |
| [`3-understand-schema`](skills/3-understand-schema/SKILL.md) | Valid, honest structured data (schema/JSON-LD) | "add schema", "structured data", "rich results" | Rung 3 |
| [`4-connect-architecture`](skills/4-connect-architecture/SKILL.md) | Internal links, site architecture, canonicals | "internal linking", "canonical", "orphan pages", "site structure" | Rung 4 |
| [`5-rank-relevance`](skills/5-rank-relevance/SKILL.md) | **The goal.** Good and relevant enough to rank: intent, quality, E-E-A-T, topical authority | "why am I not ranking", "improve my rankings", "is my content good enough", "search intent" | Rung 5 |
| [`cite-aeo-geo`](skills/cite-aeo-geo/SKILL.md) | *On top of the ladder:* format to be *eligible* for AI citation, after a page ranks | "AI Overviews", "get cited by ChatGPT", "AEO", "llms.txt" | Layer on top |
| [`seo-migrations`](skills/seo-migrations/SKILL.md) | Preserve rankings when URLs change | "redesign", "moving domain/CMS", "changed our URLs", "404s after relaunch" | Technical specialist |
| [`seo-measurement-setup`](skills/seo-measurement-setup/SKILL.md) | Install analytics / Search Console / web-vitals (setup only) | "set up analytics", "install GA4", "verify Search Console" | Technical specialist |
| [`seo-content-audit`](skills/seo-content-audit/SKILL.md) | Assess content **across the site**; recommend keep/improve/consolidate/prune per page | "content audit", "which pages to update or remove", "is my content good" | Strategy tier |
| [`seo-content-editing`](skills/seo-content-editing/SKILL.md) | Improve the copy on **one specific page** (edit, never generate) | "improve this page's copy", "make this page clearer", "tighten this" | Strategy tier |
| [`seo-positioning-strategy`](skills/seo-positioning-strategy/SKILL.md) | What topics to own (topical authority), how to differentiate | "topical authority", "what topics should we cover", "competitive analysis" | Strategy tier |
| [`seo-proposal-roadmap`](skills/seo-proposal-roadmap/SKILL.md) | Package findings into a prioritised action plan / client proposal | "build a roadmap", "what should we do first", "SEO proposal" | Strategy tier |
| [`seo-automations`](skills/seo-automations/SKILL.md) | Run the audit automatically in CI/CD — regression gate on deploy/PR, scheduled re-audits | "run SEO checks in CI", "catch regressions automatically", "GitHub Action for SEO" | Automation / advanced |
| [`seo-media`](skills/seo-media/SKILL.md) | Image & video SEO — alt/formats, `VideoObject` schema, media sitemaps, transcripts | "image SEO", "video SEO", "get my videos in Google", "image sitemap" | Automation / advanced |
| [`seo-programmatic`](skills/seo-programmatic/SKILL.md) | Generate pages at scale from data, white-hat (quality gate; no doorway pages) | "programmatic SEO", "pages from a database", "location pages at scale" | Automation / advanced |
| [`seo-log-analysis`](skills/seo-log-analysis/SKILL.md) | Server-log & crawl-budget analysis — what crawlers actually fetch (large sites) | "log file analysis", "crawl budget", "what is Googlebot crawling" | Automation / advanced |

**Tiers, plainly:**
- **Entry** — the orchestrator; your default for anything broad.
- **Rungs 1–5** — the Visibility Ladder, the core SEO method, climbing to the goal: **Rank**. Fixed in order: you can't climb a rung until the ones below pass.
- **Layer on top** — `cite-aeo-geo` (AEO): makes a page that already ranks *eligible* to be cited by AI answers. Additive, after ranking, not a rung.
- **Technical specialists** — jobs that don't fit a single rung (URL changes; measurement plumbing).
- **Strategy tier** — the content & marketing layer (assess, edit, position, package). Secondary to the technical rungs, and sharper when you connect your own data tools.
- **Automation / advanced** — keep a site healthy automatically (CI/CD) and handle the harder cases (media, scale, large-site crawl budget). Reach for these once the core is solid.

No host? Every skill has a paste-into-chat mini in [`install/copy-paste/`](install/copy-paste/) — start with [`audit.md`](install/copy-paste/audit.md).
