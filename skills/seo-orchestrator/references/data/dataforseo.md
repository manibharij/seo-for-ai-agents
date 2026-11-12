# DataForSEO: named workflows

Read this when the environment has DataForSEO credentials (`DATAFORSEO_LOGIN` and
`DATAFORSEO_PASSWORD`) or the DataForSEO MCP server, and a skill needs data that Search
Console cannot give it. For the connection details, auth and module list, see
[`third-party-mcps.md`](third-party-mcps.md). This file is the part that matters in
practice: **specific analyses, with the endpoint, the filter and the honest limits.**

Everything here was verified against DataForSEO's own documentation in November 2026
(verified 2026-11). Endpoints change; check the response against a live call before relying
on a nested field path.

## Why this tool earns its own recipe

Three of the pack's analyses are described elsewhere and have no mechanism without it:

1. **Cannibalisation on a site you do not own.** The Search Console method in
   `seo-substance-content-audit/references/decay-cannibalisation-actions.md` needs the
   owner's data. The `client-audit` job never has it.
2. **Proving an intent shift.** `seo-substance-quality/references/search-intent.md` says the
   result shape changing over time is the clearest evidence of an intent shift, and gives no
   way to observe it.
3. **Any measurement at all on an AI surface.** `surfaces/google-ai-mode.md` reports
   partial verification, and sampled prompts are the only alternative.

## The rules, before any call

These override convenience, every time:

- **Say before you spend.** Every call is billed. State how many calls and why, then ask.
  One call with `filters` and a high `limit` beats twenty small ones.
- **Label every number as the vendor's estimate**, with the date and the location and
  language used. "DataForSEO estimate, United Kingdom, en, 2026-11-12: 1,900 a month."
- **Search Console wins for your own site.** Where the two disagree on your clicks,
  impressions or position, Search Console is the fact and this is the model. Use this for
  what Search Console cannot see: competitors, sites you do not own, and the SERP itself.
- **Never fill a gap.** No volume returned means unknown, not zero.
- **Read only.** No task creation, no tracked-keyword management, unless asked.
- **Resolve locations properly.** Use `location_name` (for example
  `"London,England,United Kingdom"`) or look the code up from the locations endpoint. Do not
  copy a `location_code` from an example and assume it is the country you want; the examples
  in the docs are not all the same market.

Confidence for anything from here is `inferred`, never `established`. It is a third party's
model of a surface, and the finding should say so.

---

## 1. Cannibalisation without Search Console

**Answers:** which of my keywords have more than one of my own pages competing for them.

`POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live`

```json
[{ "target": "example.com", "location_name": "United Kingdom", "language_code": "en",
   "limit": 1000, "offset": 0, "item_types": ["organic"] }]
```

`limit` defaults to 100 and maxes at 1000, so page with `offset` until a response returns
fewer rows than the limit. Each item carries:

| Field | What it is |
|---|---|
| `keyword_data.keyword` | the keyword |
| `keyword_data.keyword_info.search_volume` | average monthly volume (the vendor's estimate) |
| `ranked_serp_element.serp_item.url` | **the ranking URL** |
| `ranked_serp_element.serp_item.rank_group` | position within elements of the same type |
| `ranked_serp_element.serp_item.rank_absolute` | absolute position among all SERP elements |

**The analysis:** group the items by `keyword_data.keyword`. Any keyword with two or more
distinct `url` values from the target domain is a **cannibalisation candidate**. Sort the
clusters by `search_volume` so the expensive ones surface first.

That is a candidate, not a verdict. Confirm it with workflow 2 before recommending a merge,
because a domain legitimately holding two positions for one query is not always a problem.

> The docs' schema nests element objects under `serp_item` while the sample response places
> `type` directly on `serp_item`. Check one live response and adapt the path before parsing
> at scale.

## 2. Which page Google actually prefers, and whether it is flipping

**Answers:** for a contested keyword, which of my URLs does Google choose, and is the choice
stable?

`POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced`

```json
[{ "keyword": "contested phrase", "location_name": "London,England,United Kingdom",
   "language_code": "en", "device": "desktop", "depth": 20 }]
```

Read the items whose `url` is on the target domain and record which one appeared, with the
date.

**The innovation is repeating it.** Run the same keyword on a schedule and keep the history.
A URL that **flips between two of your pages across runs is confirmed cannibalisation**:
Google cannot decide which page answers the query, which is exactly the problem, and it is a
far stronger signal than a single snapshot. A stable winner with a second page far below is
usually fine and should be left alone.

Store each run as a row (`date, keyword, winning_url, rank_absolute`) so the flip is visible
rather than inferred from memory.

## 3. Intent-shift detection

**Answers:** did this query change meaning, or did my page get worse?

`content-decay.md` separates four causes of a decline that all look identical in a traffic
graph. This distinguishes two of them with evidence.

Call the same SERP endpoint as workflow 2, then record the **`type`** of every item, not just
the organic ones. The documented types include `organic`, `paid`, `featured_snippet`,
`people_also_ask`, `ai_overview`, `video`, `shopping`, `local_pack`, `discussions_and_forums`,
`top_stories`, `images`, `knowledge_graph` and many more.

**The analysis:** snapshot the type mix per keyword, then re-run monthly and diff it.

- The mix is stable and you fell: your page got worse, or a competitor improved. That is
  **decay**, and `content-decay.md` applies.
- The mix changed (organic giving way to `shopping`, or `video`, or `discussions_and_forums`
  appearing): **the intent moved**, and `search-intent.md`'s fourth mismatch pattern applies.
  The page did not fail. Rewriting it to be "better" will not recover the position, because
  Google is now answering a different question.
- `ai_overview` appearing where it did not before explains a click decline with flat
  impressions, which is the pattern people most often misreport as a ranking loss.

This is the mechanism `search-intent.md` describes and could not previously perform.

## 4. AI Overview references: a real measurement on a surface that has none

**Answers:** which of my pages are being cited in AI Overviews, for which queries, and which
sentence was used.

Call `ranked_keywords/live` with the item type changed:

```json
[{ "target": "example.com", "location_name": "United Kingdom", "language_code": "en",
   "limit": 1000, "item_types": ["ai_overview_reference"] }]
```

The `ai_overview_reference` element carries `source`, `domain`, `title`, `url`, and `text`,
documented as "text snippet from the page that was used to generate the
`ai_overview_element`".

That last field is the valuable one, and it is unusual: it tells you **which passage of your
page was good enough to lift**. Feed it back into `seo-surface-assistants` and
`seo-substance-quality`: the passages that get used are the pattern to extend, and a page
with none while competitors have several has an extractability problem, not a ranking one.

**The honesty, which matters more here than anywhere else in this file.** This is a vendor's
observation of a volatile surface, not Google reporting on you. It does not change the
claimable outcome, which stays **eligibility**. Report it as a dated sample from one location
and language, use it to direct work, and never convert it into a score or a share. Run it
against competitors in the same call pattern to see whether the surface favours anyone at
all for your topics; frequently it favours nobody consistently, and that is a finding.

Related request-side note: the SERP endpoint has a `load_async_ai_overview` parameter for
AI Overviews that load asynchronously, and it carries an extra charge. Decide deliberately.

## 5. Striking distance on a site you do not own

**Answers:** what is close enough to page one to be worth the effort?

`ranked_keywords/live` accepts up to 8 `filters` combined with `and`/`or`:

```json
"filters": [
  ["ranked_serp_element.serp_item.rank_group", ">", 10],
  "and",
  ["ranked_serp_element.serp_item.rank_group", "<=", 20],
  "and",
  ["keyword_data.keyword_info.search_volume", ">", 100]
]
```

`order_by` takes up to three rules, so sort by `search_volume` descending and work down. This
is the `grow` job's step 3 for a site whose Search Console you cannot see, which in practice
means every `client-audit`.

## 6. Page-level competitor comparison

**Answers:** which of a competitor's pages is actually carrying their search presence?

`POST https://api.dataforseo.com/v3/dataforseo_labs/google/relevant_pages/live` with
`target` set to the domain (no protocol, no `www`). Each item gives:

- `page_address`, the page URL
- `metrics.organic.count`, the number of organic SERPs containing that page
- `metrics.organic.pos_1`, `pos_2_3` and the other bands, the ranking distribution
- `metrics.organic.etv`, estimated traffic volume
- the same under `paid`, `featured_snippet` and `local_pack`

Run it for the competitor and for yourself, then compare the shape rather than the totals. A
competitor whose presence sits in five deep pages is beatable page by page; one whose
presence is spread over four hundred is a different problem and a different plan.

**`etv` is an estimate and is never reported as traffic.** It is useful for ranking pages
against each other within one domain, and misleading across domains.

---

## What this tool cannot tell you

State these when you use it, because the numbers look authoritative:

- **Your real clicks and impressions.** Only Search Console has those. Everything here is
  modelled from rank and volume.
- **Position for a person.** Results are a snapshot from one location, one language and one
  device. Personalisation and locality mean there is no single true position.
- **Why anything moved.** You get the what and the when, never the cause.
- **Whether an AI Overview citation persists.** The surface is volatile, and a reference
  observed today may be gone tomorrow with no change on your side.
- **Anything about a page a crawler cannot reach.** If Access is failing, fix that first;
  this data will only describe the failure expensively.

## The other modules

Backlinks, OnPage, Content Analysis and the local endpoints have their own recipes in
[`dataforseo-modules.md`](dataforseo-modules.md), workflows 7 to 14. **The rules at the top
of this file apply to all of them** and are not repeated there.

| # | Workflow | Module |
|---|---|---|
| 7 | The authority gap, quantified against named competitors | Backlinks |
| 8 | Lost links, for reclamation | Backlinks |
| 9 | Broken backlinks, which is a redirect job rather than a campaign | Backlinks |
| 10 | Render-gap detection at scale, by calling the same URL with and without JavaScript | OnPage |
| 11 | On-page triage on a site you cannot crawl yourself | OnPage |
| 12 | Unlinked mentions, found by subtracting linkers from mentioners | Content Analysis + Backlinks |
| 13 | The geo-grid, from `location_coordinate` | SERP Maps |
| 14 | Google listing consistency without asking for a screenshot | Business Data |

Ahrefs and Semrush have their own recipes in
[`ahrefs-semrush.md`](ahrefs-semrush.md), which also carries the table of **which of the
three tools can do which workflow**. They are not interchangeable: DataForSEO is the only
one of the three verified here for cannibalisation, the geo-grid and render-gap detection,
and Ahrefs is the only one verified for AI citations across more than one engine.

Domain Analytics (technologies, Whois) and the task-based full-site OnPage crawl have **no
verified recipe in either file**. They are reachable through the capability detection in
[`live-data-integrations.md`](../live-data-integrations.md). Say that in the finding rather
than implying these files covered them.
