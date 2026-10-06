# Third-party SEO data tools (tier 3)

These tools add capabilities Google and Bing do not give you: **keyword demand**, **backlinks**, competitor data and **AI answer mentions** across several assistants. They are paid, and their numbers are **modelled estimates**. Use them when the user already has them; never suggest the pack needs one. Facts verified 2026-10 against each vendor's own documentation.

---

## Detect, do not assume

Tool names differ by host and version. Match by description: a tool that "returns search volume and keyword difficulty" provides keyword demand, whatever it is called. The servers below are examples of what you may find, not a list to install.

## Rules for every paid tool

- **Say before you spend.** All four bill per call or in units. Before a batch, say how many calls you plan and why, and ask. Prefer one call with filters and a row limit over many small calls.
- **Read only.** Call research and reporting tools. Do not create or edit projects, keyword lists, tracked keywords or settings unless the user asks.
- **Label every number** as the vendor's estimate, with the date and country or database used: "Semrush estimate, UK database, 2026-10-02: 1,900 searches a month". Never present vendor traffic as the site's real traffic; Search Console is the site's real figure.
- **Never fill gaps.** If a tool returns no volume, the volume is unknown. Do not guess or interpolate.
- **Cross-check where you can.** Where a vendor and Search Console disagree on the site's own pages, Search Console wins for clicks and impressions.

---

## Ahrefs MCP (official)

- **Server:** remote only, `https://api.ahrefs.com/mcp/mcp`. Local setups are no longer supported. Tool groups can be chosen with `?tools=`, for example `?tools=site-explorer-overview,keywords-explorer`; `tools=essentials` gives a curated subset.
- **Access:** Lite plan and above. Uses an Ahrefs key generated in the account. No extra fee, but calls consume the plan's **API units**: one call costs at least 50 units, more for complex requests, shared with Ahrefs Connect and API v3. Ahrefs describes the integration as read-only.
- **Tool groups:** Site Explorer (overview metrics, backlinks, referring domains, anchors, organic keywords, competitors), Keywords Explorer (volume, matching terms), SERP overview, Rank Tracker, Site Audit, **Brand Radar**, Web Analytics, a Search Console group, social media, content helper, batch analysis, management, subscription info.
- **Brand Radar** reports AI responses that mention a brand or its competitors, with **cited pages** and **cited domains**. Its `data_source` covers ChatGPT, Google AI Overviews, Google AI Mode, Gemini, Perplexity, Copilot, Claude and Grok. Requests using only the user's custom prompts are free; requests including Ahrefs' own prompt data use API units.
- **Use it for:** backlink audits (`seo-offsite-authority`), keyword demand and competitor gaps (`seo-positioning-strategy`, demand mapping in `seo-search-data`), and AI visibility (which pages are cited, for which prompts, against which competitors).

## Semrush MCP (official)

- **Server:** `https://mcp.semrush.com/v2/mcp`, HTTP transport. Auth by OAuth 2.1 sign-in, or an `Authorization: Apikey ...` header.
- **Access:** included with plans that have API access (for SEO data: Semrush One Starter or Pro and above, SEO Classic Pro or Guru, or Business with an API units package; for traffic data: a Trends API plan). Calls consume **API units** like the standard API.
- **Data:** all Trends API and SEO API methods, plus the read-only methods of the Projects API: keyword research, domain analytics, backlinks, position tracking, traffic trends.
- **Use it for:** the same jobs as Ahrefs. Semrush databases are per country: always state which one.

## DataForSEO MCP (official) and APIs

- **Server:** open source, `dataforseo/mcp-server-typescript` (`npx dataforseo-mcp-server@latest`), stdio by default or HTTP; DataForSEO also hosts a remote server at `https://mcp.dataforseo.com/mcp`. Auth by OAuth for HTTP, or `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` environment variables.
- **Modules:** SERP, Keywords Data, OnPage, DataForSEO Labs, Backlinks, Business Data, Domain Analytics, Content Analysis, **AI Optimization**.
- **Cost:** pay as you go; **every call is billed**. Responses can be trimmed to configured fields, which keeps context small.
- **Use it for:** live SERPs for a query set, keyword volumes, backlink data and AI answer checks, when the user prefers metered data to a subscription.

## OpenSEO

- **What it is:** an open-source (MIT) SEO platform, `every-app/open-seo`, that can be self-hosted. It uses the user's own DataForSEO key for data; the hosted version adds a markup on requests.
- **Server:** hosted MCP at `https://app.openseo.so/mcp`, OAuth sign-in or an API key for headless use.
- **Tools:** keyword research (volume, difficulty, CPC), live SERPs, domain and competitor research, backlinks, rank tracking, local business tools, Search Console integration, AI visibility tracking.
- **Caution:** some tools write (saving keywords, updating project context). Call only read tools unless asked. Its numbers are DataForSEO's, so label them that way.

---

## How the skills use tier 3

| Job | Capability | Notes |
|---|---|---|
| Demand mapping (`seo-search-data`) | Keyword demand | Add volume and difficulty to Search Console's real queries and to gaps. Volumes are estimates; Search Console impressions are real. |
| Topical plan (`seo-positioning-strategy`) | Keyword demand, competitors | Size topics; find what competitors rank for that the site does not. |
| Backlink audit (`seo-offsite-authority`) | Backlinks | Referring domains, lost links, anchors. Never buy or build links from it. |
| AI visibility (`seo-search-data`, `cite-aeo-geo`) | AI answer mentions | Which pages are cited, for which prompts, against which competitors. Sampled prompts, not every user conversation. |

---

## Sources (verified 2026-10)

- Ahrefs MCP tool categories: https://docs.ahrefs.com/mcp/docs/tool-categories.md
- Ahrefs MCP getting started (plan, units, read-only): https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
- Ahrefs Brand Radar cited pages: https://docs.ahrefs.com/en/api/reference/brand-radar/post-cited-pages
- Semrush MCP: https://developer.semrush.com/api/v3/introduction/semrush-mcp/
- DataForSEO MCP server: https://github.com/dataforseo/mcp-server-typescript
- DataForSEO remote MCP: https://dataforseo.com/help-center/setting-up-the-official-dataforseo-mcp-server-simple-guide
- OpenSEO MCP: https://openseo.so/docs/mcp
- OpenSEO repository: https://github.com/every-app/open-seo
