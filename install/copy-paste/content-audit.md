# Content Audit — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the content-audit skill. Assesses your existing content and recommends an action per page. Pairs with content-editing.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** It assesses real content and never fabricates content or metrics. Review its verdicts before acting. See the repo's `DISCLAIMER.md`.

---

You are auditing my existing **content** (not just markup): quality, search-intent match, gaps, cannibalisation, E-E-A-T, freshness/decay, and internal-link opportunities — and recommending one action per page. Work in four steps. **Assess real content on the served output; never fabricate content, metrics, or quality you can't observe.**

## Step 1 — Inventory
List my real content pages (sitemap/routes/CMS/crawl), grouped by topic/type. **If I've connected Search Console** (optional, my own key), pull impressions/clicks/position to see what actually performs/declines — otherwise assess on content signals and say so. **If a keyword tool (DataForSEO/Ahrefs) is connected**, use real demand/competitor data for gaps; otherwise infer and flag the limitation.

## Step 2 — Assess each page
On the served content: **quality/depth** (specific and comprehensive, or thin/generic?), **intent match** (does it answer what the visitor wants?), **E-E-A-T** (genuine authorship/expertise/sources, or anonymous?), **freshness/decay** (outdated? declining in GSC?), **cannibalisation** (multiple pages competing for one intent?), **topical gaps**, and **internal-link opportunities**.

## Step 3 — Recommend one action per page
- **Keep** (performs + good), **Improve** (good bones, needs work → content-editing), **Refresh** (decaying/outdated → genuinely update + truthful date), **Consolidate** (merge cannibalising/overlapping pages, 301 the rest), **Prune** (valueless — carefully, redirect if it has equity), **Create** (real in-demand gap → write a **brief for me**, don't auto-generate the article).
Prioritise by real traffic/opportunity (with GSC) or topical importance + effort (without).

## Step 4 — Report
Give me the inventory with each page's verdict, recommended action + why, the prioritised list, and gaps as briefs. **Label the basis** (live-data-backed vs content-signal inference). Don't store my API keys anywhere. **Boundary:** this assesses and plans; producing improved content is editing real content (not invention), and ongoing performance is live data.
