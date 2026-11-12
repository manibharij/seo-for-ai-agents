# Profile: affiliate and comparison

Use for sites that review, compare or recommend things they do not sell: "best X" roundups,
versus pages, deal sites, buyer's guides, price comparison, and content monetised by referral.
Combine with `content-blog` for the content fundamentals.

This profile exists because the modality has a structural honesty problem that no other one has,
and pretending otherwise is how these sites get flattened. You are recommending products, you
are paid by the outcome, and in most cases you have not used them. Each of those is manageable.
Together they describe exactly the pattern Google's reviews guidance and its helpful-content
systems were built to demote.

So the leading question is not "how do we rank this". It is **"what do we have that the
manufacturer's page and the ten other roundups do not"**, and if the honest answer is nothing,
the page should not exist.

## How the five systems shift

- **Demand** (observed). Commercial-investigation demand, which is lucrative and therefore the
  most contested territory on the web. The useful judgement is which of it is reachable: "best
  CRM" is held by sites with a decade of authority, while a specific, narrow, well-served
  comparison may be genuinely open. Read it honestly and say which.
- **Identity** (built). **The constraint on this profile.** Who is recommending, why they are
  qualified to, and how they tested. A named reviewer with relevant experience, a published
  methodology, and clear disclosure of the commercial relationship. An anonymous roundup with
  affiliate links is the exact shape of the thing quality systems demote, and no amount of
  Access work rescues it.
- **Substance** (built). First-hand evidence, or an honest statement of its absence. Original
  photographs, measurements, test results, screenshots from actual use, the thing that went
  wrong. Where you genuinely have not used a product, say so and say what the assessment is
  based on instead. A page that reads as if it tested things it did not has lied, and that is
  the failure mode here.
- **Access** (built). The Visibility Ladder, in dependency order.
  1. **Reach.** Standard checks. Watch comparison tables and filters rendered client-side, which
     hide the substance of the page, and faceted comparison URLs multiplying.
  2. **Read.** The verdict and the key differences present in the served HTML, not inside a
     JavaScript widget. Prices and availability, where shown, either current or clearly dated.
  3. **Understand.** `Review` or `ItemList` only where the review is genuinely yours, with a real
     `author`. Never `AggregateRating` aggregating other people's ratings as though they were
     yours. `Product` markup on a product you do not sell is a misrepresentation.
  4. **Connect.** A coherent structure: category hubs, individual reviews linked from the
     roundups and back, and no near-duplicate roundups competing for one intent.
- **Distribution** (earned, advisory). The hardest system on this profile, because the thing you
  publish is the thing everyone publishes, so nobody links to it. This is precisely why original
  testing matters commercially as well as ethically: test data is the only part of an affiliate
  page anyone has a reason to cite.

**On assistant surfaces.** Assistants answer "what should I buy" constantly and draw on
comparison content heavily, but they favour sources with a resolvable identity and visible
methodology, which is the same constraint. There is an added risk worth naming: an assistant may
lift your verdict without your caveats or your disclosure, so the verdict itself has to be
defensible standing alone. Eligibility remains the only claim. See `surfaces/` and
`seo-surface-assistants`.

## Type-specific checks

- **Disclosure, prominent and before the links.** Required by the FTC in the US, by the CMA and
  ASA in the UK, and by equivalents elsewhere. "Prominent" means visible without scrolling or
  expanding, not a line in the footer. Non-compliance is a legal exposure, not a ranking
  nuance.
- **Rel attributes on monetised links.** `rel="sponsored"` on affiliate and paid links (Google
  accepts `nofollow` where `sponsored` is impractical). Undisclosed monetised links that pass
  authority are a link spam policy breach, and at scale on a site this is the thing that gets
  it demoted.
- **Methodology page, and an honest one.** How products were selected, how they were assessed,
  what was and was not tested, who did it, and how the commercial relationship works. Linked
  from every review.
- **Evidence of genuine use.** Original images rather than manufacturer stock, measurements,
  screenshots, specifics only an actual user would know. Its absence is the finding.
- **Honest negatives.** A roundup where every product is excellent and every link is affiliate
  is not a review. Real drawbacks, and at least one genuine "do not buy this if".
- **Price and stock currency.** Stale prices are the most common factual error on these pages
  and they erode trust fastest. Date them, pull them from a feed, or omit them.
- **Ranking order justified.** If the order correlates with commission rather than with the
  assessment, say so or change it. It is also usually obvious to readers.
- **Thin duplication across the site.** Twenty roundups recombining the same ten products is
  the doorway pattern in another costume. Consolidate.

## The honest boundary

- **The agent will not fabricate a review.** No invented testing, no invented hands-on detail,
  no pretending to an experience nobody had. Where first-hand evidence is missing, the output is
  a finding saying what evidence the page needs and who would have to produce it.
- **It will not write the disclosure to be unobtrusive.** Prominent means prominent.
- **It cannot assess your legal compliance.** It flags missing disclosure and missing `rel`
  attributes as findings; whether the site meets its jurisdiction's advertising rules is a
  question for the business and its advisers.
- **This modality is structurally exposed.** Sites in it have been hit hardest by every
  helpful-content and reviews update. A page that only aggregates what is already available is
  the specific thing being demoted, and that risk cannot be engineered away, only answered with
  genuine first-hand substance.

## Common failures

- No disclosure, or disclosure buried in the footer.
- Affiliate links without `rel="sponsored"` or `nofollow`.
- Anonymous reviews, or an invented reviewer persona with a stock photograph.
- "We tested 14 products" where nothing was tested.
- Manufacturer copy and stock images reworded.
- `AggregateRating` markup built from other sites' ratings.
- Every product recommended, no real negatives, order set by commission.
- Prices years out of date presented as current.
- Dozens of overlapping roundups cannibalising each other.

## Priority tilt

Weight **Identity** (who is recommending, how they tested, disclosed properly) and **Substance**
(genuine first-hand evidence) highest. They are the same constraint seen from two sides, and
together they are the only thing separating a site that survives an update from one that does
not. Access is routine. Expect the honest finding on many pages to be "this needs first-hand
evidence or it should not exist", and report it rather than softening it.
