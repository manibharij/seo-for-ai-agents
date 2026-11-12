---
surface: google-images
title: Google Images
verification: moderate
verification_methods: [served_html, serp, search_console_api, crawl]
claimable_outcome: measured_presence
weighting: [access, substance, demand, identity, distribution]
---

# Google Images

## What this surface is

Image search, plus image thumbnails inside web results. It is the most overlooked surface
in this model relative to how cheap the work is, and for a few sectors, retail, recipes,
interiors, travel, trades with visible results, it carries meaningful commercial traffic.

It is also the surface where almost all of the work is Access, which makes it unusually
tractable for an agent: most of what matters is in the markup and the delivery, and can be
verified directly.

## What decides whether your images appear

1. **Access.** Dominant, and nearly all of it checkable:
   - The image must be crawlable. Images blocked in `robots.txt`, served from a blocked
     CDN path, or loaded only by JavaScript after interaction are invisible.
   - **Lazy loading must be done natively** (`loading="lazy"`) or with a real `src`
     present. A custom lazy loader that leaves `src` empty until scroll hides the image
     from Google entirely. This is the single most common failure here.
   - The image needs a stable, indexable URL, and ideally an image sitemap.
   - Format and size matter for the page experience the image sits in.
2. **Substance.** What the image is and the context around it: descriptive `alt` text that
   describes the image rather than listing keywords, a filename that says what it is,
   nearby text and a caption, and the image being genuinely relevant to the page. Google
   reads the page to understand the image.
3. **Demand.** Visual demand is sector-specific and worth checking before investing: for
   some categories people search images first, for most they do not.
4. **Identity.** Licensing and attribution, including `ImageObject` licence metadata where
   the images are yours and licensing is a commercial concern.
5. **Distribution.** Where your images are reused and credited elsewhere.

## How to verify

- **Served HTML** for `src`, `alt`, `srcset`, `loading`, and whether the image is present
  before JavaScript runs. This catches the lazy-loading failure immediately.
- **Search Console** for image impressions and clicks, filterable by search appearance, and
  for whether image URLs are indexed.
- **A crawl** for missing `alt` at scale, oversized files, and images referenced only in
  CSS, which are not indexable as content.
- **The image results themselves** for presence, which is a sample.

## What is unknowable here

- Ranking logic for images, which is less documented than for web results.
- How much weight the surrounding page text carries versus the image itself.
- Click behaviour inside image results, beyond Search Console's aggregate.

## What may never be claimed

Presence and measured impressions may be claimed, from Search Console, dated.

Do not claim image traffic will convert. It converts poorly in most sectors, and that is a
material caveat when recommending investment in image work for a client expecting leads.

Never write `alt` text that misrepresents the image for keyword gain, and never mark up
licence metadata for images you do not have the rights to.

## Honest note on effort

The honest position: this is cheap hygiene that should be done properly on every site, and
a dedicated campaign on very few.

The hygiene is real and takes an afternoon: real `alt` text, descriptive filenames, native
lazy loading, modern formats, correct dimensions, an image sitemap where images matter. It
improves accessibility and page experience at the same time, which is the better argument
for it than image traffic.

Beyond that, look at the Search Console data before investing. If image impressions are
already meaningful, there is something to optimise. If they are negligible and the sector
is not visual, the budget belongs on another surface.
