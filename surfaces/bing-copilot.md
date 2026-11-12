---
surface: bing-copilot
title: Bing and Microsoft Copilot
verification: strong
verification_methods: [served_html, response_headers, serp, api_response, sampled_prompt]
claimable_outcome: measured_position
weighting: [access, substance, identity, distribution, demand]
---

# Bing and Microsoft Copilot

## What this surface is

Bing's web index, and Copilot, which is generated on top of it. Treating them as one
surface is deliberate: Copilot's retrieval leans on Bing, so the work that makes you
visible in Bing is the work that makes you available to Copilot. You cannot sensibly
pursue the second while ignoring the first.

Bing is routinely dismissed on share alone, which misses two things. Its tooling is more
generous than Google's in places, and it is the index behind a set of assistant surfaces
that matter more than its search share implies.

## What decides whether you rank

The weighting is close to Google's, with real differences in emphasis:

1. **Access.** The floor, as ever. Bing has historically been less tolerant of heavy
   client-side rendering than Google, so a site that scrapes by in Google can fail here
   outright. It also supports **IndexNow**, which is a genuine advantage: you can push
   URL changes rather than waiting to be crawled.
2. **Substance.** Intent match and depth. Bing is widely observed to weight on-page
   signals and exact-phrase relevance somewhat more literally than Google. Do not turn
   that into keyword stuffing; do make sure the page plainly says what it is about.
3. **Identity.** Clear entity signals and conventional trust markers.
4. **Distribution.** Earned links and mentions, on similar principles.
5. **Demand.** Worth checking separately rather than assuming Google's demand transfers.
   The audience skews differently by device, geography and sector, and in some B2B and
   desktop-heavy markets the difference is material.

## How to verify

- **Bing Webmaster Tools** for index coverage, crawl information, backlinks and query
  data. It surfaces some things Google's equivalent does not, including a more usable
  backlink view, and it is free.
- **IndexNow** to submit new and changed URLs. Verify submissions were accepted, and treat
  it as a Reach-rung capability on this surface.
- **Served output as BingBot**, checking particularly that content survives without
  JavaScript.
- **Sampled prompts in Copilot**, recorded the same way as any assistant surface: prompt,
  date, whether named, sources cited. Copilot shows citations, which makes the sample
  more informative than an opaque engine's.

## What is unknowable here

- How much of Copilot's retrieval is Bing's index versus other sources, and how the
  generated layer weights them.
- The relative weighting of Bing's own ranking signals.
- Whether Copilot's behaviour will track Bing's index as the products diverge.

## What may never be claimed

Position in Bing is measurable and may be reported as measured, dated, with its source.
Copilot inclusion is sampled and carries the same ceiling as every assistant surface:
**eligibility**, never a guaranteed mention.

Do not claim that work done for Google automatically delivers Bing, or the reverse. They
overlap heavily and differ specifically, and the differences are cheap to check.

## Honest note on effort

The honest position for most projects: do the work for Google, then spend an hour on the
Bing-specific items, because they are cheap and a few of them are free wins.

That hour is: verify the site in Bing Webmaster Tools, wire up IndexNow, confirm the
content renders without JavaScript for BingBot, and check nothing in your CDN or bot
policy is blocking it. That is nearly the whole opportunity for a typical site, and it is
also the groundwork for Copilot. Deeper Bing-specific optimisation is worth it only where
the data shows your audience is genuinely there.
