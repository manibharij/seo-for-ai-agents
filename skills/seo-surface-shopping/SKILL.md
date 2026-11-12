---
name: seo-surface-shopping
description: >-
  Product feeds and shopping surfaces: Merchant Center, free product listings,
  feed-to-page parity, disapprovals, identifiers and variant URLs. Use on any
  "Merchant Center", "product feed", "shopping", "my products are disapproved",
  "mismatched value", "price mismatch", "GTIN", "free listings", "product
  listings", or "my products don't show in Google Shopping" request. Fixes the
  data at source so the feed, the visible page and the markup agree.
---

# Shopping — the feed, the page and the markup must agree

Most shops send Google the same facts twice: once in a Merchant Center feed and once on the
product page, visibly and in JSON-LD. Google crawls the landing page and compares. **Nearly
every problem on this surface is a disagreement between those copies.**

That makes this skill unusual in the pack: the diagnosis is a diff, and the fix is almost
always at the data source rather than in the markup. Patching the JSON-LD to match the feed
leaves the underlying divergence in place, and it drifts again on the next price change.

Scope: **free product listings and the organic shopping surface.** Paid Shopping campaign
management is a different discipline and is not covered here, though the feed quality work
below serves both.

Depth lives in `seo-orchestrator/references/profiles/ecommerce.md` (feed parity, variant
URLs, out-of-stock handling) and `surfaces/google-shopping.md` (weighting and verification).

Work the four steps: **Diagnose → Fix → Verify (on served output) → Report.**

---

## When this fires
- Products disapproved in Merchant Center, or "Mismatched value (page crawl)".
- Products missing from free listings or the Shopping tab.
- Prices or availability shown wrongly, especially during and after a sale.
- Variant handling: colours and sizes competing, or only one variant reachable.
- A new shop setting up a feed for the first time.

## Inputs and modes

Infer these before Step 1. Ask only if a wrong guess would be costly (see `seo-orchestrator/references/operating-modes.md`).
- **Access:** URL only, read-only repo, or write access. Reading the Merchant Center account itself needs the owner's access; without it, record the feed comparison as `needs-human`.
- **Mode:** `audit` (default) never changes the site. `fix` applies approved findings on a branch, verified on the served output. `re-check` re-tests.
- **Scope:** a sample, a category, or the catalogue. On a large catalogue always sample deliberately and say what the sample was.
- **Context:** prices, availability, delivery and returns are `[established]` facts from the business, never inferred.
- **Record findings** with `skill: seo-surface-shopping`, `system: access` for rendering and markup, `system: identity` for identifiers and shop entity.

---

## Step 1 — Diagnose

**Sample deliberately.** Four products catch nearly everything: a simple product, a variant,
a sale item, and one that is out of stock.

For each, compare the three copies:
- **Price and currency** in the feed, in the visible page, and in the JSON-LD `price`. For
  every variant, during and after a sale. Sales are when this breaks.
- **Availability** in all three. A cached page still saying "In stock" after the feed says
  otherwise is a mismatch.
- **Identifiers**: the feed's `id`, `gtin` and `mpn` against the markup's `sku` and GTIN for
  that variant.
- **The link** opens that exact variant, preselected, with its own price and stock **in the
  served HTML**. A price that only appears after JavaScript runs fails, even though shoppers
  see the right number.
- **Shipping and returns** set in Merchant Center or Search Console take precedence over
  markup. The markup should agree rather than compete.

Then the structural checks: one indexable page per variant you want shown, `ProductGroup`
where a single page carries a picker, and no sort or tracking parameters multiplying variant
URLs.

## Step 2 — Fix

- **Fix parity at the data source**, not in the template. If the price comes from one system
  into the page and another into the feed, that is the finding.
- Ensure price and availability render server-side into the HTML.
- Correct `Product` and `Offer` markup to match the visible page exactly, including
  `priceCurrency` and `availability`.
- Set variant URLs deliberately: either one page per variant that self-canonicalises, or one
  page with `ProductGroup` listing each variant's own `offers.url`.
- Apply the out-of-stock policy from the `ecommerce` profile: keep a temporarily unavailable
  product live at `200` with `OutOfStock`, `301` a discontinued one to a genuine equivalent,
  and never bulk-redirect to the homepage.

**Never**: fabricate a GTIN or identifier to get an item approved; mark up a rating or review
that is not real and on the page; state stock or a price the business has not confirmed.

## Step 3 — Verify (on the served output)

- Re-fetch each sampled product page and read the price, availability and identifiers out of
  the raw HTML.
- Validate the structured data and diff every value against the visible page.
- Where the owner has granted access, re-check the item's status in Merchant Center
  diagnostics. That is the authoritative answer and it is first-party.
- Confirm each variant URL loads its own variant with its own price.

## Step 4 — Report

- **Feed health may be claimed as measured**: this many items approved, these disapprovals
  resolved, parity verified on this sample on this date. That is real and checkable, and it
  is usually the highest-return work available on a shop with disapprovals.
- **Placement may not be promised.** Which products appear and where is a ranking question
  like any other.
- Anything needing Merchant Center access that you did not have stays `needs-human`, with
  the exact check to run.

---

## Reference files
- `seo-orchestrator/references/profiles/ecommerce.md` — the depth: feed and page parity in full, variant URL strategies, faceted navigation, and out-of-stock and discontinued handling.
- `surfaces/google-shopping.md` — the weighting (Identity first, on identifiers), what is strongly verifiable (feed) versus moderately (placement), and what may never be claimed.
- `seo-access-understand/references/schema-types-and-jsonld.md` — `Product`, `Offer`, `ProductGroup` and the merchant listing fields.
- `seo-access-understand/references/validation.md` — the parity checklist and validation steps.
