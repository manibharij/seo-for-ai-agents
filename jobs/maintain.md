---
job: maintain
title: Keep it from breaking
situation: >-
  The site is in good shape and the work now is to keep it that way: catch the
  regression a deploy introduces, notice the fact that went stale, and re-verify
  what was fixed before anyone has to rescue it again.
roles: [technical-engineer, identity-steward, account-reporter]
data:
  required: []
  helpful: [search-console, analytics, server-logs, deploy-history]
guardrails: [do-not-regress, established-facts-only, fenced-autonomy-only]
default_autonomy: 4
stop_when: Every watched finding is re-verified and any regression is open again
done_when: >-
  Each previously verified finding has been re-checked on served output this
  cycle, regressions are reopened with evidence, stale facts are flagged, and
  the report says plainly what changed and what did not.
---

# Maintain

This is the job that makes the whole model worth running, and the one most people skip.
Visibility decays. A fix verified in March is undone by a deploy in April, a price changes,
a member of staff leaves, a plugin update strips a meta tag, a CDN rule starts blocking a
crawler. None of it announces itself.

Autonomy is high here, higher than in `grow` or `rescue`, for a reason worth
understanding: this job is **narrow and repetitive**. It does not decide anything new. It
re-runs known checks against known expectations, and the only actions it takes
unsupervised are the small reversible ones in the `fenceable` list. A job that cannot
surprise you is a job you can let run.

The most common way this job goes wrong is becoming a second audit. An agent that arrives
on a maintenance cycle and starts finding new opportunities has drifted into `grow`, and
the thing it was meant to catch goes unnoticed for another month. Re-verify first. Always.

## Order of work

### 1. Re-verify every previously verified finding
`operations/regression-detection`.

The core of the job. For each finding in `.seo/state.json` with status `verified`, re-run
its `verify.method` against its `verify.expect` on the current served output.

- Still true: record the date and move on.
- No longer true: the finding's status becomes `regression`, with the new evidence
  attached and `regressed_from` pointing at the original. **It reopens itself.** Nobody
  has to notice it.

A regression is more urgent than a new finding of the same severity, because something
that was working is now broken, which means a process allowed it, and the same process
will allow it again.

### 2. Check what the deploys did
`operations/regression-detection`, `access/reach`, `access/markup`.

Correlate regressions against deploy history. The output that actually prevents the next
one is not the fix, it is naming the cause: a template change, a dependency upgrade, a CMS
plugin, a CDN rule, an environment variable that differs in production.

Where a regression came through a repeatable route, propose a CI check for it rather than
only fixing the instance. See `operations/ci-gate`.

### 3. Re-check the directives that can silently de-index
`access/reach`, `access/bot-policy`, `access/canonicalisation`.

A short, fixed list, every cycle, because each of these can remove a site from search
without any visible symptom on the page:
- `robots.txt`, meta robots and `X-Robots-Tag` on the primary templates.
- Canonical targets, especially after any platform or framework upgrade.
- CDN, firewall and bot rules, which change without a deploy.
- Certificate validity and redirect behaviour on both `www` and apex.
- The sitemap: still present, still current, still listing what it should.

### 4. Flag facts that have gone stale
`identity/context`.

Context facts carry a `stale_after` date for exactly this. Prices, opening hours, staff,
credentials, awards and claims decay, and a page asserting last year's price is both a
trust problem and, for a shop, a feed mismatch.

The agent flags these; it does not update them. A new fact needs a source, and the source
is the business.

### 5. Watch the slow-moving signals
`demand/search-data`, `access/page-experience`.

Things that only mean something over time: index coverage trending the wrong way, Core Web
Vitals field data degrading as the page gains third-party scripts, 404s accumulating in
logs, and pages that were earning and quietly stopped.

Report the trend, not the datapoint. One week of movement is noise.

### 6. Report, including when nothing happened
`operations/reporting`.

A maintenance report that says "nine findings re-verified, all still holding, one fact
approaching staleness, no regressions" is a **successful** report and has to be written
with the same care as an eventful one. Silence is indistinguishable from a broken job, so
the cycle always produces a dated summary even when the news is that there is no news.

## What this job must never do

- Skip re-verification to do something more interesting.
- Widen beyond the `fenceable` list unsupervised, however obvious a larger fix looks. An
  unattended cycle is not the moment to exercise judgement.
- Update a stale fact from inference. Flag it and ask.
- Close a regression without served-output evidence that it is fixed.
- Report nothing because nothing happened.

## Output

A dated cycle report: what was re-verified and still holds, what regressed with its
evidence and probable cause, what was fixed within the fence, what is flagged as stale,
what trends are moving, and what needs a human. Appended to `.seo/log.md` so the history
accumulates.

Over enough cycles this history becomes the most valuable thing in `.seo/`, because it is
the only record of what this site's particular failure modes are. A site that breaks its
canonicals on every framework upgrade will do it again, and the log is how anyone knows
to look.
