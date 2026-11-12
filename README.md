# seo-for-ai-agents

**A drop-in skill pack that teaches AI coding agents (Claude Code, Cursor, Codex) to build *and audit* sites that search engines rank and AI assistants can name. New sites or existing ones.**

> ⚡ **The problem it fixes:** sites built by AI agents look perfect in a browser and are often nearly **invisible to crawlers**. They serve an empty shell with no real content in the HTML. This pack catches that, and much more, by checking **what is actually served to a crawler**, not the source an agent edited and hoped about.

`experimental · v0.2 (current as of 2026-10) · MIT` — **[Which skill when?](SKILLS.md)** · [Method](METHOD.md) · [Use cases](USE-CASES.md) · [Changelog](CHANGELOG.md) · [Disclaimer](DISCLAIMER.md)

> **New here?** Paste [`install/copy-paste/audit.md`](install/copy-paste/audit.md) into your agent. It audits a new or existing site and **changes nothing**. When you have reviewed the findings, [`fix.md`](install/copy-paste/fix.md) applies only the ones you approve, and [`recheck.md`](install/copy-paste/recheck.md) re-tests them later. About to go live? Use [`launch-qa.md`](install/copy-paste/launch-qa.md). → [Install](#install)

> **Upgrading?** Every skill was renamed to the system it belongs to, so saved prompts need updating. The full mapping is in [CHANGELOG.md](CHANGELOG.md).

## Contents
- [Three modes: audit, fix, re-check](#three-modes-audit-fix-re-check)
- [The method: the Visibility Model](#the-method-the-visibility-model)
- [The skills, by system](#the-skills-by-system)
- [The agentic structure](#the-agentic-structure)
- [It runs as a loop](#it-runs-as-a-loop-not-a-one-shot)
- [Who it's for, and how it adapts](#who-its-for-and-how-it-adapts) · [Use cases by site type](USE-CASES.md)
- [Install](#install) · [Which skill when? (skills index)](SKILLS.md)
- [The honest boundary](#the-honest-boundary-and-how-live-data-fits) · [Disclaimer](#disclaimer)

It is primarily **SEO**: the technical, content and entity fundamentals that drive ranking, done correctly and verified on the served output rather than the source. **AI assistant visibility is treated as a surface, not a bolt-on**, because being named by ChatGPT draws on the same five systems and is simply verified far more weakly. Citation is never guaranteed, and the only thing this pack will ever claim is **eligibility**. The full distinction is in **[METHOD.md](METHOD.md)**. It is horizontal (any site, any industry) and built for people who do not want to become SEOs in order to ship a findable site.

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
Run seo-access-reach in re-check mode.
```

Without an install, the same three modes are copy-paste minis: [`audit.md`](install/copy-paste/audit.md), [`fix.md`](install/copy-paste/fix.md) and [`recheck.md`](install/copy-paste/recheck.md). Every skill also adapts to what it can reach (a URL only, a read-only repo, or write access), to a scope or time budget, and to whatever data your environment already has: see [`operating-modes.md`](skills/seo-orchestrator/references/operating-modes.md).

---

## The method: the Visibility Model

Five systems produce visibility. One loop keeps it. Many surfaces judge it. The systems are separated by **your relationship to control**, because that is what decides whether an agent may act, advise, or only observe.

| System | Relationship | The question it answers |
|---|---|---|
| **Demand** | Observed | What are people and machines actually asking, and which of it is worth having? |
| **Identity** | Built | Who are you, provably, everywhere you appear? |
| **Substance** | Built | Is what you offer and say actually worth choosing? |
| **Access** | Built | Can a machine get it, read it, understand it, and move through it? |
| **Distribution** | Earned | Does anything outside your control point at you? |

Around all five runs the **Operations loop**: measure, verify on served output, catch regressions, monitor, report, repeat.

### The Visibility Ladder is the Access system

Four rungs, in dependency order. **Diagnose top to bottom, fix bottom to top**, because the lowest broken rung quietly caps everything above it.

| Rung | The question it answers | Skill |
|---|---|---|
| 1. **Reach** | Can a crawler reach the URL and see its content in the served HTML? | [`seo-access-reach`](skills/seo-access-reach/SKILL.md) |
| 2. **Read** | Is there real, readable content, correct metadata, and a usable page experience? | [`seo-access-read`](skills/seo-access-read/SKILL.md) |
| 3. **Understand** | Can engines identify the entities? (structured data) | [`seo-access-understand`](skills/seo-access-understand/SKILL.md) |
| 4. **Connect** | Is the page wired into a coherent site? (internal links, canonicals) | [`seo-access-connect`](skills/seo-access-connect/SKILL.md) |

Fixing content on a page Google cannot render is wasted work. The ladder stops that, and inside Access it is as strict as it ever was.

### Rank is the outcome, not a step

Rank used to be rung five. It is now **the result the whole model produces**, which is a promotion rather than a demotion: "improve rankings" was never one rung you could climb to. Its old contents moved to where the work actually happens. Search intent and genuine quality to **Substance**, experience and expertise and authorship to **Identity**, and the authority you can only earn to **Distribution**.

Dependency runs one way only inside Access. **Everything else is simultaneous.** A perfect Access score with no Demand reading is a fast, well-formed, beautifully structured page that nobody was looking for.

Full narrative in **[METHOD.md](METHOD.md)**; the canonical reference is [`model/`](model/).

---

## The skills, by system

The **[`seo-orchestrator`](skills/seo-orchestrator/SKILL.md)** is the entry point for any broad request ("audit my SEO", "why am I not showing up", "get named by ChatGPT"). It works out your stack, platform and site type, finds what is failing, dispatches in order, and runs the whole thing as a repeatable loop.

**Demand** — what is actually being asked
- **[`seo-demand-search-data`](skills/seo-demand-search-data/SKILL.md)** reads the search data your environment already provides to see what Google actually concluded: indexing reasons and its chosen canonical, which pages earn traffic and must be protected, real demand and striking-distance queries, and whether a change worked. It detects capabilities, not products, and never requires data.

**Identity** — who you provably are
- **[`seo-identity-context`](skills/seo-identity-context/SKILL.md)** learns the business before touching its words: what it sells, who it serves and in *their* vocabulary, which differentiators are provable, what real proof exists, how it writes, and what it may not claim. Written once to `.seo/context.md`. Every fact is labelled established / inferred / unknown, and **only an established fact may ever reach published copy or schema**. This is how the pack answers "do not fabricate" with something better than a refusal: go and find the real material first.
- **[`seo-identity-positioning`](skills/seo-identity-positioning/SKILL.md)** what topics to own, how to differentiate, and a pillar and cluster plan.

**Substance** — whether it is worth choosing
- **[`seo-substance-quality`](skills/seo-substance-quality/SKILL.md)** whether a page deserves to win: intent, depth, honest experience and expertise.
- **[`seo-substance-content-audit`](skills/seo-substance-content-audit/SKILL.md)** assess content across the site and recommend keep / improve / consolidate / refresh / prune / create.
- **[`seo-substance-content-editing`](skills/seo-substance-content-editing/SKILL.md)** improve existing copy on one page. Strictly editing, never generation.
- **[`seo-substance-media`](skills/seo-substance-media/SKILL.md)** image and video: `VideoObject`, media sitemaps, real transcripts.
- **[`seo-substance-at-scale`](skills/seo-substance-at-scale/SKILL.md)** pages at scale from data, behind a quality gate that refuses thin or doorway pages.

**Access** — the ladder, plus its specialists
- **[`seo-access-performance`](skills/seo-access-performance/SKILL.md)** Core Web Vitals deep work: field data first, then lab and the cause.
- **[`seo-access-migrations`](skills/seo-access-migrations/SKILL.md)** preserve rankings when URLs change.
- **[`seo-access-logs`](skills/seo-access-logs/SKILL.md)** large-site server logs and crawl budget: what crawlers actually fetch.

**Distribution** — earned, advisory only
- **[`seo-distribution-authority`](skills/seo-distribution-authority/SKILL.md)** backlink audit, toxic links and a disavow file, the competitor authority gap, and white-hat link and digital-PR strategy. It audits and advises. It never executes outreach and never buys links.

**Operations** — keeping it true
- **[`seo-operations-launch-qa`](skills/seo-operations-launch-qa/SKILL.md)** go-live checks on the production URL, split into launch blockers and fix-this-week.
- **[`seo-operations-measurement`](skills/seo-operations-measurement/SKILL.md)** wire up analytics, Search Console and web-vitals so results *can* be measured. Setup only.
- **[`seo-operations-automation`](skills/seo-operations-automation/SKILL.md)** run the audit in CI/CD: a regression gate that fails a deploy which would make the site invisible, plus scheduled re-audits.
- **[`seo-operations-reporting`](skills/seo-operations-reporting/SKILL.md)** package the audit into a prioritised plan or client proposal, with honest outcome language.

**Surfaces** — where visibility is judged
- **[`seo-surface-assistants`](skills/seo-surface-assistants/SKILL.md)** make a page *eligible* to be named by AI answer engines, on a page whose fundamentals are already sound.

Full index with trigger phrases: **[SKILLS.md](SKILLS.md)**.

---

## The agentic structure

The pack is not only a library a human points an agent at. It is the executable method behind an agentic workflow.

| Folder | What it holds |
|---|---|
| [`model/`](model/) | The canonical method: [systems](model/systems.md), [surfaces](model/surfaces.md), [invariants](model/invariants.md) |
| [`jobs/`](jobs/) | The nine situations you actually arrive with, which scope the model and activate roles. Nobody arrives with a rung |
| [`roles/`](roles/) | Six roles: what each owns, which tools it may use, what it must ask before doing, its budget, and what finishing means |
| [`surfaces/`](surfaces/) | Sixteen surface profiles: what weighs there, how it is verified, and what is simply unknowable |
| [`contracts/`](contracts/) | Machine-readable schemas for findings, context facts, work items and evidence, so results can be stored, diffed and compared rather than only read |

One detail worth knowing: `finding.verify.method` in the schema has no `source` option. "Verify on served output" is enforced by the contract rather than by good intentions.

### Start from the situation you are actually in

Jobs are the front door. Each one says which system leads, in what order to work, and what
the honest negative answer looks like.

| You are saying | Job | Leading system |
|---|---|---|
| "I have an idea and I am about to build it" | [`new-site`](jobs/new-site.md) | Demand |
| "We are going live this week" | [`launch`](jobs/launch.md) | Access |
| "Something is wrong and I do not know why" | [`rescue`](jobs/rescue.md) | Operations, then Access |
| "It works, and I want more of it" | [`grow`](jobs/grow.md) | Demand, Substance, Distribution |
| "The URLs are changing" | [`migrate`](jobs/migrate.md) | Access |
| "I need a lot of pages" | [`scale`](jobs/scale.md) | Substance, as a gate |
| "I want AI assistants to recommend me" | [`ai-visible`](jobs/ai-visible.md) | Identity |
| "I need to audit a site I do not control" | [`client-audit`](jobs/client-audit.md) | Whichever is the constraint |
| "Keep it from breaking" | [`maintain`](jobs/maintain.md) | Operations |

The autonomy each job defaults to tracks **what is at risk**, not how hard the work is.
`new-site` and `maintain` are the most autonomous, because a new site has nothing to break
and maintenance only re-runs known checks. `migrate` and `grow` are the least, because both
can destroy something that already earns.

---

## It runs as a loop, not a one-shot

The pack **remembers**. The orchestrator writes a `.seo/` folder into your project: `audit.md` (a readable scorecard), `state.json` (every finding with status), `log.md` (dated history). So it works the first time and every time after.

- **First run** (`audit`): a baseline across all five systems, findings recorded with ids. Nothing on the site changes.
- **Then** (`fix`): you approve findings and the agent applies only those, logging each change with a date.
- **Later runs** (`re-check`): re-verify past fixes, **catch regressions** after deploys, measure what changed where data is available, and find what is new.

Visibility decays. A fix verified in March is undone by a deploy in April, which is exactly why Operations is a loop rather than a step.

## Who it's for, and how it adapts

- **New or vibe-coded sites** — catch the classic failure where an AI-built site looks perfect in a browser but is nearly invisible to crawlers, and ship it correct from the start.
- **Existing sites** — audit a real codebase and fix safely *without regressing what already ranks*. It protects URLs, canonicals and intentional past decisions.

It adapts to the site: per-stack guidance (Next.js, Astro, Nuxt, SvelteKit, Remix, Gatsby, SPAs, static, plus an honest boundary for hosted platforms like WordPress and Shopify where fixes live in the platform rather than the code), and site-type profiles (content/blog, news, e-commerce, local, SaaS, docs, international) that tune which issues matter most. **[USE-CASES.md](USE-CASES.md)** maps each site type to its profile, priority tilt and a ready-to-paste starter prompt.

---

## Four rules that make it better than a flat checklist

The full set is in [`model/invariants.md`](model/invariants.md).

1. **Work it out yourself, do not interrogate the user.** You should not have to know SEO or describe your site. The agent reads the codebase and the served pages, infers the context, acts on sensible defaults, and pauses only for the few calls a human genuinely must make. Inferring beats asking.
2. **Verify on served output, not source.** An agent editing JSX and declaring "meta tags added" proves nothing. It changed an intention. Every skill confirms what is actually served by re-fetching the URL.
3. **Only established facts may be published.** Every fact carries its provenance. An inferred fact may guide strategy and may never be asserted.
4. **On an existing site, first do no harm.** A `noindex`, a canonical or a blocked path that looks wrong may be load-bearing. Understand what is deliberate before changing it, and put risky changes in front of a human.

---

## Install

| Host | Guide |
|------|-------|
| **Claude Code** | [install/claude-code.md](install/claude-code.md) — drop into `~/.claude/skills/` or project `.claude/skills/` |
| **Cursor** | [install/cursor.md](install/cursor.md) — `.cursor/rules/*.mdc` |
| **AGENTS.md hosts** (Codex, Gemini CLI, Zed…) | [install/agents-md.md](install/agents-md.md) |
| **No host? Copy-paste** | [install/copy-paste/](install/copy-paste/) — self-contained minis to paste into any chat |
| **Optional MCP power-ups** | [install/mcp.md](install/mcp.md) — sharper verification, never required |
| **Optional data integrations** | [install/data-integrations.md](install/data-integrations.md) — bring-your-own-key (Search Console, DataForSEO, Ahrefs…), never required |

Install copies the **whole `skills/` folder**. The orchestrator carries the shared cross-cutting references (lifecycle, profiles, adapters), so keep the skills together. Skills are deliberately one level deep, because a flat copy into `~/.claude/skills/` is what makes them discoverable; `scripts/check-links.py` enforces that.

### Fastest start (no setup)
- [**`audit.md`**](install/copy-paste/audit.md): the best all-rounder. Audits a new or existing site, records findings in `.seo/`, changes nothing.
- [**`fix.md`**](install/copy-paste/fix.md): applies only the findings you approve, one commit each, verified on the served output.
- [**`recheck.md`**](install/copy-paste/recheck.md): re-tests earlier findings and catches regressions.
- [**`launch-qa.md`**](install/copy-paste/launch-qa.md): the go-live pass, blockers first.
- [**`reach.md`**](install/copy-paste/reach.md): the highest-impact single fix and the best demo, catching a site that is invisible to crawlers.
- [**`context.md`**](install/copy-paste/context.md): the foundation for content work, so nothing downstream has to guess.
- Then the rest, one per skill, in [`install/copy-paste/`](install/copy-paste/).

## Two sizes per skill

- **Full** — the canonical `SKILL.md` plus `references/`, the deep standards and worked examples. Used by hosts with skill support.
- **Mini** — a single self-contained file in [`copy-paste/`](install/copy-paste/), the same logic trimmed of references, for pasting into any chat.

---

## Scope: owned media is built, earned media is advised

This pack **builds owned media**: everything on your own pages and in your own entity. Identity, Substance and Access are all build-time, owned work.

**Earned media**, the off-site half, cannot be built into your code. It is earned through outreach and reputation over time, and faking it with bought links or fake reviews is the black-hat behaviour this pack refuses. So Distribution has a real place in the model and a real skill behind it, and that skill audits and strategises only. The earning itself stays off-site, ongoing work, yours or a managed service's.

## The honest boundary (and how live data fits)

At their core the skills are build-time work. They **never require live data** and work fully with nothing connected.

They get sharper with whatever your environment already has. The pack detects capabilities, not products: if your agent has a tool for search performance, URL inspection, Core Web Vitals field data, revenue by landing page, keyword demand, backlinks or AI answer mentions (an MCP server, a connector, a CLI, your own keys, or an exported file), the skills use it read-only and record which sources each report used. Nothing is connected for you and nothing is a precondition. See [install/data-integrations.md](install/data-integrations.md).

Prefer not to run your own data? Ongoing managed monitoring (rank tracking, geo-grid, AI visibility) is what **SearchOps** does, and **MB Search** offers done-for-you optimisation.

The line that never moves: **no build-time capability is ever paywalled, and nothing here requires a paid key to function.** And reading your *current* data is never a promise of *future* rankings or citations.

---

## Contributing

Issues and PRs welcome. The bar is correctness and restraint over coverage. In short: respect the ladder's order inside Access, verify on served output, stay strictly white-hat, be honest about the boundary, and match the skill template. Full guidance in **[CONTRIBUTING.md](CONTRIBUTING.md)**.

Good contribution areas: surface profiles in [`surfaces/`](surfaces/), new site-type profiles, and deeper per-platform (WordPress, Shopify) fix guidance.

Run `python scripts/check-links.py` before opening a PR. It checks every relative link, that each skill's `name:` matches its directory, and that no skill is nested.

---

## Disclaimer

**This is experimental, and its skills are run by AI agents, which make mistakes.** Treat the output as a well-informed starting point to *review*, not a final authority to apply blindly: verify on the served output as the skills instruct, read the diff, test, and keep everything in version control before publishing. The method reflects an experienced professional SEO mindset (around fifteen years of practice), but the guidance is general, your situation is specific, and **nothing here guarantees rankings or citations**. Full terms in **[DISCLAIMER.md](DISCLAIMER.md)**.

## Licence

[MIT](LICENSE). The value here is the method and the editorial correctness, not lock-in. Use it, fork it, build on it.
