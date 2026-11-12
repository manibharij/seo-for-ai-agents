---
surface: google-shopping
title: Google Shopping and product surfaces
verification: strong_on_feed_moderate_on_placement
verification_methods: [api_response, feed, served_html, serp]
claimable_outcome: measured_feed_health
weighting: [identity, access, substance, demand, distribution]
---

# Google Shopping and product surfaces

## What this surface is

Product results: the Shopping tab, product panels, and free listings in Search. The
distinctive feature is that **you submit the data**. Elsewhere Google infers what your
page is about; here you declare it in a feed, Google crawls the landing page, and
compares the two.

That gives the surface an unusual verification profile. Feed health is strongly
verifiable, because Merchant Center tells you item by item what was accepted and why
something was disapproved. Placement is only moderately verifiable, because that is a
ranking question like any other.

## What decides whether your products appear

1. **Identity.** First, because this surface is built on identifiers. GTIN, MPN, brand,
   and a consistent product identity across feed, page and markup. A product the system
   cannot resolve to a known item competes poorly or not at all, and the merchant account
   itself is an identity that can be suspended.
2. **Access.** The landing page must be crawlable and must serve the price and
   availability in the HTML. The single most common disapproval is a mismatch caused by a
   price that only appears after JavaScript runs.
3. **Substance.** Titles and descriptions that describe the actual product specifically,
   complete attributes (size, colour, material, condition), and real images. Thin or
   boilerplate product data underperforms here in a directly measurable way.
4. **Demand.** Product and comparison demand, with seasonality that moves sharply.
5. **Distribution.** Reviews and third-party presence, earned.

## Parity is the whole discipline

The recurring failure on this surface has one shape: the feed, the visible page and the
JSON-LD disagree. Google crawls the landing page and compares, and a mismatch gets the
item disapproved with "Mismatched value (page crawl)".

Check parity on a deliberate sample, not at random: a simple product, a variant, a sale
item, and an out-of-stock item. Those four catch nearly everything.

- **Price and currency** identical in all three, for every variant, during and after a
  sale. Sales are when this breaks.
- **Availability** identical in all three. A cached page still saying "in stock" after the
  feed says otherwise is a mismatch.
- **Identifiers** matching: the feed's `id`, `gtin` and `mpn` against the markup's `sku`
  and GTIN for that variant.
- **Links** opening that exact variant, preselected, with its own price and stock in the
  served HTML.
- **Shipping and returns** set in Merchant Center take precedence over markup, so the
  markup should agree rather than compete.

Fix parity **at the data source**. Patching the markup to match the feed leaves the
underlying divergence in place, and it will drift again on the next price change.

## How to verify

- **Merchant Center diagnostics**: item-level approval status and disapproval reasons.
  This is first-party and authoritative, and it requires the owner's access. Without it,
  the feed comparison is recorded as `needs-human`.
- **A served fetch of the landing page** for price, availability and identifiers in the
  raw HTML.
- **Rich Results Test or Schema validation** for the `Product` and `Offer` markup.
- **The Shopping results themselves** for placement, which is a sample like any SERP
  check.

## What is unknowable here

- Placement logic, and why one merchant's listing shows above another's.
- The effect of a single attribute improvement in isolation.
- Competitor pricing dynamics driving the comparison, beyond what is publicly visible.

## What may never be claimed

**Feed health may be claimed as measured**: this many items approved, these disapprovals
resolved, parity verified on this sample on this date. That is real and checkable, and it
is the most useful thing this surface produces.

Placement may not be guaranteed. And never fabricate an identifier, a rating, a review or
a stock level to get an item approved. An invented GTIN is a data-quality violation that
risks the whole account, not just the item.

## Honest note on effort

The return here is unusually legible: a disapproved item earns nothing, an approved item
can, and the gap between them is often one wrong field. For a shop with disapprovals,
this is frequently the highest-return work available anywhere in the model, and it is
mechanical rather than strategic.

Start by reading the diagnostics and fixing the disapprovals at source. Only then worry
about optimising titles and attributes for placement.
