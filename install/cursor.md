# Install for Cursor

Cursor uses **Project Rules** — Markdown-with-frontmatter files in `.cursor/rules/*.mdc` that get pulled into context based on their description or globs. `seo-for-ai-agents` maps cleanly onto them: one rule per rung, plus a router rule.

> Cursor doesn't run the SKILL packaging format directly, so you adapt each skill into a `.mdc` rule. The logic is identical; only the wrapper changes.

---

## Layout

```
<your-project>/.cursor/rules/
├── seo-orchestrator.mdc
├── 1-reach-indexation.mdc
├── 2-read-content.mdc
├── 3-understand-schema.mdc
├── 4-connect-architecture.mdc
└── 5-cite-aeo-geo.mdc
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

Repeat for each rung using the matching mini:
- `1-reach-indexation.mdc` ← `copy-paste/reach.md`
- `2-read-content.mdc` ← `copy-paste/read.md`
- `3-understand-schema.mdc` ← `copy-paste/understand.md`
- `4-connect-architecture.mdc` ← `copy-paste/connect.md`
- `5-cite-aeo-geo.mdc` ← `copy-paste/cite.md`

For the orchestrator, create `seo-orchestrator.mdc` with a description like *"Entry point for broad SEO requests; diagnose the Visibility Ladder top-to-bottom and fix the lowest failing rung first"* and summarise the routing table from `skills/seo-orchestrator/SKILL.md` in the body.

## Rule type

- Set `alwaysApply: false` and rely on the `description` so rules activate when a request matches (keeps context lean).
- Alternatively, scope a rule with `globs` (e.g. `app/**/*.tsx`) if you want it to apply when editing certain files.
- Keep the orchestrator as the rule you reference for any broad "improve my SEO" request.

## Want the full references too?

The minis carry the full logic. If you want the deeper standards (e.g. the schema type catalogue or the canonical edge-cases), copy the relevant `skills/<rung>/references/*.md` into the project (e.g. under `docs/seo/`) and point to them from the rule body, or paste the specific reference inline when you need that depth.

## Optional MCP power-ups

See [`install/mcp.md`](mcp.md) — optional servers (render/fetch, Lighthouse, schema validator, Search Console) sharpen verification. Nothing is required; the rules work as-is.
