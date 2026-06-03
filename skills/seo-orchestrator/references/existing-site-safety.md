# Existing-site safety: don't regress what works

Read this whenever the site is **live with real traffic, rankings, or history** — i.e. most existing sites a developer points an agent at. A new "vibe-coded" site has nothing to lose; an established one has *equity you can destroy with a careless "fix."* The prime directive here:

> **First, do no harm. Understand what's working and what's intentional before you change it.**

This discipline runs *alongside* the ladder, gating every change.

---

## Why existing sites are different

- They have **rankings and traffic** that a wrong move can drop overnight.
- They have **intentional past decisions** — canonicals, redirects, `noindex`s, blocked paths — that may look "wrong" but exist for a reason. What looks like a bug may be load-bearing.
- They have **scale and legacy** — thousands of URLs, old templates, mixed patterns. A template change touches everything at once.
- They may be **earning their position partly off-site** (links, brand) — so on-page changes interact with equity you can't see.

The agent's instinct to "fix everything it sees" is exactly the wrong instinct here.

---

## The rules

### 1. Understand intent before changing
Before "correcting" a canonical, redirect, `noindex`, or `Disallow`, ask: *is this deliberate?* A `noindex` on a thank-you page, a canonical consolidating variants, a blocked `/admin` — these are correct. Surface what you find and **confirm with the user** before changing anything that could be intentional. When unsure, treat it as intentional.

### 2. Never break URLs silently — preserve equity
URLs that rank carry equity. If a URL must change (slug change, restructure, framework move):
- **Always add a `301` redirect** from old → new. Never leave a ranking URL returning `404`.
- Update internal links and the sitemap to the new URL.
- Map redirects 1:1 where possible; avoid chains and avoid dumping everything to the homepage.
- For anything beyond a handful of URLs, this is a **migration** — use the `seo-migrations` skill, which exists for exactly this.

### 3. Prefer additive, reversible changes
Adding a meta description, alt text, schema, or an answer block is low-risk and additive. Removing content, changing URLs, altering canonicals/redirects, or restructuring navigation is high-risk. Bias to additive fixes; stage the risky ones.

### 4. Stage and confirm the big rocks
For high-risk changes (URL structure, navigation/IA, removing pages, SPA→SSR, canonical strategy): **present options and trade-offs and get sign-off** — don't apply them autonomously. Recommend doing them on a branch/preview and reviewing before production.

### 5. Make everything reversible
Work in version control; keep changes in reviewable commits; recommend a deploy the user can roll back. The `.seo/log.md` entry should record what changed so a regression can be traced to a run.

### 6. Measure before and after (honestly)
Where the user has analytics/Search Console, note the **before** state so impact can be judged later — but be clear that *attributing* ranking/traffic change to a specific fix is live-data analysis, on the other side of the boundary. Set up the plumbing (`seo-measurement-setup`) if it's missing; don't pretend the build can prove the outcome.

---

## Don't-touch-without-asking checklist
Treat these as intentional until the user confirms otherwise:
- [ ] Existing `301`/`302` redirects and redirect rules.
- [ ] Existing `<link rel="canonical">` targets that consolidate variants.
- [ ] `noindex` / `X-Robots-Tag` directives.
- [ ] `robots.txt` `Disallow` rules.
- [ ] `hreflang` clusters on international sites.
- [ ] URL structure / slugs of pages that may rank.
- [ ] Primary navigation and information architecture.
- [ ] Pages with meaningful traffic (don't prune without confirming).

For each, the move is: **observe → explain what it does → ask if it's intended → only then change** (with a redirect/safeguard if needed).

---

## How this changes the lifecycle
On an existing site, the first run leans **audit-heavy**: produce the prioritised report and the quick, safe, additive wins, but hold the big rocks for explicit sign-off. The value is the clear picture plus low-risk improvements — not a sweeping rewrite that risks the rankings the site already has. Progression runs then chip away at the backlog safely, with regression checks guarding what you've changed.
