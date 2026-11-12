---
job: rescue
title: Something is wrong and I do not know why
situation: >-
  The site ranked, or was indexed, and now is not. Traffic dropped, pages
  disappeared, or an engine has stopped returning anything. Cause unknown.
roles: [technical-engineer, account-reporter]
data:
  required: []
  helpful: [search-console, analytics, server-logs, deploy-history]
guardrails: [do-not-regress, no-url-change-without-approval, established-facts-only]
default_autonomy: 2
stop_when: Cause established with evidence, or all five systems cleared
done_when: >-
  The cause is evidenced, the fix is verified on served output, and a regression
  check now covers it so the same failure reopens itself.
---

# Rescue

The most common way this job goes wrong is starting with fixes. A site that has
dropped is a site where **something changed**, and the change is nearly always
findable. Guessing wastes the one advantage you have, which is that a before and an
after both exist.

## Order of work

Diagnose in this order and stop as soon as the cause is established. Do not continue
down the list out of thoroughness, and do not fix anything above the step you are on.

### 1. Establish what changed, and when
`operations/baseline` then `operations/incident-response`.

Before touching the site, pin the shape of the drop. Which URLs, which queries, which
surface, which date, and whether it is gradual or a cliff. A cliff on a single date
points at a deploy, a directive or a manual action. A slope points at competition,
decay or an algorithm update.

Correlate the date against deploy history, Search Console index coverage, and any
redirect or robots change. **This step alone resolves most rescues.**

Evidence required: the drop itself, with dates, and a list of candidate changes in the
same window.

### 2. Access, top to bottom
`access/reach` then `access/rendering` then `access/canonicalisation` then
`access/redirects`.

In that order, because the ladder's dependency still holds inside Access. Check on
served output: status codes, robots directives, the rendered DOM, canonical targets,
redirect chains. A `noindex` shipped by accident and a canonical pointing at the wrong
host are the two most common single causes, and both are invisible in source.

Stop here if found. Do not proceed to content theories while a machine cannot reach
or index the page.

### 3. Identity consistency
`identity/nap-consistency`, `identity/entity-graph`.

Relevant when the drop is local or brand-related rather than page-level. A changed
address, a merged or suspended profile, or a broken entity reference will move local
visibility without touching a single page.

### 4. Substance
`substance/intent-match`, `substance/decay-detection`.

Only once Access is clean. A page that lost ranking while remaining reachable has
usually either stopped matching the intent (the SERP changed shape) or decayed while
competitors improved. Say which, with the SERP as evidence.

### 5. Distribution, last and advisory
`distribution/backlink-audit`.

Lost links are a real cause and the slowest to act on. Report it, advise on reclamation,
execute nothing.

## What this job must never do

- Change URLs, canonicals, robots directives or redirects without approval. On a site
  that is already damaged, a confident wrong fix is worse than the original fault.
- Treat an existing directive as a mistake. Assume it was intentional until the history
  says otherwise.
- Report a cause as established on the strength of correlation alone. If the evidence is
  circumstantial, the finding's confidence is `inferred` and it is labelled as such.

## Output

A single finding at `critical` or `high` carrying the cause, its evidence and its fix,
plus the cleared systems recorded as checked so nobody repeats the work. Then a
regression check added to `operations/regression-detection` so this specific failure
reopens itself if it recurs.

If every system is clear and the drop is real, say so plainly: the honest answer is
sometimes that the market moved, and that is a `grow` job, not a rescue.
