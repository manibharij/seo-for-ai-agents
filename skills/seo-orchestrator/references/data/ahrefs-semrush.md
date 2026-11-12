# Ahrefs and Semrush: named workflows

The third of the paid-tool recipes. [`dataforseo.md`](dataforseo.md) carries **the spend and
honesty rules that apply here too**: say before you spend, label every number as the
vendor's estimate with its date and database, Search Console wins for your own site, never
fill a gap, read only. They are not repeated.

Verified against each vendor's documentation in November 2026 (verified 2026-11). Confirm
column names against a live response before parsing at scale; both vendors version their
schemas.

## Which tool for which workflow

The most useful thing in this file. These tools are not interchangeable, and choosing by
habit rather than by capability is how an analysis ends up impossible halfway through.

| Workflow | DataForSEO | Ahrefs | Semrush |
|---|---|---|---|
| Cannibalisation: two of your URLs on one keyword | **Yes.** `ranked_keywords` returns an item per ranked element | **No.** `organic-keywords` returns `best_position_url`, one URL per keyword | Not verified here |
| AI citations across several engines | Google AI Overviews only (its AI Optimization module is not verified here) | **Yes.** Brand Radar, eight engines | Not verified here |
| Geo-grid from precise coordinates | **Yes.** `location_coordinate` | Not verified here | Not verified here |
| Render gap, with and without JavaScript | **Yes.** `on_page/instant_pages` | Not verified here | Not verified here |
| Authority gap against named competitors | Yes | Yes | **Yes.** `backlinks_overview` |
| Keyword gap against a named competitor | Partial | Yes | **Yes.** `domain_domains` |
| Period-over-period change in one call | Not verified here | **Yes.** `date_compared` | Not verified here |
| Cost model | per call | API units, 60 requests a minute | **per line returned**, so predictable |

"Not verified here" means exactly that: nothing in these files has checked it, not that the
tool cannot do it. Say which it is in a finding.

**Before planning around either of these, check the user can actually call it.** Ahrefs
documents API v3 access from the Lite plan upward, and separately states that new
applications require an Enterprise subscription for activation, so an existing key and a new
key are not the same situation. Semrush API access depends on the plan carrying API units.
Confirm access before designing a workflow that needs it.

---

# Ahrefs

Base URL `https://api.ahrefs.com/v3/{tool}/{endpoint}`. Rate limit 60 requests a minute by
default; exceeding it returns `429`.

**The `select` pattern.** Most endpoints require `select`, a comma-separated list of the
columns to return, with valid identifiers defined in each endpoint's response schema. This
is a cost control as much as a convenience: ask only for what the analysis uses, because
some columns are billed individually.

## A1. AI citations across eight engines

**Answers:** which of our pages are being cited by assistants, and by which ones?

This is the reason to reach for Ahrefs. Everything else here has an equivalent elsewhere;
multi-engine citation data does not.

`POST https://api.ahrefs.com/v3/brand-radar/cited-pages`

```json
{ "select": ["url", "title", "responses"],
  "data_source": ["chatgpt"],
  "brands": [{ "url_groups": [{ "target": "example.com", "scope": "domain" }] }],
  "date": "2026-11-01",
  "limit": 1000 }
```

`select` and `data_source` are both required. `data_source` accepts `chatgpt`,
`google_ai_overviews`, `google_ai_mode`, `gemini`, `perplexity`, `copilot`, `claude`, `grok`,
plus `google_ai_overviews_keywords` and `google_ai_mode_keywords`. `brands` and `competitors`
take `names` and `url_groups`, where each group needs a `target` and a `scope` of `url`,
`path`, `domain` or `subdomains`.

**Three limits that decide how you use it:**

1. **The response does not say which engine, and does not return the prompt.** You get
   `url`, `title` and `responses` (the number of responses citing that page). So to attribute
   by engine, **run one call per `data_source`** and keep them separate. A combined call
   gives you a total you cannot break down.
2. **`claude` supports custom prompts only.** Use `prompts: "custom"` with a `report_id`
   for that source.
3. **`volume` is deprecated (2026-03-24) and `mentions` is deprecated (2026-02-10).** Do not
   build a report on either.

**Cost:** requests returning only custom-prompt data are free; requests including Ahrefs'
own prompt data consume API units. So a tracked set of your own prompts is cheap to run
often, which is the better habit anyway.

**What it does not change.** This is a vendor's sampled observation of volatile surfaces,
not an engine reporting on you. Confidence is `inferred`, every figure is dated, and
**eligibility remains the only claimable outcome**, exactly as `surfaces/chatgpt.md` says.
Run competitors in the same call pattern: finding that the surface favours nobody
consistently for your topics is a real and useful finding.

## A2. What changed between two dates, in one call

**Answers:** what actually moved since the last audit?

`GET https://api.ahrefs.com/v3/site-explorer/organic-keywords` requires `select`, `target`
and `date` (`YYYY-MM-DD`). The optional **`date_compared`** returns the comparison in the
same response, which is the neat part: one call, both periods, no reconciling two exports.

Useful `select` columns: `keyword`, `best_position` ("the top position your target ranks for
in the organic search results for a keyword"), `best_position_url` ("the ranking URL in
organic search results"), `volume`, `sum_traffic`. `volume` and `sum_traffic` are billed at
10 units each, so leave them out when the question is only about position.

`mode` accepts `exact`, `prefix`, `domain` or `subdomains` and defaults to `subdomains`.
Set it deliberately: the default silently includes subdomains you may not have meant.

This feeds the progress half of the Operations loop and `content-decay.md`'s "report the
trend, not the datapoint".

## A3. Striking distance, filtered server-side

The same endpoint takes a `where` JSON filter expression and `order_by`. Filter
`best_position` to the 11-to-20 band and order by `volume` descending to get the
striking-distance list without pulling the whole keyword set and filtering locally, which
costs less and returns faster.

## What Ahrefs cannot do here

**Cannibalisation.** `organic-keywords` returns `best_position_url`, one ranking URL per
keyword, so two of your own pages competing for one query does not appear. Use DataForSEO's
`ranked_keywords` for that analysis, or say it was not performed. Do not approximate it by
inference and present the result as a finding.

---

# Semrush

**Two different base URLs**, which is the most common integration mistake:

- Domain and keyword reports: `https://api.semrush.com/`
- Backlinks reports: `https://api.semrush.com/analytics/v1/`

Responses are CSV with a header row, which is convenient: **confirm the column codes against
that header** rather than trusting any mapping, including the one below.

**Billing is per line returned**, which makes Semrush the most predictable of the three to
budget. Always set `display_limit`: omitting it defaults to 10,000 lines, and on an
expensive report type that is a large accidental bill.

## S1. Keyword gap against a named competitor

**Answers:** what do they rank for that we do not?

`type=domain_domains` (Domain vs Domain) takes `domains` (plural) rather than `domain`.
Required alongside it: `key`, `database`, and `type`.

**It is the most expensive report here: 80 API units per line, 400 for historical.** So set
`display_limit` low, sort to the rows you actually need, and say the number of lines before
running it. A 10,000-line default on this report is not a mistake you make twice.

`earning-angles.md` requires a comparison against **named** competitors rather than a
category. Use S3 first to discover who they actually are.

## S2. Organic keyword inventory

`type=domain_organic`, required `key`, `type`, `domain`, `database`. At **10 units per line**
(50 historical) this is the cheapest per-line keyword inventory of the three tools, which
makes it the sensible default for a first pass on a site you do not own.

`export_columns` is optional but always worth setting. For this report the sample response
uses `Ph` (keyword), `Po` (position), `Nq` (search volume), `Ur` (URL) and `Tr` (traffic).
Those are read from the documented example rather than from a published mapping table, so
confirm them against the CSV header on the first call.

`database` selects the country and is not optional in effect: a figure without the database
named is unreportable, because "1,900 searches" means nothing without knowing which market.

## S3. Who actually competes, discovered rather than assumed

**Answers:** who are the named competitors?

`type=domain_organic_organic` returns competitors in organic search, at 40 units per line.

This is worth running before any gap analysis, because the competitors a business names in a
meeting are frequently not the ones holding its search demand. The sites taking the traffic
are often publishers, marketplaces or comparison sites the business does not think of as
competitors at all, and a plan built against the wrong set is wasted. Feed the result into
S1 and into `earning-angles.md`.

## S4. Backlink profile summary

`type=backlinks_overview` against `https://api.semrush.com/analytics/v1/`, with `target`,
`target_type` and a required `export_columns`.

Documented example columns include `ascore` (authority score), `total` (total backlinks),
`domains_num` (referring domains), `urls_num`, `ips_num`, `ipclassc_num`, `follows_num`,
`nofollows_num` and `sponsored_num`.

**`domains_num` is the number that matters, not `total`.** The same trap as everywhere else:
one partner with a sitewide footer link inflates `total` into the thousands from a single
domain, and a comparison on it says the opposite of the truth. `follows_num` against
`nofollows_num` tells you how much of the profile passes authority.

`type=backlinks_refdomains` lists the referring domains themselves, with per-domain authority
score, backlink count, country and first and last seen dates, which is the input to the lost
links and reclamation work.

A figure of 40 API units per request appears on the general backlinks documentation; it was
not confirmed for the analytics endpoint specifically. Check the current pricing before a
large run rather than quoting that number to anyone.

---

## What none of these three is

They are models of the web, built by crawling and estimation. None of them is:

- **Your traffic.** Search Console and your analytics are the facts. Vendor traffic
  estimates are for comparing domains against each other, never for reporting your own
  numbers.
- **Complete.** No backlink index sees every link, and no keyword database sees every query.
  A gap in a report is a gap in the index, not a fact about the web.
- **A reason to buy one.** The pack works with none connected. Never tell a user they need a
  particular product; use what is already in their environment, as
  [`live-data-integrations.md`](../live-data-integrations.md) requires.

When two vendors disagree, say so and say which you used. Picking the flattering number and
reporting it alone is the quiet way this discipline loses its credibility.
