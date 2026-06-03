# Install for Claude Code

`seo-for-ai-agents` is a set of [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills). Claude Code discovers skills automatically and invokes them when a request matches their `description`. You have two install scopes.

---

## Option A — Personal skills (available in every project)

Copy the skill folders into your user-level skills directory:

```
~/.claude/skills/
```

On Windows that's `C:\Users\<you>\.claude\skills\`.

Copy each skill directory (the folder containing `SKILL.md` and its `references/`) so you end up with:

```
~/.claude/skills/
├── seo-orchestrator/        # the conductor — runs the audit lifecycle; carries shared references (lifecycle, profiles, stack/platform adapters)
├── 1-reach-indexation/
├── 2-read-content/
├── 3-understand-schema/
├── 4-connect-architecture/
├── 5-rank-relevance/        # rung 5 (the goal): good & relevant enough to rank
├── cite-aeo-geo/            # the AEO layer on top of the ladder (after a page ranks)
├── seo-migrations/          # specialist: URL changes / redirects / site moves
├── seo-measurement-setup/   # specialist: analytics / Search Console / web-vitals plumbing
├── seo-content-audit/       # content: assess content, recommend actions
├── seo-content-editing/     # content: improve real copy (edit, not generate)
├── seo-positioning-strategy/# content: topical authority + positioning plan
├── seo-proposal-roadmap/    # content: package findings into a proposal/roadmap
├── seo-automations/         # automation: CI/CD regression gate + scheduled audits
├── seo-media/               # advanced: image & video SEO
├── seo-programmatic/        # advanced: white-hat pages-at-scale from data
├── seo-log-analysis/        # advanced: server-log & crawl-budget analysis
└── seo-offsite-authority/   # off-page: backlink audit + white-hat link-building strategy
```

Copy the **whole `skills/` folder** — keep the skills together. The orchestrator holds the cross-cutting references (audit lifecycle, site-type profiles, stack/platform adapters) the others rely on.

**PowerShell:**
```powershell
$dst = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Item -Recurse -Force ".\skills\*" $dst
```
**macOS/Linux:**
```bash
mkdir -p ~/.claude/skills && cp -R ./skills/* ~/.claude/skills/
```

## Option B — Project skills (committed to one repo)

Put them under the project so your whole team gets them:

```
<your-project>/.claude/skills/
```

Copy the same skill folders there and commit them. Project skills take precedence and travel with the repo.

---

## Using them

Once installed, just describe the problem — the descriptions are written to trigger the right skill:

- *"Audit my site's SEO"* / *"why isn't my site showing up?"* → the **orchestrator** runs the audit lifecycle, usually starting at **Reach**.
- *"Add structured data to my product pages."* → **Understand**.
- *"Why am I not ranking / improve my rankings."* → the **orchestrator** climbs to **Rank** (rung 5).
- *"Help my pages get cited by ChatGPT and AI Overviews."* → the **orchestrator** ranks the page first, then applies the **Cite (AEO)** layer.
- *"We're redesigning / changing our URLs — don't lose rankings."* → **`seo-migrations`**.
- *"Set up analytics and Search Console."* → **`seo-measurement-setup`**.
- *"Audit my content / which pages should I update or cut?"* → **`seo-content-audit`**.
- *"Improve / tighten this page's copy."* → **`seo-content-editing`**.
- *"What topics should we own / how do we differentiate?"* → **`seo-positioning-strategy`**.
- *"Put together an SEO proposal / roadmap."* → **`seo-proposal-roadmap`**.
- *"Catch SEO regressions in CI / GitHub Action for SEO."* → **`seo-automations`**.
- *"Get my images/videos into search."* → **`seo-media`**.
- *"Generate location/product pages at scale."* → **`seo-programmatic`**.
- *"What is Googlebot actually crawling / crawl budget."* → **`seo-log-analysis`**.
- *"Audit my backlinks / how do I get more authority?"* → **`seo-offsite-authority`**.

Connect your own data tools (Search Console, DataForSEO, Ahrefs) to sharpen all of these — optional, see [data-integrations.md](data-integrations.md).

You can also invoke a skill explicitly by name (e.g. "use the 1-reach-indexation skill on this site").

The **orchestrator** is the best entry point for broad requests — it detects your stack, platform, and site type, finds the lowest failing rung, dispatches in order, and runs everything as a repeatable audit.

### The `.seo/` folder
On a broad audit, the orchestrator writes a **`.seo/` folder into your project** — `audit.md` (readable scorecard), `state.json` (issue tracker), `log.md` (history). **Commit it** (don't gitignore it): it persists progress so later runs re-verify past fixes, catch regressions, and advance. It's yours to read any time to see where your SEO stands.

---

## Optional: mention the method in `CLAUDE.md`

To make Claude lean on the ladder by default for any web project, add a short note to your project's `CLAUDE.md`:

```markdown
## SEO
This project uses the seo-for-ai-agents skill pack (the Visibility Ladder).
For any SEO/indexing/AI-search work, use the seo-orchestrator skill; it diagnoses
top-to-bottom and fixes bottom-to-top, verifying on served HTML. Never fabricate
authors, reviews, or trust signals — flag missing ones as human tasks.
```

This is optional — the skills trigger on their descriptions regardless.

---

## Optional MCP power-ups

The skills work with zero configuration. If you want sharper verification (raw-vs-rendered HTML, Lighthouse, schema validation, Search Console), see [`install/mcp.md`](mcp.md). Nothing is required.

## No host? Use the copy-paste minis

If you'd rather not install skills, each rung has a single-file version in [`install/copy-paste/`](copy-paste/) you can paste straight into a chat.
