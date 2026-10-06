# Analytics and business data: direct-API recipe

Use this for the capability **revenue or leads by landing page**: which pages people land on from organic search, and what those sessions go on to do. GA4 is the common free source. A CRM (HubSpot, Salesforce) or a warehouse often holds the truer answer: leads, pipeline and revenue. Prefer a tool already in the environment; use the GA4 Data API directly only when the user has configured credentials. Everything here is read-only. Facts verified 2026-10.

---

## What it adds

- **Prioritisation by value.** A page with modest traffic and many key events can matter more than a high-traffic page that converts nothing. Weight `prioritisation.md` impact by key events or revenue where present.
- **Measuring changes.** After a logged change, organic sessions and key events on the changed pages are the business-side check beside Search Console clicks.
- **AI assistant referrals.** GA4's default channel group has an **AI Assistant** channel (below).

GA4 counts sessions in the browser; Search Console counts clicks on Google. They never match exactly (consent banners, blockers, redirects, attribution). Compare trends within one source, never totals across the two.

---

## Auth

Scope: `https://www.googleapis.com/auth/analytics.readonly`.

1. In Google Cloud, enable the **Google Analytics Data API** and create a service account with a JSON key, stored outside the repo.
2. In GA4, go to **Admin > Access management** (property level) and add the service account's email with the **Viewer** role. Viewer reads reports and changes nothing.
3. Set `GOOGLE_APPLICATION_CREDENTIALS`. You also need the numeric **property ID** (Admin > Property details), for example `properties/123456789`.

An official, experimental **Google Analytics MCP server** exists (`googleanalytics/google-analytics-mcp`) with read-only tools such as `run_report`, using the same read-only scope. If the user has it, use it.

---

## Quotas (verified 2026-10)

Standard properties, Core reporting: 200,000 tokens per day, 40,000 per hour, 14,000 per project per property per hour, 10 concurrent requests, 10 server errors per hour, 120 potentially thresholded requests per hour. Analytics 360 is ten times higher for tokens. Add `"returnPropertyQuota": true` to see what each request consumed.

---

## runReport

`POST https://analyticsdata.googleapis.com/v1beta/properties/{propertyId}:runReport`

Useful API names (all in the Data API schema):
- Dimensions: `landingPage`, `landingPagePlusQueryString`, `sessionDefaultChannelGroup`, `sessionSource`, `sessionMedium`, `pagePath`, `date`.
- Metrics: `sessions`, `engagedSessions`, `keyEvents`, `sessionKeyEventRate`, `totalRevenue`. Per-event variants use the form `keyEvents:<event_name>`.

`limit` defaults to 10,000 and the API returns at most 250,000 rows per request. Page with `offset` until you have `rowCount` rows.

### Organic landing pages with key events

```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://analyticsdata.googleapis.com/v1beta/properties/123456789:runReport" \
  -d '{
    "dateRanges": [{"startDate": "2026-07-01", "endDate": "2026-09-28"}],
    "dimensions": [{"name": "landingPage"}],
    "metrics": [{"name": "sessions"}, {"name": "keyEvents"}, {"name": "totalRevenue"}],
    "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup",
                                   "stringFilter": {"matchType": "EXACT", "value": "Organic Search"}}},
    "orderBys": [{"metric": {"metricName": "sessions"}, "desc": true}],
    "limit": 10000, "offset": 0
  }'
```

### Python

```python
# pip install google-analytics-data
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Dimension, Metric, FilterExpression, Filter)

client = BetaAnalyticsDataClient()  # reads GOOGLE_APPLICATION_CREDENTIALS
def report(channel, offset=0):
    return client.run_report(RunReportRequest(
        property="properties/123456789",
        date_ranges=[DateRange(start_date="2026-07-01", end_date="2026-09-28")],
        dimensions=[Dimension(name="landingPage")],
        metrics=[Metric(name="sessions"), Metric(name="keyEvents")],
        dimension_filter=FilterExpression(filter=Filter(
            field_name="sessionDefaultChannelGroup",
            string_filter=Filter.StringFilter(value=channel))),
        limit=10000, offset=offset))

rows, offset = [], 0
while True:
    r = report("Organic Search", offset)
    rows += r.rows
    offset += len(r.rows)
    if not r.rows or offset >= r.row_count:
        break
```

### Node

```js
// npm install @google-analytics/data
const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const client = new BetaAnalyticsDataClient();
const [res] = await client.runReport({
  property: 'properties/123456789',
  dateRanges: [{ startDate: '2026-07-01', endDate: '2026-09-28' }],
  dimensions: [{ name: 'landingPage' }],
  metrics: [{ name: 'sessions' }, { name: 'keyEvents' }],
  dimensionFilter: { filter: { fieldName: 'sessionDefaultChannelGroup', stringFilter: { value: 'Organic Search' } } },
  limit: 10000,
});
```

---

## The AI Assistant channel

GA4's default channel group includes **AI Assistant**: traffic where the medium is exactly `ai-assistant`, which GA4 sets (with campaign `(ai-assistant)`) when the referrer matches its list of AI assistants. Run the report above with `"value": "AI Assistant"` to see which landing pages AI assistants send people to. Caveat (judgement): some AI clicks arrive without a referrer, from apps for example, and land in Direct, so treat the channel as a floor, not a count of AI influence. Organic Search is "source matches a list of search sites, or medium exactly matches organic", which includes Google traffic from AI Overviews and AI Mode.

---

## CRM and warehouse data

When the environment has a CRM or warehouse tool (HubSpot, Salesforce, BigQuery, Snowflake), look for the field that records the **first landing page** or **original source** on a contact or deal, then aggregate leads, pipeline or revenue by landing page for organic contacts. Rules:
- read only: never create, update or delete records, and never run a query that writes or creates tables;
- warn before a query that scans a lot of data on a billed warehouse;
- keep aggregates by page; never copy names, emails or deal records into `.seo/` or chat;
- record the object, field and date range in `data_sources`.

---

## Pitfalls

- `landingPage` is a path without the host; join it to Search Console's full `page` URLs by path, and strip query strings unless you used `landingPagePlusQueryString`.
- **Thresholding** can hide rows in properties with Google signals enabled; low-volume pages may vanish. Say so rather than reading absence as zero.
- **Key events** are whatever the property marks as key events. Ask what they mean for this business before treating them as conversions.
- Data in the latest day or two can still change; end windows a couple of days back.

---

## Sources (verified 2026-10)

- runReport: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
- Quotas: https://developers.google.com/analytics/devguides/reporting/data/v1/quotas
- API schema (dimensions and metrics): https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
- Client libraries and credentials: https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart
- Default channel group (AI Assistant, Organic Search): https://support.google.com/analytics/answer/9756891
- Access management: https://support.google.com/analytics/answer/9305788
- Google Analytics MCP server: https://github.com/googleanalytics/google-analytics-mcp
