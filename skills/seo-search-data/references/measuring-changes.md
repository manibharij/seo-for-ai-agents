# Measuring changes

How to say whether a logged change helped, without fooling anyone. Search data is noisy; most honest answers are ranges and caveats, and some are "too early" or "inconclusive".

---

## 1. Preconditions

- The change is in `.seo/log.md` with a deploy date, the URLs or template, and a baseline.
- The change is live on the served output (re-fetch a sample).
- Google has recrawled: check `lastCrawlTime` on a few changed URLs with URL Inspection, or Googlebot hits in logs. Before recrawl, nothing can have changed in search.

## 2. Windows

- **Equal length**, whole weeks (judgement: 28 days each side is a sensible default; shorter for big sites, longer for small).
- **Exclude** the deploy day, the recrawl gap if you can see it, and the last 3 days (Search Console data is usually available after 2 to 3 days).
- **Same weekdays** in both windows.
- **Seasonal sites:** also compare each window with the same dates last year. Search Console keeps 16 months, so this works for changes up to about four months old.

## 3. Same pages, plus a control

- Measure exactly the changed URLs, aggregated by page (`dimensions: ["page"]` with a page filter, or by date with a page filter for a time series).
- **Control group:** comparable pages or templates that did not change in either window, ideally similar in traffic and intent (other product categories, other blog sections). Pull the same metrics for them.
- **Result = change in treated pages minus change in control.** A 15% rise with a 12% rise in the control is a 3 point effect at most.
- If no control exists (the whole site changed), say so and lean on year-on-year comparison and the time series shape.

## 4. Metrics

- **Clicks** for traffic, **impressions** for visibility, **CTR** for title and snippet changes, **position** only with caution (an average that moves when the query mix changes).
- With business data: sessions, key events and revenue for the same landing pages and windows.
- For Core Web Vitals changes, use the CrUX History API and remember each weekly point is a 28-day window: the full effect shows about four weeks after release.

## 5. Confounders to check every time

- **Google ranking updates** during either window: https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history lists core, spam and other ranking updates with dates (verified 2026-10).
- Other entries in `.seo/log.md` touching the same pages or site-wide templates.
- Seasonality, promotions, PR, outages, migrations.
- Tracking changes (consent banner, GA4 configuration) for analytics metrics.
- Search Console data anomalies Google has announced (Search Console Help, "Data anomalies in Search Console").

## 6. Wording

Write the result with its numbers, windows, control and caveats:

> Clicks to the 40 rewritten product pages: 3,120 to 3,690 (+18%) over 28-day windows (2026-08-04 to 08-31 vs 2026-09-08 to 10-05, GSC). Unchanged categories (control, 55 pages): +6%. Net effect roughly +12 points. The September 2026 spam update rolled out during the after window; treat as indicative and re-check on 2026-11-02.

Rules:
- **Small numbers:** below a few hundred clicks per window, percentages mislead. Report the counts and call it inconclusive.
- **No causal claims** beyond what the control supports.
- **Negative results are results.** Report them, and propose a rollback for pages above the traffic threshold.
- Update the log entry with the measured result and the date measured.
