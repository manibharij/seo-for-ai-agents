# Performance: copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the seo-performance skill: deep Core Web Vitals work. Run Reach and Read first; this goes further than Read's light page-experience pass.*

> ⚠️ **Experimental, and run by an AI agent, which can make mistakes.** Review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are fixing my site's Core Web Vitals: **LCP** (loading), **INP** (responsiveness) and **CLS** (layout stability). Decide what to fix from **field** data (real users), prove each fix in the **lab** and in the **served HTML**, and be honest that the field result can only be confirmed weeks later. Work in four steps. Ask before risky changes; never remove or delay a marketing, analytics or consent tag without its owner's approval.

Thresholds (web.dev, verified 2026-10), judged at the **75th percentile** of real visits, separately for mobile and desktop. A page passes when all three are Good:
- **LCP:** Good ≤ 2.5 s, Poor over 4.0 s.
- **INP:** Good ≤ 200 ms, Poor over 500 ms.
- **CLS:** Good ≤ 0.1, Poor over 0.25.

## Step 1: Diagnose
**Field (what users get).** Real-user data comes from the Chrome UX Report (CrUX): a rolling 28-day window at the 75th percentile. Use an API key from an environment variable.
```bash
curl -s -X POST "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com/page","formFactor":"PHONE","metrics":["largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift","largest_contentful_paint_image_resource_load_delay"]}' \
  | jq '{period: .record.collectionPeriod, p75: (.record.metrics | map_values(.percentiles.p75))}'
```
```powershell
$body = @{ url = "https://example.com/page"; formFactor = "PHONE"; metrics = @("largest_contentful_paint","interaction_to_next_paint","cumulative_layout_shift") } | ConvertTo-Json
$r = Invoke-RestMethod -Method Post -ContentType "application/json" -Body $body -Uri "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$env:CRUX_KEY"
$r.record.metrics.PSObject.Properties | ForEach-Object { "{0}: p75={1}" -f $_.Name, $_.Value.percentiles.p75 }
```
Or use the PageSpeed Insights API (`https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=...&strategy=mobile&key=...`) and read `loadingExperience` (check `origin_fallback`). No record means too little traffic: try `"origin"` instead of `"url"`. Label every field number as **live CrUX data** with its period.

**Lab (why it is slow).** Run a production build, three times, and take the median:
```bash
npx lighthouse https://example.com/page --only-categories=performance --output=json --output-path=./lh.json --chrome-flags="--headless" --quiet
```
Read `lcp-phases-insight`, `lcp-discovery-insight`, `render-blocking-insight`, `third-parties-insight` and `cls-culprits-insight`. INP cannot be measured in the lab (Total Blocking Time is a proxy), so record the slow interaction in the Chrome DevTools Performance panel with CPU throttling.

**Find the cause.** LCP: which element, and which sub-part is biggest: TTFB, resource load delay, resource load duration or element render delay? INP: input delay, processing or presentation delay? CLS: which elements shift, and why? Which third-party scripts cost the most main-thread time?

## Step 2: Fix (largest cause on the worst metric first)
- **LCP:** cache HTML at the server or CDN and cut redirects (TTFB). Put the LCP image in the server HTML with `fetchpriority="high"`, never `loading="lazy"`, and preload it only if it is not in the HTML. Right-size it (`sizes`) in a modern format (AVIF/WebP) from a CDN. Remove render-blocking CSS and JS. **Next.js 16:** `priority` is deprecated; use `fetchPriority="high"` or `loading="eager"` on the LCP `<Image>` (or `preload`, but not combined with those).
- **INP:** keep `"use client"` on small leaves so less hydrates; lazy-load heavy client components (`next/dynamic`); split tasks over 50 ms and yield after the visible update (`scheduler.yield()` with a `setTimeout(resolve, 0)` fallback); keep the DOM small. Use the Long Animation Frames API (`long-animation-frame`) to name the script behind a slow frame.
- **CLS:** `width`/`height` or `aspect-ratio` on all media; `next/font` (self-hosted, adjusted fallback); reserve space for ads, embeds and banners, or overlay them; animate `transform`, not layout properties; make pages bfcache-eligible (no `unload` listeners, no `Cache-Control: no-store` on non-sensitive pages).
- **Third-party tags:** list each with owner, purpose and measured cost (block it in DevTools and re-record). Then remove, replace with a click-to-load facade, defer (`<Script strategy="lazyOnload">` for chat and social; the default `afterInteractive` for analytics), or keep with a reason. `beforeInteractive` only for consent managers and bot detection, in the root layout. Get the owner's sign-off before changing any tag.
- Flag hosting changes, interaction rewrites and caching of private pages for me instead of doing them.

## Step 3: Verify (lab and served HTML)
Re-run Lighthouse with the same settings (median of three). Fetch the **served** HTML and confirm the LCP `<img>` has `fetchpriority="high"` and no `loading="lazy"`, preloads are present, media have dimensions, and deferred scripts left the initial HTML:
```bash
curl -s https://example.com/page | grep -o '<img[^>]*fetchpriority="high"[^>]*>'
```
```powershell
[regex]::Matches((Invoke-WebRequest https://example.com/page -UseBasicParsing).Content, '<img[^>]*fetchpriority="high"[^>]*>') | ForEach-Object Value
```
Re-test bfcache in DevTools (Application > Back/forward cache) if you touched it. **Do not claim a field improvement**: CrUX is a rolling 28-day window, so the change is fully reflected only after about 28 days of real traffic.

## Step 4: Report
1. **What real users get** (field numbers, labelled live, with the period).
2. **What causes it** (the sub-part, phase or shifting element, with lab evidence).
3. **What you changed and why**, with before and after lab medians and served-HTML proof.
4. **What needs me:** hosting, tags only their owners can remove, larger rewrites.
5. **The boundary:** give me the date to re-check field data (about 28 days after release) and the command. Good Core Web Vitals help users and are one ranking signal among many; Google says they do not guarantee top rankings.
