# Search Console: direct-API recipe

Use this when no tool in the environment provides search performance or URL inspection, but the user has configured Google credentials. If an MCP tool or connector already wraps Search Console, use that instead and keep these notes for the limits and pitfalls, which are the same. Everything here is read-only. Facts verified 2026-10 against Google's own documentation (sources at the end).

---

## What the API exposes, and what it does not

| Exposed (read) | Not exposed |
|---|---|
| Search Analytics: clicks, impressions, CTR, position by query, page, country, device, date, hour, search appearance | The **Page indexing report** as a whole (reason counts, example URLs). Only per-URL inspection is available. |
| URL Inspection: per-URL index status, coverage state, Google-selected and user-declared canonical, last crawl, robots and noindex state, rich results | The **generative AI performance report** (AI Overviews, AI Mode). UI and export only. |
| Sitemaps: list and read submitted sitemaps, errors and warnings | Live URL test, "Request indexing", removals, Core Web Vitals report, Links report, manual actions, crawl stats |
| Sites: the properties this account can see and its permission level | Anonymised queries (counted in totals, never listed) |

When you need something from the right-hand column, ask the user for an export (most reports have an Export button) or a screenshot, and record it as a file source in `data_sources`.

---

## Auth

The API accepts OAuth 2.0 only. Use the read-only scope: `https://www.googleapis.com/auth/webmasters.readonly`. (`.../auth/webmasters` is read and write: do not use it.)

**Service account (best for agents and CI):**
1. In Google Cloud, create a project, enable the **Google Search Console API**, create a service account and download its JSON key. Store the key outside the repo.
2. In Search Console, open the property, go to **Settings > Users and permissions > Add user**, and add the service account's email address (`name@project.iam.gserviceaccount.com`). **Restricted** permission gives view access to most data, including Performance. Grant **Full** if inspection calls are refused. Only an owner can add users.
3. Set `GOOGLE_APPLICATION_CREDENTIALS` to the key file's path.

**OAuth client (a person's own access):** create an OAuth client ID (desktop app) in the same project, run a local consent flow once with the read-only scope, and keep the refresh token in the OS keychain or a secrets manager, never in `.seo/`.

**`siteUrl` formats.** A Domain property is `sc-domain:example.com`. A URL-prefix property is the full prefix with its trailing slash, `https://www.example.com/`. In a path segment it must be URL-encoded: `sc-domain%3Aexample.com`, `https%3A%2F%2Fwww.example.com%2F`. Call `sites.list` first to see exactly which properties the credential can read.

---

## Quotas (verified 2026-10)

| Resource | Limits |
|---|---|
| Search Analytics | 1,200 queries per minute per site and per user; 40,000 per minute and 30,000,000 per day per project. Also a load quota, measured over 10-minute and 1-day windows, that expensive queries use up faster. |
| URL Inspection | **2,000 per day and 600 per minute per site**; 15,000 per minute and 10,000,000 per day per project. |
| Everything else (sites, sitemaps) | 20 per second and 200 per minute per user; 100,000,000 per day per project. |

The URL Inspection limit is the one you will meet. Inspect a **sample** per template and per indexing reason, not every URL.

---

## Search Analytics query

`POST https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query`

Request body fields:
- `startDate`, `endDate` (required): `YYYY-MM-DD`, in Pacific Time.
- `dimensions`: any of `query`, `page`, `country`, `device`, `searchAppearance`, `date`, `hour`.
- `type`: `web` (default), `image`, `video`, `news`, `discover`, `googleNews`.
- `dimensionFilterGroups`: filters with operators `equals`, `contains`, `notEquals`, `notContains`, `includingRegex`, `excludingRegex`.
- `aggregationType`: `auto` (default), `byPage`, `byProperty`.
- `rowLimit`: 1 to 25,000 (default 1,000). `startRow`: zero-based offset.
- `dataState`: `final` (default), `all` (includes fresh, incomplete data), `hourly_all`.

Rows come back sorted by clicks, descending (by date when grouped by date). Each row has `keys`, `clicks`, `impressions`, `ctr` (0 to 1) and `position`.

### curl

`$TOKEN` is an OAuth access token with the read-only scope (the Python snippet below prints one from a service account).

```bash
SITE='sc-domain%3Aexample.com'
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://www.googleapis.com/webmasters/v3/sites/$SITE/searchAnalytics/query" \
  -d '{
    "startDate": "2026-07-01", "endDate": "2026-09-28",
    "dimensions": ["page", "query"],
    "type": "web",
    "dimensionFilterGroups": [{"filters": [{"dimension": "page", "operator": "contains", "expression": "/blog/"}]}],
    "rowLimit": 25000, "startRow": 0
  }'
```

PowerShell:

```powershell
$site = [uri]::EscapeDataString('sc-domain:example.com')
$body = @{ startDate='2026-07-01'; endDate='2026-09-28'; dimensions=@('page','query'); rowLimit=25000; startRow=0 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "https://www.googleapis.com/webmasters/v3/sites/$site/searchAnalytics/query" `
  -Headers @{ Authorization = "Bearer $env:GSC_TOKEN" } -ContentType 'application/json' -Body $body
```

### Python (paged)

```python
# pip install google-api-python-client google-auth
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
creds = service_account.Credentials.from_service_account_file(
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=SCOPES)
sc = build("searchconsole", "v1", credentials=creds)

def query_all(site, body):
    rows, start = [], 0
    while True:
        resp = sc.searchanalytics().query(
            siteUrl=site, body={**body, "rowLimit": 25000, "startRow": start}).execute()
        batch = resp.get("rows", [])
        rows += batch
        if len(batch) < 25000:
            return rows
        start += 25000

rows = query_all("sc-domain:example.com", {
    "startDate": "2026-07-01", "endDate": "2026-09-28",
    "dimensions": ["page", "query"], "type": "web"})
```

To print a token for curl: `from google.auth.transport.requests import Request; creds.refresh(Request()); print(creds.token)`. Do not write it to a file.

### Node

```js
// npm install googleapis
const { google } = require('googleapis');
const auth = new google.auth.GoogleAuth({ scopes: ['https://www.googleapis.com/auth/webmasters.readonly'] });
const sc = google.searchconsole({ version: 'v1', auth });

const res = await sc.searchanalytics.query({
  siteUrl: 'sc-domain:example.com',
  requestBody: { startDate: '2026-07-01', endDate: '2026-09-28', dimensions: ['page'], rowLimit: 25000, startRow: 0 },
});
console.log(res.data.rows ?? []);
```

### Paging and completeness

- Page by re-running the same query with `startRow` increased by 25,000 until a response has fewer rows than you asked for (or none).
- The API returns the **top rows, not all rows**. Google documents a ceiling of 50,000 rows of data per day per search type, sorted by clicks. For a large site, query **one day at a time** and add the days up, and filter by page path to split the site into sections.
- Grouping by page or query can drop some data so the query completes; totals from a grouped query will be lower than the property total.

### Pitfalls

- **Data lag.** Data is usually available after 2 to 3 days. End windows at least 3 days ago, or check `metadata.first_incomplete_date` when using `dataState: all`. Never compare a window that includes incomplete days with one that does not.
- **Retention.** Search Console keeps 16 months of performance data. Store your own snapshots if you need longer baselines.
- **Anonymised queries.** Rare queries are withheld to protect privacy. They count in chart totals but never appear as rows, so query rows will not sum to the page total. Say so when you report a gap.
- **Page versus property aggregation.** Data grouped by query, country, device or date is aggregated by property; grouped by page or search appearance it is aggregated by page. Impressions, clicks and position differ between the two. Compare like with like.
- **Position is an average** of the site's topmost result position. Small samples swing wildly: treat positions with very few impressions as noise.
- **Dates are Pacific Time.**
- **AI features are in the totals.** Appearances in AI Overviews and AI Mode are counted in the Performance report under the Web search type, mixed with classic results.

---

## URL Inspection

`POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect`

Body: `inspectionUrl` (must sit under the property), `siteUrl`, optional `languageCode`. It returns the status of the version **in Google's index**, not a live test.

Fields under `inspectionResult.indexStatusResult`:

| Field | Values and meaning |
|---|---|
| `verdict` | `PASS` (indexed), `FAIL` (error), `NEUTRAL` (excluded) |
| `coverageState` | The Page indexing reason as text, for example "Crawled - currently not indexed" |
| `robotsTxtState` | `ALLOWED`, `DISALLOWED` |
| `indexingState` | `INDEXING_ALLOWED`, `BLOCKED_BY_META_TAG`, `BLOCKED_BY_HTTP_HEADER` |
| `pageFetchState` | `SUCCESSFUL`, `SOFT_404`, `NOT_FOUND`, `SERVER_ERROR`, `ACCESS_DENIED`, `ACCESS_FORBIDDEN` (and others) |
| `lastCrawlTime` | RFC 3339 timestamp of the last crawl by the primary crawler |
| `crawledAs` | `MOBILE` or `DESKTOP` |
| `googleCanonical` | The canonical Google selected |
| `userCanonical` | The canonical the page declares |
| `sitemap`, `referringUrls` | Sitemaps that list the URL and pages that link to it, as known to Google (not exhaustive) |

Also `inspectionResultLink` (open it in the UI), `richResultsResult` (absent when no rich results are detected) and `ampResult`. `mobileUsabilityResult` is deprecated.

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect" \
  -d '{"inspectionUrl": "https://example.com/blog/post", "siteUrl": "sc-domain:example.com"}'
```

```python
res = sc.urlInspection().index().inspect(body={
    "inspectionUrl": "https://example.com/blog/post",
    "siteUrl": "sc-domain:example.com"}).execute()
s = res["inspectionResult"]["indexStatusResult"]
mismatch = s.get("googleCanonical") and s.get("userCanonical") and s["googleCanonical"] != s["userCanonical"]
```

```js
const r = await sc.urlInspection.index.inspect({
  requestBody: { inspectionUrl: 'https://example.com/blog/post', siteUrl: 'sc-domain:example.com' },
});
const s = r.data.inspectionResult.indexStatusResult;
```

Pitfalls: one URL per call, so budget against 2,000 per day per site; space calls under 600 per minute; the result can lag the live page by days or weeks, so a recent fix will not show until Google recrawls; compare canonicals after normalising trailing slashes and protocol, and report a mismatch only when they truly differ.

---

## Sitemaps

- List: `GET https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps`
- Get one: `GET https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}` (feedpath URL-encoded)

Fields: `path`, `lastSubmitted`, `lastDownloaded`, `isPending`, `isSitemapsIndex`, `type`, `warnings`, `errors`, `contents[].submitted`. `contents[].indexed` is **deprecated: do not use it** as an index count. `submit` and `delete` exist but are writes: leave them to the user.

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aexample.com/sitemaps"
```

Use it to check that Google has downloaded the sitemap recently and that `errors` is 0, then compare the sitemap's URLs with the served sitemap (Reach owns the fix).

---

## The Indexing API: do not use it for ordinary pages

Google's Indexing API is only for pages with `JobPosting` structured data or a `BroadcastEvent` embedded in a `VideoObject`. Using it for anything else is outside its documented purpose, and Google warns that abuse can lead to access being revoked. For normal pages, fix discoverability (internal links, sitemaps, `lastmod`) and let Google crawl. The pack never calls it unless the site genuinely publishes job postings or livestreams and the user asks.

---

## The generative AI performance report

Search Console has a **Generative AI performance report** for Search (AI Overviews, AI Mode) and one for Discover, rolled out to all sites by 31 August 2026. It shows **impressions only** (no clicks), by page, country, device and date, with a 1,000-row table limit. Google documents an Export button; it documents **no API access**, and the Search Analytics `type` values do not include it (verified 2026-10). So:
- read it through a tool in the environment only if that tool's description says it covers this report;
- otherwise ask the user to export it (CSV or Sheets) and point you to the file;
- record it in `data_sources` as a file source with its date range.

---

## Sources (verified 2026-10)

- Search Analytics query: https://developers.google.com/webmaster-tools/v1/searchanalytics/query
- Getting all your data (paging, 50,000 rows, data lag): https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data
- Usage limits: https://developers.google.com/webmaster-tools/limits
- API reference index (base URLs): https://developers.google.com/webmaster-tools/v1/api_reference_index
- URL Inspection: https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect and https://developers.google.com/webmaster-tools/v1/urlInspection.index/UrlInspectionResult
- Sitemaps: https://developers.google.com/webmaster-tools/v1/sitemaps
- Sites and `siteUrl` formats: https://developers.google.com/webmaster-tools/v1/sites
- Authorisation and scopes: https://developers.google.com/webmaster-tools/v1/how-tos/authorizing
- Users and permissions: https://support.google.com/webmasters/answer/7687615
- Data discrepancies, anonymised queries, 2 to 3 day lag: https://support.google.com/webmasters/answer/17010575
- Page indexing report reasons: https://support.google.com/webmasters/answer/7440203
- 16 months of data: https://support.google.com/analytics/answer/13682862
- AI features in the Performance report: https://developers.google.com/search/docs/appearance/ai-features
- Generative AI performance report: https://support.google.com/webmasters/answer/16984139
- Indexing API scope: https://developers.google.com/search/apis/indexing-api/v3/quickstart
