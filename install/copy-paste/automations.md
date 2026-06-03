# Automations / CI-CD — copy-paste mini (paste this into your AI coding agent)

*Self-contained version of the automations skill. Turns the audit into a CI guard rail that catches SEO regressions before they ship.*

> ⚠️ **Experimental, and run by an AI agent — which can make mistakes.** Review the CI config and confirm the gate actually fails on a real regression before relying on it. See the repo's `DISCLAIMER.md`.

---

You are automating my SEO audit so regressions are caught in CI before they ship. **The honest split:** CI runs without you, so it runs the **mechanisable** checks (served-HTML content presence, status codes, noindex, canonical, redirects, sitemap, Core Web Vitals via Lighthouse CI). The **deeper judgement audit** (content quality, schema honesty, positioning) stays a periodic run with me in the loop — CI is the gate, not the whole audit. Work in four steps.

## Step 1 — Diagnose
What CI exists (GitHub Actions, GitLab…)? Is there a **deploy-preview URL** (Vercel/Netlify preview, staging) to run checks against — CI needs a running URL to inspect served HTML. What's worth gating: primary content missing from served HTML (Reach broke), non-200/redirect chains, stray noindex, missing/wrong canonical, invalid sitemap, post-migration redirects that lost their target, CWV regressions.

## Step 2 — Set up (write into my repo)
- A **served-HTML regression check** (GitHub Action): for key pages, assert 200, that a distinctive content phrase is in the **raw** HTML, no stray noindex, a correct canonical, and a reachable sitemap — **fail the build** on a critical miss.
- **Lighthouse CI** on key templates for CWV + the SEO audit, with budgets (gate SEO hard, performance as a warning).
- **Link/redirect checks** (broken links; post-migration old URLs still 301/308 single-hop).
- A **scheduled (cron) re-audit** against production for drift.
- Optional **pre-deploy/pre-commit hooks** for fast local feedback.
- Keep it fast, deterministic, **no paid data required**. **Fail** only on genuine high-severity regressions; **warn** on minor drift (don't cause false-failure fatigue).

## Step 3 — Verify
Confirm the workflow runs on the right trigger; **prove it catches a regression** (temporarily point a check at a known noindex/client-rendered page → job fails; healthy build → passes); confirm it hits the right URL (preview for PRs, prod for schedule) and leaks no secrets.

## Step 4 — Report
Tell me what's automated, what it gates vs warns, when the scheduled audit runs, and the boundary: **CI catches mechanisable regressions; run the full audit periodically for depth, and live performance is still live data.**
