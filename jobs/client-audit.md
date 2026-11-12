---
job: client-audit
title: I need to audit a site I do not control
situation: >-
  An agency, consultant or freelancer auditing someone else's site: a pitch, a
  new engagement, a second opinion, or due diligence before an acquisition. No
  repository access, often no analytics access, and a deliverable someone pays
  for.
roles: [technical-engineer, demand-analyst, identity-steward, distribution-strategist, account-reporter]
data:
  required: []
  helpful: [search-console, analytics, serp-data, backlink-data, keyword-demand]
guardrails: [read-only, established-facts-only, no-unauthorised-access, state-what-is-unknown]
default_autonomy: 1
stop_when: >-
  Every system has been assessed from publicly observable evidence, and what
  could not be determined without access is listed as such.
done_when: >-
  A prioritised, evidenced report exists that a non-specialist can act on, with
  every finding sourced to something observable and every gap stated plainly.
---

# Client audit

This job is unusual in two ways: autonomy is **rung 1, observe only**, because you have no
mandate to change anything, and the deliverable is the product. Elsewhere the report
describes the work; here the report *is* the work, and someone is paying for it.

That changes the standard. An internal finding can be terse. A finding in a client audit
has to survive being read by a sceptical developer who built the thing, and by a
non-technical decision-maker who is choosing whether to hire you. Both will test it.

The most common way this job goes wrong is volume. A 90-page audit listing every
imperfection a crawler can find is easy to generate and nearly useless: it buries the two
things that matter, it cannot be actioned, and it signals a tool rather than judgement.
Find the constraint, prove it, and rank everything else beneath it.

## Order of work

### 1. Work out what you can actually see
URL-only mode is the default here. Establish what evidence is available before promising
any conclusion: the served HTML and headers, the rendered DOM, `robots.txt`, sitemaps, a
crawl, public SERPs, third-party backlink data if you have a subscription, and whatever
the client has granted.

Write down what you do **not** have. An audit that silently guesses at the things only
Search Console could tell you is worth less than one that names them, because the client
can then grant access and get the real answer.

### 2. Assess all five systems, briefly, before going deep
`access/reach`, `substance/intent-match`, `identity/entity-graph`,
`demand/gap-analysis`, `distribution/authority-gap`.

A quick pass across everything first, specifically so you do not spend the whole budget in
the system you find most interesting. The output of this pass is a single judgement: where
is the constraint? Then go deep there.

### 3. Prove the constraint on served output
Whatever you found, evidence it the way the client's own developer would have to accept:
the actual request, the actual response, the specific line. Screenshots of a third-party
tool's score are not evidence. A `curl` of their page that contains no content is.

This is also what separates a credible audit from a generated one, and the client can tell.

### 4. Size it honestly
`operations/reporting`, `operations/prioritisation`.

For each finding: the impact if fixed, the effort, the risk of fixing it, and the
confidence. Use the `established` / `inferred` / `unknown` vocabulary and show it. A
finding marked `inferred` that turns out to be right builds more trust than one asserted
as fact that turns out to be wrong.

### 5. Write it for the person signing it off
`operations/reporting`.

Two layers, in this order: what to do and why it matters, in plain language, up front;
then the technical detail and evidence behind each item, for whoever implements it. Never
the reverse, and never only one of them.

## Scope boundaries to state in the document

Say these before the findings, not in a footnote:

- **No access, no change.** This is an assessment. Nothing was modified, and the
  recommendations are proposals requiring the owner's approval.
- **What live data would sharpen.** Index coverage reasons, which pages actually earn,
  real Core Web Vitals field data, and whether a change worked. All need the owner's
  Search Console and analytics, and the audit says which conclusions would firm up.
- **Rankings and citations are outcomes, not deliverables.** They depend on competition
  and earned authority, and an audit does not move them by itself.
- **Earned media is advisory.** The authority gap can be analysed and strategised. It
  cannot be executed here, and anyone offering to buy it is selling a risk.
- **Sampling on large sites.** If the site is too large to crawl fully, state the sample
  size and how it was chosen, so a finding about "the product templates" is understood as
  being about the templates you actually looked at.

## What this job must never do

- Attempt access it was not granted: no logging in, no guessing at staging URLs, no
  probing admin paths, no scraping behind a paywall or a login. Read what is public.
- Crawl aggressively. Rate-limit, respect `robots.txt`, and do not cost the client's host
  money to produce a report they did not commission.
- Present a tool's number as a finding. "Their score is 54" is not a diagnosis.
- Pad the report. Severity has to mean something, and a long list of `low` findings next to
  one `critical` finding trains the reader to ignore both.
- Assume a directive is a mistake. A `noindex`, a canonical or a blocked path may be
  deliberate and commercially load-bearing. Flag it as a question, not an error.
- Imply the previous agency was incompetent. Describe the state of the site, not the
  character of whoever built it. It is also frequently the same people you will have to
  work with.

## Output

A prioritised report: the constraint first with its evidence, then findings by system with
impact, effort, risk and confidence, then the explicit list of what could not be determined
without access and what each would tell you.

Where the engagement continues, this becomes the baseline in `.seo/` and the job changes to
`rescue`, `grow` or `maintain` depending on what the audit found.
