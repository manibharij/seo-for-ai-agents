---
job: scale
title: I need a lot of pages
situation: >-
  Many pages from one template and a dataset: locations, products, routes,
  comparisons, integrations. The question is whether they deserve to exist, and
  the honest answer is often "some of them".
roles: [demand-analyst, content-editor, technical-engineer, account-reporter]
data:
  required: []
  helpful: [keyword-demand, search-console, serp-data]
guardrails: [quality-gate, established-facts-only, no-doorway-pages, crawl-budget-control]
default_autonomy: 2
stop_when: >-
  The quality gate has been applied to the whole set and the subset that passes
  is named, with the rest refused and the reason recorded.
done_when: >-
  Only pages that pass the gate are published and indexable, crawl budget is
  controlled deliberately, and the first cohort is being measured before the
  second is built.
---

# Scale

Pages at scale is the most dangerous capability in this pack, because it is the one where
an agent can do enormous damage quickly while appearing extremely productive. Four hundred
generated pages is a satisfying deliverable and, if they are thin, a sitewide quality
problem that affects the pages that were fine.

So this job is mostly a gate. The work is not "generate the pages", it is **decide which
pages deserve to exist**, and then build only those. An honest run of this job frequently
returns a much smaller number than was asked for, and occasionally returns zero.

The most common way this job goes wrong is starting from the dataset. A list of two
thousand towns, or every possible pair of integrations, is a combinatorial fact about your
data, not evidence of demand. Start from demand and intersect.

## The quality gate

Every page in the set must pass **all** of these before it is built. A page failing any
one of them is refused, and the refusal is recorded with its reason.

1. **Observed demand.** Someone actually searches for this, and it was observed rather
   than assumed from the template's existence. Not every combination has demand, and the
   long tail of a combinatorial set is usually empty.
2. **Substantive difference.** The page differs from its siblings in ways that matter to
   a reader, from real data. Swapping a name into a sentence is not a difference. If the
   only variable content is the title and one noun, the set fails.
3. **Real underlying data.** The facts on the page come from a dataset that is genuinely
   true and current, and are `established` in `.seo/context.md` terms. A generated page
   asserting invented specifics is the worst output available here.
4. **Standalone usefulness.** A visitor landing on it can accomplish something without
   being funnelled to a generic page. Google's doorway-page policy names exactly this
   pattern: pages aimed at many regions or variants that shunt visitors to one place.
5. **A place in the architecture.** Reachable from a browsable hub and from relevant
   sibling pages, not only from a sitemap. A set that exists only in the sitemap is a set
   nobody intended to be found by a human.
6. **It would survive a human reading it.** If showing one of these pages to the business
   owner would embarrass them, it fails. This is a real test and it catches what the
   mechanical ones miss.

## Order of work

### 1. Read demand across the set, not for the set
`demand/query-demand`, `demand/worth-having`.

Sample the intended dimension and find where demand actually lives. The usual shape is
that a small head has real demand, a middle has some, and a vast tail has none. The
output is the subset worth building, with volumes and sources.

### 2. Apply the gate, and report the refusals
`substance/at-scale`, `substance/depth`.

Run all six criteria over the candidate set. Report two numbers: how many passed and how
many were refused, with the refusal reasons grouped. The refusals are the most valuable
part of this output, because they are what stops the damage.

### 3. Build the template so each page earns its difference
`substance/at-scale`, `access/markup`.

The template's job is to present real per-page data prominently, not to pad around a
variable. Where the data is thin for a given page, the template should be able to show
less rather than filling space. Schema is generated from the same data, so it cannot
disagree with the visible page.

### 4. Control crawl budget and indexation deliberately
`access/crawl-budget`, `access/architecture`, `access/canonicalisation`.

At scale this stops being hygiene and becomes the main technical concern: hub pages that
make the set browsable in a sensible depth, a sitemap listing only pages that passed,
`noindex` on anything built for users but not for search, and no parameter or filter
combinations multiplying the set further.

### 5. Ship a cohort, measure it, then decide about the rest
`operations/baseline`, `demand/search-data`.

Publish the first cohort, which is the strongest-demand subset. Wait for real index and
performance data. If the cohort earns, build the next. If it does not get indexed, or
gets indexed and earns nothing, **that is the answer for the whole set** and the cheapest
possible way to have learned it.

Never build the whole set before the first cohort has been measured.

## What this job must never do

- Generate the full set because the dataset contains it.
- Write specifics it cannot source. Invented hours, prices, distances, specifications or
  testimonials are refused, and a template that requires them is the wrong template.
- Create a page per location where the business has no presence or service. That is the
  doorway pattern, and it is refused regardless of commercial intent.
- Fabricate reviews, ratings, authors or local proof to make generated pages look
  established.
- Publish the set and the measurement plan at the same time. Measurement comes first.
- Treat "it is indexed" as success. Indexed and earning nothing is still a cost, because
  it dilutes the crawl and the site's overall quality signal.

## Output

The candidate set with a pass or refuse per page and the reason, the cohort plan, the
template specification including which data fields are required for a page to qualify,
and the crawl-control decisions.

If the gate refuses most of the set, that is the finding. A hundred pages that earn beat
two thousand that dilute, and the owner can make that trade properly only if the refusals
are shown rather than quietly absorbed.
