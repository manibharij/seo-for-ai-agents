---
surface: google-news-discover
title: Google News, Top Stories and Discover
verification: weak
verification_methods: [search_console_api, serp, served_html]
claimable_outcome: eligibility
weighting: [identity, substance, access, demand, distribution]
---

# Google News, Top Stories and Discover

## What this surface is

Three related placements with one thing in common: **you cannot make them happen**. Top
Stories in Search, the Google News product, and Discover, which is a feed with no query at
all.

Discover is the strangest surface in this model. There is no search behind it, so there is
no query to target, no position to hold, and no intent to match. Google decides to show
something to someone based on inferred interest. Traffic can arrive in enormous volume and
vanish just as fast, with no diagnosable cause.

Policy gating matters more here than anywhere else. These placements have eligibility
requirements and content policies, and failing one removes you entirely rather than moving
you down.

## What decides whether you appear

1. **Identity.** First and decisive. Real credentialled journalists with resolvable
   `Person` entities, a publisher `Organization` with a logo, a visible corrections policy,
   editorial standards and ownership pages. For news this is not a trust garnish, it is the
   eligibility gate.
2. **Substance.** Original reporting, accurate sourcing, headlines that match the story.
   Clickbait that mismatches the article is specifically penalised in Discover.
3. **Access.** Speed is the Access concern that dominates: a story crawled late is a story
   wasted. Fresh sitemaps plus a Google News sitemap for recent articles, article bodies in
   the served HTML, honest `NewsArticle` markup with true timestamps, and large, high-quality
   images, which Discover requires to present an article at all.
4. **Demand.** Spiky and short-lived. The useful judgement is which stories this title can
   credibly own in the next few hours, not a keyword plan.
5. **Distribution.** Being cited by other outlets, which builds the standing these
   placements draw on.

## How to verify

Weakly, and the gaps are structural:

- **Search Console's Discover report**, which exists only once you have enough Discover
  traffic to qualify for it. No report does not mean no eligibility, it means not enough
  volume yet. There is a separate Google News report on the same basis.
- **Served output** for the checkable half: `NewsArticle` markup, timestamp honesty,
  article body present without JavaScript, image dimensions, news sitemap freshness.
- **The SERP** for whether Top Stories appears for a query at all, which is volatile.
- **Publisher Center** for Google News inclusion status, which needs the owner's access.

Everything on the site side is strongly verifiable. Everything on the placement side is
not, and the report should separate the two rather than averaging them.

## What is unknowable here

- Why Discover showed or stopped showing an article. This is the least explicable traffic
  in search, and large swings routinely have no findable cause.
- Who Discover showed it to, beyond aggregate country data.
- Whether an editorial or policy decision was applied to your site.
- Top Stories inclusion logic, and why a competitor was carried and you were not.

## What may never be claimed

**Nothing but eligibility, and say so before the engagement starts.** Top Stories, Google
News and Discover inclusion are Google's editorial and algorithmic decisions. Done right
you are eligible; nothing makes you guaranteed.

Never forecast Discover traffic. It is the most volatile traffic source most publishers
have, and a forecast built on last month's figures will be wrong in both directions.

Never bump a date to simulate freshness. Date-bumping without a real update is dishonest
markup, engines increasingly detect it, and on this surface trust is the eligibility gate
itself.

## Honest note on effort

The work splits cleanly, and the split is the useful thing to tell a publisher.

The site-side work is real, bounded and verifiable: news sitemap, honest `NewsArticle`
markup, server-rendered article bodies, large images, visible bylines, a corrections policy
and standards pages, and credentialled author entities. Do all of it, and you can prove you
did.

The placement is then out of your hands. A publisher who understands that distinction will
value the first half properly. One who was promised Discover traffic will consider the same
work a failure, which is why the expectation has to be set in writing on day one.
