---
surface: google-web
title: Google web search
verification: strong
verification_methods: [served_html, response_headers, render_trace, serp, api_response, crawl]
claimable_outcome: measured_position
weighting: [access, substance, identity, distribution, demand]
---

# Google web search

## What this surface is

The one surface in this model where an outcome is genuinely observable. There is an index
you can inspect, a position you can measure, a coverage report that tells you why a URL is
not included, and an API that answers questions about your own pages.

That makes it the anchor for everything else. When you want to know whether work is
landing, this is where you can actually find out, and a claim made here can be checked.

## What decides whether you rank

1. **Access.** The floor, and unlike the assistant surfaces it is genuinely first. A page
   that is not reachable, not rendered into the served HTML, or not indexable does not
   compete at all. This is where most AI-built sites fail, and no amount of work above it
   has any effect until it is cleared.
2. **Substance.** Once the page is eligible, whether it deserves to win: intent match,
   depth, information gain against what already ranks. The gap between "indexed" and
   "ranking" is nearly always here.
3. **Identity.** Real experience, expertise and authorship, and an entity the engine can
   resolve. Decisive in YMYL territory and increasingly everywhere.
4. **Distribution.** Earned authority still moves this surface more than any single
   on-page change, and it is the part you cannot execute. Where your pages are as good as
   the ones above you and still lose, this is usually why.
5. **Demand.** Last in the weighting but first in the work: ranking for something nobody
   searches is worth nothing, however well you did it.

## How to verify

The full tool ladder is available here, and the order matters because confidence differs:

- **Search Console URL Inspection** for index status and Google's chosen canonical, which
  is the only place that tells you what Google actually decided rather than what you asked
  for. A declared canonical and the chosen canonical disagreeing is a real finding.
- **Search Console Search Analytics** for impressions, clicks, average position, by query
  and by page. This is sampled and thresholded, but it is first-party.
- **A served fetch** (`curl`, or a fetch tool) for the raw HTML, status and headers.
- **A rendering check** (headless browser or rendering MCP) for what survives JavaScript,
  compared against the raw fetch. The difference between those two is the single most
  valuable diagnostic in this pack.
- **A crawl** for architecture, orphans, depth and internal linking at scale.
- **CrUX and PageSpeed Insights** for field and lab page experience, field first.
- **The SERP itself** for what is actually competing, which shape of result Google has
  chosen for the query, and whether the intent you assumed matches the one Google serves.

Record which of these produced each finding. A finding from URL Inspection is
`established`. A finding from a third-party rank tracker is `inferred`.

## What is unknowable here

- The ranking algorithm's weights, and the relative contribution of any one change.
- Why a specific page sits at a specific position.
- Impressions and clicks below Search Console's privacy threshold, which on a small site
  can be most of them.
- Personalised and localised variation: the position you see is one of many.
- Whether a ranking change was caused by your work, a competitor's, or an algorithm
  update, without a controlled change and a long enough window.

## What may never be claimed

A guaranteed position, a timeline to a position, or a causal claim from correlation alone.
Rankings are an outcome produced by five systems against competitors who are also working,
and no build-time change promises one.

What **may** be claimed, and what makes this surface valuable, is the measured state:
this page is now indexed where it was not; the served HTML now contains the content it did
not; this page moved from position 14 to 6 over this window, measured in Search Console.
Observed and dated, not forecast.

## Honest note on effort

This surface rewards the fundamentals more reliably than any other, and the work is
cumulative rather than fashionable. It is also the surface where this pack's core
discipline pays off most directly: verify on served output, because Google indexes what it
receives, not what your source intends.

If a project has limited budget and is choosing between surfaces, this is the one to spend
it on. It is the largest, the most measurable, and the work transfers: a site that earns
here is also the site an assistant is most likely to be able to resolve and quote.
