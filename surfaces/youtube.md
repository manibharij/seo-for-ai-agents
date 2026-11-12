---
surface: youtube
title: YouTube and video results
verification: strong
verification_methods: [api_response, serp, served_html]
claimable_outcome: measured_position_and_engagement
weighting: [demand, substance, identity, access, distribution]
---

# YouTube and video results

## What this surface is

Two related things, and conflating them causes most of the confusion: **search within
YouTube**, and **video results inside Google Search**. They rank differently and are
verified differently.

YouTube search is its own engine with its own ranking signals, dominated by engagement.
Google's video results can surface a YouTube video or a video hosted on your own site,
and that second path is the one a build can actually influence.

This surface is strongly verifiable: YouTube Studio gives first-party data of a depth no
other surface in this model offers, down to per-second retention.

## What decides whether you rank

1. **Demand.** First, and more decisively than on any other surface. Video demand differs
   sharply from text demand: "how to" and demonstration intent dominate, and a topic with
   strong text demand can have almost no video demand. Reading it wrongly wastes the most
   expensive content type in the model.
2. **Substance.** Here it means the video: does it retain attention, does it deliver what
   the title promised, is it genuinely the best answer in video form. Retention is the
   signal, and no metadata work substitutes for it.
3. **Identity.** The channel is the entity. Consistency, authority within a topic, and a
   real person or brand attached.
4. **Access.** Where the build matters, and only for the Google side: `VideoObject`
   markup with honest values, a video sitemap, a real transcript as text on the page, a
   proper thumbnail, and the video embedded on a page that is itself indexable. A video
   page that renders client-side gives Google nothing.
5. **Distribution.** Embeds, shares and references, earned.

## What a build can and cannot do here

Worth stating early in any engagement, because expectations default wrongly:

**A build can**: make a self-hosted or embedded video eligible in Google's video results
with correct `VideoObject` markup and a video sitemap; put a real transcript in the served
HTML, which makes the page itself rank for the spoken content; set honest `uploadDate`,
`duration` and `thumbnailUrl`; ensure the hosting page is fast and indexable.

**A build cannot**: make a video retain attention, choose a title that earns a click, or
affect YouTube's internal ranking, which is driven by engagement a repository does not
contain. Nothing in a codebase moves YouTube search.

So an agent's honest contribution here is the Access and markup half, plus advice. The
video itself is a production question.

## How to verify

- **YouTube Studio** for impressions, click-through rate, average view duration, retention
  curves and traffic sources. First-party and extremely detailed.
- **The YouTube Data API** for programmatic metadata checks across a library.
- **Search Console** for video impressions and clicks from Google Search, and the video
  indexing report, which states whether Google found and indexed the video on your page
  and why not where it failed.
- **Served HTML** for `VideoObject` markup, the transcript as real text, and the video
  sitemap.

## What is unknowable here

- YouTube's ranking weights, and why a video is or is not recommended.
- Recommendation-driven views as a function of anything you control. Recommendations
  dominate views on YouTube and are opaque.
- Whether Google will choose your self-hosted video over a YouTube video for a query.

## What may never be claimed

Position and engagement may be claimed as measured, because they genuinely are: this video
ranks here for this query, retention is this, click-through is this, on this date.

Never fabricate `VideoObject` values to gain eligibility: an invented `duration`,
`uploadDate` or `thumbnailUrl`, or markup for a video that is not actually on the page, is
the same dishonest-markup problem as a fake review. Never claim a build change will
improve YouTube search ranking.

## Honest note on effort

For most sites the whole worthwhile job here is small and well defined: if you already
have videos, mark them up honestly, add the transcript as text, add them to a video
sitemap, and make sure the hosting pages are indexable. That is cheap and it makes
existing assets eligible on a surface they were invisible on.

Commissioning video **for** SEO is a different and much larger decision, and it should be
made on video demand evidence rather than on the observation that competitors have
videos.
