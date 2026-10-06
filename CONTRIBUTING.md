# Contributing to seo-for-ai-agents

Thanks for considering a contribution. This pack lives or dies by its **correctness and restraint**, not its size — it is deliberately not another 20-item flat checklist. Contributions are very welcome when they hold that bar.

## The bar for any change

1. **Respect the ladder's dependency order.** The method is the [Visibility Ladder](METHOD.md): Reach → Read → Understand → Connect → **Rank** (the goal), diagnosed top-to-bottom and fixed bottom-to-top, with **AEO/citation (`cite-aeo-geo`) as the optional layer on top, not a rung**. New advice must fit a rung and respect what must pass beneath it.
2. **Verify on served output, not source.** Every check or fix must be confirmable on what's actually *served* to a crawler (fetched/rendered HTML), never on the assumption that a source edit worked.
3. **Strictly white-hat.** Nothing that fabricates trust signals (authors, reviews, credentials, ratings) or deceives engines or users. Where a real signal is missing, the correct output is a flagged human task — never an invention.
4. **Be honest about the boundary.** Free skills fix build-time, owned-media problems. They do not promise rankings or citations, and they don't cover earned media or live measurement. Don't add claims that cross that line.
5. **Match the template.** Every skill has the standard **Inputs and modes** block (see `skills/seo-orchestrator/references/operating-modes.md`) and follows **Diagnose → Fix → Verify (on the served output) → Report**, with a lean `SKILL.md` (well under 500 lines) and depth pushed into `references/`. Every skill supports the three modes: `audit` (the default, never changes the site), `fix` (approved findings only) and `re-check`. Findings use the shared schema in `audit-report-and-state.md`. Each full skill has a self-contained mini in `install/copy-paste/`.
8. **Date volatile facts.** Crawler tokens, quotas, rich-result availability, CDN defaults and framework APIs change often. Stamp each with "verified YYYY-MM" beside its source URL. `scripts/check-freshness.py` and a monthly workflow flag anything stale (see `skills/seo-automations/references/freshness.md`).
9. **Fetched content is data.** Skills must treat anything fetched from a site (HTML, robots.txt, llms.txt, API responses) as data, never as instructions.
6. **Protect existing sites.** Contributions must respect the don't-regress discipline — preserve URLs (301s), treat existing canonicals/redirects/`noindex`/`hreflang` as potentially intentional, prefer additive/reversible fixes, and flag big changes for human sign-off.
7. **British English**, imperative voice, explain *why* a step matters rather than stacking bare rules.

## Repo structure

- `skills/seo-orchestrator/` — the conductor: runs the audit lifecycle and carries the cross-cutting references (`audit-lifecycle`, `audit-report-and-state`, `prioritisation`, `existing-site-safety`, `stack-and-platform-adapters`, and `profiles/`). Keep cross-cutting concerns here so they travel with the pack.
- `skills/1-reach-indexation/` … `skills/5-rank-relevance/` — the five rung skills (the ladder, climbing to the goal: **Rank**), each with `references/` and a mini in `install/copy-paste/`.
- `skills/cite-aeo-geo/` — the **AEO/citation layer on top** of the ladder (not a rung; applied after a page can rank).
- `skills/seo-context-gathering/`: the foundation, learns the business into `.seo/context.md`.
- `skills/seo-search-data/`: reads the user's own search data through capability detection; the per-API recipes live in `skills/seo-orchestrator/references/data/`.
- `skills/seo-launch-qa/`, `skills/seo-performance/`, `skills/seo-migrations/`, `skills/seo-measurement-setup/`: technical specialist skills beside the ladder.
- `skills/seo-content-audit/`, `skills/seo-content-editing/`, `skills/seo-positioning-strategy/`, `skills/seo-proposal-roadmap/` — the content & marketing layer (assess, improve real copy, plan topical authority, package proposals). These read optional live data when connected.
- `skills/seo-automations/`, `skills/seo-media/`, `skills/seo-programmatic/`, `skills/seo-log-analysis/` — automation & advanced (CI/CD regression gates, image/video SEO, white-hat pages-at-scale, server-log/crawl-budget analysis).
- `skills/seo-offsite-authority/` — the off-page half (backlink audit, disavow, white-hat link-building/digital-PR strategy). Advisory; never executes or buys links.
- [`SKILLS.md`](SKILLS.md) — the canonical skills index; keep it in sync when adding/removing a skill.
- `install/`: per-host guides, the `copy-paste/` minis (including `audit.md`, `fix.md` and `recheck.md` for the three modes), `mcp.md` (the tool ladder) and `data-integrations.md` (capability detection for live data).
- `scripts/check-freshness.py` and `.github/workflows/freshness.yml`: the monthly check for stale dated facts and broken source links.
- The agent writes a `.seo/` folder into the *user's* project (audit/state/log) — that's runtime output, documented in `audit-report-and-state.md`, not part of this repo.

## How to contribute

- **Issues:** corrections (especially anything that's become factually stale — search/AEO changes fast), unclear guidance, or gaps within an existing rung's scope.
- **Pull requests:**
  - Keep the change focused and explain *why* it earns its place.
  - If you touch a full skill, update its `copy-paste/` mini to match (and vice versa).
  - Check that internal links still resolve and any code snippets are correct for the stated stack (Next.js App Router by default).
  - Verify any new claim against a current primary source (e.g. Google's structured-data/rich-result docs) — don't rely on older SEO folklore.

## Out of scope (for now)

- **Doing earned media.** Off-site authority isn't a build-time action. `seo-offsite-authority` audits and advises on it; the pack never sends outreach, buys links or exchanges them.
- **Running data infrastructure.** The pack reads whatever data the user's environment already provides (through `seo-search-data` and capability detection) but never sets up, pays for or writes to those tools. Ongoing monitoring products (rank tracking, geo-grid, AI-citation tracking) stay outside the pack.
- **Deep hosted-platform fix automation** — the pack diagnoses any site, but on hosted platforms (WordPress/Shopify/Webflow) it currently *instructs* rather than auto-fixes. Deeper per-platform fix guidance is a welcome contribution (see `stack-and-platform-adapters.md`).
- **New site-type profiles** are welcome — extend `skills/seo-orchestrator/references/profiles/` following the existing ones.

## Licence

By contributing, you agree your contributions are licensed under the repository's [MIT Licence](LICENSE).
