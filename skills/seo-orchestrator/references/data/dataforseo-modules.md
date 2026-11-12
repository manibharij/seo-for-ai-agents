# DataForSEO: Backlinks, OnPage, Content Analysis and local

The second half of the DataForSEO recipes. [`dataforseo.md`](dataforseo.md) covers the
keyword, SERP and AI workflows and carries **the spend and honesty rules that apply to
everything here too**. Read those first; they are not repeated.

Verified against DataForSEO's documentation in November 2026 (verified 2026-11). Check a
live response before parsing a nested path at scale.

| # | Workflow | Module | Serves |
|---|---|---|---|
| 7 | The authority gap, quantified | Backlinks | `seo-distribution-authority` |
| 8 | Lost links, for reclamation | Backlinks | `seo-distribution-authority` |
| 9 | Broken backlinks, the free win | Backlinks | `seo-access-migrations` |
| 10 | **Render-gap detection at scale** | OnPage | `seo-access-reach` |
| 11 | On-page triage on a site you do not own | OnPage | `client-audit` |
| 12 | **Unlinked mentions, by subtraction** | Content Analysis + Backlinks | `seo-distribution-authority` |
| 13 | **The geo-grid** | SERP Maps | `surfaces/google-maps.md` |
| 14 | GBP consistency without a screenshot | Business Data | `profiles/local-business.md` |

---

## 7. The authority gap, quantified against named competitors

**Answers:** do they have authority we do not, and how much?

`roles/distribution-strategist.md` requires the gap to be quantified "against named
competitors" and `earning-angles.md` requires it answered before any campaign is
recommended. This is the mechanism.

`POST https://api.dataforseo.com/v3/backlinks/summary/live`

```json
[{ "target": "example.com", "include_subdomains": true,
   "backlinks_status_type": "live", "rank_scale": "one_hundred" }]
```

Run it once for the site and once per named competitor, **with identical settings**, then
compare:

| Field | What it is |
|---|---|
| `referring_main_domains` | distinct linking root domains. **The number that matters.** |
| `referring_domains` | counts subdomains separately, so it is inflated |
| `backlinks` | total links, inflated by sitewide footer and template links |
| `rank` | the vendor's authority score, on the scale set by `rank_scale` |
| `referring_links_attributes` | counts by `nofollow`, `sponsored`, `ugc` |
| `broken_backlinks` | links pointing at URLs that do not resolve. See workflow 9 |

**Compare `referring_main_domains`, not `backlinks`.** One partner with a sitewide footer
link produces thousands of backlinks from a single domain, and a comparison on the raw count
tells you the opposite of the truth. This is the most common way an authority report
misleads.

To isolate links that pass authority, add `"backlinks_filters": [["dofollow", "=", true]]`
and run it again; there is no dedicated dofollow count in the summary.

Then answer the prior question honestly: if the site's pages are weaker than the ones
outranking it, authority is **not** the constraint and this number does not change that.

## 8. Lost links, for reclamation

**Answers:** who used to link to us and no longer does?

The same endpoint with `"backlinks_status_type": "lost"`. Individual links carry `lost_date`
and `first_seen`.

Lost links are the best-value item in any Distribution plan, because the relationship
already existed and somebody made the decision to link once. A page that was redesigned,
consolidated or pruned on their side is usually recoverable with a short, honest note.

**It remains advisory.** The strategist produces the list, the reason each one probably
disappeared, and what to say. A person sends anything that gets sent. Nothing here moves
that line, at any autonomy rung.

## 9. Broken backlinks, which is an Access fix wearing a Distribution hat

**Answers:** is anyone linking to a URL on our site that no longer resolves?

`broken_backlinks` in the summary gives the count. Every one is authority arriving at a dead
URL, and recovering it needs **no outreach at all**: a `301` to the genuine equivalent
captures it, which is a change you control entirely.

This is worth naming explicitly because it is routinely filed under link building and sold
as a campaign, when it is a redirect map. It belongs to `seo-access-migrations`, and after a
migration it is the first place to look, because an incomplete redirect map shows up here as
externally linked 404s.

Never redirect them all to the homepage. Google may treat that as a soft 404, and the
equivalence has to be genuine.

---

## 10. Render-gap detection at scale

**Answers:** does this page's content exist for a crawler that does not run JavaScript?

This is the single most valuable workflow in either file, because it automates the pack's
number-one finding.

`POST https://api.dataforseo.com/v3/on_page/instant_pages`

`enable_javascript` **defaults to `false`**. So call the same URL twice and diff:

```json
[{ "url": "https://example.com/pricing" }]
```
```json
[{ "url": "https://example.com/pricing", "enable_javascript": true }]
```

Read `checks` and `onpage_score` from both. If `no_title`, `no_h1_tag` or `no_description`
are `true` without JavaScript and `false` with it, **the content does not exist for a
crawler that does not execute scripts**, which includes several AI crawlers. That is the
failure this whole method was built around, now detectable across hundreds of URLs instead
of one at a time.

Practical limits, which matter here:

- One request can carry **up to 20 tasks**, but **requests with more than 5 identical
  domains are not accepted**. So batch at most 5 URLs per domain per request, and expect
  more requests than you first estimated. Say so before you spend.
- `enable_javascript` carries an extra charge, so the diff costs more than two plain calls.
- `custom_user_agent` defaults to `Mozilla/5.0 (compatible; RSiteAuditor)`. If the
  question is whether a specific crawler is blocked at the edge, set the user agent
  deliberately rather than inferring from the default.
- `enable_browser_rendering` adds Core Web Vitals and automatically turns on
  `enable_javascript` and `load_resources`.

**The finding's confidence is `inferred`, and the fix must still be verified yourself.** A
third-party crawler's observation is a strong lead; invariant 1 says a fix is proven on the
output you fetched. Use this to find the pages, then confirm the ones that matter with your
own request. Never close a Reach finding on a vendor's score.

## 11. On-page triage on a site you do not own

**Answers:** where are the structural problems on a site I cannot crawl myself?

The same endpoint across a URL set gives `checks` (including `no_title`, `title_too_long`,
`title_too_short`, `no_description`, `no_h1_tag`, `high_loading_time`, `is_broken`,
`has_render_blocking_resources`), `onpage_score`, a `page_timing` object, and
`resource_errors` with `line`, `column`, `message` and `status_code` per entry.

For `client-audit` this is the difference between an opinion and an evidenced finding across
a sample. Choose the sample deliberately (a template of each type) and say what the sample
was, as that job requires.

On `page_timing`: `largest_contentful_paint` and `first_input_delay` here are **lab figures
from one run**. The pack's order is field data first. Use CrUX for what real users
experience and this to reproduce a cause. Note also that INP replaced FID as the Core Web
Vital for responsiveness, so an FID number is not the metric being assessed.

---

## 12. Unlinked mentions, by subtraction

**Answers:** who has already written about us without linking?

`earning-angles.md` lists unlinked mentions as "the highest hit rate available and
frequently sitting unexamined". Two modules together find them.

**Step one, who mentions you:**

`POST https://api.dataforseo.com/v3/content_analysis/search/live`

```json
[{ "keyword": "Your Brand Name", "limit": 1000 }]
```

Each item carries `url`, `domain`, `main_domain`, `content_info.snippet` and
`content_info.highlighted_text`, plus `content_info.connotation_types` (positive, negative,
neutral) and `content_info.sentiment_connotations`.

**Step two, who links to you:** the referring domains from the Backlinks module
(workflow 7).

**Step three, subtract.** Domains in the first list and not the second have written about
you and not linked. Sort by whether the mention is substantive, read the `snippet`, and hand
the list to a human with the reason each one might add a link.

Honest limits, and they are real:

- The docs describe this as **citation data for a keyword**, not a brand-mention product. A
  brand name that is also a common word will return mostly noise, and a distinctive name
  will work well. Judge the output before reporting a number from it.
- Sentiment fields are a model's guess. Use them to sort a list for a human to read. Never
  report sentiment as a fact about how a publication feels.
- A mention with no link is not a problem to be fixed by asking. Some will decline, some
  have a policy, and that is normal.

---

## 13. The geo-grid

**Answers:** where do we actually rank in the local pack, across the area we serve?

`surfaces/google-maps.md` states that there is no such thing as your position "in a town",
only positions at points, and that the only honest way to report local visibility is a grid
with its coordinates and date. It had no mechanism. This is it.

`POST https://api.dataforseo.com/v3/serp/google/maps/live/advanced`

```json
[{ "keyword": "emergency plumber", "language_code": "en",
   "location_coordinate": "53.7996388,-1.5491222,15z", "depth": 20 }]
```

`location_coordinate` takes `"latitude,longitude,zoom"`. Zoom runs 3z to 21z and defaults to
17z, and the coordinates take up to 7 decimal places. Items in `maps_search` give `title`,
`rank_absolute`, `rank_group`, `rating.value`, `rating.votes_count`, and the `cid`,
`place_id` and `feature_id` identifiers.

**The grid:** generate a lattice of coordinates across the service area, run the same
keyword and zoom at each point, and record `rank_absolute` for your `cid` per point. Use
`cid` or `place_id` to identify yourself rather than matching on `title`, since names are
not unique and chains repeat.

**Cost, stated before you run it.** Each Live call is one task and one coordinate, so a 7x7
grid is 49 calls for one keyword, one run. Three keywords tracked monthly is roughly 1,764
calls a year. Decide the grid size and keyword set with the owner first; this is the single
most expensive thing in either file and the one most likely to surprise somebody.

Keep the zoom constant between runs, or the comparison is meaningless. Report the grid with
its coordinates and dates, never flattened into one position.

## 14. GBP consistency without asking for a screenshot

**Answers:** does the Google listing agree with the site?

`profiles/local-business.md` carries a consistency checklist that currently begins "ask the
owner for the GBP values (or a screenshot)". Much of it can be observed instead.

`POST https://api.dataforseo.com/v3/business_data/google/my_business_info/live`

```json
[{ "keyword": "cid:1234567890", "location_name": "Leeds,England,United Kingdom",
   "language_code": "en" }]
```

`keyword` takes the business name, or a `cid:` or `place_id:` identifier, which is more
reliable. One location field and one language field are required. The response gives
`title`, `address` and `address_info` (`address`, `city`, `zip`, `region`, `country_code`),
`phone`, `category` plus `additional_categories`, `work_time.work_hours.timetable`,
`current_status`, `rating.value` and `rating.votes_count`, `attributes` and **`is_claimed`**.

**The analysis:** diff each field against the site's served HTML and its `LocalBusiness`
markup. Every mismatch is a finding with both values quoted. `is_claimed` being false is its
own finding and a high-priority one, because an unclaimed listing can be edited by the
public.

Two boundaries hold regardless:

- **The site side is yours to fix; the listing side is not.** A GBP mismatch stays
  `needs-human` with the exact value to change, because only the owner can edit the profile.
  The agent never logs in, and `roles/identity-steward.md` forbids creating or claiming a
  listing at any rung.
- **Confirm the source.** The documentation describes this as information about a business
  entity from Google and does not explicitly state it is the public Google Business Profile
  record. Treat it as a strong observation, label it as the vendor's, and check anything
  surprising against the listing itself before telling an owner their profile is wrong.

---

## Still not covered

**Domain Analytics** (technologies, Whois) has no recipe here. It is reachable through the
capability detection in [`live-data-integrations.md`](../live-data-integrations.md), and
nothing in this file has verified it.

The OnPage module also has a **task-based full-site crawl** beyond the single-page
`instant_pages` call used here. For large sites that is the right tool, and its task
lifecycle is not documented in this file yet. Say so rather than implying it was covered.
