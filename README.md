# seo-for-ai-agents

**A drop-in SEO + AEO skill pack that teaches AI coding agents (Claude Code, Cursor, Codex) to build *and audit* sites that search engines rank — and AI answer engines can cite. New sites or existing ones.**

> ⚡ **The problem it fixes:** sites built by AI agents look perfect in a browser and are often nearly **invisible to crawlers** — they serve an empty shell with no real content in the HTML. This pack catches that (and four rungs more), checking **what's actually served to a crawler**, not the source an agent edited and hoped about.

`experimental · v0.1 (current as of 2026-06) · MIT` — **[Which skill when?](SKILLS.md)** · [Method](METHOD.md) · [Changelog](CHANGELOG.md) · [Disclaimer](DISCLAIMER.md)

> **New here?** Paste [`install/copy-paste/audit.md`](install/copy-paste/audit.md) into your agent to audit an **existing** site, or [`install/copy-paste/reach.md`](install/copy-paste/reach.md) for the highest-impact fix on a **new** build. → [Install](#install)

## Contents
- [The method — the Visibility Ladder](#the-method-the-visibility-ladder)
- [It runs as an audit lifecycle](#it-runs-as-an-audit-lifecycle-not-a-one-shot)
- [Who it's for, and how it adapts](#who-its-for-and-how-it-adapts)
- [Install](#install) · [Which skill when? (skills index)](SKILLS.md)
- [The honest boundary](#the-honest-boundary-and-how-live-data-fits) · [Disclaimer](#disclaimer)

It's primarily **SEO** — the technical and on-page fundamentals that drive ranking, done correctly and verified on the served output (not the source). On top sits **AEO** (answer-engine optimisation): the owned-media work to make a page *eligible* to be cited by AI answers. The two are related but not the same, and citation is never guaranteed — the full distinction is in **[METHOD.md](METHOD.md)**. It's **horizontal** (any site, any industry) and built for people who don't want to become SEOs to ship a findable site.

---

## The method: the Visibility Ladder

Five rungs, fixed in sequence. **You cannot climb a rung until the ones beneath it pass.** Diagnose top-to-bottom; fix bottom-to-top.

| # | Rung | The question it answers | Skill |
|---|------|------------------------|-------|
| 1 | **Reach** | Can a crawler reach the URL and see its content in the served HTML? | [`1-reach-indexation`](skills/1-reach-indexation/SKILL.md) |
| 2 | **Read** | Is there real, readable content, correct metadata, and a good page experience (speed + mobile)? | [`2-read-content`](skills/2-read-content/SKILL.md) |
| 3 | **Understand** | Can engines identify the entities? (structured data) | [`3-understand-schema`](skills/3-understand-schema/SKILL.md) |
| 4 | **Connect** | Is the page wired into a coherent site? (internal links, canonicals) | [`4-connect-architecture`](skills/4-connect-architecture/SKILL.md) |
| 5 | **Cite** | Is it formatted to be cited by AI search? (AEO/GEO) | [`5-cite-aeo-geo`](skills/5-cite-aeo-geo/SKILL.md) |

Fixing content (Read) on a page Google can't render (Reach) is wasted work. The ladder stops that. The full philosophy is in **[METHOD.md](METHOD.md)** — read it; it's the heart of the pack.

The **[`seo-orchestrator`](skills/seo-orchestrator/SKILL.md)** is the entry point for any broad request ("audit my SEO", "improve my rankings", "why am I not showing up", "get cited by ChatGPT"). It detects your stack, platform, and site type, finds the lowest failing rung, dispatches in order — and runs the whole thing as a **repeatable audit lifecycle** (below).

**Specialist skills** sit beside the ladder for jobs that don't fit a single rung:

*Technical:*
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

The content & marketing skills get sharper when you connect your own data tools (see [the boundary](#the-honest-boundary-and-how-live-data-fits)), but work without them. `seo-automations` is the one to add once your site is healthy — it keeps it that way.

---

## It runs as an audit lifecycle (not a one-shot)

The pack **remembers**. The orchestrator writes a `.seo/` folder into your project — `audit.md` (a readable health scorecard), `state.json` (every finding with status), `log.md` (dated history) — so it works the first time *and every time after*:

- **First run** → baseline audit across all five rungs, fix the safe wins, record state.
- **Later runs** → re-verify past fixes (**catch regressions** after deploys/edits), find what's new, and advance the prioritised backlog.

That turns it from a one-time fixer into a system that keeps a site healthy over time — which is exactly what an **existing** site needs.

## Who it's for, and how it adapts

- **New / "vibe-coded" sites** — catch the classic failure where an AI-built site looks perfect in a browser but is nearly invisible to crawlers, and ship it correct from the start.
- **Existing sites (developers on Claude Code)** — audit a real codebase, fix safely *without regressing what already ranks* (it protects URLs, canonicals, and intentional decisions — see the don't-regress discipline), and track progress run over run.

It **adapts** to the site: per-stack guidance (Next.js, Astro, Nuxt, SvelteKit, Remix, Gatsby, SPAs, static — plus an honest boundary for hosted platforms like WordPress/Shopify where fixes live in the platform, not the code), and **site-type profiles** (content/blog, e-commerce, local, SaaS/marketing, docs, international) that tune which issues matter most.

---

## Three principles that make it better than a flat checklist

1. **Verify on rendered output, not source.** An agent editing JSX and declaring "meta tags added" proves nothing. Every skill confirms what is actually *served* by re-fetching the URL — because client-rendered content invisible to crawlers is the #1 failure of AI-built sites (and a frequent silent regression on established ones after a refactor or replatform).
2. **Talk to the agent, serve the non-SEO human.** The skill instructs the agent; the agent fixes what's safe, explains every change in plain English and why it matters, and flags what only a human can decide.
3. **Strictly white-hat.** Never fabricate authors, credentials, reviews, or E-E-A-T signals. Where real trust signals are missing, they're flagged as human tasks — never invented. (This isn't only ethics: AI answer engines are built to discount manufactured authority.)

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
- [**`audit.md`**](install/copy-paste/audit.md) — the best all-rounder: runs the full audit lifecycle on a **new or existing** site (creates the `.seo/` report, fixes the floor up).
- [**`reach.md`**](install/copy-paste/reach.md) — the highest-impact single fix and the best demo: catch a site that's invisible to crawlers.
- Then the per-rung minis (`read`, `understand`, `connect`, `cite`), the technical specialists (`migrations`, `measurement`), and the content/marketing minis (`content-audit`, `content-editing`, `positioning-strategy`, `proposal-roadmap`).

On a host with skill support, the [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) does the routing and runs the lifecycle for you.

---

## Two sizes per skill

- **Full** — the canonical `SKILL.md` plus `references/` (the deep standards, type catalogues, and examples). Used by hosts with skill support.
- **Mini** — a single self-contained file in [`copy-paste/`](install/copy-paste/), same logic trimmed of references, for pasting into any chat. The low-friction onramp.

---

## Scope: owned media (your site), not earned media

This pack optimises **owned media** — the website an agent is building or editing. That's everything on your own pages: rendering, content, metadata, speed, mobile, schema, architecture, and answer formatting. It is comprehensive *for that*.

It deliberately does **not** cover **earned media** — the off-site half of SEO: backlinks, digital PR, brand mentions, and reviews on third-party sites. Off-site authority is real and it matters, but it isn't something an AI agent can *build* into your code; it's earned through outreach, relationships, and reputation over time. We flag where it's relevant (e.g. real external profiles for entity trust) but we don't pretend a build can manufacture it — and manufacturing it (fake reviews, bought links) is exactly the black-hat behaviour the pack refuses. Earned media is a genuine, separate discipline, not an oversight here.

---

## The honest boundary (and how live data fits)

The free skills are **build-time and owned-media** at their core — rendering, content, metadata, speed and mobile, schema, structure, architecture, AEO formatting — and they **never require live data**: they work fully with nothing connected. But you can bring data in, two ways:

- **Optional, bring-your-own-key (DIY).** Connect tools you already use — Search Console (free), DataForSEO, Ahrefs, Bing Webmaster — with your **own** API keys, and the audit sharpens: real indexation and rankings, traffic-weighted priorities, and real demand/competitor context for the content and positioning work. Optional and self-service. See [install/data-integrations.md](install/data-integrations.md).
- **Done-for-you (managed).** Don't want to wire up and pay for your own data APIs, or want ongoing managed monitoring — rank tracking, geo-grid, AI-citation tracking — hands-off? That's **SearchOps** (managed data) and **MB Search** (done-for-you optimisation).

The line that never moves: **no build-time capability is ever paywalled, and nothing here requires a paid key to function.** And reading your *current* data is never a promise of *future* rankings or citations — see the closing note in the [Cite skill](skills/5-cite-aeo-geo/SKILL.md).

---

## Contributing

Issues and PRs welcome — the bar is correctness and restraint over coverage (this isn't a 20-item flat checklist). In short: respect the ladder's order, verify on served output, stay strictly white-hat, be honest about the boundary, and match the skill template. Full guidance in **[CONTRIBUTING.md](CONTRIBUTING.md)**.

Site-type profiles (content, e-commerce, local, SaaS/marketing, docs, international) ship as [orchestrator references](skills/seo-orchestrator/references/profiles/); new profiles and deeper per-platform (WordPress/Shopify) fix guidance are good contribution areas.

---

## Disclaimer

**This is experimental, and its skills are run by AI agents — which make mistakes.** Treat the output as a well-informed starting point to *review*, not a final authority to apply blindly: verify on the served output as the skills instruct, read the diff, test, and keep everything in version control before publishing. The method reflects an experienced, professional SEO mindset (around fifteen years of practice), but the guidance is general, your situation is specific, and **nothing here guarantees rankings or citations**. Full terms in **[DISCLAIMER.md](DISCLAIMER.md)**.

---

## Licence

[MIT](LICENSE). The value here is the method and the editorial correctness, not lock-in — use it, fork it, build on it.
