# Optional MCP power-ups

**Everything in this pack works with zero configuration**, using the agent's built-in tools. The skills verify Reach by fetching a URL and inspecting the served HTML — no extra servers required.

MCP (Model Context Protocol) servers are an **optional** layer that makes *verification* sharper. The skills are written to **detect and use them if present, and fall back silently if not.** Nothing here is a dependency.

> **For live-data tools** (Google Search Console, DataForSEO, Ahrefs, Bing Webmaster) connected with **your own API key** to *enrich* the audit, see **[data-integrations.md](data-integrations.md)** — those can be exposed via an MCP server or directly via env vars. This file covers the MCP layer specifically.

> **The boundary, kept intact:** the free core never *requires* any paid or live-data integration — it works fully with none connected. Live data is **optional enrichment** (your own keys, DIY) or **managed/done-for-you** (SearchOps for data, MB Search for the work). Optional integrations only *add live context and sharpen verification* — they never gate or paywall a build-time capability the pack gives away.

---

## How skills use these

Each skill checks, at its Verify step, whether a relevant server is available:
- **If present:** use it for a sharper check (e.g. a true raw-vs-rendered HTML comparison).
- **If absent:** fall back to built-in fetch + inspection, which is sufficient on its own.

A skill should never block, warn, or degrade its core advice because an MCP is missing.

---

## Recommended optional servers (by rung)

### Reach (rung 1) — the ones that matter most here
- **A render/fetch server (headless browser).** Lets you fetch both the **raw HTML** (no JS) and the **JS-rendered HTML**, and diff them. This is the cleanest way to prove a client-rendering blind spot without a local headless setup. Without it, `curl`/`Invoke-WebRequest` for the raw view plus the agent's own fetch is enough.
- **Lighthouse / PageSpeed Insights.** Its SEO and crawlability audits flag blocked resources, stray `noindex`, non-`200` responses, and missing canonicals in one pass.
- **Google Search Console.** The only source of *real* indexation status — the Pages/Coverage report and URL Inspection show what Google actually did with a URL. This is **live data and strictly optional**; the build-time checks stand on their own. Treat anything it reveals about live performance as pointing across the product boundary.

### Higher rungs (used by later skills)
- **A schema / structured-data validator** — for rung 3 (Understand): validates JSON-LD against schema.org and checks rich-result eligibility.
- **A render/fetch server** is reused across rungs wherever "verify on the rendered output" applies.

---

## Detection pattern for skill authors

When writing or extending a skill's Verify step, follow this shape:

> "If a render/fetch MCP server is available, fetch both the raw and JS-rendered HTML and compare. Otherwise, fetch the raw HTML with the built-in fetch tool (or `curl -sL` / `Invoke-WebRequest -UseBasicParsing`) and inspect it directly. Either path must end in the same evidence: the primary content is present in the raw served HTML."

Keep the built-in path first-class. The MCP is an accelerator, never a gate.

---

*Optional throughout. The pack's verification — every rung — runs on the agent's built-in fetch/inspection; these servers only sharpen it. Per-host install guides live in [`claude-code.md`](claude-code.md), [`cursor.md`](cursor.md), and [`agents-md.md`](agents-md.md).*
