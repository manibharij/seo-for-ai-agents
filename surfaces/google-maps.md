---
surface: google-maps
title: Google Maps and the local pack
verification: strong
verification_methods: [serp, api_response, served_html]
claimable_outcome: measured_presence_by_point
weighting: [identity, distribution, substance, demand, access]
---

# Google Maps and the local pack

## What this surface is

The map results and local pack, driven primarily by a **Google Business Profile** rather
than by a website. This is the surface where the thing being ranked is not your page: it
is your business entity, and your site is a supporting signal.

It is strongly verifiable and easy to measure wrongly, which is a combination worth
understanding before reporting anything. You can see exactly where you rank, but only
**from a point**. Move a few hundred metres and the answer changes, because proximity is a
ranking factor. A single check is a single coordinate, and it does not represent an area.

## What decides whether you appear

1. **Identity.** Overwhelmingly first, and not close. The business name, the address, the
   category, the hours, the service area, the phone number, and the consistency of all of
   it between the profile, the website and every third-party listing. An inconsistent
   entity is the classic local failure, and it is the one thing a build can genuinely fix.
2. **Distribution.** Reviews, in volume and recency and rating, plus local citations in the
   directories that matter for the sector and the country. Earned, off-site, and the agent
   never touches it beyond advising.
3. **Substance.** Genuinely useful location and service content on the site, which
   supports the entity and converts the visit. Real local specifics, not a template with
   the town swapped.
4. **Demand.** Local intent is specific and modifier-heavy, and the phrasing varies by
   area and trade.
5. **Access.** Last, and genuinely last on this surface: the site must be reachable and
   carry the address in the served HTML, but a technically immaculate site does not move
   the map pack.

## How to verify

- **A geo-grid**: the same query run from many coordinates across the service area,
  producing a map of positions rather than one number. This is the only honest way to
  report local position, and it needs a tool or an API that can set location.
- **Google Business Profile insights** for how people found the profile, what they did, and
  which queries surfaced it. First-party and the most reliable source here.
- **Served HTML** for the site's half: the textual address, hours and phone present and not
  only inside a map embed, and `LocalBusiness` markup that matches the visible page.
- **A consistency sweep** across the profile, the site, the schema, and the major
  directories, comparing values character by character.

The site side is fully checkable by the agent. The profile side requires the owner's
access, so a mismatch found there is recorded as `needs-human` with the exact value to
change.

## What is unknowable here

- Your position "in a town". There is no such number. There are positions at points.
- How Google weighs proximity against prominence for a given query, which varies by
  density: in a city centre proximity dominates, in a rural area it cannot.
- The effect of a single review, or of a profile edit, in isolation.
- Why a competitor with a worse site and fewer reviews outranks you from one coordinate and
  not another.

## What may never be claimed

- **Map pack position as a single figure.** Report a grid, with the coordinates and the
  date, or do not report position at all.
- **Any guarantee of local pack inclusion**, which is Google's call and depends heavily on
  factors off the site.
- **That build work alone will move the map pack.** It will not. Say this at the start of a
  local engagement, because the expectation otherwise forms by default.

Never create a physical address the business does not occupy, invent hours, or mark up
reviews that were not left by real customers. Fabricated local identity is both the most
tempting shortcut on this surface and the fastest route to a suspended profile.

## Honest note on effort

The highest-value local work is unglamorous and mostly not code: one consistent name,
address and phone everywhere; the right primary category; accurate hours including
holidays; a real page per real location; and a genuine process for earning reviews.

A site can be made perfect for this surface in a day or two of careful consistency work.
Everything beyond that is Distribution, it is earned, and the owner has to do it. An agent
that implies otherwise is selling something it cannot deliver.
