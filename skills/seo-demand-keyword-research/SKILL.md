---
name: seo-demand-keyword-research
description: >-
  Find out what people actually search, size it honestly, cluster it by intent
  and decide which of it is worth having. Use on any "keyword research", "what
  keywords should I target", "find keywords", "search volume", "keyword
  difficulty", "keyword gap", "what should we write about", "topic ideas", or
  "is there demand for this" request. Reads demand, never invents it: every
  number carries its source and date, and "there is no reachable demand here" is
  a valid and valuable answer.
---

# Keyword research — reading demand, not generating lists

The Demand system is **observed**: you read it and choose, and you never invent it.
`model/systems.md` is blunt about the stakes, because reading demand wrongly "is the most
expensive mistake available, because every other system is then pointed at the wrong
target". Perfect execution aimed at nothing is the worst outcome in this method.

This skill is the discovery half. Its sibling `seo-demand-search-data` reads the demand you
**already touch**, from Search Console and analytics; this one finds demand you do not have
yet and decides whether it is reachable. Where it goes next is Identity:
`seo-identity-positioning` decides which territory to own.

Autonomy here is **rung 1, observe and recommend**. There is nothing to execute: the output
is a judgement that redirects everyone else's work.

Work the four steps: **Seed → Expand → Cluster & size → Choose, and report what you rejected.**

---

## When this fires
- A new site or a new section, before anything is written (`jobs/new-site.md`).
- "What should we write about next."
- A content plan that was built from a tool's suggestions with no intent reading.
- Entering a new market, where demand must be read in that market rather than translated.

## Inputs and modes

Infer these before Step 1. Ask only if a wrong guess would be costly (see `seo-orchestrator/references/operating-modes.md`).
- **Data:** whatever the environment already has. Search Console for queries you already touch; a keyword tool for volume and difficulty; the SERP itself, which is free and the most informative of the three. Detect, never require: see `seo-orchestrator/references/live-data-integrations.md`.
- **Mode:** `audit` is the only meaningful mode here. Nothing is changed.
- **Context:** read `.seo/context.md` first. Seeds come from the business, not from a tool.
- **Record findings** with `skill: seo-demand-keyword-research`, `system: demand`. Every volume figure carries its source, date, country and database, or it does not get written down.

---

## Step 1 — Seed from the business, not from a tool

Start from `.seo/context.md`: what is actually sold, to whom, in the words **they** use. A
tool's suggestions anchored on a single seed will reproduce that seed's framing and miss the
vocabulary the customer actually has.

Good seeds: the offer in plain words; the problem it solves, stated as a customer would
state it; the competitors a buyer would compare; the questions the business is genuinely
asked, from support tickets, sales calls and community threads.

Where customer vocabulary and practitioner vocabulary differ, record both. That gap is
frequently the whole opportunity.

## Step 2 — Expand

- **Search Console** first where it exists: queries you already get impressions for are
  observed demand, not estimated, and they are the most reliable input you will have.
- **A keyword tool**, where the environment has one, for volume, difficulty and related
  terms. See `seo-orchestrator/references/data/dataforseo.md` and `ahrefs-semrush.md`.
- **The SERP itself**, which costs nothing: related searches, People Also Ask, and the shape
  of the results.
- **Communities**, read as evidence of real phrasing. Never posted to.

**With no tool at all, say so and carry on.** Search Console plus the SERP plus the business
gets you most of the way; the honest report names what a tool would have sharpened.

## Step 3 — Cluster by intent, and size honestly

**Cluster by what the searcher wants, not by string similarity.** Two phrasings that return
substantially the same results are one cluster and should be one page. Two phrasings that
look alike and return different result types are two intents and must not share a page. The
SERP is the arbiter, and checking it is the step that makes this work rather than guesswork.
Method and worked example: `seo-identity-positioning/references/serp-competitor-and-keyword-research.md`.

For each cluster record: the dominant intent, the result shape Google has chosen, who
currently holds it, the volume with its source and date, and the difficulty as a judgement
rather than a borrowed score.

**Never invent a number.** No volume returned means unknown. An interpolated figure is worse
than no figure, because somebody will build a business on it. Prompt demand in particular
has no volume source and is always `inferred`.

## Step 4 — Choose, and report what you rejected

The output is not a list, it is a decision. For each cluster: pursue, defer, or decline, and
why. Judge on:

- **Reachability.** Demand held by sites with a decade of authority is not addressable for a
  new project in any useful timeframe. Say so rather than listing it.
- **Commercial relevance.** High volume with no relationship to what is sold is a trap.
- **Information gain available.** Can this business add anything the current results lack?
  If not, the page should not be written (`seo-substance-quality/references/information-gain.md`).
- **Intent fit.** Can you serve the intent the SERP shows, with what you have?

Map the survivors one intent per page, flag any that would cannibalise an existing page, and
hand the territory decision to `seo-identity-positioning`.

**The rejection list is the most valuable part of the output** and the part usually dropped.
It records what was considered and why it was declined, which stops the same unreachable
target being proposed again next quarter.

## The honest negative

"There is no reachable demand here" is a valid finding, and on a new venture it is the
cheapest possible moment to discover it. Deliver it plainly, with the evidence, and with the
narrower opening if one exists. A confident plan aimed at nothing serves nobody.

---

## Reference files
- `seo-identity-positioning/references/serp-competitor-and-keyword-research.md` — SERP analysis, the intent and format table per cluster, clustering with and without data, and a worked example.
- `seo-demand-search-data/references/demand-and-protection.md` — the demand you already touch, and protecting pages that earn.
- `seo-substance-quality/references/search-intent.md` — reading intent off the SERP and the four mismatch patterns.
- `seo-orchestrator/references/data/dataforseo.md` and `ahrefs-semrush.md` — volume, difficulty and striking distance where a paid tool is connected.
- `seo-orchestrator/references/live-data-integrations.md` — detecting what is available, and working without it.
