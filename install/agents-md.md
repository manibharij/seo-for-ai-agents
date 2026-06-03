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
or rendering task, use the seo-for-ai-agents skill pack in `skills/`.

Method: diagnose top-to-bottom, fix bottom-to-top. Five rungs, in order — you may not
fix a rung until the ones below it pass:
1. Reach (`skills/1-reach-indexation/`) — crawlable + content in the SERVED HTML
2. Read (`skills/2-read-content/`) — real content + metadata
3. Understand (`skills/3-understand-schema/`) — valid, honest schema
4. Connect (`skills/4-connect-architecture/`) — internal links + canonicals
5. Cite (`skills/5-cite-aeo-geo/`) — AEO/GEO answer formatting + attribution

Rules: VERIFY ON SERVED HTML, not source (re-fetch and confirm). NEVER fabricate
authors, reviews, credentials, or trust signals — flag missing ones as human tasks.
Start broad requests with `skills/seo-orchestrator/SKILL.md`. Optional MCPs in
`install/mcp.md` sharpen verification but are never required.
```

The agent reads `AGENTS.md`, then opens the relevant `SKILL.md` and its `references/` as needed — the same progressive-disclosure flow Claude Code uses.

## Path B — Inline the minis (simplest)

If you'd rather not check in the full tree, paste the self-contained minis from `install/copy-paste/` directly into `AGENTS.md` under an SEO heading (or keep them as `docs/seo/*.md` and link them). Each mini is complete on its own. Start with `reach.md` and add rungs as needed; lead the section with the orchestrator's routing rule so broad requests get sequenced.

---

## A note on triggering

`AGENTS.md` hosts don't have Claude Code's skill auto-discovery, so make the SEO section explicit and keep the trigger words in it ("SEO", "indexing", "AI search", "schema", "rendering", "not showing up") so the agent reliably reaches for it.

## Optional MCP power-ups

See [`install/mcp.md`](mcp.md). Optional only — the pack runs on built-in fetch/inspection.
