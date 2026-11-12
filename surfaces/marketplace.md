---
surface: marketplace
title: Marketplaces
verification: moderate
verification_methods: [api_response, feed, serp, served_html]
claimable_outcome: presence_and_parity
weighting: [identity, substance, demand, distribution, access]
---

# Marketplaces

## What this surface is

Amazon, eBay, Etsy, Not On The High Street, Faire, sector-specific B2B marketplaces, and
the integration or app directories that function as marketplaces for software.

Two distinct things are going on, and separating them is the point of this profile:
**ranking inside the marketplace**, which is its own discipline with its own levers, and
**the marketplace as a web and assistant surface**, where listings rank in Google and get
drawn on by answer engines, often above your own site.

The pack's useful contribution is mostly the second, plus the consistency work that spans
both. It does not do marketplace ranking optimisation, and should not pretend to.

## The strategic question that comes first

Before any optimisation, there is a commercial question worth surfacing, because it is
often unexamined: **your marketplace listing may be competing with your own site.**

For a lot of products, the marketplace listing outranks the brand's own product page for
the product's own name. That can be fine, since a sale is a sale, or it can be expensive,
because you pay commission, you do not own the customer relationship, and you cannot change
the page. The right answer is a business decision, and the agent's job is to make the
situation visible rather than to optimise one side blindly.

## What this pack can usefully do

1. **Identity.** One consistent brand entity across the marketplace storefront, your own
   site and your schema: same name, same company, same contact, same imagery. Marketplaces
   are a major source of the third-party signals that answer engines draw on, so
   inconsistency here leaks into assistant eligibility.
2. **Substance, through parity.** Titles, descriptions, specifications, images and
   variants that agree between the marketplace listing, your own product page and your
   JSON-LD. Divergence between the two is both a trust problem and a conversion problem.
3. **Demand.** Marketplace search demand is its own thing, and genuinely useful as
   evidence: what people search on Amazon is often a better signal of commercial intent
   than web volumes. Read it where the environment provides it; never invent it.
4. **Distribution.** Marketplace reviews are earned, never fabricated, never incentivised
   in ways the platform prohibits.
5. **Access**, on your own side: your product pages indexable and strong enough to compete
   with your own listings, honest `Product` and `Offer` markup, and clean canonicals so
   your site is not also competing with itself.

## How to verify

- **The web SERP** for your product names, recording whether your page, a marketplace
  listing, or a competitor ranks. This is the finding that matters most and it takes
  minutes.
- **Sampled prompts** in answer engines for product and comparison questions, recording
  whether marketplace listings are cited rather than your site. They frequently are.
- **Parity checks** between the listing, your page and your markup, on a sample: a simple
  product, a variant, a sale item, an out-of-stock item.
- **Marketplace APIs** for listing status and content, which need the seller's credentials
  and are `needs-human` without them.

## What is unknowable here

- Internal marketplace ranking algorithms, and the effect of any single listing change.
- Buy Box and equivalent allocation logic.
- How much of a marketplace's traffic would have reached your site instead.

## What may never be claimed

No claims about ranking inside a marketplace: that is a separate discipline and not in
scope here.

Never fabricate reviews, ratings or stock, on the marketplace or in your own markup, and
never mark up a marketplace's aggregate rating as if it were your site's own.

What may be claimed is presence and parity, verified: your listings and your own pages
agree on the facts, your brand entity is consistent across both, and you know which of them
currently owns the search result for your product names.

## Honest note on effort

The cheapest valuable work here is a single afternoon of looking: search your own product
names, note what ranks, sample a few answer-engine prompts, and check whether the facts
agree between your listing and your page.

That usually produces one or two findings with real commercial weight, of the kind nobody
had framed before, such as "a reseller's listing outranks you for your own product name,
with the wrong specification on it". Fixing that is worth more than a month of marketplace
listing tweaks, and it is squarely inside what this method can actually do.
