# Install for AGENTS.md hosts (Codex, Gemini CLI, Zed, and others)

Many agents read a project-root `AGENTS.md` (or a tool-specific equivalent) for standing instructions. `seo-for-ai-agents` works with these via two paths: a **pointer** in `AGENTS.md` plus the skill content checked into the repo, or **inlining** the minis for the simplest setup.

> `AGENTS.md` is an emerging cross-tool convention. Where a specific host uses a different filename (e.g. `GEMINI.md`), apply the same content to that file.

---

## Path A — Pointer + checked-in skills (recommended)

1. Copy the `skills/` directory into your repo (e.g. keep it at `skills/` or move under `docs/seo/`).
2. Add a section to `AGENTS.md` telling the agent the method, the order, and where the detail lives:

```markdown
## SEO — the Visibility Ladder

For any SEO, indexing, "not showing up", AI-search/citation, schema, internal-linking,
rendering, redirect/migration, or analytics task, use the seo-for-ai-agents skill pack
in `skills/`. Works on new or existing sites.

Method: diagnose top-to-bottom, fix bottom-to-top. Four Access rungs, in order — you may not
fix a rung until the ones below it pass:
1. Reach (`skills/seo-access-reach/`) — crawlable + content in the SERVED HTML + HTTPS
2. Read (`skills/seo-access-read/`) — content + metadata + page experience (speed/mobile)
3. Understand (`skills/seo-access-understand/`) — valid, honest schema
4. Connect (`skills/seo-access-connect/`) — internal links + canonicals
5. Rank (`skills/seo-substance-quality/`) — the goal: good enough, and trusted enough, to win (intent, quality, on-page E-E-A-T, topical authority; off-site authority advised via `seo-distribution-authority`)
The assistant surface (once a page can rank): `skills/seo-surface-assistants/` — eligible to be named by AI answers. A surface, not a rung.
Modes: every skill runs in `audit` (default, read-only), `fix` (approved findings only) or `re-check`.
Foundation and data: `skills/seo-identity-context/` (learn the business first), `skills/seo-demand-search-data/`
(the user's own search data: indexing, traffic, demand, change impact).
Specialists: `skills/seo-operations-launch-qa/` (pre-launch and go-live), `skills/seo-access-performance/` (Core Web Vitals),
`skills/seo-access-migrations/` (URL changes/redirects), `skills/seo-operations-measurement/` (analytics/GSC),
`skills/seo-substance-content-audit/` (assess content), `skills/seo-substance-content-editing/` (improve real copy — edit not generate),
`skills/seo-identity-positioning/` (topical authority/positioning), `skills/seo-operations-reporting/` (proposal/roadmap),
`skills/seo-operations-automation/` (CI/CD regression gate + scheduled audits), `skills/seo-substance-media/` (image/video SEO),
`skills/seo-substance-at-scale/` (white-hat pages-at-scale), `skills/seo-access-logs/` (server-log/crawl-budget, large sites),
`skills/seo-distribution-authority/` (off-page: backlink audit + white-hat link-building strategy, advisory).
Optional live-data tools (GSC/DataForSEO/Ahrefs, bring-your-own-key) enrich the audit — see `install/data-integrations.md`; never required.

Start broad requests with `skills/seo-orchestrator/SKILL.md` — it runs an AUDIT LIFECYCLE:
write/read a `.seo/` folder in the project (audit.md, state.json, log.md); on later runs
re-verify past fixes (catch regressions) and advance. It also adapts to the stack/platform
and site-type profile (`skills/seo-orchestrator/references/`).

Rules: VERIFY ON SERVED HTML, not source (re-fetch and confirm). NEVER fabricate authors,
reviews, credentials, or trust signals — flag missing ones as human tasks. On an EXISTING
site, don't regress what works — preserve URLs (301s), respect intentional decisions, get
sign-off on big changes. Optional MCPs in `install/mcp.md` sharpen verification but are
never required.
```

The agent reads `AGENTS.md`, then opens the relevant `SKILL.md` and its `references/` as needed — the same progressive-disclosure flow Claude Code uses.

## Path B — Inline the minis (simplest)

If you'd rather not check in the full tree, paste the self-contained minis from `install/copy-paste/` directly into `AGENTS.md` under an SEO heading (or keep them as `docs/seo/*.md` and link them). Each mini is complete on its own. For broad requests, lead with **`audit.md`** (it runs the whole lifecycle and writes `.seo/`); add the per-rung minis (`reach`, `read`, …), the technical specialists (`migrations`, `measurement`), and the content/marketing minis (`content-audit`, `content-editing`, `positioning-strategy`, `proposal-roadmap`) as needed.

---

## A note on triggering

`AGENTS.md` hosts don't have Claude Code's skill auto-discovery, so make the SEO section explicit and keep the trigger words in it ("SEO", "indexing", "AI search", "schema", "rendering", "not showing up") so the agent reliably reaches for it.

## Optional MCP power-ups

See [`install/mcp.md`](mcp.md). Optional only — the pack runs on built-in fetch/inspection.
