# Bing Webmaster Tools: direct-API recipe

Use this for Bing's view of the site: search performance by query and page, crawl issues, index details per URL, and inbound links. Bing also grounds Microsoft Copilot answers, which is why its **AI Performance** report matters. Prefer a Bing tool already in the environment. Everything here is read-only. Facts verified 2026-10.

---

## Auth

Two methods, per Microsoft: **OAuth 2.0 (recommended)** or an **API key**. For an API key: sign in to Bing Webmaster Tools, add and verify the site, then **Settings > API Access**, accept the terms and **Generate API Key**. One key per user, valid for all of that user's verified sites. Store it as an environment variable such as `BING_WEBMASTER_API_KEY`; never commit it.

## Endpoints

Use the JSON format. **Legacy SOAP and POX (XML) endpoints retire on 31 August 2026**; Microsoft says to migrate to the REST APIs.

- GET: `https://ssl.bing.com/webmaster/api.svc/json/METHOD_NAME?apikey=API_KEY&param1=VALUE`
- POST: `https://ssl.bing.com/webmaster/api.svc/json/METHOD_NAME?apikey=API_KEY`

Errors return HTTP 400 with a JSON body such as `{"ErrorCode":3,"Message":"InvalidApiKey"}`. Dates come back in the .NET form `"/Date(1316156400000-0700)/"` (milliseconds since the epoch, then the offset).

## Useful read methods

| Method | Returns |
|---|---|
| `GetUserSites` | Sites the user can read |
| `GetRankAndTrafficStats(siteUrl)` | Daily impressions and clicks for the site |
| `GetQueryStats(siteUrl)` | Top queries: impressions, clicks, average click and impression position. Microsoft notes the data updates weekly. |
| `GetPageStats(siteUrl)` | Top pages with traffic |
| `GetQueryPageStats(siteUrl, query)`, `GetPageQueryStats(siteUrl, page)` | Pages for a query, queries for a page |
| `GetUrlInfo(siteUrl, url)`, `GetUrlTrafficInfo` | Index details and traffic for one URL |
| `GetCrawlStats`, `GetCrawlIssues` | Crawl volume and issues |
| `GetLinkCounts`, `GetUrlLinks` | Pages with inbound links, and links to one URL |
| `GetFeeds` | Submitted sitemaps and feeds |
| `GetKeywordStats` | Historical statistics for a keyword |

Write methods exist (`SubmitUrl`, `SubmitUrlBatch`, `SubmitFeed`, blocking and settings methods). Do not call them unless the user asks. Bing's URL submission and IndexNow are publishing actions, not data reads.

```bash
curl -s "https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats?siteUrl=https%3A%2F%2Fexample.com%2F&apikey=$BING_WEBMASTER_API_KEY"
```

PowerShell:

```powershell
$site = [uri]::EscapeDataString('https://example.com/')
Invoke-RestMethod "https://ssl.bing.com/webmaster/api.svc/json/GetPageStats?siteUrl=$site&apikey=$env:BING_WEBMASTER_API_KEY"
```

Python:

```python
import os, re, requests, datetime as dt
r = requests.get("https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats",
                 params={"siteUrl": "https://example.com/", "apikey": os.environ["BING_WEBMASTER_API_KEY"]},
                 timeout=30)
rows = r.json()["d"]
def to_date(s):  # "/Date(1316156400000-0700)/"
    return dt.datetime.utcfromtimestamp(int(re.search(r"\d+", s).group()) / 1000).date()
```

Node:

```js
const u = new URL('https://ssl.bing.com/webmaster/api.svc/json/GetPageStats');
u.searchParams.set('siteUrl', 'https://example.com/');
u.searchParams.set('apikey', process.env.BING_WEBMASTER_API_KEY);
const { d: rows } = await (await fetch(u)).json();
```

Paging: the stats methods above take only the site (and a query or page) and return a list; there is no offset parameter. Quota: Microsoft does not document a read quota on these pages; space calls out and stop on errors. (`GetUrlSubmissionQuota` covers submissions only.)

---

## The AI Performance report

Bing Webmaster Tools has an **AI Performance** report (public preview since February 2026) showing when the site is cited in AI-generated answers across **Microsoft Copilot, AI-generated summaries in Bing, and select partner integrations**: total citations, average cited pages, grounding queries (a sample of the phrases the AI used to retrieve content), page-level citation activity and trends. A June 2026 update added intents, topics, citation share and comparison views.

**It is not in the Webmaster API** (verified 2026-10): the `IWebmasterApi` reference has no AI Performance method, and Microsoft's announcement mentions no API. Read it through a tool in the environment only if that tool's description says it covers this report; otherwise ask the user for an export (where the dashboard offers one) or a screenshot, and record it as a file source. It counts citations, not clicks or traffic, and does not cover Google, ChatGPT, Perplexity or other non-Microsoft surfaces.

---

## What Bing does not expose through the API

- **AI Performance** (citations, cited pages, grounding queries, intents, topics, citation share): dashboard only. Neither announcement mentions an API or an export (verified 2026-10).
- Anything not in the `IWebmasterApi` method list above. When the user needs a UI-only report, ask for an export or screenshot.

---

## Sources (verified 2026-10)

- API overview and SOAP/POX retirement note: https://learn.microsoft.com/en-us/bingwebmaster/
- Getting access (OAuth, API key steps): https://learn.microsoft.com/en-us/bingwebmaster/getting-access
- Protocols and JSON URL format: https://learn.microsoft.com/en-us/bingwebmaster/api-protocols
- Getting started (error format): https://learn.microsoft.com/en-us/bingwebmaster/getting-started
- Method list: https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi?view=bing-webmaster-dotnet
- GetQueryStats (weekly update, sample response): https://learn.microsoft.com/en-us/dotnet/api/microsoft.bing.webmaster.api.interfaces.iwebmasterapi.getquerystats?view=bing-webmaster-dotnet
- AI Performance announcement: https://blogs.bing.com/webmaster/2026/2/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- AI Performance June 2026 update: https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare
- Microsoft Q&A, no API for AI Performance: https://learn.microsoft.com/en-us/answers/questions/5780844/bing-webmaster-tools-ai-performance-report-is-ther
