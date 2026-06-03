# Optional data integrations (bring your own key)

**Everything in this pack works with zero data integrations.** The audit, the fixes, and the verification all run on what's actually served — no API keys required, ever.

If you *already* use search-data tools, you can connect them with **your own API keys** to make the audit sharper: real indexation and rankings instead of inferences, real search demand and competitor context for content and positioning work. This is the **DIY** path — optional, self-service, free (beyond whatever you already pay the tool).

> Prefer not to wire up and pay for your own data APIs, or want ongoing managed monitoring (rank tracking, geo-grid, AI-citation tracking) without the setup? That's the **done-for-you** tier — **SearchOps** (managed data) and **MB Search** (done-for-you optimisation). The build skills here never require either; they just get sharper with data, however you supply it.

---

## Security — read this first

API keys are secrets. The skills are instructed to:
- Read keys **only from environment variables** (or your host's secrets manager) — never hard-coded, never written into `.seo/`, the repo, logs, or commits.
- Make sure **your own project's** `.gitignore` excludes env and credential files (e.g. `.env*`, `*-credentials.json`) so a key is never committed — that's where your keys actually live. (This pack's own `.gitignore` excludes them too, for anyone working in the pack repo.)
- Never ask you to paste a key into a chat. Set the env var; the skills detect and use it, or carry on without it.

---

## The integrations (connect any, all, or none)

### Google Search Console — start here (it's free)
The single highest-value connect: real indexation status, impressions/clicks/average position per page and query, and coverage errors — the ground truth the build can only infer.
- **Set up:** create Google Cloud credentials (OAuth client or a service account) with Search Console API access, grant the service account access to your GSC property, and expose the credentials via env var (e.g. `GOOGLE_APPLICATION_CREDENTIALS` pointing to the service-account JSON).
- Used to: confirm what's actually indexed, **prioritise by real traffic**, find near-ranking query opportunities, and track recovery after fixes.

### DataForSEO
Keyword volume, SERP and rank data, competitor/SERP-feature data via one paid API.
- **Set up:** set `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` env vars.
- Used to: ground the content audit and positioning work in real search demand and competition.

### Ahrefs / Semrush
Backlink/authority (the earned-media picture), keyword and competitor research, content-gap analysis.
- **Set up:** set the provider's API key env var (e.g. `AHREFS_API_KEY`).
- Used to: inform positioning/strategy and surface the off-site/earned-media context the build can't see (earned media itself remains outside what a build can change).

### Bing Webmaster Tools
Bing's indexation/performance data (relevant to Bing-powered surfaces incl. Copilot).
- **Set up:** set the Bing Webmaster API key env var.

### PageSpeed Insights API
Field Core Web Vitals (real-user CrUX data) plus lab audits.
- **Set up:** set a `PAGESPEED_API_KEY` env var (a free Google API key).

---

## How the skills use them
- **Detect → use → degrade.** Each skill checks whether a relevant integration is configured. If yes, it enriches (e.g. prioritises by real GSC traffic, grounds content gaps in real demand). If no, it falls back to the served-output checks, which stand on their own.
- **Honest labelling.** The report marks which findings came from live data and which are build-time inferences, and cites the source.
- **No gating, no paywalling.** A connected key never unlocks a *build-time* capability that's otherwise withheld — it only adds *live context*. Reading today's data is never a promise of future results.

These can be exposed to the agent directly (env vars the skill reads) or via MCP servers where one exists (see [`mcp.md`](mcp.md) for the MCP layer). Either way: optional, your keys, your call.
