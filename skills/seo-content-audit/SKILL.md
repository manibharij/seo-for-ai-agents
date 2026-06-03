---
name: seo-content-audit
description: >-
  Audit a site's existing CONTENT (not just its markup) — quality and depth,
  search-intent match, topical gaps, keyword cannibalisation, E-E-A-T, freshness and
  decay, and internal-link opportunities — and recommend a keep / improve /
  consolidate / prune / refresh action for each page. Use when you want page-by-page
  content DECISIONS across the whole site — "content audit", "is my content good",
  "content gaps", "which pages to update, merge, or remove", "thin content across my
  site". (For the full technical+content audit use seo-orchestrator; to rewrite one
  specific page's copy use seo-content-editing; for topic/positioning strategy use
  seo-positioning-strategy.) Assesses real content on the served output; uses
  connected live data (Search Console / keyword tools) when present, never required.
---

# Content Audit — assess the content itself

A specialist skill for the **content** layer of search marketing: not "is the title tag set" (that's Read) but "**is this page actually good, for the right intent, and worth keeping?**" It produces a content inventory with an honest quality verdict and a clear action per page. It pairs with `seo-content-editing` (which does the improving) and feeds `seo-proposal-roadmap`.

> White-hat, always: this **assesses and recommends** on real content. It never fabricates content, metrics, or quality it can't observe. Where it needs live demand/performance data it doesn't have, it says so rather than guessing.

Work: **Inventory → Assess → Recommend an action per page → Report.** (Diagnosis-led; the *fixing* is `seo-content-editing`'s job.)

---

## Step 1 — Inventory

- Build a list of the site's real content pages (from routes/sitemap/CMS, or a crawl). Group by template/type and by topic.
- If **Search Console** is connected (optional — see `seo-orchestrator/references/live-data-integrations.md`), pull impressions/clicks/position per page: this tells you what's actually working, declining, or invisible. If not connected, assess on content signals alone and say so.
- If a **keyword tool** (DataForSEO/Ahrefs) is connected, pull demand and competitor context for the topics. If not, base gap analysis on on-page/topical signals and flag the limitation.

## Step 2 — Assess each page

On the **served content** (what's actually there), judge:
- **Quality & depth** — does it comprehensively, specifically, and accurately serve its topic, or is it thin/generic/padded? (See `references/quality-and-intent.md`.)
- **Search-intent match** — does it answer what someone arriving actually wants (informational/commercial/transactional/navigational)? Mismatch is a top failure.
- **E-E-A-T** — is there genuine experience/expertise/authorship/sourcing, or is it anonymous and unsupported? (Real signals only — never invent them.)
- **Freshness / decay** — is it current where recency matters? With GSC, is traffic **declining** (decay) — a prime refresh candidate?
- **Cannibalisation** — do multiple pages target the same intent and compete? (See `references/decay-cannibalisation-actions.md`.)
- **Topical gaps** — what should exist for this topic and doesn't (gaps), grounded in real demand if a keyword tool is connected.
- **Internal-link opportunities** — strong pages that should link to weaker/related ones (coordinate with the Connect rung).

## Step 3 — Recommend an action per page

Assign each page one clear action (the classic content-audit decisions — detailed in `references/decay-cannibalisation-actions.md`):
- **Keep** — performing and good; leave it (maybe minor internal-linking).
- **Improve** — good bones, needs depth/clarity/intent/E-E-A-T work → hand to `seo-content-editing`.
- **Consolidate** — merge cannibalising/overlapping thin pages into one strong page (and `301` the losers → `seo-migrations`).
- **Refresh** — decaying or outdated; genuinely update it (not just a date bump).
- **Prune** — remove/`noindex` genuinely valueless pages (carefully, with redirects if they have any equity — `seo-migrations`).
- **Create** (gap) — a topic that should be covered isn't → a content brief for the human (this skill briefs; it does not auto-generate articles).

Prioritise by impact: with GSC, weight by real traffic/opportunity; without, by topical importance and effort.

## Step 4 — Report

Produce a content-audit summary the user (or their client) can act on: the inventory with each page's quality verdict, the recommended action and why, the prioritised list, and the topical gaps as briefs. Record actionable findings into `.seo/` (so the lifecycle tracks them) — but **never store raw API keys or paste in private data dumps**; store conclusions, not credentials.

Be explicit about the **basis**: which judgements used live data (cite it — "GSC: −38% clicks over 6 months → refresh") and which are content-signal inferences. And the boundary: this assesses and plans; producing the improved content is editing (real content, by a human or with `seo-content-editing`), and ongoing performance is live data.

---

## Reference files
- `references/quality-and-intent.md` — how to judge content quality, depth, search-intent match, and genuine E-E-A-T (without fabricating any of it).
- `references/decay-cannibalisation-actions.md` — spotting decay and cannibalisation, and the keep/improve/consolidate/refresh/prune/create decision framework.
