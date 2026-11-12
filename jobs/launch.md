---
job: launch
title: We are going live, this week
situation: >-
  The build is finished or nearly finished and a launch date exists. The risk is
  not imperfection, it is shipping something a machine cannot reach, or shipping
  a staging directive into production.
roles: [technical-engineer, account-reporter]
data:
  required: []
  helpful: [search-console, deploy-history]
guardrails: [do-not-regress, established-facts-only, blockers-before-polish]
default_autonomy: 3
stop_when: Every launch blocker is cleared and verified on the production URL
done_when: >-
  The production URL serves real content, is indexable, carries no staging
  directive, and the first-week watch list is recorded in `.seo/`.
---

# Launch

A launch job is triage with a deadline. The work splits hard into two piles, and
conflating them is how launches go wrong: **blockers**, which make the site invisible or
actively harmful if shipped, and **everything else**, which can be fixed next week with
no lasting cost.

The most common way this job goes wrong is polishing. An agent that spends launch day
improving meta descriptions while a `noindex` from the staging environment is still in
the production template has failed completely, however good the descriptions are.

Verify every single check on the **production URL**, not staging, not localhost, not the
preview deployment. The entire category of launch disaster is a difference between
environments.

## Order of work

### 1. Blockers, on the production URL
`operations/launch-qa`, `access/reach`, `access/rendering`.

Nothing else happens until these pass. Each is a single, binary, evidenced check:

- **A staging directive shipped.** `noindex`, `X-Robots-Tag: noindex`, a
  `Disallow: /` in `robots.txt`, or HTTP auth still on the production host. This is the
  single most common launch failure and it makes the site invisible completely.
- **Content is in the served HTML.** Fetch the production URL without JavaScript. If the
  body is an empty root div, the site does not exist to a crawler.
- **The canonical points at production.** A canonical left pointing at the staging host
  or at `localhost` hands the index to a URL nobody can reach.
- **HTTPS resolves and redirects are clean.** One hop, correct host, no chain, no loop.
  Check `www` and non-`www`, and `http` and `https`.
- **The sitemap exists, is reachable, and lists production URLs.** Not staging URLs.
- **Nothing returns a soft 404 or a 500** on the primary routes.
- **Analytics and Search Console are live** on production, so day one is measured.

### 2. Fix-this-week, recorded not rushed
`access/markup`, `access/architecture`, `substance/intent-match`.

Everything that is genuinely worth doing and genuinely survives a week: missing
descriptions, heading structure, internal links, schema, image weight, copy that does not
match intent. Record each as a finding with a severity and leave it in `.seo/`. Do not
hold the launch for any of it, and do not quietly fix a long list on launch day either,
because every unreviewed change on launch day is a change nobody can correlate later.

### 3. Set the first-week watch list
`operations/regression-detection`, `operations/baseline`.

The job does not end at go-live. Record what to watch and when:
- Index coverage in Search Console, checked on days 2, 7 and 14.
- The production URL re-fetched daily for the first week, confirming the blockers stayed
  fixed. Deploys undo launch fixes more often than anyone expects.
- Core Web Vitals field data, which needs real traffic before it says anything.
- 404s appearing in logs, which reveal links the launch broke.

## If this is a relaunch rather than a first launch

A relaunch of an existing site is **not** this job on its own: URL changes make it a
`migrate` job, and that has to run first. Treat the redirect map as a launch blocker in
its own right. The most expensive launch failure available is relaunching a site that
already ranked onto new URLs with no redirects, and it is also one of the most common.

Before go-live on a relaunch, additionally confirm:
- Every old URL with traffic or links resolves, by `301`, to its genuine equivalent.
- The old sitemap's URLs are accounted for, one by one.
- Existing canonicals, `hreflang` clusters and deliberate `noindex` rules survived the
  rebuild. Treat each as intentional until the history proves otherwise.

## What this job must never do

- Approve a launch with an unresolved blocker, however close the deadline. Say what is
  broken and what shipping it costs, and let the human decide.
- Verify on anything but the production URL.
- Apply a large batch of unreviewed changes on launch day.
- Add schema, bylines or trust signals to fill a template. A launch deadline is not a
  reason to assert something unproven; an empty field is better than a fabricated one.
- Treat green lab Core Web Vitals as evidence of real performance. Field data needs
  traffic, and on launch day there is none.

## Output

A go or no-go, with blockers listed individually and each one evidenced on the production
URL. Then the fix-this-week backlog in `.seo/state.json`, and the first-week watch list
with dates. The human-facing version comes from the Account Reporter and says plainly
whether it is safe to launch, in words a founder can act on without knowing what a
canonical is.
