# Core Web Vitals diagnosis: commands, causes and a worked example

Read this when you run `seo-performance`. It holds the commands for field and lab data in bash and PowerShell, the cause-and-fix detail for each metric, the Next.js specifics, third-party triage, the served-markup checks, and a worked example.

Facts here were checked against web.dev, developer.chrome.com, developers.google.com and nextjs.org in October 2026 (verified 2026-10). Re-check thresholds, API fields and framework props if this file is older than a few months: they do change (Lighthouse 13 renamed many audits; Next.js 16 deprecated `next/image`'s `priority`).

---

## 1. Field versus lab

| | Field (CrUX) | Lab (Lighthouse, DevTools) |
|---|---|---|
| What it is | Real Chrome users on their own devices and networks | One simulated load on one device and network profile |
| Window | Rolling 28 days, updated daily (History API: weekly, on Mondays) | The moment you run it |
| Statistic | 75th percentile, split by phone and desktop | One run (take the median of several) |
| INP | Measured | Not measurable; Total Blocking Time is a load-time proxy |
| Use it to | Decide what to fix and confirm, weeks later, that users benefit | Find the cause and prove a fix before it ships |

When both exist and disagree, the field decides priority: it is what users get. The lab explains why. Never present a lab score as the user's experience, and never present a field number as a property of today's code: it describes the last 28 days.

A page passes the Core Web Vitals assessment when the 75th percentile of LCP, INP and CLS are all Good. Thresholds (verified 2026-10, web.dev):

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP | ≤ 2.5 s | over 2.5 s up to 4.0 s | over 4.0 s |
| INP | ≤ 200 ms | over 200 ms up to 500 ms | over 500 ms |
| CLS | ≤ 0.1 | over 0.1 up to 0.25 | over 0.25 |
| TTFB (diagnostic only) | ≤ 0.8 s | over 0.8 s up to 1.8 s | over 1.8 s |

INP counts clicks, taps and key presses. Hovering, scrolling and zooming do not count. CLS is the largest burst of shifts, where a burst ("session window") groups shifts less than 1 second apart, up to 5 seconds in total.

---

## 2. Field data commands

Both APIs need a Google Cloud API key. The CrUX API requires one, enabled for the Chrome UX Report API, and allows 150 queries a minute per project at no cost. The PageSpeed Insights API documents the key as optional, but a keyless call can fail with a 429 quota error (seen 2026-10), so use a key. Keep keys in environment variables, never in committed files or reports.

### PageSpeed Insights API (field and lab in one call)
`loadingExperience` is the URL's field data, `originLoadingExperience` the origin's, and `lighthouseResult` a lab run on Google's servers. If the URL lacks traffic, `loadingExperience.origin_fallback` is `true` and the numbers are the origin's.

```bash
URL="https://example.com/pricing"
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$(jq -rn --arg u "$URL" '$u|@uri')&strategy=mobile&category=performance&key=$PSI_KEY" > psi.json
jq '.loadingExperience | {id, origin_fallback, overall_category, metrics: (.metrics | map_values({percentile, category}))}' psi.json
```

```powershell
$url = [uri]::EscapeDataString("https://example.com/pricing")
$psi = Invoke-RestMethod "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$url&strategy=mobile&category=performance&key=$env:PSI_KEY"
$psi.loadingExperience | Select-Object id, origin_fallback, overall_category
$psi.loadingExperience.metrics.PSObject.Properties | ForEach-Object { "{0}: p75={1} ({2})" -f $_.Name, $_.Value.percentile, $_.Value.category }
```

The metric keys are `LARGEST_CONTENTFUL_PAINT_MS`, `INTERACTION_TO_NEXT_PAINT`, `CUMULATIVE_LAYOUT_SHIFT_SCORE` and others. CLS is not reported in the same units in every API, so read each metric's `category` rather than comparing a raw CLS number from PSI against 0.1.

### CrUX API (field only, with LCP sub-parts)
`formFactor` is `PHONE`, `DESKTOP` or `TABLET`; leave it out to get all devices combined. Use `url` for one page or `origin` for the whole site. No record for a URL means too little traffic: retry with `origin`.

```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com/pricing","formFactor":"PHONE","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","experimental_time_to_first_byte","largest_contentful_paint_image_time_to_first_byte","largest_contentful_paint_image_resource_load_delay","largest_contentful_paint_image_resource_load_duration","largest_contentful_paint_image_element_render_delay"]}' \
  | jq '{period: .record.collectionPeriod, p75: (.record.metrics | map_values(.percentiles.p75))}'
```

```powershell
$body = @{
  url        = "https://example.com/pricing"
  formFactor = "PHONE"
  metrics    = @("largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift",
                 "experimental_time_to_first_byte",
                 "largest_contentful_paint_image_time_to_first_byte",
                 "largest_contentful_paint_image_resource_load_delay",
                 "largest_contentful_paint_image_resource_load_duration",
                 "largest_contentful_paint_image_element_render_delay")
} | ConvertTo-Json
$r = Invoke-RestMethod -Method Post -ContentType "application/json" -Body $body `
  -Uri "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$env:CRUX_KEY"
$r.record.collectionPeriod | ConvertTo-Json -Depth 4
$r.record.metrics.PSObject.Properties | ForEach-Object { "{0}: p75={1}" -f $_.Name, $_.Value.percentiles.p75 }
```

The CrUX API returns CLS as a decimal string with two places (for example `"0.05"`). The four LCP sub-part metrics are p75 values in milliseconds and only cover pages whose LCP element is an image.

### CrUX History API (the trend, to see a fix land)
Same body plus `collectionPeriodCount` (default 25, maximum 40 weekly periods). Each period is itself a 28-day window, so a fix shows as a slope over about four weekly points, not a step.

```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"origin":"https://example.com","formFactor":"PHONE","metrics":["largest_contentful_paint"],"collectionPeriodCount":12}' \
  | jq '.record.metrics.largest_contentful_paint.percentilesTimeseries.p75s'
```

```powershell
$body = @{ origin = "https://example.com"; formFactor = "PHONE"; metrics = @("largest_contentful_paint"); collectionPeriodCount = 12 } | ConvertTo-Json
$h = Invoke-RestMethod -Method Post -ContentType "application/json" -Body $body `
  -Uri "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord?key=$env:CRUX_KEY"
$h.record.metrics.largest_contentful_paint.percentilesTimeseries.p75s
```

### Field attribution from your own users
CrUX gives numbers, not causes. For INP causes on a live site, the `web-vitals` attribution build reports the element and the phase breakdown per interaction:

```js
import { onINP } from 'web-vitals/attribution';

onINP(({ value, attribution }) => {
  const { interactionTarget, inputDelay, processingDuration, presentationDelay, longAnimationFrameEntries } = attribution;
  // Send to the site's existing analytics endpoint; do not add a new data processor without the owner's approval.
});
```

Adding this to a live site sends user data somewhere. Treat it as a measurement change for the owner to approve (see `seo-measurement-setup`).

---

## 3. Lab commands

### Lighthouse CLI
Lighthouse needs Node 22 or later and a local Chrome. It runs mobile emulation with simulated throttling by default. Run it at least three times and use the median.

```bash
for i in 1 2 3; do
  npx lighthouse https://example.com/pricing --only-categories=performance \
    --output=json --output-path=./lh-pricing-$i.json --chrome-flags="--headless" --quiet
done
jq -r '[.audits["largest-contentful-paint"].displayValue, .audits["total-blocking-time"].displayValue, .audits["cumulative-layout-shift"].displayValue] | @tsv' lh-pricing-*.json
```

```powershell
1..3 | ForEach-Object {
  npx lighthouse https://example.com/pricing --only-categories=performance `
    --output=json --output-path="./lh-pricing-$_.json" --chrome-flags="--headless" --quiet
}
Get-ChildItem lh-pricing-*.json | ForEach-Object {
  $a = (Get-Content $_ -Raw | ConvertFrom-Json).audits
  "{0}  LCP {1}  TBT {2}  CLS {3}" -f $_.Name, $a.'largest-contentful-paint'.displayValue, $a.'total-blocking-time'.displayValue, $a.'cumulative-layout-shift'.displayValue
}
```

Add `--preset=desktop` for a desktop run. Test a production build (`next build` then `next start`), never the dev server: development mode adds work that does not exist in production.

The insight audits name the cause (Lighthouse 13 IDs):

| Insight audit | Tells you |
|---|---|
| `lcp-phases-insight` | The LCP element and how its time splits across the sub-parts |
| `lcp-discovery-insight` | Whether the LCP image is in the HTML, lazy-loaded, or missing `fetchpriority="high"` |
| `document-latency-insight` | Redirects, slow server response, missing compression (TTFB) |
| `render-blocking-insight` | CSS and scripts that hold up first render |
| `image-delivery-insight` | Oversized, uncompressed or old-format images |
| `font-display-insight` | Fonts that hide text while loading |
| `cls-culprits-insight` | The elements that shifted and the likely cause |
| `third-parties-insight` | Third-party transfer size and main-thread time by provider |
| `use-cache-insight` | Static assets with short cache lifetimes |

```bash
jq '.audits["lcp-phases-insight"].details, .audits["third-parties-insight"].details' lh-pricing-1.json
```

```powershell
$a = (Get-Content lh-pricing-1.json -Raw | ConvertFrom-Json).audits
$a.'lcp-phases-insight'.details | ConvertTo-Json -Depth 8
```

### Chrome DevTools
- **Performance panel, record a reload:** shows the LCP element, the network request for it, and the main-thread work before it paints. Enable CPU throttling (4x or more) to approach a mid-range phone.
- **Performance panel, record an interaction:** click the element the field data points to, then read the interaction's input delay, processing and presentation in the Interactions track and the long tasks beneath it.
- **Network panel:** request blocking lets you load the page without a given third-party script, which measures what that script costs.
- **Application > Back/forward cache > Run test:** reports whether the page can be restored from bfcache and, if not, why.

### Long Animation Frames in the console
A long animation frame is a rendering update delayed beyond 50 ms. Paste this into the console (Chrome 123+), interact, and read which scripts own the blocking time:

```js
new PerformanceObserver((list) => {
  for (const e of list.getEntries()) {
    console.log(Math.round(e.duration), 'ms, blocking', Math.round(e.blockingDuration), 'ms');
    for (const s of e.scripts) console.log('  ', s.invokerType, s.invoker, s.sourceURL, s.sourceFunctionName, Math.round(s.duration), 'ms');
  }
}).observe({ type: 'long-animation-frame', buffered: true });
```

---

## 4. LCP by sub-part

LCP splits into four sub-parts. Web.dev suggests roughly 40% each for TTFB and resource load duration and under 10% each for the two delays, so a large delay is the clearest sign of a fixable problem.

| Sub-part | What it is | Fixes |
|---|---|---|
| **TTFB** | Navigation start to the first byte of HTML | Cache the HTML at the server or CDN (Next.js: static rendering, `revalidate`); remove redirect hops; avoid URL parameters that bypass the CDN cache; move slow data fetching off the critical path or stream it |
| **Resource load delay** | First byte to the start of the LCP resource's download | Put the LCP image in the server HTML as an `<img>`; `fetchpriority="high"`; never `loading="lazy"` on it; `<link rel="preload">` only when it is not in the HTML (CSS background, JS-inserted); host it on the same origin where possible |
| **Resource load duration** | The download itself | Right size (`srcset`/`sizes`), modern format (AVIF, WebP), compression, a CDN, long cache lifetimes for static assets |
| **Element render delay** | Download finished to the element painted | Remove render-blocking CSS and JS, render the element on the server, break up long tasks before first paint, and avoid fonts that hide text (`font-display` other than `auto` or `block`) |

`fetchpriority` is a hint, not an order. Use it on the one LCP image per template; marking several images high cancels the benefit. It is supported in Chrome and Edge 102+, Firefox 132+ and Safari 17.2+.

If the LCP element is text, the image sub-parts do not apply: look at TTFB, render-blocking resources and web fonts.

### Next.js `next/image` for the LCP image (Next.js 16)

```tsx
import Image from 'next/image'

export default function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Team reviewing a dashboard"
      width={1600}
      height={900}
      sizes="100vw"
      fetchPriority="high"   // or loading="eager"; use preload only when it must be fetched from <head>
    />
  )
}
```

- `priority` is deprecated from Next.js 16 in favour of `preload`. The docs advise `loading="eager"` or `fetchPriority="high"` in most cases, and say not to combine `preload` with `loading` or `fetchPriority`, nor use it when different images are the LCP at different viewports.
- `next/image` lazy-loads by default, which is right for every image except the LCP one.
- The default `images.formats` is `['image/webp']`. Add AVIF with `formats: ['image/avif', 'image/webp']` in `next.config.js`; both variants are then cached, which uses more storage.
- `sizes` tells the browser which `srcset` width to pick. Without it a full-width layout can download a far larger file than it shows.

---

## 5. INP by phase

An interaction's latency is **input delay** (until the handlers start), **processing duration** (the handlers) and **presentation delay** (until the next frame paints).

| Phase | Usual causes | Fixes |
|---|---|---|
| Input delay | Long tasks already running: script evaluation during load, hydration, third-party scripts, timers | Less client JS; defer third parties; split hydration (smaller client components, `next/dynamic`) |
| Processing | Handlers doing everything before the screen updates | Update the UI first, then yield; move non-urgent work (analytics, saves) after the yield; debounce input handlers |
| Presentation delay | Large DOM, layout thrashing, big HTML rendered by JS | Smaller DOM, `content-visibility: auto` for off-screen sections, avoid reading layout right after writing it |

A **long task** is any task over 50 ms. Yield inside long work so the browser can respond to input in between:

```js
function yieldToMain() {
  if (globalThis.scheduler?.yield) return scheduler.yield();
  return new Promise((resolve) => setTimeout(resolve, 0));
}

async function onSave() {
  showSpinner();           // visible feedback first
  await yieldToMain();     // let the frame paint
  await saveToServer();
  sendAnalytics();
}
```

`scheduler.yield()` is in Chrome and Edge 129+ and Firefox 142+, not Safari, hence the fallback. `isInputPending()` is no longer recommended.

### Hydration cost (React and Next.js)
During hydration the browser runs the client components' JavaScript for everything on the page, as long tasks, before many interactions can be handled. Early taps then wait in input delay. In the App Router:
- Layouts and pages are Server Components by default, and the Next.js docs recommend them to reduce the JavaScript sent to the browser. Once a file is marked `"use client"`, everything it imports joins the client bundle, so keep the directive on the smallest interactive leaves, not on layouts or whole pages. Server Components passed as `children` to a Client Component stay on the server.
- Load heavy client components that are below the fold or behind an interaction with `next/dynamic`.
- Render context providers as deep in the tree as possible, wrapping `{children}` rather than the whole document.
- Compare the client JavaScript per route before and after a change with a bundle analyser. A route whose client bundle grew is a likely INP regression.

Large rewrites (changing state management, splitting a big client tree) are for the team to decide. Report the measured long tasks and the proposal.

---

## 6. CLS by cause

| Cause | Fix |
|---|---|
| Images, video, iframes without dimensions | `width` and `height` attributes, or CSS `aspect-ratio`; `next/image` with dimensions, or `fill` in a sized parent |
| Web fonts swapping | `next/font` (self-hosted, preloaded, adjusted fallback by default); elsewhere `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override` on the fallback, and `font-display: optional` where acceptable |
| Ads, embeds, late widgets | Reserve space with `min-height` or `aspect-ratio`; place late content lower on the page |
| Injected banners (cookie, promo, app install) | Overlay rather than push content; insert only after a user action; reserve the slot if it must sit in flow |
| Animations | Animate `transform` and `opacity`, not `top`, `left`, `width` or `height` |
| Back and forward navigations | Make the page bfcache-eligible (below) |

### bfcache eligibility
A page restored from the back/forward cache appears instantly and fully laid out. The main blockers:
- an `unload` event listener (use `pagehide` instead; check third-party scripts too);
- `Cache-Control: no-store` on the HTML of a page that is not sensitive (use `no-cache` or `max-age=0` when you only need freshness);
- open IndexedDB connections, in-flight `fetch` or XHR requests, open WebSocket or WebRTC connections when the user leaves;
- a non-null `window.opener`.

Test with DevTools **Application > Back/forward cache**. In the field, the `NotRestoredReasons` API reports why a navigation was not restored. Keep `no-store` on genuinely private pages (account, checkout): that is a correct trade.

### Next.js `next/font`

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], display: 'swap' })

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-GB" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

Font files are downloaded at build time and served from the site, so the browser makes no request to Google. `display` defaults to `swap`, `preload` to `true`, and `adjustFontFallback` to `true` for Google fonts (`'Arial'` for local fonts). Define each font once and import it where needed, so it is not duplicated.

---

## 7. Third-party tag triage

1. **Inventory.** From the served page, list every third-party origin and script: Lighthouse `third-parties-insight`, the DevTools Network panel, and the tag manager's container. For each, record the owner, purpose, transfer size and main-thread time.
2. **Measure.** Block one script at a time in DevTools and re-record. The difference is that script's real cost on this page.
3. **Classify.**

| Decision | When | How (Next.js App Router) |
|---|---|---|
| Remove | Unused, duplicated, no owner | Delete the tag (owner sign-off) |
| Facade | Heavy embed users rarely open (video, chat, maps) | A static placeholder that loads the real embed on click |
| Defer, idle | Chat and social widgets | `<Script src="..." strategy="lazyOnload" />` |
| Defer, after hydration | Analytics, tag managers | `<Script src="..." />` (the default `afterInteractive`) |
| Load early | Consent managers, bot detection | `strategy="beforeInteractive"` in the root layout only |
| Keep | Needed early and already light | Record the reason |

The `worker` strategy is experimental and does not work with the App Router, so do not rely on it.

4. **Hand over.** Tags belong to marketing, analytics, legal or sales. Never remove or delay one without its owner's approval: record it as `needs-human` with the measured cost and the proposed change. Changing consent behaviour has legal implications and is never a performance-only decision.

Tags added through a tag manager do not appear in the codebase. Check the container as well as the source.

---

## 8. Served-markup checks (Verify)

Fetch the production HTML, not the source, and confirm each fix reached it.

```bash
curl -s -A "Mozilla/5.0" https://example.com/pricing > served.html
grep -o '<img[^>]*fetchpriority="high"[^>]*>' served.html           # LCP image is high priority
grep -o '<img[^>]*fetchpriority="high"[^>]*loading="lazy"[^>]*>' served.html   # should print nothing
grep -o '<link[^>]*rel="preload"[^>]*>' served.html                   # image and font preloads
grep -o '<img[^>]*>' served.html | grep -v 'width=' | head            # images missing dimensions
grep -o '<script[^>]*src="https\?://[^"]*"' served.html               # third-party scripts still in the initial HTML
curl -sI https://example.com/pricing | grep -iE 'cache-control|age|cf-cache-status|x-vercel-cache'
```

```powershell
$r = Invoke-WebRequest -Uri "https://example.com/pricing" -UseBasicParsing
$html = $r.Content
[regex]::Matches($html, '<img[^>]*fetchpriority="high"[^>]*>') | ForEach-Object Value
[regex]::Matches($html, '<link[^>]*rel="preload"[^>]*>') | ForEach-Object Value
[regex]::Matches($html, '<img[^>]*>') | Where-Object { $_.Value -notmatch 'width=' } | Select-Object -First 10 | ForEach-Object Value
[regex]::Matches($html, '<script[^>]*src="https?://[^"]*"') | ForEach-Object Value
$r.Headers['Cache-Control']; $r.Headers['Age']
```

Attribute order varies, so a pattern that prints nothing is a prompt to look, not proof of absence. Cache header names depend on the CDN (`cf-cache-status` on Cloudflare, `x-vercel-cache` on Vercel); `Age` above zero usually means a cache served the page.

---

## 9. The honest boundary

- **One signal among many.** Google says page experience aligns with what its core ranking systems reward, that it always seeks the most relevant content even when page experience is sub-par, and that good Core Web Vitals reports do not guarantee top rankings (Search Central, checked 2026-10). Never promise a ranking change from this work.
- **Field data lags.** CrUX is a rolling 28-day window, updated daily for the CrUX API and PSI, and weekly for the History API. A fix shipped today is fully reflected after about 28 days of traffic, and a low-traffic URL may never get its own field data. Search Console's Core Web Vitals report is built on the same CrUX data and groups similar URLs; its "Start tracking" validation runs a 28-day monitoring window (it does not trigger re-indexing).
- **What you can verify now:** the lab medians and the served markup. **What you cannot:** that the 75th percentile of real users improved. Say exactly that, give the re-check date, and leave the finding's field confirmation open.

---

## 10. Worked example

The figures below are illustrative, to show the method. They are not from a real site.

**Request:** "Our pricing page fails Core Web Vitals on mobile."

**Diagnose, field.** CrUX API, `url` = `/pricing`, `PHONE`: LCP p75 3.9 s (needs improvement), INP p75 310 ms (needs improvement), CLS p75 0.04 (good). Sub-parts p75: TTFB 600 ms, resource load delay 1,700 ms, resource load duration 900 ms, element render delay 300 ms. Reported as "live CrUX data, 28 days ending on the collection period's last date".

The resource load delay is 44% of LCP against a target under 10%, so the image is found or requested late.

**Diagnose, lab.** Three Lighthouse mobile runs on a production build: LCP median 4.4 s, TBT 690 ms. `lcp-discovery-insight` flags the hero `<Image>` as lazy-loaded. `third-parties-insight` shows a chat widget and a heatmap script as the largest main-thread costs. A DevTools recording of a tap on the "Monthly / Annual" toggle shows a 280 ms input delay during hydration of the whole page, which is one large client component.

**Fix.**
1. Hero image: removed the explicit `loading="lazy"`, added `fetchPriority="high"` and `sizes="100vw"`. Safe and reversible, applied.
2. Chat widget: moved to `<Script strategy="lazyOnload">`. Its owner (support) approved; the heatmap script was recorded as `needs-human` for marketing with its measured cost of 210 ms main-thread time.
3. Pricing page: moved `"use client"` from the page down to the toggle and the FAQ accordion, so the plan tables render as Server Components. A larger change, so it went in its own PR for review.

**Verify.** Lab medians after the changes: LCP 2.4 s, TBT 180 ms. Served HTML shows `fetchpriority="high"` on the hero `<img>` and no `loading="lazy"`; the chat script is no longer in the initial HTML. The toggle interaction, re-recorded at the same throttling, has no long task over 50 ms.

**Report (to a non-specialist).** "Real visitors on phones waited about 3.9 seconds for the main image, mostly because the page asked for it last. It now asks for it first. In our tests the page loads that image about two seconds sooner and responds to the plan toggle without lag. Google's real-user data covers the last 28 days, so it will not show the change until around [ship date + 28 days]; I'll give you the command to check then. The heatmap script costs about 0.2 seconds of blocked time on every visit; marketing needs to decide whether to keep it. Faster pages help visitors and are one of many signals Google uses; this alone will not move rankings."
