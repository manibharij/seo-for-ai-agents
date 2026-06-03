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

Method: diagnose top-to-bottom, fix bottom-to-top. Five rungs, in order — you may not
fix a rung until the ones below it pass:
1. Reach (`skills/1-reach-indexation/`) — crawlable + content in the SERVED HTML + HTTPS
2. Read (`skills/2-read-content/`) — content + metadata + page experience (speed/mobile)
3. Understand (`skills/3-understand-schema/`) — valid, honest schema
4. Connect (`skills/4-connect-architecture/`) — internal links + canonicals
5. Rank (`skills/5-rank-relevance/`) — the goal: good enough, and trusted enough, to win (intent, quality, on-page E-E-A-T, topical authority; off-site authority advised via `seo-offsite-authority`)
On top of the ladder (once a page can rank): `skills/cite-aeo-geo/` — AEO, eligible to be cited by AI answers (secondary, not a rung).
Specialists: `skills/seo-migrations/` (URL changes/redirects), `skills/seo-measurement-setup/` (analytics/GSC),
`skills/seo-content-audit/` (assess content), `skills/seo-content-editing/` (improve real copy — edit not generate),
`skills/seo-positioning-strategy/` (topical authority/positioning), `skills/seo-proposal-roadmap/` (proposal/roadmap),
`skills/seo-automations/` (CI/CD regression gate + scheduled audits), `skills/seo-media/` (image/video SEO),
`skills/seo-programmatic/` (white-hat pages-at-scale), `skills/seo-log-analysis/` (server-log/crawl-budget, large sites),
`skills/seo-offsite-authority/` (off-page: backlink audit + white-hat link-building strategy, advisory).
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
