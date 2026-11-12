# Install for Cursor

Cursor uses **Project Rules** — Markdown-with-frontmatter files in `.cursor/rules/*.mdc` that get pulled into context based on their description or globs. `seo-for-ai-agents` maps cleanly onto them: one rule per rung, plus a router rule.

> Cursor doesn't run the SKILL packaging format directly, so you adapt each skill into a `.mdc` rule. The logic is identical; only the wrapper changes.

---

## Layout

```
<your-project>/.cursor/rules/
├── seo-audit.mdc            # the all-rounder: audit mode, changes nothing (best default)
├── seo-access-reach.mdc
├── seo-access-read.mdc
├── seo-access-understand.mdc
├── seo-access-connect.mdc
├── seo-substance-quality.mdc
├── seo-surface-assistants.mdc        # the AI assistant surface (once a page can rank)
├── seo-identity-context.mdc # learn the business first
├── seo-demand-search-data.mdc     # your own search data: indexing, traffic, change impact
├── seo-operations-launch-qa.mdc       # pre-launch and go-live checks
├── seo-access-performance.mdc     # Core Web Vitals deep work
├── seo-access-migrations.mdc       # URL changes / redirects
├── seo-operations-measurement.mdc
├── seo-substance-content-audit.mdc    # content: assess + recommend actions
├── seo-substance-content-editing.mdc  # content: improve real copy (edit, not generate)
├── seo-identity-positioning.mdc
├── seo-operations-reporting.mdc
├── seo-operations-automation.mdc      # CI/CD regression gate + scheduled audits
├── seo-substance-media.mdc            # image & video SEO
├── seo-substance-at-scale.mdc     # white-hat pages-at-scale
├── seo-access-logs.mdc     # server-log & crawl-budget (large sites)
└── seo-distribution-authority.mdc # off-page: backlinks + link-building strategy
```

## Converting a skill to a rule

For each skill, create a `.mdc` file with Cursor frontmatter, then paste the skill's body. Use the **copy-paste mini** versions (`install/copy-paste/*.md`) as the body — they're self-contained (no `references/` needed), which suits a single rule file.

Example — `.cursor/rules/seo-access-reach.mdc`:

```mdc
---
description: >-
  Make sure search engines and AI crawlers can reach pages and see content in the
  served HTML. Use first on any SEO/indexing/"not showing up"/SSR/CSR/rendering task.
alwaysApply: false
---

<paste the body of install/copy-paste/reach.md here>
```

Repeat for each mini:
- `seo-audit.mdc` ← `copy-paste/audit.md` *(the all-rounder: audits and records findings, changes nothing; make this your go-to broad rule)*
- `seo-access-reach.mdc` ← `copy-paste/reach.md`
- `seo-access-read.mdc` ← `copy-paste/read.md`
- `seo-access-understand.mdc` ← `copy-paste/understand.md`
- `seo-access-connect.mdc` ← `copy-paste/connect.md`
- `seo-substance-quality.mdc` ← `copy-paste/rank.md`
- `seo-surface-assistants.mdc` ← `copy-paste/cite.md`
- `seo-fix.mdc` ← `copy-paste/fix.md` *(applies approved findings only)*
- `seo-recheck.mdc` ← `copy-paste/recheck.md` *(re-tests findings, changes nothing)*
- `seo-identity-context.mdc` ← `copy-paste/context.md`
- `seo-demand-search-data.mdc` ← `copy-paste/search-data.md`
- `seo-operations-launch-qa.mdc` ← `copy-paste/launch-qa.md`
- `seo-access-performance.mdc` ← `copy-paste/performance.md`
- `seo-access-migrations.mdc` ← `copy-paste/migrations.md`
- `seo-operations-measurement.mdc` ← `copy-paste/measurement.md`
- `seo-substance-content-audit.mdc` ← `copy-paste/content-audit.md`
- `seo-substance-content-editing.mdc` ← `copy-paste/content-editing.md`
- `seo-identity-positioning.mdc` ← `copy-paste/positioning-strategy.md`
- `seo-operations-reporting.mdc` ← `copy-paste/proposal-roadmap.md`
- `seo-operations-automation.mdc` ← `copy-paste/automations.md`
- `seo-substance-media.mdc` ← `copy-paste/media.md`
- `seo-substance-at-scale.mdc` ← `copy-paste/programmatic.md`
- `seo-access-logs.mdc` ← `copy-paste/log-analysis.md`
- `seo-distribution-authority.mdc` ← `copy-paste/offsite.md`

`copy-paste/audit.md` is effectively the orchestrator in a single file — it walks the whole ladder, writes the `.seo/` state, and handles first-run vs progression. For broad requests, point Cursor at that rule. (The deeper lifecycle/profiles/adapters references live in `skills/seo-orchestrator/references/`; copy the ones you want into `docs/seo/` and cite them if you need that depth.)

## Rule type

- Set `alwaysApply: false` and rely on the `description` so rules activate when a request matches (keeps context lean).
- Alternatively, scope a rule with `globs` (e.g. `app/**/*.tsx`) if you want it to apply when editing certain files.
- Keep the orchestrator as the rule you reference for any broad "improve my SEO" request.

## Want the full references too?

The minis carry the full logic. If you want the deeper standards (e.g. the schema type catalogue or the canonical edge-cases), copy the relevant `skills/<rung>/references/*.md` into the project (e.g. under `docs/seo/`) and point to them from the rule body, or paste the specific reference inline when you need that depth.

## Optional MCP power-ups

See [`install/mcp.md`](mcp.md) — optional servers (render/fetch, Lighthouse, schema validator, Search Console) sharpen verification. Nothing is required; the rules work as-is.
