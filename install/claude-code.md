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
├── seo-orchestrator/
├── 1-reach-indexation/
├── 2-read-content/
├── 3-understand-schema/
├── 4-connect-architecture/
└── 5-cite-aeo-geo/
```

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

- *"Why isn't my site showing up in Google?"* → the **orchestrator** routes you, usually starting at **Reach**.
- *"Add structured data to my product pages."* → **Understand**.
- *"Help my pages get cited by ChatGPT and AI Overviews."* → the **orchestrator** walks the ladder up to **Cite**.

You can also invoke a skill explicitly by name in your prompt (e.g. "use the 1-reach-indexation skill on this site").

The **orchestrator** is the best entry point for broad requests — it detects your stack, finds the lowest failing rung, and dispatches in order.

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
