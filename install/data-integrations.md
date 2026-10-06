# Live data: what sharpens the pack, and how to provide it

**Everything in this pack works with no data connected.** The audit, the fixes and the verification run on what your site actually serves. Live data adds what Google concluded: which pages it indexed, which canonical it chose, which queries it shows you for, and what that traffic is worth.

The pack does not connect anything itself. It runs inside your environment (Claude Code, Cursor, Claude with connectors, CI) and **uses whatever you already have**: MCP servers, connectors, CLIs, API keys, a data warehouse, a CRM, or a file you export. The agent looks for each capability it needs, uses what it finds read-only, and tells you once what would sharpen the result. It never asks you to set something up before it starts.

---

## What the agent looks for

| Capability | Free way to provide it | Paid or other examples |
|---|---|---|
| Search performance by query and page | Google Search Console, Bing Webmaster Tools | Supermetrics, a warehouse with the Search Console bulk export |
| URL indexing status and Google's canonical | Search Console (URL Inspection) | |
| Revenue or leads by landing page | GA4 | HubSpot, Salesforce, a warehouse |
| Core Web Vitals field data | CrUX API (free key) | |
| Keyword demand | (none reliable) | Ahrefs, Semrush, DataForSEO, OpenSEO |
| Backlinks | Bing Webmaster (partial) | Ahrefs, Semrush, DataForSEO |
| AI answer mentions | Search Console generative AI report and Bing AI Performance (both UI only: export or screenshot) | Ahrefs Brand Radar, DataForSEO AI Optimization |

Product names are examples. Any tool that provides the capability works.

## The tiers

- **Tier 0, nothing connected:** build-time checks only.
- **Tier 1, Search Console:** the strongly recommended default, and free. Unlocks indexing triage, traffic-weighted priorities, protection of pages that earn traffic, and before-and-after measurement.
- **Tier 2, plus analytics or a CRM, CrUX and Bing:** value by landing page, real-user Core Web Vitals, Bing and Copilot visibility.
- **Tier 3, plus a third-party SEO data tool:** keyword demand, backlinks, competitor gaps, AI citation tracking. Their numbers are estimates and the agent labels them so.

## Three ways to provide data (the agent tries them in this order)

1. **A tool already in your environment.** If your host has an MCP server or connector for Search Console, GA4, Ahrefs, Semrush, DataForSEO or similar, there is nothing more to do. See [`mcp.md`](mcp.md) for the MCP layer.
2. **API credentials as environment variables.** Set them in your shell or your host's secrets manager. Recipes the agent follows, with exact endpoints and quotas, are in `skills/seo-orchestrator/references/data/`.
3. **An export.** Download a CSV from Search Console, Bing, GA4 or your CRM and tell the agent where it is. Good for one-off audits and for reports that have no API (the AI reports above, the Page indexing report).

## Setting up Search Console API access (recommended)

1. In Google Cloud, create a project and enable the **Google Search Console API**.
2. Create a **service account** and download its JSON key. Keep it outside the repo.
3. In Search Console, open your property, then **Settings > Users and permissions > Add user**, and add the service account's email address. Restricted access is enough to read performance data.
4. Point the standard variable at the key:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/gcloud/gsc-reader.json"
```

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "$HOME\.config\gcloud\gsc-reader.json"
```

The agent uses the read-only scope. For GA4, add the same service account under **Admin > Access management** with the Viewer role and enable the Google Analytics Data API. For CrUX, create an API key restricted to the Chrome UX Report API and set it as `CRUX_API_KEY`. For Bing, generate an API key under **Settings > API Access** in Bing Webmaster Tools and set `BING_WEBMASTER_API_KEY`. Third-party tools document their own setup; see `skills/seo-orchestrator/references/data/third-party-mcps.md`.

---

## What the agent will and will not do

- **Read only.** It never submits URLs, requests indexing, changes settings, or writes to analytics, a CRM or a warehouse.
- **Asks before spending.** Paid tools bill per call or in units. The agent says how many calls it plans before a batch.
- **Never invents numbers.** If no tool returned a figure, the report says it is unknown. Every figure carries its source and date range, and the report ends with a `data_sources` list so the run can be repeated.
- **Keeps secrets out.** Keys are read from the environment only, never written to `.seo/`, the repo, logs or chat. Make sure your project's `.gitignore` covers `.env*` and credential files. Never paste a key into a chat.
- **Keeps personal data out.** CRM and query data are summarised by page; no customer records go into `.seo/`.

## The boundary

Data is a snapshot: it explains what happened and guides priorities, and promises no rankings or citations. It never gates a build-time capability. If you would rather not wire up data or run ongoing monitoring yourself, that is the managed tier: **SearchOps** (managed data) and **MB Search** (done-for-you optimisation).
