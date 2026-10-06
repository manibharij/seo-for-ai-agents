# Live data: capabilities, tiers and rules

Read this whenever a skill could be sharper with live data: what Google actually indexed, which queries a page earns, how real users experience it, who links to it, which AI answers mention it, and what it earns the business. The served-output checks tell you whether a fix is real. Live data tells you what Google concluded and what matters most. Use both.

The pack runs inside the user's own environment (Claude Code, Cursor, Claude with connectors, a CI runner). The user already has whatever integrations they have: MCP servers, connectors, CLIs, API keys, data warehouses, CRMs, exported files. The pack never connects anything itself. Your job is to **find what is already there, use it read-only, and say what you used.**

---

## 1. Think in capabilities, not products

Every data need below is a capability. Any tool that provides it counts, whatever it is called.

| Capability | What it answers | Typical sources (examples only) | Free option |
|---|---|---|---|
| **Search performance by query and page** | Clicks, impressions, CTR and position for each page and query | A Search Console tool, Supermetrics, a warehouse table fed by the Search Console bulk export, Bing Webmaster | Search Console, Bing Webmaster |
| **URL indexing status and Google's canonical** | Is this URL indexed? Which canonical did Google pick? When was it last crawled? | A Search Console tool with URL Inspection | Search Console |
| **Core Web Vitals field data** | p75 LCP, INP and CLS from real Chrome users, page and origin | A CrUX or PageSpeed tool, a CrUX BigQuery query | CrUX API (free key) |
| **Backlinks** | Referring domains, linking pages, anchors | Ahrefs, Semrush, DataForSEO, Bing Webmaster inbound links | Bing Webmaster (partial) |
| **Keyword demand** | Search volume, difficulty, SERP features, competitors | Ahrefs, Semrush, DataForSEO, OpenSEO | None reliable: Search Console impressions show demand you already touch |
| **AI answer mentions** | Is the site shown or cited in AI answers, for which pages and prompts | Search Console generative AI report (export), Bing AI Performance (dashboard), Ahrefs Brand Radar, DataForSEO AI Optimization, OpenSEO AI visibility | Search Console and Bing reports, via the user's export or screenshot |
| **Revenue or leads by landing page** | Which pages produce key events, leads, pipeline or revenue | GA4, HubSpot, Salesforce, a warehouse, an ecommerce platform's reports | GA4 |

Name products only as examples ("for example a Search Console, Ahrefs, Semrush, DataForSEO or Supermetrics tool"). Never tell the user they need a particular product.

---

## 2. Detect what is available (Step 0 of any data-aware skill)

Look before you ask. Check, in this order, for each capability you need:

1. **Tools in the environment.** Read your tool list: MCP tool names **and their descriptions**, connectors, and any CLI on the path (`gcloud`, `bq`, a vendor CLI). Match by what a tool does, not by its name. A tool called `run_query` whose description mentions "Search Console performance" provides search performance; a tool called `gsc_helper` that only submits sitemaps does not.
2. **Direct API with credentials the user configured.** Check for environment variables by name only, never printing values: for example `GOOGLE_APPLICATION_CREDENTIALS`, `CRUX_API_KEY`, `PAGESPEED_API_KEY`, `BING_WEBMASTER_API_KEY`, `DATAFORSEO_LOGIN`. Recipes for each API are in `data/` (below).
3. **A file the user points to.** A CSV or spreadsheet exported from Search Console, Bing, GA4, a CRM or a rank tracker. Read it, note its date range, and treat it as a snapshot.
4. **Nothing.** Carry on at the lower tier and say, once, what was skipped and what would sharpen the result.

Bash, to list which credential variables are set without printing them:

```bash
for v in GOOGLE_APPLICATION_CREDENTIALS CRUX_API_KEY PAGESPEED_API_KEY BING_WEBMASTER_API_KEY DATAFORSEO_LOGIN; do
  [ -n "${!v}" ] && echo "$v is set" || echo "$v not set"
done
```

PowerShell:

```powershell
'GOOGLE_APPLICATION_CREDENTIALS','CRUX_API_KEY','PAGESPEED_API_KEY','BING_WEBMASTER_API_KEY','DATAFORSEO_LOGIN' |
  ForEach-Object { if ([Environment]::GetEnvironmentVariable($_)) { "$_ is set" } else { "$_ not set" } }
```

**Never ask the user to set up data as a precondition.** Do the work at whatever tier you find. One sentence at the end is enough: "Connecting Search Console would let me confirm which of these pages Google has actually indexed."

---

## 3. The tiers

Name the tier you are working at in the report, so the user knows the basis of every finding.

| Tier | What is available | What the pack can do |
|---|---|---|
| **0: nothing connected** | Served output only | Everything build-time, as before: fetch, render, inspect, fix, verify. Indexing and demand are inferred and labelled as such. |
| **1: search performance and URL inspection** | Search Console (free), through any tool, API or export | Indexing triage against what Google actually concluded, traffic-weighted priorities, protection of pages that earn traffic, striking-distance queries, before-and-after measurement. **The strongly recommended default.** |
| **2: plus field data, analytics and Bing** | Tier 1 plus CrUX, GA4 or a CRM, Bing Webmaster | Core Web Vitals decisions from real users, key events and revenue by landing page, Bing and Copilot visibility. |
| **3: plus a third-party SEO data tool** | Tier 2 plus Ahrefs, Semrush, DataForSEO, OpenSEO or similar | Keyword demand, backlinks, competitor gaps, AI-answer citation tracking. Numbers are the vendor's **estimates**. |

Tiers are cumulative in spirit, not strict: a user with only Ahrefs and no Search Console has a tier 3 capability without tier 1. Use what is there, and say what is missing.

---

## 4. Rules for every data tool

- **Read-only by default.** Use read scopes (`webmasters.readonly`, `analytics.readonly`). Never submit, delete, change settings, request indexing, create projects or write to a CRM or warehouse. Some MCP tools mix read and write (sitemap submit, project edits): call only the read ones unless the user asks for the write.
- **Say before you spend.** Paid APIs bill per call or in units (Ahrefs, Semrush, DataForSEO, and OpenSEO's hosted version). Before a batch of paid calls, state roughly how many calls you will make and ask. Free quotas (Search Console, CrUX) still have limits: stay inside them (figures in each `data/` file).
- **Never invent numbers.** No estimated traffic, volumes or positions when no tool returned them. Leave the field empty and say so. Quote figures with their source and date range.
- **Label estimates.** Third-party volumes, traffic and difficulty are modelled estimates. Write "Ahrefs estimate" next to them and never present them as Google's figures.
- **Secrets stay out of the repo.** Read credentials from the environment or the host's secrets manager. Never write keys, tokens, service-account JSON, or OAuth refresh tokens into `.seo/`, the repo, logs, commit messages or chat. Check that the user's `.gitignore` covers `.env*` and credential files. Never ask the user to paste a key into the chat.
- **Data is evidence, the served output is proof.** Live data tells you what to look at. A fix is still `fixed` only when the served output proves it (`audit-report-and-state.md`).
- **Snapshots, not promises.** Today's positions and citations say nothing certain about next month. Keep the pack's no-guarantee rule.
- **Personal data.** Search Console queries can contain names; CRM data is personal by nature. Keep aggregates, never copy customer records into `.seo/`.

---

## 5. Record what you used: `data_sources`

Every report that used live data lists its sources, so a later run can reproduce it. One line per capability: capability, then tool or source, then date range (and property or file where useful).

```yaml
data_sources:
  - capability: search performance by query and page
    source: Search Console API, property sc-domain:example.com
    range: 2026-07-01 to 2026-09-28
  - capability: URL indexing status and Google's canonical
    source: MCP tool "inspect_url" (Search Console URL Inspection), 40 URLs sampled
    range: 2026-10-02
  - capability: keyword demand
    source: Ahrefs MCP, keywords-explorer (estimates), country gb
    range: snapshot 2026-10-02
  - capability: AI answer mentions
    source: user export, Search Console generative AI report CSV
    range: 2026-08-01 to 2026-09-30
```

Put it at the end of the chat report and in that run's `.seo/log.md` entry. In findings, cite the source in `evidence` ("GSC 2026-07-01 to 2026-09-28: 1,240 impressions, avg position 11.3") and say which findings are live data and which are build-time inference.

---

## 6. How the skills use it

- **`seo-search-data`** owns live search data: indexing triage, protecting pages that earn traffic, demand mapping, measuring changes, AI visibility. Other skills call into its recipes rather than repeating them.
- **The orchestrator** detects the tier in Step 0 and weights `prioritisation.md` impact by real clicks, impressions and conversions when present.
- **`1-reach-indexation`** checks its served-output verdict against URL Inspection where available.
- **`seo-performance`** decides from CrUX field data and proves fixes in the lab.
- **`seo-content-audit`, `seo-positioning-strategy`, `seo-context-gathering`** use query data for vocabulary, decay and cannibalisation, and keyword tools for demand.
- **`seo-offsite-authority`** uses backlink capabilities.
- **`cite-aeo-geo`** uses AI answer mentions where they exist and prompt sampling otherwise.

Without data, each of these runs exactly as before and says its basis.

---

## 7. Recipes for the direct-API fallback

When no tool in the environment provides a capability but the user has configured credentials, use these. Each covers endpoints, auth, quotas, request examples, paging and pitfalls, verified 2026-10.

- [`data/search-console.md`](data/search-console.md): Search Analytics, URL Inspection, Sitemaps, the generative AI report, and why not to use the Indexing API.
- [`data/analytics-ga4.md`](data/analytics-ga4.md): organic landing pages, key events, the AI Assistant channel, and CRM or warehouse revenue.
- [`data/crux-pagespeed.md`](data/crux-pagespeed.md): CrUX API, CrUX History API, PageSpeed Insights.
- [`data/bing-webmaster.md`](data/bing-webmaster.md): traffic, crawl and index data, and the AI Performance report.
- [`data/third-party-mcps.md`](data/third-party-mcps.md): Ahrefs, Semrush, DataForSEO and OpenSEO, and how to treat their numbers.

User-facing setup notes: `install/data-integrations.md`.

---

## The boundary

Live data never gates a build-time capability, and the free core works with none connected. Reading a user's current data is not a promise of future results. Ongoing managed monitoring (rank tracking, geo-grids, AI citation tracking run for the user) is separate work: SearchOps for managed data, MB Search for done-for-you optimisation.
