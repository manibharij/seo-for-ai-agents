# Which skill do I use when?

**Start with the orchestrator** for anything broad: it works out the site, finds what is
failing, routes to the rest, and runs the audit lifecycle. Reach for a specific skill
only when your request is already scoped.

Looking by *site type* instead (shop, blog, SaaS, docs, local, news, international)? See
**[USE-CASES.md](USE-CASES.md)**. Looking for the method behind the grouping? See
**[METHOD.md](METHOD.md)** and [`model/`](model/).

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
Run seo-access-reach in re-check mode.
```

Without an install, the same three modes are copy-paste minis:
[`audit.md`](install/copy-paste/audit.md), [`fix.md`](install/copy-paste/fix.md) and
[`recheck.md`](install/copy-paste/recheck.md). Every skill also adapts to what it can
reach (a URL only, a read-only repo, or write access), to a scope or time budget, and to
whatever data your environment already has: see
[`operating-modes.md`](skills/seo-orchestrator/references/operating-modes.md).

---

## Entry point

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-orchestrator`](skills/seo-orchestrator/SKILL.md) | Works out the stack, platform and site type, runs the whole model as a repeatable audit, routes to every other skill | "audit my SEO", "improve my rankings", "why isn't my site showing up" |

## Demand: what is actually being asked

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-demand-search-data`](skills/seo-demand-search-data/SKILL.md) | Reads the search data your environment already has (Search Console, analytics, CrUX, Bing, an SEO tool) to triage indexing, protect pages that earn traffic, map demand and measure whether changes worked | "why aren't these pages indexed", "did our change work", "what's in striking distance" |

## Identity: who you provably are

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-identity-context`](skills/seo-identity-context/SKILL.md) | **Run this before any content work.** Learns the business (offer, audience and their vocabulary, provable differentiators, real proof, voice, claim constraints) and writes `.seo/context.md`. Every fact labelled established / inferred / unknown | "understand my business", "what's our voice", "who are we writing for" |
| [`seo-identity-positioning`](skills/seo-identity-positioning/SKILL.md) | What topics to own, how to differentiate, pillar and cluster planning | "topical authority", "what should we cover", "competitive analysis" |

## Substance: whether it is worth choosing

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-substance-quality`](skills/seo-substance-quality/SKILL.md) | Whether a page deserves to win: search intent, genuine quality and depth, honest on-page experience and expertise | "why am I not ranking", "is my content good enough", "search intent" |
| [`seo-substance-content-audit`](skills/seo-substance-content-audit/SKILL.md) | Assess content across the site: keep, improve, consolidate, refresh, prune, create | "content audit", "which pages to update or remove" |
| [`seo-substance-content-editing`](skills/seo-substance-content-editing/SKILL.md) | Improve the copy on one specific page. Editing, never generation | "improve this page's copy", "tighten this" |
| [`seo-substance-media`](skills/seo-substance-media/SKILL.md) | Image and video: alt text, formats, `VideoObject`, media sitemaps, real transcripts | "image SEO", "video SEO", "image sitemap" |
| [`seo-substance-at-scale`](skills/seo-substance-at-scale/SKILL.md) | Pages at scale from data, white-hat, behind a quality gate that refuses thin or doorway pages | "programmatic SEO", "location pages at scale" |

## Access: whether a machine can get it, read it, understand it, move through it

This is where **the Visibility Ladder** lives. Four rungs in dependency order: diagnose
top to bottom, fix bottom to top.

| Rung | Skill | The question it answers |
|---|---|---|
| 1. Reach | [`seo-access-reach`](skills/seo-access-reach/SKILL.md) | Can a crawler reach the URL and see its content in the served HTML? |
| 2. Read | [`seo-access-read`](skills/seo-access-read/SKILL.md) | Is there real, readable content, correct metadata, and a usable page experience? |
| 3. Understand | [`seo-access-understand`](skills/seo-access-understand/SKILL.md) | Can engines identify the entities? (structured data) |
| 4. Connect | [`seo-access-connect`](skills/seo-access-connect/SKILL.md) | Is the page wired into a coherent site? (internal links, canonicals) |

Plus the Access specialists:

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-access-performance`](skills/seo-access-performance/SKILL.md) | Core Web Vitals deep work: field data first, then lab, LCP sub-parts, INP, CLS, third-party tags | "Core Web Vitals failing", "fix our LCP", "site is slow" |
| [`seo-access-migrations`](skills/seo-access-migrations/SKILL.md) | Preserve rankings when URLs change | "redesign", "moving domain", "404s after relaunch" |
| [`seo-access-logs`](skills/seo-access-logs/SKILL.md) | Server-log and crawl-budget analysis on large sites: what crawlers actually fetch | "log file analysis", "crawl budget" |

## Distribution: what points at you (earned, advisory only)

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-distribution-authority`](skills/seo-distribution-authority/SKILL.md) | Backlink audit, toxic links and a disavow file, the competitor authority gap, white-hat link and digital-PR strategy. Audits and advises, never executes outreach or buys links | "backlinks", "link building", "off-page SEO", "disavow" |

## Operations: keeping it true

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-operations-launch-qa`](skills/seo-operations-launch-qa/SKILL.md) | Pre-launch and go-live checks on the production URL, split into launch blockers and fix-this-week | "we're about to launch", "going live" |
| [`seo-operations-measurement`](skills/seo-operations-measurement/SKILL.md) | Install analytics, Search Console and web-vitals. Setup only | "set up analytics", "install GA4" |
| [`seo-operations-automation`](skills/seo-operations-automation/SKILL.md) | Run the audit in CI/CD: a regression gate on deploy or PR, plus scheduled re-audits | "SEO checks in CI", "catch regressions automatically" |
| [`seo-operations-reporting`](skills/seo-operations-reporting/SKILL.md) | Package findings into a prioritised plan or client proposal, with honest outcome language | "build a roadmap", "what should we do first" |

## Surfaces: where visibility is judged

| Skill | What it does | Reach for it when you say… |
|---|---|---|
| [`seo-surface-assistants`](skills/seo-surface-assistants/SKILL.md) | Make a page *eligible* to be named by AI answer engines. Eligibility only: citation is never guaranteed | "AI Overviews", "get cited by ChatGPT", "AEO", "llms.txt" |

Per-surface profiles, stating what weighs there and how honestly it can be verified, live
in [`surfaces/`](surfaces/).

---

## How the grouping works

Six groups, because visibility is produced by five systems and kept by one loop. The
systems are separated by **your relationship to control**:

- **Demand** is *observed*. You read it and choose. You never invent it.
- **Identity**, **Substance** and **Access** are *built*. Diagnose and change them.
- **Distribution** is *earned*. Analyse and advise. Never execute.
- **Operations** is the *loop*. Measure, verify, catch regressions, report, repeat.

Dependency runs one way only inside Access: nothing downstream matters if a machine
cannot reach the page. Everything else is simultaneous. A perfect Access score with no
Demand reading is a well-built page nobody was looking for.

**Rank is not in this list**, because it is not a step. It is the outcome all five
systems produce together. See [METHOD.md](METHOD.md).

No host? Every skill has a paste-into-chat mini in
[`install/copy-paste/`](install/copy-paste/). Start with
[`audit.md`](install/copy-paste/audit.md), which changes nothing, then
[`fix.md`](install/copy-paste/fix.md) for the findings you approve.
