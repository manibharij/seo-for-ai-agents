# The audit lifecycle: first run vs progression

Read this to run the Visibility Ladder as a repeatable audit, not a one-shot. The defining idea: **the pack remembers.** State in `.seo/` (see `audit-report-and-state.md`) lets every run build on the last — baseline, then progress, then maintain.

The three phases a site moves through:
1. **Baseline** (first run) — find everything, fix the safe wins, record state.
2. **Progress** (next runs) — re-verify what was fixed, find what's new, advance the backlog.
3. **Maintain** (ongoing) — catch regressions after deploys/content changes, keep the score healthy.

---

## Walking the ladder as an audit

Whether baseline or progression, the audit itself is the same top-to-bottom sweep — you're taking the site's vitals, not fixing yet.

For a **representative sample of templates** (homepage *and* an article, a product, a listing, a deep page — not just the homepage, which often hides problems), assess each rung on the **served HTML**:

1. **Reach** — content present in raw served HTML (not just after JS)? `200`? HTTPS? no stray `noindex`? robots sane? sitemap present and correct?
2. **Read** — one descriptive `<h1>`? unique sensible title/description? substantive, intent-matched content? mobile-friendly? no glaring Core Web Vitals causes?
3. **Understand** — appropriate, valid, **honest** JSON-LD for the page's entities, present in served HTML?
4. **Connect** — real `<a href>` internal links, no orphans, exactly one correct canonical, no duplicate-URL sprawl?
5. **Rank** — does the page match the intent it should serve, with genuine quality/depth, real on-page E-E-A-T, and a credible topical cluster? (The owned-media half; off-site authority is advised separately, not scored here.)
- **+ Cite (on top of the ladder, not a rung)** — self-contained answer blocks, question-shaped headings, consistent entities, genuine attribution, AI-crawler access. Assess for pages whose ranking fundamentals are already sound.

Record each finding (see the state format): which rung, which page/template, severity, and an effort estimate. **Score each rung** (e.g. pass / minor issues / failing) so the report shows a clear health picture and an obvious floor.

> The **floor** is the lowest failing rung. It's where fixing starts, because it caps everything above it.

---

## Mode A — First run (baseline)

1. **Confirm there's no `.seo/`** (Step 0). This is a clean baseline.
2. **Full audit sweep** across the sample templates and all five rungs. Capture every finding; don't fix mid-sweep.
3. **Write the baseline state** — create `.seo/audit.md`, `.seo/state.json`, `.seo/log.md` (templates in `audit-report-and-state.md`). Every finding starts `open`.
4. **Fix from the floor up.** Dispatch to the lowest failing rung's specialist skill; run its Diagnose→Fix→Verify→Report; mark fixed findings `fixed` (with the served-HTML proof noted); then climb. Apply safe fixes autonomously; set risky/judgement items to `needs-human` and surface them.
5. **Don't over-reach on a first run.** It's fine — often better — to fix the safe, high-impact wins and leave a clear prioritised backlog for the next run, especially on a large or established site. Record what you deliberately deferred.
6. **Report**: the baseline scorecard, what was fixed (with proof), what needs the user, and the honest boundary.

---

## Mode B — Progression run

1. **Read prior state first** (`state.json`, `log.md`). You are continuing, not restarting.
2. **Regression check (do this before new work).** For every finding marked `fixed`, re-verify on the **served HTML** that the fix still holds. Deploys, refactors, CMS edits, and content changes silently undo fixes. Any that broke → set back to `open`, tag `regression`, and treat as **high priority** (a regression on something you previously fixed is worse than a never-fixed minor issue).
3. **Re-audit for new issues.** New pages, new templates, new content since the last run — sweep them. Add new findings as `open`.
4. **Advance the backlog.** Work items in this order: **regressions → highest priority score → rung order**. Pick up `deferred`/`needs-human` items the user is now ready for.
5. **Update state.** Change statuses, add new findings, and append a dated `log.md` entry summarising this run (what regressed, what's new, what advanced, current scores).
6. **Report the trend.** Show movement since last run — score deltas per rung, regressions caught, net progress. This is the payoff of the lifecycle: the user sees a system improving over time, not a black box.

---

## How often to run
- **After any significant change/deploy** — the fastest way to catch regressions.
- **When adding content or pages** — new templates need auditing.
- **Periodically** for a live site — search engines, AI engines, and your own site all change.

Each run is cheap because state makes it incremental: re-verify, find new, advance. The first run is the big one; the rest compound.

---

## What stays out of the lifecycle
The lifecycle tracks **build-time, owned-media** state — what's in the code/served output and whether your fixes hold. It does **not** track live outcomes (actual rankings, traffic, AI citations, competitor moves); those need live data and live monitoring, which is the product boundary, not something `.seo/` should pretend to know. Keep `.seo/` honest: it records what was changed and verified, not what the market did in response.
