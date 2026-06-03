# Contributing to seo-for-ai-agents

Thanks for considering a contribution. This pack lives or dies by its **correctness and restraint**, not its size — it is deliberately not another 20-item flat checklist. Contributions are very welcome when they hold that bar.

## The bar for any change

1. **Respect the ladder's dependency order.** The method is the [Visibility Ladder](METHOD.md): Reach → Read → Understand → Connect → Cite, diagnosed top-to-bottom and fixed bottom-to-top. New advice must fit a rung and respect what must pass beneath it.
2. **Verify on served output, not source.** Every check or fix must be confirmable on what's actually *served* to a crawler (fetched/rendered HTML), never on the assumption that a source edit worked.
3. **Strictly white-hat.** Nothing that fabricates trust signals (authors, reviews, credentials, ratings) or deceives engines or users. Where a real signal is missing, the correct output is a flagged human task — never an invention.
4. **Be honest about the boundary.** Free skills fix build-time, owned-media problems. They do not promise rankings or citations, and they don't cover earned media or live measurement. Don't add claims that cross that line.
5. **Match the template.** Every skill follows **Diagnose → Fix → Verify (on rendered output) → Report to the user (plain English)**, with a lean `SKILL.md` (well under 500 lines) and depth pushed into `references/`. Each full skill has a self-contained `copy-paste/` mini.
6. **Protect existing sites.** Contributions must respect the don't-regress discipline — preserve URLs (301s), treat existing canonicals/redirects/`noindex`/`hreflang` as potentially intentional, prefer additive/reversible fixes, and flag big changes for human sign-off.
7. **British English**, imperative voice, explain *why* a step matters rather than stacking bare rules.

## Repo structure

- `skills/seo-orchestrator/` — the conductor: runs the audit lifecycle and carries the cross-cutting references (`audit-lifecycle`, `audit-report-and-state`, `prioritisation`, `existing-site-safety`, `stack-and-platform-adapters`, and `profiles/`). Keep cross-cutting concerns here so they travel with the pack.
- `skills/1..5-*/` — the five rung skills, each with `references/` and a `copy-paste/` mini.
- `skills/seo-migrations/`, `skills/seo-measurement-setup/` — technical specialist skills beside the ladder.
- `skills/seo-content-audit/`, `skills/seo-content-editing/`, `skills/seo-positioning-strategy/`, `skills/seo-proposal-roadmap/` — the content & marketing layer (assess, improve real copy, plan topical authority, package proposals). These read optional live data when connected.
- `install/` — per-host guides + `copy-paste/` minis + `mcp.md` (MCP layer) + `data-integrations.md` (optional bring-your-own-key live-data tools).
- The agent writes a `.seo/` folder into the *user's* project (audit/state/log) — that's runtime output, documented in `audit-report-and-state.md`, not part of this repo.

## How to contribute

- **Issues:** corrections (especially anything that's become factually stale — search/AEO changes fast), unclear guidance, or gaps within an existing rung's scope.
- **Pull requests:**
  - Keep the change focused and explain *why* it earns its place.
  - If you touch a full skill, update its `copy-paste/` mini to match (and vice versa).
  - Check that internal links still resolve and any code snippets are correct for the stated stack (Next.js App Router by default).
  - Verify any new claim against a current primary source (e.g. Google's structured-data/rich-result docs) — don't rely on older SEO folklore.

## Out of scope (for now)

- **Earned media** (backlinks, digital PR, third-party reviews) — off-site authority isn't a build-time action.
- **Live data** (rank tracking, AI-citation monitoring, geo-grid/local visibility) — separate, ongoing disciplines, not build-time fixes. `seo-measurement-setup` wires up the *instruments* only; reading them is out of scope.
- **Deep hosted-platform fix automation** — the pack diagnoses any site, but on hosted platforms (WordPress/Shopify/Webflow) it currently *instructs* rather than auto-fixes. Deeper per-platform fix guidance is a welcome contribution (see `stack-and-platform-adapters.md`).
- **New site-type profiles** are welcome — extend `skills/seo-orchestrator/references/profiles/` following the existing ones.

## Licence

By contributing, you agree your contributions are licensed under the repository's [MIT Licence](LICENSE).
