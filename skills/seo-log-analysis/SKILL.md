---
name: seo-log-analysis
description: >-
  Advanced, large-site analysis of server/CDN access logs to see what crawlers
  ACTUALLY fetch — crawl frequency, important pages never crawled, crawl-budget
  wasted on junk (faceted URLs, redirects, 404s, parameters), and crawl errors. Use
  on "log file analysis", "crawl budget", "what is Googlebot crawling", "are my
  pages being crawled", "wasted crawl budget", or large-site crawl diagnostics.
  Needs access to the user's own server logs (their data); verifies crawler identity
  rather than trusting user-agent strings.
---

# Log-file Analysis — what crawlers really do

A specialist, advanced skill for large or crawl-constrained sites. Everything else in the pack inspects what's *served* on demand; this inspects the **server/CDN access logs** to see what crawlers have *actually fetched over time* — the ground truth no on-page check can give you. It's how you find pages crawlers ignore and budget they waste.

> Scope & honesty: this needs **the user's own access logs** (their data — they provide them; logs can contain PII/IPs, so handle carefully and never commit them). It's most valuable for **large sites** (thousands+ of URLs) where crawl budget is a real constraint; small sites rarely need it. Ongoing crawl monitoring is live/continuous work — this does the analysis from the logs you have.

Work the four steps: **Get logs → Analyse → Recommend → Report.**

---

## Step 1 — Get the logs (and identify real crawlers)

- **Source the logs** — server (Nginx/Apache), CDN (Cloudflare/Fastly), or hosting access logs the user exports. Confirm the time range and that they're representative.
- **Identify genuine crawlers, don't trust the user-agent.** Anyone can spoof `Googlebot`. Verify by **reverse DNS** (the IP resolves to `googlebot.com`/`google.com` and forward-resolves back) or against the engines' **published IP ranges**. Separate real Googlebot/Bingbot/AI crawlers from spoofers and bots.
- Handle logs as **sensitive** (IPs, possibly PII): analyse locally, store conclusions not raw logs, and never commit log files (add to `.gitignore`).

## Step 2 — Analyse

From the verified-crawler hits, surface:
- **Coverage gaps** — important pages (from the sitemap/key templates) that crawlers **rarely or never fetch**. Under-crawled key pages are a discoverability problem (often a depth/internal-linking issue → Connect).
- **Crawl-budget waste** — where crawlers spend hits on **low-value URLs**: faceted/parameter URLs, redirect chains, `404`s/soft-404s, infinite spaces (calendars, filters), duplicate variants. On a big site this starves the pages that matter.
- **Status/error patterns** — spikes of `4xx`/`5xx` to crawlers, redirect hops, `noindex`'d URLs still being hammered.
- **Crawl frequency vs importance** — are your most important pages crawled often enough? Are trivial pages crawled more than key ones?
- **Crawler mix** — how often AI crawlers (vs classic) fetch you, and which sections (informs the Cite rung's AI-crawler access work).

## Step 3 — Recommend (coordinate with the rungs)

Turn findings into fixes, mostly executed by other rungs:
- **Reduce waste:** `noindex`/`robots` disallow/canonicalise the low-value URLs eating budget (faceted/param/duplicate) — coordinate with Reach + Connect; on a large e-commerce site, the faceted-nav plan (ecommerce profile).
- **Fix error/redirect waste:** resolve `4xx`/`5xx` patterns and collapse redirect chains (`seo-migrations`).
- **Surface under-crawled key pages:** improve internal linking/crawl depth and sitemap inclusion so important pages get discovered (Connect).
- **Prioritise by impact** (with GSC connected, weight by traffic/opportunity).
These are recommendations + handoffs — log analysis diagnoses; the rungs fix.

## Step 4 — Report

Plain English: what crawlers are actually doing ("Googlebot spends 60% of its crawls on filter URLs and rarely reaches your product pages"), the concrete waste and gaps found, the recommended fixes (and which rung/skill owns each), and the boundary — this is a point-in-time read of the logs you provided; **ongoing crawl monitoring is continuous/live work**, and any rankings impact is live data. Record conclusions (not raw logs) in `.seo/`.

---

## Reference files
- `references/log-analysis-and-crawl-budget.md` — verifying crawler identity (reverse DNS / IP ranges), what to extract from logs, the crawl-budget waste patterns and fixes, log privacy handling, and how findings map to the rungs.
