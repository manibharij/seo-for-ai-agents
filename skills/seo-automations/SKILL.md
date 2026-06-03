---
name: seo-automations
description: >-
  Automate the SEO audit so regressions are caught before they ship — set up CI/CD
  checks (a GitHub Action that runs the served-HTML audit on every deploy/PR and
  fails the build on a critical regression), scheduled re-audits, and pre-deploy
  hooks. Use on "run SEO checks in CI", "GitHub Action for SEO", "catch SEO
  regressions automatically", "fail the build if the site isn't indexable",
  "schedule an audit", or "automate the audit". Codifies the mechanisable checks; the
  deeper agent audit stays a periodic human-in-the-loop run.
---

# Automations — turn the audit into a guard rail

A specialist skill that automates the pack's own audit. The lifecycle already *remembers* and re-checks for regressions when you run it — this skill makes that **happen automatically**, so a deploy that would make the site invisible to crawlers gets caught in CI, not weeks later in lost traffic. It's the natural extension of the regression-catching lifecycle.

> **The honest split that makes this work.** CI runs without the AI agent, so it can only run the **mechanisable** checks — the deterministic ones (is the content in the served HTML, status codes, stray `noindex`, canonical present, redirects resolve, sitemap valid, Core Web Vitals via Lighthouse CI). The **deeper, judgement-based audit** (content quality, schema honesty, intent, positioning) stays a periodic run with a human in the loop. CI is the regression *gate*; the agent audit is the *depth*. Don't pretend CI replaces the full audit.

Work the four steps: **Diagnose → Set up → Verify → Report.**

---

## Step 1 — Diagnose

- **What CI/CD exists?** GitHub Actions (most common), GitLab CI, etc. Is there a deploy preview URL (Vercel/Netlify preview, staging) the checks can run against? CI checks need a **running URL** to inspect served HTML — a PR preview is ideal.
- **What's worth gating?** The high-severity, mechanisable regressions: primary content missing from served HTML (Reach broke — e.g. a refactor shipped client-only rendering), non-`200`/redirect chains on key URLs, a stray `noindex`, a missing/incorrect canonical, an invalid or empty sitemap, a `301` that lost its target (post-migration), Core Web Vitals falling below threshold.
- **What's already automated?** Any existing Lighthouse CI, link-checking, or sitemap validation to build on rather than duplicate.

## Step 2 — Set up

Write the automation into the user's repo (see `references/ci-recipes.md` for ready workflows):

- **A served-HTML regression check in CI** — a small script (curl/fetch + assertions, or a tiny test) that, against the deploy-preview URL, confirms: key pages return `200`, the primary content is in the **raw** HTML, no stray `noindex`, exactly one correct canonical, the sitemap is reachable and lists `200` URLs. Fail the job (and the PR) on a critical miss. This is the core guard rail.
- **Lighthouse CI** — for Core Web Vitals + the SEO audit on key templates, with budgets that fail on regression.
- **Link & redirect checks** — broken internal links; post-migration, that old URLs still `301` (or `308`) correctly in a single hop (ties to `seo-migrations`).
- **Scheduled re-audit** — a `cron`-triggered workflow (e.g. weekly) that re-runs the checks against production and reports drift; optionally updates `.seo/`.
- **Pre-deploy / pre-commit hooks** — optional local gates for fast feedback before CI.
- Keep checks **fast and deterministic**, and **don't require paid data** — they run the same served-output logic the pack uses, so they're free and host-agnostic. Any live-data enrichment stays optional.

> Tune severity to avoid false-failure fatigue: **fail** the build only on genuine high-severity regressions; **warn** (annotate the PR) on lower-severity drift. A gate that cries wolf gets disabled.

## Step 3 — Verify

- Confirm the workflow **runs** on the intended trigger (PR/deploy/schedule) and reports status.
- **Prove it catches a real regression:** temporarily introduce a failure (e.g. point a check at a known client-rendered or `noindex` page) and confirm the job fails; then confirm a healthy build passes. A gate you haven't seen fail is unproven.
- Confirm it runs against the right URL (preview for PRs, production for scheduled) and doesn't leak any secrets in logs.

## Step 4 — Report

Explain, plainly: what's now automated (e.g. "every PR now checks your key pages are still crawlable and indexable, and fails if a change makes them invisible"), what it gates vs warns, when the scheduled audit runs, and the boundary — **CI catches the mechanisable regressions; run the full agent audit periodically for depth** (content, schema honesty, positioning), and live performance is still live data. Record the automation in `.seo/log.md`.

---

## Reference files
- `references/ci-recipes.md` — a ready GitHub Actions workflow (served-HTML regression check + Lighthouse CI + scheduled re-audit), what to gate vs warn on, running against deploy previews, and hook setup.
