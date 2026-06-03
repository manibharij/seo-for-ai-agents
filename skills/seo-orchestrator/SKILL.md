---
name: seo-orchestrator
description: >-
  The entry point and conductor for all SEO/AEO work — use for any broad or unscoped
  request ("improve my SEO", "audit my site", "why isn't my site showing up",
  "optimise for AI search", "fix my indexing") on a NEW or EXISTING site. Detects the
  stack, platform, and site type; runs the Visibility Ladder as a repeatable AUDIT
  LIFECYCLE with persistent state in .seo/; fixes the lowest failing rung first; and
  on later runs re-verifies past fixes, catches regressions, and advances. Routes to
  the specialist rung skills and protects existing sites from regressions.
---

# SEO Orchestrator — the conductor

This is the brain of the pack. It turns the five rung skills into one **adaptive audit lifecycle** that works the first time *and every time after*, on a freshly built site or a mature one with existing rankings. Read `METHOD.md` for the philosophy; this skill runs it.

Two ideas drive everything here:
- **The Visibility Ladder** — five rungs in dependency order (Reach → Read → Understand → Connect → Cite). Diagnose top-to-bottom; fix bottom-to-top; never fix a rung while a lower one fails. Verify on the **served HTML**, never the source. Stay strictly white-hat.
- **The lifecycle** — an audit is not a one-shot. The first run establishes a baseline and fixes the safe wins; **every later run reads what happened before, re-verifies it still holds (regressions), finds what's new, and advances.** State lives in a `.seo/` folder in the project so progress persists across sessions.

| Rung | Skill | Question |
|---|---|---|
| 1. Reach | `1-reach-indexation` | Crawlable, rendered in served HTML, HTTPS, indexable? |
| 2. Read | `2-read-content` | Real content + metadata + page experience (speed/mobile)? |
| 3. Understand | `3-understand-schema` | Entities identifiable via valid, honest schema? |
| 4. Connect | `4-connect-architecture` | Wired into a coherent site (links, canonicals)? |
| 5. Cite | `5-cite-aeo-geo` | Owned-side AEO — formatted to be *eligible* for citation? |

Specialist skills outside the ladder, dispatched when relevant:
- **`seo-migrations`** — URL changes / redirects / site moves.
- **`seo-measurement-setup`** — analytics / Search Console instrumentation.
- **`seo-content-audit`** — assess existing content (quality, intent, gaps, cannibalisation, decay).
- **`seo-content-editing`** — improve existing copy (white-hat: edit real content, never generate fake).
- **`seo-proposal-roadmap`** — turn the audit into a client-style proposal / prioritised roadmap.
- **`seo-positioning-strategy`** — messaging, competitive positioning, topical-authority planning.

---

## Step 0 — Detect context (before anything)

Establish four things; they shape the whole run:

1. **First run or progression?** Check for a **`.seo/` folder** in the project.
   - **No `.seo/`** → this is a **first run**. Go to the First-run lifecycle.
   - **`.seo/` exists** → this is a **progression run**. Read `.seo/state.json` and `.seo/log.md` first, then go to the Progression lifecycle.
2. **Stack & platform.** Detect the framework (`next.config.*`, `astro.config.*`, etc.) and whether it's a **code-editable** app or a **hosted/CMS** platform (WordPress/Shopify/Webflow). This changes *how* fixes are applied. See `references/stack-and-platform-adapters.md`. If you can't tell, ask — don't guess.
3. **Site type (profile).** Content/blog, marketing/SaaS, e-commerce, local business, docs, or international? This tunes which issues matter most and adds type-specific checks. See `references/profiles/`.
4. **Existing site?** If the site is live with real traffic/rankings, switch on the **don't-regress discipline** (`references/existing-site-safety.md`) — understand what's working and intentional before you change anything.
5. **Any live-data integrations connected?** Check for **optional** BYO-key data tools (Search Console, DataForSEO, Ahrefs, Bing) via env vars/MCP. If present, use them to *enrich* the audit (real indexation, traffic-weighted priorities, demand/competitor data); if not, proceed on served-output checks alone. **Never required, never a gate** — see `references/live-data-integrations.md`. (Read keys only from env vars; never store them in `.seo/` or commits.)

> New or existing, the method is the same climb — but on an existing site you protect what already works while you improve it.

---

## The lifecycle

### Mode A — First run (no `.seo/` yet)

1. **Baseline audit.** Walk the ladder **top-to-bottom** and record the state of every rung on a representative set of pages (sample templates, not just the homepage). Don't fix yet — locate the floor and capture everything. Score each rung and collect findings. See `references/audit-lifecycle.md` and `references/prioritisation.md`.
2. **Write the baseline** to `.seo/` — `audit.md` (readable report), `state.json` (every finding with status, severity, rung, effort), `log.md` (run history). Format in `references/audit-report-and-state.md`.
3. **Fix from the floor up.** Dispatch to the lowest failing rung's skill, run its full Diagnose→Fix→Verify→Report, then climb. Apply safe fixes; **flag human decisions** (architecture, trust/E-E-A-T, anything risky on an existing site) rather than forcing them.
4. **Update state** as each finding is fixed/deferred; append to `log.md`.
5. **Report** the baseline, what was fixed, what needs the user, and the honest boundary (below).

### Mode B — Progression run (`.seo/` exists)

1. **Read prior state** (`state.json`, `log.md`) — you now know what was found, fixed, and deferred.
2. **Re-verify (regression check).** For each previously **fixed** finding, confirm on the **served HTML** that it still holds. A regression (something that was fixed and broke again — common after a deploy or content change) is high priority. Mark regressions back to `open`.
3. **Diagnose what's new.** Re-walk the ladder for new pages/templates and new issues since the last run.
4. **Advance.** Work the highest-priority open items (regressions first, then by priority score, always respecting rung order). Pick up deferred items the user is now ready for.
5. **Update `.seo/`** — new findings, status changes, a new `log.md` entry with a dated summary of this run.
6. **Report progress** — what regressed, what's new, what advanced, what's left, and the trend since last run.

Progression is what makes this a system: the second, fifth, twentieth run is never starting from scratch.

---

## Dispatch rules

- Run the specialist skill for the **lowest failing rung**, complete its verify, then climb. Skip rungs that already pass (don't redo good work) but never skip *upward over* a failing rung.
- If the user's goal is a higher rung (e.g. AI citation), still resolve every lower failing rung first — then reach the goal rung legitimately.
- Pull in **`seo-migrations`** whenever URLs change or the site moves, and **`seo-measurement-setup`** when analytics/Search Console plumbing is missing or broken.
- Pull in the **content/marketing skills** when the work is about the content itself, not just its markup: **`seo-content-audit`** (assess), **`seo-content-editing`** (improve real copy), **`seo-positioning-strategy`** (messaging/competitive/topical planning), and **`seo-proposal-roadmap`** (package the findings as a proposal/roadmap deliverable). These read live data (demand/competitor) when it's connected, and say so honestly when it isn't.
- **Enrich, don't gate.** When a live-data integration is present, use it to prioritise by real impact and ground content/positioning in real demand — but the audit and fixes never *require* it.
- Apply the active **profile** (`references/profiles/<type>.md`) and **stack/platform adapter** so each rung's checks and fixes fit this specific site.
- On an **existing site**, gate every change through `references/existing-site-safety.md`.

---

## Step — Report (plain English) + the honest boundary

Summarise for a non-SEO user (or a developer who wants the SEO judgement, not a lecture):
- **Where the site stands** — the rung scores, the floor, the trend vs last run.
- **What was fixed**, rung by rung, each with why it matters and **proof on the served HTML**.
- **What needs you** — flagged human decisions and any real content/trust signals the pack refused to fabricate.
- **The boundary** — these are build-time, owned-media fixes. Whether you actually rank, where, against whom, or get cited by AI engines over time is **live data** (rank tracking, AI-citation monitoring, geo-grid) — a separate, ongoing discipline. Earned media (backlinks, PR) is off-site and out of scope. Never paywall a build-time capability; point across the boundary honestly. (The Cite skill carries the full handoff.)

---

## Notes
- **Always start at the bottom.** The most common real situation is a site failing Reach (client-rendered, invisible to crawlers) while the owner worries about schema or AI search. Check the floor first.
- **Verify on served output, every rung, every run.** A source edit is not a fix until the served HTML proves it.
- **Keep a human in the loop.** This is experimental guidance executed by an AI agent, which can err. Show what changed and why; surface flagged decisions; the user approves before anything goes live. On existing sites, protect what already works. (See `DISCLAIMER.md`.)
- **White-hat throughout.** Flag missing real-world trust; never invent it.
- **Optional MCPs** (render/fetch, Lighthouse, schema validator, Search Console) sharpen verification if present — see `install/mcp.md` — but nothing here requires them.

## Reference files
- `references/audit-lifecycle.md` — first-run vs progression in detail; how to walk the ladder as an audit; regression re-checks.
- `references/audit-report-and-state.md` — the `.seo/` folder: `audit.md`, `state.json`, `log.md` formats, with templates.
- `references/prioritisation.md` — scoring findings by impact × effort × confidence, and sequencing them.
- `references/existing-site-safety.md` — the don't-regress discipline: protect URLs, rankings, and intentional decisions.
- `references/stack-and-platform-adapters.md` — how each rung manifests per stack, and the code-vs-hosted-platform boundary.
- `references/profiles/` — site-type profiles (content, e-commerce, local, SaaS/marketing, docs, international) that tune the audit.
- `references/live-data-integrations.md` — optional BYO-key data tools (GSC, DataForSEO, Ahrefs…) that *enrich* the audit; detect-and-use, never required, with the boundary and key-security rules.
