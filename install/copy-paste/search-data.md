# Search Data: copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the `seo-search-data` skill. Read your live search data to see what Google actually concluded, and steer the work by it.*

> ⚠️ **Experimental, and run by an AI agent, which can make mistakes.** Read-only by design. Never paste API keys or customer data into a chat. See the repo's `DISCLAIMER.md`.

---

You are reading my site's live data to find out what Google actually did with it (indexed or not, which canonical it chose, which queries it shows pages for) and to steer SEO work by that. Work in four steps: **Diagnose, Fix, Verify, Report.**

## Rules
- **Detect capabilities, not products.** Look through your own tools (MCP tools and their descriptions, connectors, CLIs), then API credentials I have set as environment variables (check names only, never print values), then any export file I point you to. Match tools by what they do.
- Capabilities to look for: search performance by query and page; URL indexing status and Google's canonical; revenue or leads by landing page; Core Web Vitals field data; keyword demand; backlinks; AI answer mentions.
- **Never make data setup a precondition.** Work at whatever level you find and tell me once what would sharpen the result. Search Console is free and the most useful single source.
- **Read-only.** Never submit, request indexing, change settings, or write to analytics, a CRM or a warehouse. Never use Google's Indexing API: it is only for job postings and livestream videos.
- **Say before you spend.** Tell me before any batch of calls to a paid tool (Ahrefs, Semrush, DataForSEO, OpenSEO).
- **Never invent numbers.** Cite source and date range for every figure. Label third-party volumes and traffic as estimates.
- **Keep secrets and personal data out** of `.seo/`, the repo and the chat.
- Data tells you where to look. A fix only counts when the served page proves it.

## Step 1: Diagnose
State the data tier: 0 (nothing), 1 (Search Console), 2 (plus analytics or CRM, CrUX, Bing), 3 (plus a keyword or backlink tool). Then run what the request needs:

1. **Indexing triage.** Get Page indexing reasons from a tool or my export (the aggregate report is not in the API). Sample URLs per template and reason with URL Inspection (quota: 2,000 per day per property), recording coverage state, last crawl, and Google's canonical versus the declared one. Fetch each sampled URL to confirm on the served output. Route causes: crawled but not indexed to content quality or rendering; discovered but not indexed to internal links and crawl waste; Google choosing a different canonical to canonical signals and duplicate content; soft 404 to status codes or thin pages; blocked or noindex to the owner, after checking it is not intentional.
2. **Protect what earns traffic.** Before changing a live page's title, copy, URL, canonical or template, pull its last 90 days of clicks, impressions and top queries (ending 3 days ago), plus key events or revenue if available. Set a threshold that fits the site (for example the top 10% of pages by clicks, or any page with attributed revenue) and say which. Above it, show me the numbers and the proposed change and wait for my sign-off. Log every change with its date and baseline in `.seo/log.md`.
3. **Demand mapping.** From query and page data: striking-distance queries (roughly positions 8 to 20), cannibalisation (one intent split across pages, confirmed on the served pages), and gaps. Add keyword volumes only from a connected tool, labelled as estimates. Remember anonymised queries mean query rows never sum to page totals.
4. **Measure changes.** For each dated change in `.seo/log.md`: wait for recrawl, compare equal windows before and after (same weekdays, excluding the last 3 days), for the same pages, against a control group of unchanged pages. Check Google's ranking updates, other deploys and seasonality. Small numbers are inconclusive.
5. **AI visibility.** Use Search Console's generative AI report (impressions only; export, no API) and Bing's AI Performance report (citations; dashboard, no API) from my exports, or a connected AI-answer tool. Otherwise sample 10 to 30 real prompts in the assistants you can reach, record date, prompt and cited URL, and say it is a sample.

## Step 2: Fix
Turn each result into a finding (id, skill, area, target, severity, evidence with source and range, fix, risk, status, verified date, notes) and hand it to the owning area: Reach, Read, Understand, Connect, Rank, or the Cite layer. Pages above the traffic threshold stay `needs-human` until I sign off.

## Step 3: Verify
Confirm every fix on the served output. Google's data only changes after a recrawl, so record when to re-check instead of claiming success now.

## Step 4: Report
Give me: the tier and a `data_sources` list (capability, tool or source, date range); indexing problems with evidence and owners; pages you protected and the threshold; opportunities with real impressions and labelled estimates; measured changes with control and caveats; AI visibility and its limits; and one line on what would sharpen this. Data is a snapshot: it promises no rankings or citations.
