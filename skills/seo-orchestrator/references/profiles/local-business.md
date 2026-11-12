# Profile: local business

Use for businesses serving a place — shops, clinics, tradespeople, restaurants, agencies with a service area. The distinctive signals are **entity consistency** (especially NAP), `LocalBusiness` schema, and location/service-area pages. Note the honest line: a lot of local visibility is **off-site and live** (Google Business Profile, map pack, reviews) — outside what a build can fix.

## How the five systems shift

- **Demand** (observed). Local intent is specific and modifier-heavy ("plumber in <town> open on Sunday"). Read the real phrasing per service and per area rather than assuming one keyword per page.
- **Identity** (built). **The heart of this profile.** Name, address and phone identical across every page and every piece of schema. `LocalBusiness` (or a subtype: `Restaurant`, `Dentist`) with **accurate** `address`, `geo`, `telephone`, `openingHoursSpecification` and `areaServed`, and a consistent `@id` for the business across pages. A service-area business uses `areaServed` honestly rather than inventing a premises.
- **Substance** (built). Genuinely useful location and service content, not the same paragraph with the town name swapped, which is doorway-page spam. Real hours, real services, real coverage, and the local specifics only this business could write.
- **Access** (built). Usually a small site, so the ladder is mostly routine here. One rung still matters a lot.
  1. **Reach.** Standard checks. Ensure location and service pages are crawlable, indexable and in the sitemap.
  2. **Read.** The textual address, opening hours and phone number present in the served HTML, not only inside a map widget or an image.
  3. **Understand.** `LocalBusiness` markup that matches the visible page exactly, with honest hours and no invented reviews.
  4. **Connect.** A clear structure for multiple locations and services: each location page linked from a hub, self-canonical, with breadcrumbs.
- **Distribution** (earned, advisory). Google Business Profile, real customer reviews and local citations drive most of local performance, and all of it is earned off the site. Tell the owner exactly what to align. The agent cannot claim a profile, post as the business, or ask for a review.

**On assistant surfaces.** An assistant answering "best <trade> near me" has to resolve one consistent entity with a real address and a stated area served, which is why Identity carries **eligibility** here. The map pack is a separate, live surface a build does not control, and it can only be checked point by point: a single check never represents an area. See `surfaces/` and `seo-surface-assistants`.

## Type-specific checks
- **NAP consistency:** Name, Address, Phone identical across the whole site, the schema, and (the user should ensure) external listings. Inconsistent NAP is the classic local-SEO killer. The agent fixes on-site NAP and schema; off-site listings are the user's to align.
- **Multiple locations:** a real, distinct page per location with unique content, its own `LocalBusiness` schema and `@id`, linked from a locations hub. Don't generate thin templated clones.
- **Service-area businesses:** use `areaServed`; don't fake a physical address you don't have.
- **Hours/holidays:** accurate `openingHoursSpecification`; keep it true.
- **Embedded map / directions:** fine, but ensure the textual address is in the served HTML (not only in a map widget).

## Service-area and location pages without doorway pages

Google's spam policies list, as a doorway example, pages aimed at specific regions or cities that funnel visitors to one page (verified 2026-10, https://developers.google.com/search/docs/essentials/spam-policies). A page per town is legitimate only when each page is useful to someone in that town in its own right.

Before creating or keeping a location or service-area page, it must pass all of these:
- **A real presence or real service.** A physical branch at that address, or the business genuinely serves that area today. The business confirms this; it is an `[established]` fact in `.seo/context.md`, never inferred from a list of nearby towns.
- **Content that differs because the place differs:** the staff or team who cover it, local opening hours or response times, prices or call-out charges that vary, real jobs done there (with the customer's permission), local access, parking or regulations, testimonials from people there. If the only difference is the town name, it fails.
- **It stands on its own.** A visitor can act on the page (call, book, see the area covered) without being funnelled to a generic page.
- **It sits in a browsable hierarchy:** linked from a locations or areas hub and from relevant service pages, not only listed in a sitemap or footer block.

How to apply it:
- **Physical locations:** one page per real location, each with its own `LocalBusiness` block and `@id`, its own address and phone, and its own hours.
- **Service-area businesses** (plumbers, cleaners, mobile services): one strong page describing the area served (a list or map of areas, with `areaServed`) usually beats a page per town. Add a dedicated area page only when you have enough area-specific substance to pass the test above. Do not show a street address you do not want customers to visit, and never invent one.
- **Existing thin town pages:** do not delete them in bulk. Improve the ones with real substance and traffic, and consolidate the rest into the area page with `301`s, after sign-off (see `seo-access-migrations` and `existing-site-safety.md`).
- **Programmatic generation** of town pages goes through `seo-substance-at-scale`, whose quality gate applies.

## Site and Google Business Profile consistency (advisory)

The Google Business Profile lives off-site. The agent does not log in to it or change it; it checks the website against what the owner reports, and hands the owner a list. Google's GBP guidelines ask for the real-world business name, the real location (service-area businesses hide their address), and contact details that lead to the specific business (verified 2026-10, https://support.google.com/business/answer/3038177).

Ask the owner for the GBP values (or a screenshot), then check the served site against them:
- [ ] **Name** on the site, in `LocalBusiness` `name`, and in GBP is the same real-world name. No keywords or town names added to the GBP name that the business does not use.
- [ ] **Address** matches character for character in the visible footer or contact page, the schema `address`, and GBP. For a service-area business that hides its address in GBP, the site does not publish it either, unless customers visit.
- [ ] **Phone** is the same local number in all three, in the same format in the schema (`+44 ...`).
- [ ] **Hours** on the site and in `openingHoursSpecification` match GBP, including holiday hours the owner has set.
- [ ] **Service area** on the site and in `areaServed` matches the areas set in GBP.
- [ ] **Categories and services** the site describes match the GBP primary category and services.
- [ ] **Website link** in GBP points to the right page (the home page, or the specific location page for multi-location businesses) and that URL returns `200`, is indexable and is self-canonical.
- [ ] **Each location** in a multi-location business has its own GBP pointing at its own location page.

Every mismatch becomes a finding. Fix the site side yourself when you have write access; list the GBP side as `needs-human` with the exact value to change, since only the owner can edit the profile.

## The honest local boundary (state this clearly)
Much of local performance is **Distribution**, which is earned rather than built, and lives **off the website**:
- **Google Business Profile** (the map pack, hours, photos, posts) — managed in GBP, not your site.
- **Reviews** on Google/third parties — earned, off-site; never fabricate, never mark up fake ones.
- **Local citations/directories** — off-site consistency.
- **Proximity/map-pack ranking and the geo-grid** — live, location-dependent data.
The build can get your **owned site** right (content, `LocalBusiness` schema, NAP consistency on-site); GBP, reviews, citations, and geo-grid visibility are separate, live/off-site work — point the user across that boundary honestly.

## Common failures
- Doorway pages: one template, town name swapped, no real local content.
- Inconsistent NAP across pages/schema.
- Fake reviews / `aggregateRating` — remove and flag.
- Address only inside a map embed, missing from the served HTML.

## Priority tilt
Weight **Identity** highest (NAP consistency and `LocalBusiness` markup) with **Substance** beside it (genuine local content). Be explicit early that **Distribution** here is earned off-site, so expectations about the map pack, reviews and the geo-grid are right from the start.
