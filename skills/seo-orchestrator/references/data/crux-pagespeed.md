# CrUX and PageSpeed Insights: direct-API recipe

Use this for the capability **Core Web Vitals field data**: how real Chrome users experience a page or a whole origin. `seo-performance` owns the diagnosis and fixes; this file is the data recipe. Prefer a CrUX or PageSpeed tool already in the environment. Facts verified 2026-10.

---

## Which API

| Need | Use |
|---|---|
| Current p75 LCP, INP, CLS for a URL or origin | **CrUX API** `records:queryRecord` |
| A trend over months, before and after a release | **CrUX History API** `records:queryHistoryRecord` |
| A lab run (Lighthouse) for debugging | **PageSpeed Insights API** `runPagespeed`, or local Lighthouse |

Google says it plans to **stop including CrUX field data in the PageSpeed Insights API** and recommends the CrUX API or CrUX History API instead (verified 2026-10). New code should read field data from CrUX and use PSI only for the lab half.

---

## The free key

Both CrUX APIs need a Google Cloud **API key** (not OAuth). In a Cloud project, enable the **Chrome UX Report API**, create an API key under Credentials, restrict it to that API, and set it as an environment variable such as `CRUX_API_KEY`. The API is free. Never commit the key or print it in reports.

Quota: **150 queries per minute per Google Cloud project**, shared by the CrUX API and the History API, free, and not increasable by payment.

---

## CrUX API

`POST https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=API_KEY`

Body: `origin` (`https://example.com`) **or** `url` (a page), optional `formFactor` (`PHONE`, `DESKTOP`, `TABLET`; omit for all), optional `metrics` list. Metrics include `largest_contentful_paint`, `interaction_to_next_paint`, `cumulative_layout_shift`, `first_contentful_paint`, `experimental_time_to_first_byte`, `round_trip_time`, `navigation_types`, `form_factors`, `largest_contentful_paint_resource_type` and the LCP image sub-parts.

Each metric returns a three-bin histogram and a `p75`. The window is a **rolling 28 days** (`collectionPeriod.firstDate` to `lastDate`), updated daily around 04:00 UTC on a best-effort basis.

```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/pricing", "formFactor": "PHONE",
       "metrics": ["largest_contentful_paint", "interaction_to_next_paint", "cumulative_layout_shift"]}'
```

PowerShell:

```powershell
$body = @{ origin = 'https://example.com'; formFactor = 'PHONE' } | ConvertTo-Json
Invoke-RestMethod -Method Post -ContentType 'application/json' -Body $body `
  -Uri "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$env:CRUX_API_KEY"
```

Python:

```python
import os, requests
r = requests.post(
    "https://chromeuxreport.googleapis.com/v1/records:queryRecord",
    params={"key": os.environ["CRUX_API_KEY"]},
    json={"url": "https://example.com/pricing", "formFactor": "PHONE"}, timeout=30)
if r.status_code == 404:
    print("No CrUX record: not enough real-user data for this URL. Try the origin.")
else:
    m = r.json()["record"]["metrics"]
    print({k: v.get("percentiles", {}).get("p75") for k, v in m.items()})
```

Node:

```js
const res = await fetch(`https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=${process.env.CRUX_API_KEY}`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ origin: 'https://example.com', formFactor: 'PHONE' }),
});
const data = res.status === 404 ? null : await res.json();
```

---

## CrUX History API

`POST https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=API_KEY`

Same body as above plus `collectionPeriodCount`: 25 periods by default, up to 40. Periods are weekly (each still a 28-day window), updated each Monday around 04:00 UTC. The response has `collectionPeriods` and, per metric, `percentilesTimeseries.p75s` (and histogram or fraction timeseries).

```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=$CRUX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"origin": "https://example.com", "formFactor": "PHONE", "collectionPeriodCount": 40,
       "metrics": ["interaction_to_next_paint"]}'
```

Use it for before-and-after: find the first period whose window starts after the release date. Because each point is a 28-day window, a change shows in full only about four weeks after it ships.

---

## PageSpeed Insights API (lab)

`GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&strategy=mobile&category=performance&key=API_KEY`

A key is optional but recommended for automated use; Google does not publish the quota on the API pages, so check the project's Quotas page in the Cloud Console. The response has `lighthouseResult` (lab) and, for now, `loadingExperience` and `originLoadingExperience` (field data, being phased out of this API).

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Fexample.com%2F&strategy=mobile&category=performance&key=$PAGESPEED_API_KEY"
```

---

## Pitfalls

- **404 means no data**, not a failing page. The API returns 404 when CrUX has no record. Check the URL exactly as users reach it (protocol, `www`, final URL after redirects), then fall back to the origin. Say "not enough real-user data" in the report, never a score.
- **Page-level data needs traffic.** Low-traffic pages often have only origin data. Report which level you used.
- **URL normalisation.** The API may apply basic normalisation to a URL so the lookup succeeds, and reports the original and normalised URLs in `urlNormalizationDetails`. It does not follow redirects. Note the URL it actually used.
- **Field moves slowly.** A fix verified in the lab and the served markup shows in field data over the following 28 days. Do not claim a field improvement the same week.
- **Form factor matters.** Report phone and desktop separately; mobile is usually what fails.

---

## Sources (verified 2026-10)

- CrUX API: https://developer.chrome.com/docs/crux/api
- CrUX History API: https://developer.chrome.com/docs/crux/history-api
- CrUX API guide (404 for no data): https://developer.chrome.com/docs/crux/guides/crux-api
- PageSpeed Insights API, get started (field data being discontinued, key optional): https://developers.google.com/speed/docs/insights/v5/get-started
- PageSpeed Insights, field versus lab and origin fallback: https://developers.google.com/speed/docs/insights/v5/about
