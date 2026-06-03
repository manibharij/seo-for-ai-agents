# Log analysis & crawl budget

Read this for the how. Server logs are the only place you see what crawlers *actually* did (not what you hope they do). The two payoffs: find **important pages crawlers ignore**, and find **budget wasted on junk**.

---

## First: verify the crawler is real (never trust the user-agent)

A user-agent string saying `Googlebot` proves nothing — spoofing is trivial and common. Before attributing any behaviour to a search engine:
- **Reverse DNS + forward confirm:** the IP should reverse-resolve to the engine's domain (`*.googlebot.com` / `*.google.com` for Google; `*.search.msn.com` for Bing) **and** that hostname should forward-resolve back to the same IP.
- **Or match published IP ranges:** Google, Bing, and several AI crawlers publish official IP lists — match the request IP against them.
- Bucket traffic into: **verified search crawlers**, **verified AI crawlers**, **other bots**, **spoofers/scrapers**, and **humans**. Only reason about SEO from the verified-crawler buckets.

## Privacy: logs are sensitive
Access logs contain IPs and can contain PII. Analyse locally, keep **conclusions not raw logs**, never paste raw logs into a chat or commit them (add log paths to `.gitignore`). Respect that this is the user's data.

---

## What to extract

From the verified-crawler requests over a representative window:
- **Per-URL crawl frequency** — how often each URL/section is fetched.
- **Coverage gap:** sitemap/key URLs with **zero or near-zero** crawler hits — important pages going undiscovered.
- **Status distribution to crawlers** — `200` vs `3xx` vs `4xx`/`5xx`; spikes of errors or redirects waste budget and signal problems.
- **Junk magnets** — URL patterns soaking up hits: `?`-parameter and faceted URLs, session IDs, calendar/filter "infinite spaces", duplicate variants, redirect chains.
- **Importance vs frequency mismatch** — are trivial URLs crawled more than money pages?
- **Crawler mix over time** — classic vs AI crawlers, and which sections each favours (feeds the Cite rung's AI-crawler decisions).

## Crawl-budget waste patterns → fixes

| Pattern in the logs | Fix (owned by) |
|---|---|
| Crawlers hammering faceted/parameter URLs | `noindex`/robots/canonical the low-value combinations; don't expose them as crawlable (Reach + Connect; ecommerce profile) |
| Many redirect hops to crawlers | Collapse to single-hop `301`/`308` (`seo-migrations`) |
| Repeated `404`/soft-404 fetches | Return correct `404`/`410`; fix broken internal links (Reach + Connect) |
| `noindex` URLs still crawled heavily | Reduce links to them; consider robots disallow once de-indexed |
| Important pages rarely/never crawled | Improve internal links + crawl depth + sitemap inclusion (Connect) |
| Infinite spaces (calendars, filters) | Block the pattern in robots / nofollow the traps |

> Crawl budget mainly matters at **scale** (large e-commerce, big publishers, huge programmatic sets). For a small site, "crawl budget" is rarely the bottleneck — say so rather than over-engineering.

---

## How findings map to the rungs
Log analysis **diagnoses**; the fixes live in the rungs/specialists:
- Waste reduction & indexation control → **Reach** + **Connect** (+ ecommerce/programmatic for faceted/at-scale).
- Redirect/error cleanup → **seo-migrations**.
- Under-crawled key pages → **Connect** (linking/depth) + sitemap.
- Prioritisation → weight by real traffic if **Search Console** is connected.

## The honest boundary
This is a **point-in-time** analysis of the logs provided. Crawl behaviour shifts continuously, so **ongoing crawl monitoring is live/continuous work** (and any rankings effect of fixes is live data) — outside a one-off build-time read. Record the conclusions and recommended fixes in `.seo/`; re-analyse periodically (or automate a log pull) if crawl budget is an ongoing concern.
