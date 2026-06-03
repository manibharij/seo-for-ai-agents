# SEO Audit, read-only — copy-paste mini (paste this into your AI coding agent)

*A safe, analysis-only version of the audit. It runs the whole Visibility Ladder and reports what it finds, but **changes nothing** — no code edits, no files written. Use it for a first look, in auto-mode, or on a live site you don't want touched. When you're ready to actually fix things, switch to [`audit.md`](audit.md), which runs Diagnose → Fix → Verify → Report and writes a `.seo/` folder.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** This prompt is read-only by design, but always sanity-check the findings; an agent can still misread context. See the repo's `DISCLAIMER.md`.

---

You are running a **read-only** SEO/AEO audit of my site using the **Visibility Ladder**. This is analysis only.

**Do not change anything.** Do not edit any code, do not create or modify any files (including a `.seo/` folder), do not run commands that alter the project, and do not apply any fixes. If you think something should change, **describe it** — don't do it. **Verify everything on the SERVED HTML, not the source.** Work out my site's purpose, audience, stack and sector yourself from the code and the served pages; don't interrogate me.

## Step 1 — Diagnose (top to bottom, on the served HTML)
On a representative sample of templates (homepage AND an article/product/listing/deep page, not just the homepage), assess each rung:
1. **Reach** — is the content in the **raw** served HTML (not just after JS)? `200`? HTTPS? no stray `noindex` (check the meta tag *and* the `X-Robots-Tag` header)? robots.txt and sitemap sane?
2. **Read** — one descriptive `<h1>`? unique, sensible title/description? substantive, intent-matched content? mobile-friendly? obvious Core Web Vitals causes (unsized/oversized images, render-blocking JS, shifting fonts)?
3. **Understand** — valid, **honest** structured data (JSON-LD) for the page's real entities, present in the served HTML?
4. **Connect** — real `<a href>` internal links, no orphans, exactly one correct canonical, no duplicate-URL sprawl?
5. **Rank** (the goal) — good enough, and trusted enough, to win: matches search intent, genuinely useful/competitive, real on-page E-E-A-T, topical authority? (Assess the owned-media half; off-site authority is out of scope for a build-time audit, just note it.)

Then, *on top of the ladder*: **Cite (AEO)** — self-contained answer blocks, question-shaped headings, consistent entities, genuine attribution, AI-crawler access. Assess for pages whose ranking fundamentals are already sound.

## Step 2 — Report (plain English, no changes made)
Give me, in chat:
- **A health scorecard** — each rung scored (pass / minor / failing) and **the floor** (the lowest failing rung, where fixing should start).
- **A prioritised list of issues** — each with the page/template, the evidence (what you saw in the served HTML), the **recommended fix**, and the **risk** of making it. Order by impact and dependency (lowest failing rung first).
- **What needs me** — any real trust signals (authors, credentials, reviews, sources) that are missing and must not be invented, plus any change risky enough to need my sign-off.
- **The boundary, plainly** — these would be build-time, owned-media fixes; they can't on their own tell me whether I actually rank or get cited (that's live data), and they don't cover earned media (backlinks/PR).

Do not apply any of it. When I've reviewed and I'm ready, I'll ask you to proceed (or I'll run the full `audit.md` mini, which fixes from the floor up and records state in `.seo/`).
