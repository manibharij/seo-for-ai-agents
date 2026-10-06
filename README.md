# seo-for-ai-agents

**A drop-in SEO + AEO skill pack that teaches AI coding agents (Claude Code, Cursor, Codex) to build *and audit* sites that search engines rank — and AI answer engines can cite. New sites or existing ones.**

> ⚡ **The problem it fixes:** sites built by AI agents look perfect in a browser and are often nearly **invisible to crawlers** — they serve an empty shell with no real content in the HTML. This pack catches that (and four rungs more), checking **what's actually served to a crawler**, not the source an agent edited and hoped about.

`experimental · v0.2 (current as of 2026-10) · MIT` — **[Which skill when?](SKILLS.md)** · [Method](METHOD.md) · [Use cases](USE-CASES.md) · [Changelog](CHANGELOG.md) · [Disclaimer](DISCLAIMER.md)

> **New here?** Paste [`install/copy-paste/audit.md`](install/copy-paste/audit.md) into your agent. It audits a new or existing site and **changes nothing**. When you have reviewed the findings, [`fix.md`](install/copy-paste/fix.md) applies only the ones you approve, and [`recheck.md`](install/copy-paste/recheck.md) re-tests them later. About to go live? Use [`launch-qa.md`](install/copy-paste/launch-qa.md). → [Install](#install)

## Contents
- [Three modes: audit, fix, re-check](#three-modes-audit-fix-re-check)
- [The method — the Visibility Ladder](#the-method-the-visibility-ladder)
- [It runs as an audit lifecycle](#it-runs-as-an-audit-lifecycle-not-a-one-shot)
- [Who it's for, and how it adapts](#who-its-for-and-how-it-adapts) · [Use cases by site type](USE-CASES.md)
- [Install](#install) · [Which skill when? (skills index)](SKILLS.md)
- [The honest boundary](#the-honest-boundary-and-how-live-data-fits) · [Disclaimer](#disclaimer)

It's primarily **SEO** — the technical and on-page fundamentals that drive ranking, done correctly and verified on the served output (not the source). On top sits **AEO** (answer-engine optimisation): the owned-media work to make a page *eligible* to be cited by AI answers. The two are related but not the same, and citation is never guaranteed — the full distinction is in **[METHOD.md](METHOD.md)**. It's **horizontal** (any site, any industry) and built for people who don't want to become SEOs to ship a findable site.

---

## Three modes: audit, fix, re-check

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

---

## The method: the Visibility Ladder

Five rungs in dependency order. The lower rungs are strict prerequisites; the top two build on them. Either way a broken lower rung quietly caps everything above it, so you **diagnose top-to-bottom and fix bottom-to-top.**

| # | Rung | The question it answers | Skill |
|---|------|------------------------|-------|
| 1 | **Reach** | Can a crawler reach the URL and see its content in the served HTML? | [`1-reach-indexation`](skills/1-reach-indexation/SKILL.md) |
| 2 | **Read** | Is there real, readable content, correct metadata, and a good page experience (speed + mobile)? | [`2-read-content`](skills/2-read-content/SKILL.md) |
| 3 | **Understand** | Can engines identify the entities? (structured data) | [`3-understand-schema`](skills/3-understand-schema/SKILL.md) |
| 4 | **Connect** | Is the page wired into a coherent site? (internal links, canonicals) | [`4-connect-architecture`](skills/4-connect-architecture/SKILL.md) |
| 5 | **Rank** | Is it good enough, and trusted enough, to win? (intent, quality, on-page E-E-A-T, topical authority) | [`5-rank-relevance`](skills/5-rank-relevance/SKILL.md) |
| + | **Cite (AEO)** | *On top of the ladder:* eligible to be cited by AI answers, on a page that can already rank | [`cite-aeo-geo`](skills/cite-aeo-geo/SKILL.md) |

**Ranking is the goal**, and rung 5 names it. The first four rungs make a page *eligible*; Rank is whether it *deserves* to win. Because ranking is an outcome you **earn**, rung 5 has two halves: **what you build** (intent, quality, on-page E-E-A-T, topical authority — the agent's job) and **what you earn** (backlinks, brand, reputation — a major factor, but off-site and ongoing, so [`seo-offsite-authority`](skills/seo-offsite-authority/SKILL.md) advises beside the ladder rather than building it). **Cite (AEO)** is the optional layer *on top*, for the AI-answer era, applied alongside ranking, never instead of it. Fixing content (Read) on a page Google can't render (Reach) is wasted work; the ladder stops that. Full philosophy in **[METHOD.md](METHOD.md)**.

The **[`seo-orchestrator`](skills/seo-orchestrator/SKILL.md)** is the entry point for any broad request ("audit my SEO", "improve my rankings", "why am I not showing up", "get cited by ChatGPT"). It detects your stack, platform, and site type, finds the lowest failing rung, dispatches in order — and runs the whole thing as a **repeatable audit lifecycle** (below).

**Specialist skills** sit beside the ladder for jobs that don't fit a single rung:

*Foundation — run this before any content work:*
- **[`seo-context-gathering`](skills/seo-context-gathering/SKILL.md)** — learn the business before touching its words: what it actually sells, who it serves and in *their* vocabulary, which differentiators are provable, what real proof exists (named authors, case studies, data), how it writes, and what it may not claim. Written once to `.seo/context.md` and read by every skill after it. Every fact is labelled established / inferred / unknown — and only an established fact may ever reach published copy or schema. This is how the pack answers "don't fabricate" with something better than a refusal: go and find the real material first.

*Data:*
- **[`seo-search-data`](skills/seo-search-data/SKILL.md)**: reads the search data your environment already has (Search Console, analytics, CrUX, Bing, or an SEO tool, whatever is connected) to see what Google actually concluded: indexing reasons and Google's chosen canonical, which pages already earn traffic and must be protected, demand and striking-distance queries, and whether a change worked. It detects capabilities, not products, and never requires data.

*Technical:*
- **[`seo-launch-qa`](skills/seo-launch-qa/SKILL.md)**: pre-launch and go-live checks on the production URL, split into launch blockers and fix-this-week.
- **[`seo-performance`](skills/seo-performance/SKILL.md)**: Core Web Vitals deep work, field data first, then lab and the cause.
- **[`seo-migrations`](skills/seo-migrations/SKILL.md)** — preserve rankings when URLs change (redesigns, replatforming, domain moves, slug changes, post-relaunch 404s).
- **[`seo-measurement-setup`](skills/seo-measurement-setup/SKILL.md)** — wire up analytics, Search Console, and web-vitals so results *can* be measured (setup only — reading the data is live-data work).

*Content & marketing (the holistic layer):*
- **[`seo-content-audit`](skills/seo-content-audit/SKILL.md)** — assess the content itself (quality, intent, gaps, cannibalisation, decay) and recommend keep/improve/consolidate/refresh/prune/create per page.
- **[`seo-content-editing`](skills/seo-content-editing/SKILL.md)** — improve existing copy (clarity, depth, answerability) — strictly *editing, not generation*; never fabricates.
- **[`seo-positioning-strategy`](skills/seo-positioning-strategy/SKILL.md)** — what topics to own (topical authority), how to differentiate, and a pillar/cluster content plan.
- **[`seo-proposal-roadmap`](skills/seo-proposal-roadmap/SKILL.md)** — package the audit into a client-ready proposal + phased roadmap (honest outcomes, no guarantees).

*Automation & advanced:*
- **[`seo-automations`](skills/seo-automations/SKILL.md)** — run the audit in CI/CD: a regression gate that fails a deploy/PR which would make the site invisible to crawlers, plus scheduled re-audits.
- **[`seo-media`](skills/seo-media/SKILL.md)** — image & video SEO: `VideoObject` schema, media sitemaps, real transcripts/captions.
- **[`seo-programmatic`](skills/seo-programmatic/SKILL.md)** — pages at scale from data, the white-hat way (a quality gate that refuses thin/doorway pages).
- **[`seo-log-analysis`](skills/seo-log-analysis/SKILL.md)** — large-site server-log & crawl-budget analysis: what crawlers actually fetch.

*Off-page (the earned-media half):*
- **[`seo-offsite-authority`](skills/seo-offsite-authority/SKILL.md)** — backlink-profile audit, toxic-link/disavow, and white-hat link-building & digital-PR strategy. Advisory: it audits and strategises (with your connected link data), it never builds or buys links.

The content & marketing skills get sharper when you connect your own data tools (see [the boundary](#the-honest-boundary-and-how-live-data-fits)), but work without them. `seo-automations` is the one to add once your site is healthy — it keeps it that way.

---

## It runs as an audit lifecycle (not a one-shot)

The pack **remembers**. The orchestrator writes a `.seo/` folder into your project — `audit.md` (a readable health scorecard), `state.json` (every finding with status), `log.md` (dated history) — so it works the first time *and every time after*:

- **First run** (`audit`): a baseline across all five rungs, findings recorded with ids. Nothing on the site changes.
- **Then** (`fix`): you approve findings and the agent applies only those, logging each change with a date.
- **Later runs** (`re-check`): re-verify past fixes, **catch regressions** after deploys and edits, measure what changed where data is available, and find what's new.

That turns it from a one-time fixer into a system that keeps a site healthy over time — which is exactly what an **existing** site needs.

## Who it's for, and how it adapts

- **New / "vibe-coded" sites** — catch the classic failure where an AI-built site looks perfect in a browser but is nearly invisible to crawlers, and ship it correct from the start.
- **Existing sites (developers on Claude Code)** — audit a real codebase, fix safely *without regressing what already ranks* (it protects URLs, canonicals, and intentional decisions — see the don't-regress discipline), and track progress run over run.

It **adapts** to the site: per-stack guidance (Next.js, Astro, Nuxt, SvelteKit, Remix, Gatsby, SPAs, static — plus an honest boundary for hosted platforms like WordPress/Shopify where fixes live in the platform, not the code), and **site-type profiles** (content/blog, news/publisher, e-commerce, local, SaaS/marketing, docs, international) that tune which issues matter most. **[USE-CASES.md](USE-CASES.md)** maps each site type to its profile, priority tilt, and a ready-to-paste starter prompt.

---

## Four principles that make it better than a flat checklist

1. **Work it out yourself; don't interrogate the user.** You shouldn't have to know SEO or describe your site. The agent reads the codebase and the served pages and figures out the context on its own — what the site is, who it's for, the stack, the platform, the sector — acts on sensible defaults, and only pauses for the few calls a human genuinely must make. Inferring beats asking.
2. **Verify on rendered output, not source.** An agent editing JSX and declaring "meta tags added" proves nothing. Every skill confirms what is actually *served* by re-fetching the URL — because client-rendered content invisible to crawlers is the #1 failure of AI-built sites (and a frequent silent regression on established ones after a refactor or replatform).
3. **Talk to the agent, serve the non-SEO human.** The skill instructs the agent; the agent fixes what's safe, explains every change and why it matters, and flags what only a human can decide.
4. **Strictly white-hat.** Never fabricate authors, credentials, reviews, or E-E-A-T signals. Where real trust signals are missing, they're flagged as human tasks — never invented. (This isn't only ethics: AI answer engines are built to discount manufactured authority.)

---

## Install

| Host | Guide |
|------|-------|
| **Claude Code** | [install/claude-code.md](install/claude-code.md) — drop into `~/.claude/skills/` or project `.claude/skills/` |
| **Cursor** | [install/cursor.md](install/cursor.md) — `.cursor/rules/*.mdc` |
| **AGENTS.md hosts** (Codex, Gemini CLI, Zed…) | [install/agents-md.md](install/agents-md.md) |
| **No host? Copy-paste** | [install/copy-paste/](install/copy-paste/) — self-contained minis to paste into any chat |
| **Optional MCP power-ups** | [install/mcp.md](install/mcp.md) — sharper verification; never required |
| **Optional data integrations** | [install/data-integrations.md](install/data-integrations.md) — bring-your-own-key (Search Console, DataForSEO, Ahrefs…) to enrich the audit; never required |

Install copies the **whole `skills/` folder** (the orchestrator carries the shared cross-cutting references — lifecycle, profiles, adapters — so keep the skills together). Each host guide has the exact steps.

### Fastest start (no setup)
Paste a mini straight into your agent:
- [**`audit.md`**](install/copy-paste/audit.md): the best all-rounder. Audits a **new or existing** site across the whole ladder, records findings with ids in `.seo/`, and changes nothing.
- [**`fix.md`**](install/copy-paste/fix.md): applies only the findings you approve, one commit each, verified on the served output.
- [**`recheck.md`**](install/copy-paste/recheck.md): re-tests earlier findings, catches regressions, and, if your environment has search data, shows what changed.
- [**`launch-qa.md`**](install/copy-paste/launch-qa.md): the go-live pass: launch blockers first, then fix-this-week.

- [**`reach.md`**](install/copy-paste/reach.md) — the highest-impact single fix and the best demo: catch a site that's invisible to crawlers.
- [**`context.md`**](install/copy-paste/context.md) — the foundation for content work: learns your business and writes it to `.seo/context.md` so nothing downstream has to guess.
- Then the per-rung minis (`read`, `understand`, `connect`, `rank`), the AEO-layer mini (`cite`), and the specialist minis: technical (`migrations`, `measurement`), content/marketing (`content-audit`, `content-editing`, `positioning-strategy`, `proposal-roadmap`), automation & advanced (`automations`, `media`, `programmatic`, `log-analysis`), and off-page (`offsite`). One per skill in [`install/copy-paste/`](install/copy-paste/).

On a host with skill support, the [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) does the routing and runs the lifecycle for you.

---

## Two sizes per skill

- **Full** — the canonical `SKILL.md` plus `references/` (the deep standards, type catalogues, and examples). Used by hosts with skill support.
- **Mini** — a single self-contained file in [`copy-paste/`](install/copy-paste/), same logic trimmed of references, for pasting into any chat. The low-friction onramp.

---

## Scope: owned media is built; earned media is advised

This pack **builds owned media** — everything on your own pages: rendering, content, metadata, speed, mobile, schema, architecture, ranking factors, and answer formatting. The whole Visibility Ladder is build-time, owned-media work.

**Earned media** — the off-site half of SEO (backlinks, digital PR, brand mentions, third-party reviews) — can't be *built* into your code; it's earned through outreach and reputation over time, and faking it (bought links, fake reviews) is the black-hat behaviour the pack refuses. So the pack doesn't *execute* it. But it's half of SEO, so the **[`seo-offsite-authority`](skills/seo-offsite-authority/SKILL.md)** skill *audits and strategises* it: read your backlink profile (via your connected data), flag toxic links and produce a disavow file, find the competitor authority gap, and recommend white-hat link-building and digital PR. Advisory and audit, never doing the outreach or buying links, that earning stays ongoing, off-site work (yours, or a managed service).

---

## The honest boundary (and how live data fits)

At their core the skills are build-time, owned-media work: rendering, content, metadata, speed and mobile, schema, structure, architecture and AI-answer readiness. They **never require live data** and work fully with nothing connected.

They get sharper with whatever your environment already has. The pack detects capabilities, not products: if your agent has a tool for search performance, URL inspection, Core Web Vitals field data, revenue or leads by landing page, keyword demand, backlinks or AI answer mentions (an MCP server, a connector, a CLI, your own API keys, or a file you export), the skills use it, read-only, and record which sources each report used. Nothing is connected for you and nothing is a precondition. See [install/data-integrations.md](install/data-integrations.md).

Prefer not to run your own data? Ongoing managed monitoring (rank tracking, geo-grid, AI citation tracking) is what **SearchOps** does, and **MB Search** offers done-for-you optimisation.

The line that never moves: **no build-time capability is ever paywalled, and nothing here requires a paid key to function.** And reading your *current* data is never a promise of *future* rankings or citations — see the closing note in the [Cite skill](skills/cite-aeo-geo/SKILL.md).

---

## Contributing

Issues and PRs welcome — the bar is correctness and restraint over coverage (this isn't a 20-item flat checklist). In short: respect the ladder's order, verify on served output, stay strictly white-hat, be honest about the boundary, and match the skill template. Full guidance in **[CONTRIBUTING.md](CONTRIBUTING.md)**.

Site-type profiles (content, news/publisher, e-commerce, local, SaaS/marketing, docs, international) ship as [orchestrator references](skills/seo-orchestrator/references/profiles/) with a per-type guide in [USE-CASES.md](USE-CASES.md); new profiles and deeper per-platform (WordPress/Shopify) fix guidance are good contribution areas.

---

## Disclaimer

**This is experimental, and its skills are run by AI agents — which make mistakes.** Treat the output as a well-informed starting point to *review*, not a final authority to apply blindly: verify on the served output as the skills instruct, read the diff, test, and keep everything in version control before publishing. The method reflects an experienced, professional SEO mindset (around fifteen years of practice), but the guidance is general, your situation is specific, and **nothing here guarantees rankings or citations**. Full terms in **[DISCLAIMER.md](DISCLAIMER.md)**.

---

## Licence

[MIT](LICENSE). The value here is the method and the editorial correctness, not lock-in — use it, fork it, build on it.
