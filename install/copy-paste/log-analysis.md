# Log-file & Crawl-budget Analysis — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the log-analysis skill. Advanced, large-site: see what crawlers actually fetch from your server logs.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Logs are sensitive (IPs/PII) — never commit them or paste raw logs into a chat. See the repo's `DISCLAIMER.md`.

---

You are analysing my server/CDN access logs to see what crawlers **actually fetch** — finding important pages they ignore and crawl budget wasted on junk. This needs my own logs (my data) and matters mainly for **large sites**. Work in four steps.

## Step 1 — Get logs + verify real crawlers
Use the logs I provide (server/CDN/hosting), a representative time range. **Don't trust the user-agent** — verify real crawlers by **reverse DNS** (IP resolves to googlebot.com/google.com, bing's search.msn.com, and forward-resolves back) or **published IP ranges**. Bucket: verified search crawlers / verified AI crawlers / other bots / spoofers / humans — reason only from the verified buckets. Treat logs as sensitive: conclusions not raw logs, never commit them.

## Step 2 — Analyse
From verified-crawler hits: **coverage gaps** (sitemap/key pages rarely or never crawled), **crawl-budget waste** (hits on faceted/parameter URLs, redirect chains, 404s/soft-404s, infinite spaces, duplicates), **status/error patterns** (4xx/5xx, redirect hops, noindex URLs still hammered), **frequency vs importance** (are money pages crawled enough?), and the **classic-vs-AI crawler mix**.

## Step 3 — Recommend (hand off to the rungs)
- Reduce waste: noindex/robots/canonical the low-value URLs eating budget (Reach + Connect; faceted nav for e-commerce).
- Fix redirect/error waste: single-hop 301/308, fix 404s (migrations + Reach/Connect).
- Surface under-crawled key pages: internal links + crawl depth + sitemap (Connect).
- Prioritise by traffic if Search Console is connected.

## Step 4 — Report
Tell me what crawlers are really doing (e.g. "Googlebot spends 60% of crawls on filter URLs and rarely reaches product pages"), the waste/gaps found, the fixes and which skill owns each. **Boundary:** this is a point-in-time read of the logs I gave you; ongoing crawl monitoring is continuous/live work, and rankings impact is live data. Record conclusions (not raw logs) in `.seo/`.
