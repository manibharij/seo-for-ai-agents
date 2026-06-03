# SEO Audit — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the orchestrator's audit lifecycle. This is the best starting point for a broad request on a NEW or EXISTING site — it runs the whole Visibility Ladder as a repeatable audit with memory.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** On an existing/live site, protect what already works: review every change on the *served* output and test before you publish. See the repo's `DISCLAIMER.md`.

---

You are running a full SEO/AEO audit on my site using the **Visibility Ladder** (5 rungs, in dependency order), as a **repeatable lifecycle with memory**. Work in four steps. **Verify everything on the SERVED HTML, not the source.** Stay strictly white-hat (never fabricate authors/reviews/credentials — flag them for me). If my site is live with real traffic, **don't regress what works** — understand what's intentional before changing it, and preserve URLs (add 301s if any URL must change).

## Step 0 — Context & memory
- **Check for a `.seo/` folder** in the project. If none → this is a **first run** (baseline). If it exists → read `.seo/state.json` and `.seo/log.md` first; this is a **progression run**.
- Detect my **stack/platform** (Next.js, Astro, WordPress, Shopify…) — diagnosis is the same everywhere, but fixes are code edits on a code site and platform settings on a hosted CMS. Ask if unsure.
- Note my **site type** (blog, e-commerce, local, SaaS/marketing, docs, international) — it changes which issues matter most.

## Step 1 — Audit (diagnose top-to-bottom, don't fix yet)
On a sample of templates (homepage AND an article/product/deep page), check each rung on the served HTML:
1. **Reach** — content in raw served HTML (not just after JS)? 200? HTTPS? no stray `noindex`? robots/sitemap ok?
2. **Read** — one descriptive `<h1>`? unique title/description? substantive, intent-matched content? mobile-friendly? Core Web Vitals causes (unsized/oversized images, render-blocking JS, shifting fonts)?
3. **Understand** — valid, **honest** schema (JSON-LD) for the page's entities, in the served HTML?
4. **Connect** — real `<a href>` links, no orphans, exactly one correct canonical, no duplicate-URL sprawl?
5. **Rank** (the goal) — good and relevant enough to rank: matches search intent, genuinely useful/competitive, real E-E-A-T, topical authority?
Then, *on top of the ladder* (only once it can rank): **Cite (AEO)** — self-contained answer blocks, question-shaped headings, consistent entities, genuine attribution, AI-crawler access.
Score each rung and find **the floor** (lowest failing rung). Work out the site's purpose, audience, stack and sector yourself, don't ask me to describe it.

## Step 2 — Save state to `.seo/`
Create/update a **`.seo/` folder** in my project (commit it — don't gitignore it):
- `audit.md` — readable health scorecard, the floor, prioritised open items, what you fixed, what needs me.
- `state.json` — every finding: id, rung, title, page, severity, effort, status (open/fixed/needs-human/deferred/wontfix/regression), evidence.
- `log.md` — a dated entry summarising this run.
On a **progression run**, first **re-verify previously fixed items on the served HTML (catch regressions)**, then add new findings.

## Step 3 — Fix (floor up, prioritised)
Fix the lowest failing rung first, verify on served HTML, then climb. Order: **regressions → the floor → high-impact/low-effort quick wins → bigger items**. Apply safe, additive fixes; for risky/big changes (URL structure, re-architecture, removing content) **present options and get my sign-off** — don't do them silently. Update `.seo/` as you go.

## Step 4 — Report (plain English)
Tell me: where my site stands (scorecard + the floor + trend vs last run), what you fixed and why (with served-HTML proof), what needs me (decisions + any real trust signals you refused to invent). **Boundary:** these are build-time, owned-media fixes — they can't by themselves tell me if I actually rank or get cited (that's live data; I can optionally connect my own Search Console/keyword tool with my keys to enrich the audit, or use a managed service), and they don't cover earned media (backlinks/PR).

Run me again after changes — I'll re-verify fixes, catch regressions, and advance.
