# Content decay: when a page that ranked stops ranking

Read this when traffic to a specific page has declined gradually, nothing is broken, and no
obvious competitor has outdone it. Decay is the slow, undramatic loss that accounts for a large
share of traffic decline on established sites, and it is routinely misdiagnosed, usually as a
technical fault and occasionally as an algorithm penalty.

Decay is not a failure of the page. It is the world moving while the page stayed still.

---

## Tell decay apart from the things it resembles

Diagnose this before acting, because the four causes have four different fixes and the symptoms
overlap.

| Pattern | Shape of the decline | Likely cause | Where to go |
|---|---|---|---|
| Cliff on one date | Vertical drop, single day | A deploy, a directive, a manual action | `jobs/rescue.md`, Access first |
| Gradual slope, same intent | Months, steady | **Decay.** This file | Below |
| Gradual slope, SERP shape changed | Months, and the results are a different *type* now | Intent shift | `references/search-intent.md` |
| Impressions holding, clicks falling | Position roughly stable | A SERP-feature change: a generated answer, more ads, a competitor's richer result | Title and snippet work, and `surfaces/google-ai-mode.md` |

That last row is worth dwelling on, because it is increasingly common and gets reported as
decay. If impressions are flat and clicks are down, the page did not lose ranking. The result
page changed around it, and no amount of content work on the page will recover the click.

**Telling rows two and three apart needs evidence, not memory.** Snapshot the type of every
element in the SERP for the keyword, then re-run it monthly and diff the mix. A stable mix
with you falling is decay; a changed mix is an intent shift, and an `ai_overview` appearing
where there was none explains falling clicks on flat impressions. Where the environment has
DataForSEO, workflow 3 in
[`seo-orchestrator/references/data/dataforseo.md`](../../seo-orchestrator/references/data/dataforseo.md)
is the mechanism.

---

## The four things that actually decay

### 1. Facts went out of date
The page says something that was true and is not. Prices, versions, statistics, legal
requirements, names of products, names of people. The most common and most fixable.

This is also a trust problem rather than only a ranking one, and for a shop it is a feed
mismatch that costs listings.

### 2. Competitors improved
Your page is as good as it was; the results above it are better than they were. The honest
assessment is a fresh information-gain pass against the current results, not against the
results you were beating two years ago. See `references/information-gain.md`.

### 3. The topic got deeper
The field itself moved: new approaches, new tools, new regulations. A page that covered the
subject completely in 2024 is now partial, through no fault of its own.

### 4. The page lost its support
Internal links were removed in a redesign, the hub that pointed at it was deleted, or the
cluster around it was pruned. This one is Access, not Substance, and it is easy to miss because
the page itself is untouched. Check the internal link graph before rewriting anything.

---

## Honest freshness: the rule that cannot bend

**Updating the date is not updating the page.** Re-dating unchanged content reads as fresh for a
week and as dishonest permanently, engines increasingly detect the pattern, and the whole method
refuses it.

So:

- If the content genuinely changed, let `dateModified` reflect that truthfully, and say what
  changed. A visible "updated: what changed" note is better for the reader than a bare date.
- If the content did not change, leave the date alone.
- Never add a year to a title to simulate currency when the content is not current. If the title
  says 2026, the content answers 2026's version of the question.
- A request to bump dates in bulk is refused, and the finding records that it was requested.

This is one of the hard lines. There is no autonomy rung and no customer instruction that
licenses it.

---

## What to do with a decaying page

In order, because the cheapest options come first:

1. **Correct what is factually out of date.** Often the whole fix, and it is fast. Only
   `established` facts, from a real source.
2. **Re-run information gain against the current results.** If the gap is closeable with
   material the business has, close it. If it is not, do not write around the absence.
3. **Check its internal support** and restore the links and hub placement it lost.
4. **Consider consolidation.** A decayed page overlapping a stronger one is often better merged
   into it with a `301` than maintained separately. This is a protected-page decision and needs
   approval.
5. **Consider letting it go.** A page addressing demand that no longer exists, or a topic the
   business no longer serves, can be retired. An honest `410`, or a redirect to a genuinely
   relevant successor, beats maintaining it. Never redirect it to the homepage.

Decide which of the five, and say why. Updating everything on a schedule is not a strategy: it
spends the most effort on the pages that happen to be oldest rather than the ones where the gap
is closeable.

---

## Catching it earlier

Decay is cheaper to fix early and it is detectable before it hurts, which makes it a
`maintain` job concern rather than a `rescue` one:

- Watch per-page impressions and position trends, not sitewide traffic. Sitewide numbers hide
  decay completely, because growth elsewhere masks it.
- Put a `stale_after` date on the context facts a page depends on, so the page's assertions
  expire explicitly rather than silently.
- Review cornerstone pages on a real cycle, with the review being an information-gain pass
  against the current results rather than a glance at the date.
