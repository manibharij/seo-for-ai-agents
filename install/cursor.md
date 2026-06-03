# Install for Cursor

Cursor uses **Project Rules** — Markdown-with-frontmatter files in `.cursor/rules/*.mdc` that get pulled into context based on their description or globs. `seo-for-ai-agents` maps cleanly onto them: one rule per rung, plus a router rule.

> Cursor doesn't run the SKILL packaging format directly, so you adapt each skill into a `.mdc` rule. The logic is identical; only the wrapper changes.

---

## Layout

```
<your-project>/.cursor/rules/
├── seo-audit.mdc            # the all-rounder: full audit lifecycle (best default)
├── 1-reach-indexation.mdc
├── 2-read-content.mdc
├── 3-understand-schema.mdc
├── 4-connect-architecture.mdc
├── 5-rank-relevance.mdc
├── cite-aeo-geo.mdc        # AEO layer on top (once a page can rank)
├── seo-migrations.mdc       # URL changes / redirects
├── seo-measurement-setup.mdc
├── seo-content-audit.mdc    # content: assess + recommend actions
├── seo-content-editing.mdc  # content: improve real copy (edit, not generate)
├── seo-positioning-strategy.mdc
├── seo-proposal-roadmap.mdc
├── seo-automations.mdc      # CI/CD regression gate + scheduled audits
├── seo-media.mdc            # image & video SEO
├── seo-programmatic.mdc     # white-hat pages-at-scale
├── seo-log-analysis.mdc     # server-log & crawl-budget (large sites)
└── seo-offsite-authority.mdc # off-page: backlinks + link-building strategy
```

## Converting a skill to a rule

For each skill, create a `.mdc` file with Cursor frontmatter, then paste the skill's body. Use the **copy-paste mini** versions (`install/copy-paste/*.md`) as the body — they're self-contained (no `references/` needed), which suits a single rule file.

Example — `.cursor/rules/1-reach-indexation.mdc`:

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
- `seo-audit.mdc` ← `copy-paste/audit.md` *(the all-rounder — runs the full lifecycle; make this your go-to broad rule)*
- `1-reach-indexation.mdc` ← `copy-paste/reach.md`
- `2-read-content.mdc` ← `copy-paste/read.md`
- `3-understand-schema.mdc` ← `copy-paste/understand.md`
- `4-connect-architecture.mdc` ← `copy-paste/connect.md`
- `5-rank-relevance.mdc` ← `copy-paste/rank.md`
- `cite-aeo-geo.mdc` ← `copy-paste/cite.md`
- `seo-migrations.mdc` ← `copy-paste/migrations.md`
- `seo-measurement-setup.mdc` ← `copy-paste/measurement.md`
- `seo-content-audit.mdc` ← `copy-paste/content-audit.md`
- `seo-content-editing.mdc` ← `copy-paste/content-editing.md`
- `seo-positioning-strategy.mdc` ← `copy-paste/positioning-strategy.md`
- `seo-proposal-roadmap.mdc` ← `copy-paste/proposal-roadmap.md`
- `seo-automations.mdc` ← `copy-paste/automations.md`
- `seo-media.mdc` ← `copy-paste/media.md`
- `seo-programmatic.mdc` ← `copy-paste/programmatic.md`
- `seo-log-analysis.mdc` ← `copy-paste/log-analysis.md`
- `seo-offsite-authority.mdc` ← `copy-paste/offsite.md`

`copy-paste/audit.md` is effectively the orchestrator in a single file — it walks the whole ladder, writes the `.seo/` state, and handles first-run vs progression. For broad requests, point Cursor at that rule. (The deeper lifecycle/profiles/adapters references live in `skills/seo-orchestrator/references/`; copy the ones you want into `docs/seo/` and cite them if you need that depth.)

## Rule type

- Set `alwaysApply: false` and rely on the `description` so rules activate when a request matches (keeps context lean).
- Alternatively, scope a rule with `globs` (e.g. `app/**/*.tsx`) if you want it to apply when editing certain files.
- Keep the orchestrator as the rule you reference for any broad "improve my SEO" request.

## Want the full references too?

The minis carry the full logic. If you want the deeper standards (e.g. the schema type catalogue or the canonical edge-cases), copy the relevant `skills/<rung>/references/*.md` into the project (e.g. under `docs/seo/`) and point to them from the rule body, or paste the specific reference inline when you need that depth.

## Optional MCP power-ups

See [`install/mcp.md`](mcp.md) — optional servers (render/fetch, Lighthouse, schema validator, Search Console) sharpen verification. Nothing is required; the rules work as-is.
