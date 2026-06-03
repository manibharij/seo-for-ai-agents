# seo-for-ai-agents

**A drop-in SEO skill pack that teaches AI coding agents to build sites that search engines rank well — and that AI answer engines can draw on.**

> **New here?** The fastest start is to paste [`install/copy-paste/reach.md`](install/copy-paste/reach.md) into your AI agent and ask it to run the steps on your site. Everything below explains why, and how to install the full pack. Jump to [Install](#install).

This is, first and foremost, a proper **SEO** pack: comprehensive, build-time, on your own site, for owners who don't know SEO and the AI agents building for them. It covers the technical and on-page fundamentals that drive search visibility — done correctly and verified on what's actually served, not just edited in the source.

It's also built for the AI-search era — but honestly. Search is moving from ten blue links toward synthesised answers that cite a handful of sources (AI Overviews, AI Mode, ChatGPT, Perplexity, Claude), and that direction matters. So the pack adds a rung for **answer-engine optimisation (AEO)**: the things you can do *on your own site* to be eligible to be cited.

One distinction most packs blur, stated plainly: **SEO and AEO are related, but not the same thing.** They share a foundation — a page has to be reachable, readable, understandable, and well-structured to do anything in either. But they diverge at the top. SEO ranks *your page*, and that ranking is largely earned by your page. Whether an AI answer actually *cites* you is far less in your control: the engine synthesises from many sources and often answers without citing anyone in particular, so even a perfectly optimised page may not be quoted. AEO improves your **eligibility**; it cannot promise the outcome.

So this is **primarily SEO, with AEO as the owned-media layer on top.** **Rungs 1–4 are the SEO fundamentals** (rendering, content, metadata, speed, mobile, schema, architecture, canonicals); **rung 5 is the owned side of AEO** — the formatting and trust signals that make a page citable, with no false promise that it will be cited. Most sites built by AI agents fail at the very bottom — perfect in a browser, nearly invisible to a crawler — so that's where the method starts.

It's **horizontal** (any site, any industry), built for users who **don't know SEO**, and it **verifies on what's actually served to a crawler** — not on the source code an agent edited and hoped about.

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

The **[`seo-orchestrator`](skills/seo-orchestrator/SKILL.md)** is the entry point for any broad request ("improve my SEO", "why am I not showing up", "get cited by ChatGPT"): it detects your stack, finds the lowest failing rung, and dispatches in order.

---

## Three principles that make it better than a flat checklist

1. **Verify on rendered output, not source.** An agent editing JSX and declaring "meta tags added" proves nothing. Every skill confirms what is actually *served* by re-fetching the URL — because client-rendered content invisible to crawlers is the #1 failure of AI-built sites.
2. **Talk to the agent, serve the non-SEO human.** The skill instructs the agent; the agent fixes what's safe, explains every change in plain English and why it matters, and flags what only a human can decide.
3. **Strictly white-hat.** Never fabricate authors, credentials, reviews, or E-E-A-T signals. Where real trust signals are missing, they're flagged as human tasks — never invented. (This isn't only ethics: AI answer engines are built to discount manufactured authority.)

---

## Install

| Host | Guide |
|------|-------|
| **Claude Code** | [install/claude-code.md](install/claude-code.md) — drop into `~/.claude/skills/` or project `.claude/skills/` |
| **Cursor** | [install/cursor.md](install/cursor.md) — `.cursor/rules/*.mdc` |
| **AGENTS.md hosts** (Codex, Gemini CLI, Zed…) | [install/agents-md.md](install/agents-md.md) |
| **No host? Copy-paste** | [install/copy-paste/](install/copy-paste/) — one self-contained mini per rung, to paste into any chat |
| **Optional MCP power-ups** | [install/mcp.md](install/mcp.md) — sharper verification; never required |

### Fastest start (no setup)
Paste [install/copy-paste/reach.md](install/copy-paste/reach.md) into your agent and ask it to run through the steps on your site. Reach is where most AI-built sites are broken — it's the highest-impact single fix and the best demo of the pack. The copy-paste folder has one mini per rung (reach → read → understand → connect → cite); there's no separate "router" mini, so for a broad request just start at `reach.md` and climb in order. On a host with skill support, the [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) does that routing for you.

---

## Two sizes per skill

- **Full** — the canonical `SKILL.md` plus `references/` (the deep standards, type catalogues, and examples). Used by hosts with skill support.
- **Mini** — a single self-contained file in [`copy-paste/`](install/copy-paste/), same logic trimmed of references, for pasting into any chat. The low-friction onramp.

---

## Scope: owned media (your site), not earned media

This pack optimises **owned media** — the website an agent is building or editing. That's everything on your own pages: rendering, content, metadata, speed, mobile, schema, architecture, and answer formatting. It is comprehensive *for that*.

It deliberately does **not** cover **earned media** — the off-site half of SEO: backlinks, digital PR, brand mentions, and reviews on third-party sites. Off-site authority is real and it matters, but it isn't something an AI agent can *build* into your code; it's earned through outreach, relationships, and reputation over time. We flag where it's relevant (e.g. real external profiles for entity trust) but we don't pretend a build can manufacture it — and manufacturing it (fake reviews, bought links) is exactly the black-hat behaviour the pack refuses. Earned media is a genuine, separate discipline, not an oversight here.

---

## The honest boundary

The free skills fix **build-time** decisions — rendering, content, metadata, speed and mobile, schema, structure, internal architecture, AEO formatting. They cannot tell you what's happening in the live world: whether you actually rank, where, against whom, in which local map cells, or whether you're being cited by AI engines over time. That requires **live data** — rank tracking, AI-citation monitoring, real-user Core Web Vitals, and geo-grid/local visibility — which is a separate, ongoing discipline.

This pack states that line plainly and **never paywalls a capability it claims to give away.** The build skills are free and complete for what they do; live measurement and done-for-you optimisation are the genuinely separate next step (see the closing note in the [Cite skill](skills/5-cite-aeo-geo/SKILL.md)).

---

## Contributing

Issues and PRs welcome — the bar is correctness and restraint over coverage (this isn't a 20-item flat checklist). In short: respect the ladder's order, verify on served output, stay strictly white-hat, be honest about the boundary, and match the skill template. Full guidance in **[CONTRIBUTING.md](CONTRIBUTING.md)**.

Per-type modifiers (local, e-commerce, international) are planned as a future addition once the five rungs have traction.

---

## Disclaimer

**This is experimental, and its skills are run by AI agents — which make mistakes.** Treat the output as a well-informed starting point to *review*, not a final authority to apply blindly: verify on the served output as the skills instruct, read the diff, test, and keep everything in version control before publishing. The method reflects an experienced, professional SEO mindset (around fifteen years of practice), but the guidance is general, your situation is specific, and **nothing here guarantees rankings or citations**. Full terms in **[DISCLAIMER.md](DISCLAIMER.md)**.

---

## Licence

[MIT](LICENSE). The value here is the method and the editorial correctness, not lock-in — use it, fork it, build on it.
