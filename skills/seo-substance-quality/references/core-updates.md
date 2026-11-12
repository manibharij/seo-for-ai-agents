# Core updates: diagnosis without panic, and what actually recovers

Read this when a site has lost visibility across many pages at once, somebody has said the
words "algorithm update", and the room wants an answer today.

This is the situation where the gap between honest advice and sellable advice is widest.
There is no switch, no penalty to remove, no file to submit, and no consultant with a
back channel. What there is: a diagnosis that can be done properly, and work that is worth
doing whether or not it recovers the traffic.

## First, confirm it is actually an update

Most "we were hit by an update" is not. Run `jobs/rescue.md`'s first step before accepting
the premise, because the alternatives are far more common and far more fixable.

| Shape | What it points at |
|---|---|
| Vertical drop on one date, specific URLs or sections | A deploy, a directive, a redirect, a `noindex`. **Check this first, always** |
| Drop across many pages over several days, site-wide | Plausibly a core update |
| A single section or template falling | A technical fault in that template, not the algorithm |
| Gradual decline over months | Decay or an intent shift, not an update |
| Impressions flat, clicks down | The result page changed shape around you |
| A message in Search Console | A **manual action**, which is a different thing entirely, with a documented process and a reconsideration request |

Then correlate the date against a confirmed update rather than against commentary. Google
publishes its ranking release history; a drop two weeks before an update began is not that
update. If the dates do not line up, the cause is somewhere else and this file is the wrong
one.

**A manual action is not a core update.** It appears in Search Console, it names the problem,
and it has a defined route out. Never conflate them: one has a process, the other does not.

## What Google says, and why that is the useful part

Google's long-standing position on core updates is that there is nothing to fix in the sense
people want. Pages that drop are not being penalised; the system has changed its assessment
of what is most helpful for a query, and others have been assessed as better. Its advice is
to focus on offering the best content you can, which reads as evasive and is, in fact, the
whole mechanism.

The practical translation, and what to tell an owner:

- **There is no recovery lever.** Anyone selling one is selling something else.
- **Recovery, where it happens, usually comes at a later update**, not immediately after
  changes. The assessment is made during an update cycle.
- **Not everything recovers.** Some sites lose a position they held because somebody else
  genuinely deserves it now. That is a strategy question, not a technical one.

Do not forecast a recovery date. There isn't one, and saying so protects the relationship
better than a guess that misses.

## The diagnosis that is worth doing

Resist the urge to change everything at once. A site that makes forty changes after an update
has destroyed its ability to learn anything from the next one.

### 1. Find out what actually moved
Segment the loss before theorising about it: by section or template, by query intent, by page
type, by whether the page has a named author, by age. The shape of the loss is the evidence.
A drop concentrated in thin programmatic pages is a different finding from one concentrated
in commercial comparison content, and they lead to different work.

### 2. Read the pages that lost against the pages that won
The single most useful hour available. Open the queries, read the pages now ranking, and ask
the information-gain question honestly: do they add something your page does not?
(`references/information-gain.md`.) This is uncomfortable and it is where the answer is.

### 3. Check the systems that are not Substance
A core update often surfaces a weakness rather than creating one:

- **Identity.** Anonymous content on topics where the winners have named, credentialled
  authors. This is the most common gap in the sites that lose, and it is Identity work
  (`seo-identity-context`), not writing.
- **Substance at scale.** Large sets of pages generated to a template with little behind
  them. The gate in `seo-substance-at-scale` exists for this.
- **Intent.** Pages serving an intent the SERP no longer has
  (`references/search-intent.md`).
- **Access.** Rarely the cause of a site-wide assessment change, but cheap to rule out and
  embarrassing to miss.

### 4. Decide what the site is actually for
The honest conclusion is sometimes that a section exists to capture search traffic rather
than to serve anyone, and that it will keep losing. Pruning it is a legitimate answer
(`seo-substance-content-audit`), and a hard conversation to have.

## What not to do, and all of these get done

- **Do not mass-edit and re-date.** Date-bumping is refused here as everywhere, and a
  site-wide "refresh" with no substantive change is exactly the pattern that loses.
- **Do not disavow in response.** Core updates are not link penalties, and a defensive
  disavow is a self-inflicted loss. See `seo-distribution-authority`.
- **Do not act on commentary.** The named theories circulating in the days after an update
  are inference from sampled data, not documentation. Treat them as hypotheses to test
  against your own evidence, never as findings.
- **Do not change forty things.** Change what the evidence supports, record the date, and
  keep the ability to attribute the next move.
- **Do not promise recovery.** Not a date, not a percentage, not at all.

## What goes in the report

The shape of the loss with its evidence, the correlation to a confirmed update or the
absence of one, the segments most affected, the honest information-gain comparison against
what now wins, the work that follows from it, and a plain statement that recovery is not
guaranteed and is not scheduled.

Then a note for the next cycle: what was changed and when, so that the following update has
something to measure against. Sites that survive updates well are usually the ones keeping
that record, which makes this an Operations habit as much as a Substance one.
