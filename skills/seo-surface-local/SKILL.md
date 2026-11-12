---
name: seo-surface-local
description: >-
  Local search: Google Business Profile, the map pack, location and service-area
  pages, NAP consistency, citations and reviews. Use on any "local SEO", "Google
  Business Profile", "GBP", "map pack", "local pack", "rank in Maps", "near me",
  "we have multiple locations", "service area", "NAP", "local citations", "get
  more reviews", or "why don't we show up in Maps" request. Fixes everything the
  build controls, and is explicit that the profile, the reviews and proximity are
  earned off-site and cannot be changed from a repository.
---

# Local — the map pack, the profile, and the half you actually control

Local is the clearest example in this method of a surface where **most of what decides the
outcome is not your website**. The build controls the entity on your own site. The Google
Business Profile, the reviews and the searcher's proximity decide the map pack, and none of
them lives in a repository.

So this skill does two things, and the second matters as much as the first: it fixes the
owned-media half properly, and it tells the owner plainly where the boundary is, early
enough that expectations are right.

**Identity leads here**, not Access. See `surfaces/google-maps.md` for the weighting and the
verification limits, and `seo-orchestrator/references/profiles/local-business.md` for the
depth, including the full GBP consistency checklist and the doorway-page test. This skill is
the workflow; those are the reference material.

Work the four steps: **Diagnose → Fix → Verify (on served output) → Report + the boundary.**

---

## When this fires
- A business serving a place: shop, clinic, tradesperson, restaurant, agency with a patch.
- "We don't show up in Maps" or "we used to be in the local pack".
- Multiple locations, or a service area with no public premises.
- NAP inconsistency, a wrong or unclaimed profile, or a listing that disagrees with the site.
- Planning location pages, which is where doorway spam usually begins.

## Inputs and modes

Infer these before Step 1. Ask only if a wrong guess would be costly (see `seo-orchestrator/references/operating-modes.md`).
- **Access:** URL only, read-only repo, or write access. Without write access, every fix becomes a precise instruction instead of an edit.
- **Mode:** `audit` (default) diagnoses and records findings and never changes the site. `fix` applies only the findings the user approves, on a branch where git exists, verifying each on the served output. `re-check` re-tests earlier findings.
- **Scope:** one location, all locations, or a budget. Honour a stated budget and stop when it is spent.
- **Context:** read `.seo/context.md` if it exists. The trading name, address, hours, services and area served must be `[established]` facts before they reach a page or schema. On this skill that rule is load-bearing: an invented address is the worst output available.
- **Record findings** with the shared schema, `skill: seo-surface-local`, `system: identity` for entity work and `system: access` for the page-level fixes.

---

## Step 1 — Diagnose

- **NAP consistency.** Name, address and phone identical across every page, the
  `LocalBusiness` schema, and the footer. Character for character, not approximately. This is
  the classic local failure and the one a build can genuinely fix.
- **The address is in the served HTML**, as text, not only inside a map embed or an image.
- **`LocalBusiness` markup** (or the right subtype) with accurate `address`, `geo`,
  `telephone`, `openingHoursSpecification` and `areaServed`, and a consistent `@id`.
- **Location pages against the doorway test.** A page per town is legitimate only when each
  one is useful to someone in that town in its own right. Apply the test in the
  `local-business` profile before creating or keeping any of them.
- **Service-area businesses:** `areaServed` used honestly, with no invented premises.
- **The profile against the site.** Where the environment has DataForSEO, workflow 14 in
  `seo-orchestrator/references/data/dataforseo-modules.md` observes `title`, `address_info`,
  `phone`, `category`, the hours timetable and `is_claimed` directly, so the diff runs
  without waiting for a screenshot. Otherwise ask the owner for the values.
- **`is_claimed`.** An unclaimed listing can be edited by the public. If it is false, that is
  a high-priority finding on its own.
- **Position, if asked, as a grid and never as a number.** Workflow 13 in the same file runs
  the same query from many coordinates. Price it before running it.

## Step 2 — Fix

Owned media only, and in this order:
- Make NAP identical everywhere, from the `[established]` values.
- Put the textual address, hours and phone in the served HTML.
- Correct or add `LocalBusiness` markup so it matches the visible page exactly.
- Build a locations hub and real per-location pages where they pass the doorway test;
  consolidate thin town pages into an area page with `301`s, after sign-off.
- Fix internal linking so every location page is reachable from the hub and from the
  relevant service pages.

**Never**: invent an address, hours, a trading name or a review; mark up ratings that are
not real and on the page; create a page per town because the list of towns exists.

## Step 3 — Verify (on the served output)

- Fetch each location page and confirm the address, hours and phone are present as text.
- Validate the `LocalBusiness` markup and check every value against the visible page.
- Confirm one consistent `@id` and no contradictory `Organization` blocks.
- Re-run the NAP sweep across the whole site, not the pages you touched.

## Step 4 — Report + the boundary

State this at the start of the engagement, not at the end:

- **Google Business Profile** drives the map pack, and it is managed in Google's dashboard.
  The agent never logs in, never claims a listing and never posts. Profile mismatches are
  `needs-human` with the exact value to change.
- **Reviews** are earned from real customers. Never fabricate, never incentivise against
  platform rules, never mark up reviews that were not left.
- **Proximity** is a ranking factor you cannot change. There is no such thing as your
  position "in a town", only positions at points, which is why position is reported as a
  dated grid or not at all.
- **Citations and directories** are Distribution work: advisory, via
  `seo-distribution-authority`.

The honest summary most local engagements deserve: the owned site can be made consistent and
trustworthy in a couple of days, and everything after that is earned off-site by the owner.

---

## Reference files
- `seo-orchestrator/references/profiles/local-business.md` — the depth: the GBP consistency checklist, the doorway-page test in full, service-area handling, and the honest boundary.
- `surfaces/google-maps.md` — the weighting (Identity first, Access last), how verification works by point, and what may never be claimed.
- `seo-orchestrator/references/data/dataforseo-modules.md` — workflow 13 (the geo-grid) and workflow 14 (observing the listing directly).
- `seo-access-understand/references/schema-types-and-jsonld.md` — `LocalBusiness` and its subtypes.
