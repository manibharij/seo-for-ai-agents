---
surface: app-store
title: App stores
verification: moderate
verification_methods: [api_response, serp, served_html]
claimable_outcome: presence_and_web_eligibility
weighting: [identity, substance, demand, distribution, access]
---

# App stores

## What this surface is

The App Store and Google Play, plus the web-indexable parts around them: your app's
listing pages as crawled by search engines, and your own site's app landing pages.

**This profile is deliberately narrow, and the boundary is the most useful thing in it.**
App Store Optimisation is a separate discipline with its own tooling, its own ranking
factors, and its own practitioners. This pack does not pretend to cover it. What it covers
is presence: the overlap between an app and the web surfaces this method does understand.

An agent working in a repository can genuinely help with the web half and the metadata
half. It cannot do ASO, and should say so rather than producing a shallow version of it.

## What this pack can usefully do

1. **Identity.** One consistent entity across the app listing, the website and the
   developer account: the same name, the same brand, the same support URL, the same
   company. Inconsistency here is common and it fragments everything.
2. **Substance, in the metadata.** Title, subtitle, description and keyword fields that
   describe the app accurately and in the language users actually use. This is adjacent to
   ASO rather than ASO proper, and it is where honest intent-matching transfers.
3. **Demand.** App store search demand differs from web demand, and reading it needs a
   store-specific data source. The pack can read whatever the environment provides and
   will not invent volumes for a store it cannot query.
4. **Distribution.** Reviews and ratings, earned, and never fabricated. Incentivised or
   fake reviews breach both stores' policies and risk removal.
5. **Access**, on the web side, which is the part that is fully in scope:
   - A real, indexable app landing page on your own domain, not just a store link. This
     ranks for your app's name and you control it.
   - `SoftwareApplication` schema with honest values, including the real rating only where
     it is genuinely published.
   - Deep links and universal links configured correctly, so content inside the app is
     addressable.
   - Where there is a web equivalent of app content, making that indexable, since the
     store listing is not a substitute for a crawlable site.

## How to verify

- **Served HTML** for the app landing page, its schema and its deep-link configuration
  files, which are a frequent silent failure.
- **Store APIs or Connect/Play Console** for listing status and metadata, which need the
  owner's credentials and are therefore `needs-human` without them.
- **The web SERP** for your app's name, to see whether your own page or only the store
  listing ranks.

## What is unknowable here

- Store ranking algorithms, which are opaque and differ between the two stores.
- Install attribution beyond what the consoles report.
- The effect of a metadata change in isolation, since both stores run their own
  experiments.

## What may never be claimed

Do not claim store ranking improvements. That is ASO, this pack does not do it, and
claiming it would be selling a capability that is not here.

Do not fabricate ratings or review counts in `SoftwareApplication` markup. Use the real
published figures or omit the field.

What may be claimed is presence and web eligibility: your app has an indexable landing page
on your own domain with honest schema, your deep links resolve, your entity is consistent
across the store and the site, verified on served output.

## Honest note on effort

The highest-value and most-missed item here is simple: **own an indexable page for your own
app**. A great many apps rely entirely on their store listing, which means a third party
owns the search result for their product name, and they cannot change what it says or
measure who arrives.

Build that page, mark it up honestly, get the deep links right, and keep the entity
consistent. Then, if app installs genuinely matter commercially, hire someone who does ASO.
Recommending that is a better outcome than an agent improvising it.
