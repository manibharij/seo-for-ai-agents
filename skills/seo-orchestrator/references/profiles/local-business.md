# Profile: local business

Use for businesses serving a place — shops, clinics, tradespeople, restaurants, agencies with a service area. The distinctive signals are **entity consistency** (especially NAP), `LocalBusiness` schema, and location/service-area pages. Note the honest line: a lot of local visibility is **off-site and live** (Google Business Profile, map pack, reviews) — outside what a build can fix.

## How each rung shifts
- **Reach** — usually a small site; standard checks. Ensure location/service pages are crawlable and in the sitemap.
- **Read** — genuinely useful location/service content (not the same paragraph with the town name swapped — that's doorway-page spam). Real address, hours, services, area served.
- **Understand** — `LocalBusiness` (or a subtype: `Restaurant`, `Dentist`, etc.) with **accurate** `address`, `geo`, `telephone`, `openingHoursSpecification`, `areaServed`. Consistent `@id` for the business across pages.
- **Connect** — clear structure for multiple locations/services; each location page linked and canonical; breadcrumbs.
- **Cite** — local-intent answers ("plumber in <town> open on Sunday") — clear, honest answers with real hours/area; consistent entity so engines trust who and where you are.

## Type-specific checks
- **NAP consistency:** Name, Address, Phone identical across the whole site, the schema, and (the user should ensure) external listings. Inconsistent NAP is the classic local-SEO killer. The agent fixes on-site NAP and schema; off-site listings are the user's to align.
- **Multiple locations:** a real, distinct page per location with unique content, its own `LocalBusiness` schema and `@id`, linked from a locations hub. Don't generate thin templated clones.
- **Service-area businesses:** use `areaServed`; don't fake a physical address you don't have.
- **Hours/holidays:** accurate `openingHoursSpecification`; keep it true.
- **Embedded map / directions:** fine, but ensure the textual address is in the served HTML (not only in a map widget).

## The honest local boundary (state this clearly)
Much of local performance lives **off the website**:
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
Weight **Understand** (LocalBusiness + NAP) and **Read** (genuine local content) highest; be explicit early about the GBP/reviews/geo-grid boundary so expectations are right.
