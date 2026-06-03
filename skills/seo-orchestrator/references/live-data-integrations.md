# Live-data integrations (optional, bring-your-own-key)

Read this to **enrich** an audit with live data when the user has connected a data tool — and to do it without ever breaking the pack's core promise. Live data makes the audit sharper (real indexation, rankings, search demand, competitor context), but it is **always optional**: every skill must work fully without it.

> **The rule that protects everyone (including the boundary):** live-data integrations are **optional enrichment, never a requirement, and never a gate.** The free build-time capabilities work with zero data tools connected. If a key is present, use it to *prioritise better and see more*; if not, fall back silently to the served-output checks that stand on their own.

---

## The boundary, restated (now that data is integratable)

There are two honest paths to live data, and the pack supports both without contradiction:

- **DIY — bring your own key.** If the user already pays for Search Console (free), DataForSEO, Ahrefs, Semrush, or Bing Webmaster Tools, they can connect it with their **own API key**. The pack reads *their* data to enrich the audit. Free, optional, self-service.
- **Done-for-you — the managed tier.** Not everyone wants to wire up and pay for their own data APIs, or run ongoing monitoring. **SearchOps** (managed rank/geo-grid/citation data) and **MB Search** (done-for-you optimisation) are the hands-off tier: the data and the work, without setup.

So the boundary is no longer "we don't touch live data." It's: **the free core never *requires* live data; live data is optional (your keys) or managed (our products); and no build-time capability is ever paywalled.** Reading the user's current data (e.g. today's rankings) is also **not a promise of future results** — keep the no-guarantee rule.

---

## Security first (non-negotiable)

API keys are secrets. When a skill uses one:
- **Read keys from environment variables** (e.g. `DATAFORSEO_LOGIN`/`DATAFORSEO_PASSWORD`, `AHREFS_API_KEY`, GSC OAuth/service-account creds) — **never** hard-code them, and **never** write them into `.seo/`, the repo, logs, or commits.
- Ensure the **user's project** `.gitignore` excludes key/credential files (`.env*`, `*-credentials.json`, service-account JSON) — that's where keys live, so confirm they can't be committed. (This pack's own `.gitignore` excludes them too.)
- If no key is configured, **do not prompt for it inline or ask the user to paste it into the chat** — tell them how to set the env var/config and proceed without it.
- Only ever send the user's site/keywords to a service the user has explicitly connected; respect that sending data to an external API is an outward action.

---

## What each tool adds (detect → use → degrade)

For each, the skill checks whether it's configured; if yes, enrich; if no, fall back to the built-in served-output checks.

### Google Search Console (free — the highest-value connect)
- **Adds:** real **indexation status** (is the page actually indexed?), **impressions/clicks/position** per page and query, and coverage errors — the ground truth the build-time checks can only infer.
- **Use it to:** confirm Reach findings against reality (a page you think is fine but GSC shows "Crawled – not indexed"), **prioritise** by real impressions/clicks (fix the high-traffic pages first), find queries a page nearly ranks for (intent/content opportunities), and detect post-fix recovery over time.
- Access via the Search Console API (OAuth or service account). It's the first integration worth having.

### DataForSEO
- **Adds:** keyword search volume, SERP data, rank tracking, competitor/SERP-feature data, on-demand — via one paid API.
- **Use it to:** ground the **content audit** and **positioning** work in real search demand and competitor context; check current rankings; size opportunities.

### Ahrefs / Semrush
- **Adds:** backlink/authority data (the **earned-media** picture the build can't see), keyword and competitor research, content-gap analysis.
- **Use it to:** inform **positioning/strategy** (competitive landscape, topical authority gaps) and flag off-site/earned-media context — while remembering earned media itself is still outside what a build can *change*.

### Bing Webmaster Tools
- **Adds:** Bing's indexation/performance data (and, by extension, signal relevant to Copilot/other Bing-powered surfaces).

### PageSpeed Insights API
- **Adds:** field Core Web Vitals (CrUX) — the real-user score the build can't produce — plus lab audits. (Lab-only Lighthouse is already an optional MCP.)

---

## How enrichment changes the lifecycle (without changing the rules)

- **Prioritisation gets real weights.** With GSC, `prioritisation.md`'s "impact" can use actual impressions/clicks/position instead of estimates — fix what genuinely matters first. Record in `.seo/state.json` (e.g. a `liveData` note on a finding), but **never store the raw keys**.
- **Diagnosis gets ground truth.** Confirm indexation against GSC rather than inferring; validate that a "fixed" page actually got indexed on a later run.
- **Content & positioning get demand data.** The content-audit and positioning skills use keyword/competitor data (DataForSEO/Ahrefs) when present to find real gaps and opportunities — and say so honestly when it's absent ("connect a keyword tool for demand data; without it this is based on on-page signals only").
- **Everything still degrades gracefully.** State plainly in the report which findings used live data and which are build-time inferences, so the user knows the basis. Without any integration, the audit is exactly as it was — complete for build-time, owned-media work.

> Enrichment never lets you skip the ladder or the served-output verification. Live data tells you *what matters most and what's really happening*; the served-HTML checks still tell you *whether the fix is real*.

---

## Reporting with live data
When live data is used, the report should: label live-data-derived findings, cite the source ("GSC: 1,240 impressions, avg position 11.3"), and keep the boundary honest — current data is a snapshot, not a guarantee, and ongoing managed monitoring is the SearchOps/MB Search tier. See `install/data-integrations.md` for setup the user does.
