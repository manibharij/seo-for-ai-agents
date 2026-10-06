# Which skill do I use when?

The pack has three tiers. **Start with the orchestrator** for anything broad — it routes to the rest and runs the audit lifecycle. Reach for a specific skill only when your request is already scoped. Looking by *site type* instead (shop, blog, SaaS, docs, local, news, international)? See **[USE-CASES.md](USE-CASES.md)**.

## Three modes, one way to ask

Every skill runs in one of three modes. The default is always `audit`.

| Mode | What it does | Changes the site |
|---|---|---|
| `audit` (default) | Diagnoses on the served output and records findings with ids, evidence, risk and the proposed fix. Saves the report to `.seo/` when it can write files. | Never |
| `fix` | Applies only the findings you approve, by id or by a rule such as "all low-risk". Works on a branch, one commit per finding, verifying each on the served output. | Only what you approve |
| `re-check` | Re-tests earlier findings: what is fixed, what regressed and, if your environment has search data, what changed. | Never |

Ask in the same shape every time: skill, mode, target, then optional scope and output.

```
Run seo-orchestrator in audit mode on https://example.com. Scope: top 10. Output: ticket list.
Run seo-orchestrator in fix mode: apply R-03 and R-07 from .seo/state.json.
Run 1-reach-indexation in re-check mode.
```

Without an install, the same three modes are copy-paste minis: [`audit.md`](install/copy-paste/audit.md), [`fix.md`](install/copy-paste/fix.md) and [`recheck.md`](install/copy-paste/recheck.md). Every skill also adapts to what it can reach (a URL only, a read-only repo, or write access), to a scope or time budget, and to whatever data your environment already has: see [`operating-modes.md`](skills/seo-orchestrator/references/operating-modes.md).

## The skills

| Skill | What it does | Reach for it when you say… | Tier |
|---|---|---|---|
| [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) | **Entry point.** Detects stack/site-type, runs the whole Visibility Ladder as a repeatable audit, routes to every other skill. | "audit my SEO", "improve my rankings", "why isn't my site showing up" | **Entry** |
| [`seo-context-gathering`](skills/seo-context-gathering/SKILL.md) | **Foundation.** Learns the business — offer, audience and their vocabulary, provable differentiators, real proof assets, voice, claim constraints — and writes it to `.seo/context.md` for every other skill to use | "understand my business", "gather context", "what's our brand voice", "who are we writing for", before any content work | **Foundation** |
| [`seo-search-data`](skills/seo-search-data/SKILL.md) | **Data.** Reads the search data your environment already has (Search Console, analytics, CrUX, Bing, or an SEO tool, whatever is connected) to triage indexing, protect pages that earn traffic, map demand and measure whether changes worked | "why aren't these pages indexed", "did our change work", "what's in striking distance", "are we in AI answers" | **Data** |
| [`1-reach-indexation`](skills/1-reach-indexation/SKILL.md) | Crawlable + rendered in served HTML + HTTPS + indexable | "Google can't find my site", "is it crawlable", SSR/CSR | Rung 1 |
| [`2-read-content`](skills/2-read-content/SKILL.md) | Real content + metadata + page experience (speed/mobile) on a page | "missing meta description", "duplicate titles", "site is slow", "mobile-friendly" | Rung 2 |
| [`3-understand-schema`](skills/3-understand-schema/SKILL.md) | Valid, honest structured data (schema/JSON-LD) | "add schema", "structured data", "rich results" | Rung 3 |
| [`4-connect-architecture`](skills/4-connect-architecture/SKILL.md) | Internal links, site architecture, canonicals | "internal linking", "canonical", "orphan pages", "site structure" | Rung 4 |
| [`5-rank-relevance`](skills/5-rank-relevance/SKILL.md) | **The goal.** Good enough, and trusted enough, to win — *what you build:* intent, quality, on-page E-E-A-T, topical authority (*what you earn* — links, brand — sits beside the ladder, see below) | "why am I not ranking", "improve my rankings", "is my content good enough", "search intent" | Rung 5 |
| [`cite-aeo-geo`](skills/cite-aeo-geo/SKILL.md) | *On top of the ladder:* format to be *eligible* for AI citation, on a page that can already rank | "AI Overviews", "get cited by ChatGPT", "AEO", "llms.txt" | Layer on top |
| [`seo-launch-qa`](skills/seo-launch-qa/SKILL.md) | Pre-launch and go-live checks on the production URL, split into launch blockers and fix-this-week | "we're about to launch", "going live", "what will stop this ranking" | Technical specialist |
| [`seo-performance`](skills/seo-performance/SKILL.md) | Core Web Vitals deep work: field data first, then lab, LCP sub-parts, INP, CLS, third-party tags | "Core Web Vitals failing", "fix our LCP", "INP", "site is slow" | Technical specialist |
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
| [`seo-offsite-authority`](skills/seo-offsite-authority/SKILL.md) | The off-page half: backlink audit, toxic-link/disavow, white-hat link-building & digital-PR strategy (advisory) | "backlinks", "link building", "off-page SEO", "domain authority", "disavow", "digital PR" | Off-page |

**Tiers, plainly:**
- **Entry** — the orchestrator; your default for anything broad.
- **Data** — `seo-search-data`: reads the user's own search data through whatever tools their environment provides. Never a precondition: every skill still works with nothing connected.
- **Foundation** — `seo-context-gathering`: learns the business and records it in `.seo/context.md`. Not a rung, and not optional for content work. It runs *before* content, positioning, E-E-A-T or entity work, because those judgements are only as good as the context behind them — and an agent without context is an agent that invents.
- **Rungs 1–5** — the Visibility Ladder, the core SEO method, climbing to the goal: **Rank**. The lower rungs are strict prerequisites; the top two build on them. A broken lower rung caps everything above it, so diagnose top-down and fix bottom-up. Rung 5 itself has two halves: *what you build* (on-page) and *what you earn* (off-page, advised beside the ladder).
- **Layer on top** — `cite-aeo-geo` (AEO): makes a page that can already rank *eligible* to be cited by AI answers. Additive, alongside ranking, never instead of it, not a rung.
- **Technical specialists** — jobs that don't fit a single rung (URL changes; measurement plumbing).
- **Strategy tier** — the content & marketing layer (assess, edit, position, package). Secondary to the technical rungs, and sharper when you connect your own data tools.
- **Automation / advanced** — keep a site healthy automatically (CI/CD) and handle the harder cases (media, scale, large-site crawl budget). Reach for these once the core is solid.
- **Off-page** — `seo-offsite-authority`: the earned-media half of SEO (backlinks, authority, digital PR). The ladder can't *build* it, but this skill *audits and strategises* it (advisory, white-hat, never buying links).

No host? Every skill has a paste-into-chat mini in [`install/copy-paste/`](install/copy-paste/). Start with [`audit.md`](install/copy-paste/audit.md), which changes nothing, then [`fix.md`](install/copy-paste/fix.md) for the findings you approve.
