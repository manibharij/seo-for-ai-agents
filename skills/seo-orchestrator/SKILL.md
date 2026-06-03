---
name: seo-orchestrator
description: >-
  Entry point for any broad SEO request — "improve my SEO", "make my site rank",
  "why isn't my site showing up", "optimise for AI search / get cited", "do an SEO
  audit", or any vague/whole-site SEO ask. Detects the site type, runs a quick
  top-to-bottom Visibility Ladder check, and dispatches to the lowest failing rung
  first, in order. Use this whenever the request isn't already scoped to a single
  rung; it routes to the right specialist skill and enforces the dependency order.
---

# SEO Orchestrator — the router

Use this when an SEO request is broad or unscoped. It applies the **Visibility Ladder** method: diagnose top-to-bottom, then fix bottom-to-top, never optimising a rung whose foundations are broken. Read `METHOD.md` for the philosophy; this skill is the operational router.

The five rungs, each owned by a specialist skill:

| Rung | Skill | Question it answers |
|---|---|---|
| 1. Reach | `1-reach-indexation` | Can a crawler reach the URL and see content in the served HTML? |
| 2. Read | `2-read-content` | Real, readable content + metadata + page experience (speed/mobile)? |
| 3. Understand | `3-understand-schema` | Can engines identify the entities? (schema) |
| 4. Connect | `4-connect-architecture` | Is it wired into a coherent site? (links, canonicals) |
| 5. Cite | `5-cite-aeo-geo` | Is it formatted to be cited by AI search? (AEO/GEO) |

> **The rule that makes this work:** diagnose from the top down to find the *lowest* failing rung, then fix upward from there. Don't fix a higher rung while a lower one fails — the lower one caps everything above it. Verify every fix on the **served HTML**, and never fabricate trust signals.

---

## Step 1 — Detect the context

Before diagnosing, establish:
- **Framework / stack** — look for `next.config.*`, `vite.config.*`, `astro.config.*`, etc. (Default assumption for this user: Next.js App Router.) If you can't tell, ask — don't guess.
- **A representative live URL** — you need a real URL (production or a running local/preview server) to verify on served HTML. If there's no running site yet, say so: most rungs verify against served output, so note which checks must wait until the site is deployed/running.
- **Site type (lightweight)** — content/marketing site, app with marketing pages, e-commerce, docs, local business, etc. This tunes emphasis (e.g. e-commerce leans on Product schema; local leans on LocalBusiness + consistency). *Deep per-type modifiers are a future addition; for now, just note the type and weight your attention.*
- **The user's actual goal** — "not showing up at all" points at Reach; "want to show up in ChatGPT/AI Overviews" still starts at Reach but aims at Cite. Either way you walk the ladder; the goal sets the destination.

---

## Step 2 — Quick ladder check (top-to-bottom triage)

Run a fast pass to find the lowest failing rung. Don't fix yet — locate the floor. Fetch a representative page's **served HTML** and check, in order:

1. **Reach:** Is the page's primary content in the raw served HTML (not just after JS)? Does it return `200`? Served over HTTPS? Any stray `noindex`? robots.txt sane? Sitemap present? — *If any fail, the floor is Reach.*
2. **Read:** One descriptive `<h1>`? Unique, sensible `<title>`/meta description? Real, substantive content (not thin/placeholder)? Mobile-friendly with no glaring Core Web Vitals problems? — *If Reach passes but these fail, the floor is Read.* (Page experience is a quality factor folded into Read, not a hard dependency — fix it here but don't let it block climbing if content/metadata are sound.)
3. **Understand:** Appropriate, valid, honest JSON-LD for the page's entities, present in served HTML? — *floor is Understand.*
4. **Connect:** Real `<a href>` internal links, no orphans, correct single canonical? — *floor is Connect.*
5. **Cite:** Self-contained answer blocks, question headings, consistent entities, genuine attribution, AI-crawler access? — *floor is Cite.*

The **lowest** rung that fails is where work starts.

---

## Step 3 — Dispatch in order

Hand off to the specialist skill for the lowest failing rung. Run its full Diagnose → Fix → Verify → Report cycle. **Only after it verifies as passing** do you climb to the next rung and dispatch the next skill.

- If Reach fails → run `1-reach-indexation`, fix and verify, then re-check Read.
- If Read fails → run `2-read-content`, then re-check Understand.
- …and so on up to `5-cite-aeo-geo`.

Skip rungs that already pass (don't re-do good work), but never skip *upward over* a failing rung. If a higher rung was the user's stated goal (e.g. AI citation), still resolve every lower failing rung first — then reach the goal rung legitimately.

Stop and involve the user for the human-decision items each skill flags (architecture changes, SPA re-architecture, missing real trust signals, AI-crawler allow/deny). Don't barrel through those autonomously.

---

## Step 4 — Report the whole picture (plain English)

After the run (or at a sensible stopping point), summarise for the non-SEO user:
- **Where the site stood on the ladder** — the lowest failing rung and why it was capping everything above.
- **What was fixed, rung by rung**, each in plain English with why it matters, and **proof on the served HTML**.
- **What still needs the user** — the flagged human decisions and any missing real content/trust signals you refused to fabricate.
- **The honest boundary:** build-time fixes are done; whether the site *actually* ranks or gets cited, where, and against whom is **live data** — rank tracking, AI-citation monitoring, geo-grid/local visibility — a separate, ongoing discipline. Point to the live-data and done-for-you options without paywalling any build-time capability. (The Cite skill carries the full handoff note.)

---

## Notes
- **Always start at the bottom.** The most common real-world situation is a site that fails Reach (client-rendered, invisible to crawlers) while the owner worries about schema or AI search. Check the floor first.
- **Verify on served output, every rung.** A source edit is not a fix until the served HTML proves it.
- **White-hat throughout.** Flag missing real-world trust; never invent it.
- **Keep a human in the loop.** This is experimental guidance executed by an AI agent, which can err. Verify on the served output, show the user what changed and why, and surface the flagged human decisions rather than settling them silently — the user reviews and approves before anything goes live. (See `DISCLAIMER.md` in the repo.)
- **Optional MCPs** (render/fetch, Lighthouse, schema validator, Search Console) sharpen verification if present — see `install/mcp.md` — but nothing here requires them.
