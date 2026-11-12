---
job: new-site
title: I have an idea and I am about to build it
situation: >-
  Nothing is built yet, or the build has just started. There is a domain, or not
  even that. The question is not "why is my site failing" but "is this worth
  building, and how do I build it so it works from the first commit".
roles: [demand-analyst, identity-steward, technical-engineer, content-editor]
data:
  required: []
  helpful: [keyword-demand, serp-data, competitor-data]
guardrails: [established-facts-only, no-fabricated-proof, demand-before-build]
default_autonomy: 4
stop_when: >-
  Demand is read and recorded, the stack decision is made, and the Access rungs
  are satisfied by the build itself rather than retrofitted.
done_when: >-
  The first deploy serves real content in the HTML, carries a resolvable entity,
  and targets demand that was observed rather than assumed. A baseline exists in
  `.seo/` so run two has something to compare against.
---

# New site

This is the only job where you can get it all right the first time, and the only one
where the highest-value work happens **before any code exists**. Autonomy is set high
because there is nothing live to break: no rankings to lose, no directives that might be
load-bearing, no traffic to regress. Use that freedom on the decisions that are
expensive to reverse later.

The most common way this job goes wrong is building first and asking about demand
afterwards. A beautifully engineered site aimed at a query nobody types is the most
expensive possible outcome, because every other system was executed perfectly in the
wrong direction. Read Demand first. It costs a day and it decides whether the rest is
worth doing.

## Order of work

### 1. Read the demand, before the build
`demand/query-demand`, `demand/prompt-demand`, `demand/competitor-holding`,
`demand/worth-having`.

Establish what people actually ask, in what volume, with what intent mix, and **who
already holds it**. The output is not a keyword list, it is a judgement: is there demand
here, can this project realistically take any of it, and which part.

Be willing to return a negative. "The three queries you are aiming at are held by sites
with a decade of authority, and the realistic opening is this narrower one" is the most
valuable finding this job can produce, and the cheapest moment to produce it.

Record every number with its source. An invented search volume is worse than no number,
because someone will build a business on it.

### 2. Decide the stack with rendering in mind
`access/rendering`, `access/javascript-hydration`.

The single decision that causes most of the failures this pack exists to fix is choosing
a client-rendered framework for content that needs to be crawled. Make it deliberately
now, in writing, rather than discovering it after launch.

The rule is simple and worth stating to the builder: **anything you want found must be
in the served HTML.** An app behind a login can be a client-rendered SPA. The marketing
pages, the content, the product pages cannot.

### 3. Establish identity before writing a word
`identity/context`, `identity/entity-graph`.

Who is this, provably? What can be claimed? What proof exists? Write `.seo/context.md`
with every fact labelled `established`, `inferred` or `unknown` before any copy gets
drafted, because copy written without it will contain claims nobody can stand behind,
and those are the hardest things to walk back once published.

On a brand-new venture most facts are legitimately `unknown`. That is fine and it is the
point: it tells the builder what they still have to decide, and it stops the agent
inventing an answer.

### 4. Build the Access rungs in, do not retrofit them
`access/reach`, `access/markup`, `access/architecture`, `access/canonicalisation`.

In a new build these are nearly free, and each becomes expensive later:
- Clean, stable URLs chosen once, because changing them later is a `migrate` job.
- One canonical per page, self-referential, from the first template.
- Real titles and descriptions as a template concern, not a per-page afterthought.
- Honest schema for the entity types that genuinely apply.
- A sitemap generated from the router, so it cannot drift.

### 5. Write substance against observed demand
`substance/intent-match`, `substance/depth`.

Each planned page answers an intent that step 1 actually observed. Pages that exist for
navigation are fine; pages that exist to target a query nobody searches are not.

### 6. Instrument before launch, not after
`operations/measurement`, `operations/baseline`.

Analytics, Search Console and web-vitals wired up **before** the first deploy, so the
baseline starts at zero rather than at "whenever we got round to it". A site that
launched without measurement has permanently lost its before.

## The specific situations this job covers

- **Validating an idea.** Steps 1 and 3 are the whole job. Do not build yet. The
  deliverable is a go, a no, or a narrower go, with the evidence behind it.
- **An exact-match domain launch.** The domain itself does nothing; Google has not
  rewarded exact-match domains for over a decade. What matters is whether the demand is
  real and whether there is any substance behind the name. If the plan is a thin site
  trading on the domain, say so: that is the doorway pattern the quality systems catch.
- **Rank-and-rent.** Treat it as a `local-business` profile with no `established` facts
  yet. Everything hinges on whether a real business will stand behind the entity. Do not
  invent an address, a phone number, hours, reviews or a trading name to make a site look
  established. That is fabricated identity and it is refused here, whatever the
  commercial plan.
- **A SaaS marketing site.** Apply the `saas-marketing` profile from step 2 onward, and
  keep the marketing routes server-rendered even though the product is an app.

## What this job must never do

- Produce a demand number it cannot source. Every volume, difficulty and trend figure
  carries its origin, or it does not get written down.
- Draft copy or schema before `.seo/context.md` exists. Without it, there is nothing to
  distinguish a claim the business can make from one the agent made up.
- Generate pages at scale. That is the `scale` job, and it has a quality gate for a
  reason. A new site with four hundred generated pages and no authority is a
  thin-content problem that starts on day one.
- Promise a ranking timeline. A new domain competing in an established market is a
  question of months and authority, and nothing in a build changes that.

## Output

A short pre-build brief: the demand that was observed with its sources, the realistic
opening, the stack decision and why, the entity to establish, and the page set worth
building. Then, once built, a `.seo/` baseline from the first deploy.

If the honest answer at step 1 is that the idea has no reachable demand, the output is
that, said plainly and early. Nobody is served by a confident plan aimed at nothing.
