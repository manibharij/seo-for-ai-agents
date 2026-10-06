# Optional MCP power-ups

**Everything in this pack works with zero configuration**, using the agent's built-in tools. The skills verify Reach by fetching a URL and inspecting the served HTML — no extra servers required.

MCP (Model Context Protocol) servers are an **optional** layer that makes *verification* sharper. The skills are written to **detect and use them if present, and fall back silently if not.** Nothing here is a dependency.

> **For live-data tools** (Google Search Console, DataForSEO, Ahrefs, Bing Webmaster) connected with **your own API key** to *enrich* the audit, see **[data-integrations.md](data-integrations.md)** — those can be exposed via an MCP server or directly via env vars. This file covers the MCP layer specifically.

> **The boundary, kept intact:** the free core never *requires* any paid or live-data integration — it works fully with none connected. Live data is **optional enrichment** (your own keys, DIY) or **managed/done-for-you** (SearchOps for data, MB Search for the work). Optional integrations only *add live context and sharpen verification* — they never gate or paywall a build-time capability the pack gives away.

---

## How skills use these

Each skill checks, at its Verify step, whether a relevant server is available, and works down the same tool ladder:

1. **A rendering MCP or headless browser** (Playwright, headless Chrome): raw and rendered HTML, so a true raw-versus-rendered comparison. High confidence.
2. **`curl` or `Invoke-WebRequest`:** exact raw HTML, status, redirects and headers. High confidence for everything except rendering, which is enough to pass most of Reach.
3. **The agent's built-in fetch tool** (WebFetch and similar): low confidence. Many return converted Markdown or a model's summary, with the `<head>` and response headers stripped. Use it to confirm visible text is reachable, never to judge `<head>` tags, headers, `noindex` or raw versus rendered, and say in the report when it was all you had.

A skill should never block on a missing MCP: rung 2 is available almost everywhere and carries most checks on its own. It should, however, be honest about which rung produced each finding. Exact commands are in `skills/1-reach-indexation/references/verification.md`.

---

## Recommended optional servers (by rung)

### Reach (rung 1) — the ones that matter most here
- **A render/fetch server (headless browser).** Lets you fetch both the **raw HTML** (no JS) and the **JS-rendered HTML**, and diff them. This is the cleanest way to prove a client-rendering blind spot without a local headless setup. Without it, use `curl`/`Invoke-WebRequest` for the raw view and headers, and a local Playwright or headless Chrome for the rendered view if one is installed. The agent's own fetch tool is not a raw view.
- **Lighthouse / PageSpeed Insights.** Its SEO and crawlability audits flag blocked resources, stray `noindex`, non-`200` responses, and missing canonicals in one pass.
- **Google Search Console.** The only source of *real* indexation status — the Pages/Coverage report and URL Inspection show what Google actually did with a URL. This is **live data and strictly optional**; the build-time checks stand on their own. Treat anything it reveals about live performance as pointing across the product boundary.

### Higher rungs (used by later skills)
- **A schema / structured-data validator** — for rung 3 (Understand): validates JSON-LD against schema.org and checks rich-result eligibility.
- **A render/fetch server** is reused across rungs wherever "verify on the rendered output" applies.

---

## Detection pattern for skill authors

When writing or extending a skill's Verify step, follow this shape:

> "If a rendering MCP or headless browser is available, fetch both the raw and JS-rendered HTML and compare. Otherwise, fetch the raw HTML and headers with `curl -sL` / `Invoke-WebRequest -UseBasicParsing` and inspect them directly. Use a built-in fetch tool only as a last resort, mark what it showed as low confidence, and never read headers or `<head>` tags from it. Every path must end in the same evidence: the primary content is present in the raw served HTML."

Keep the `curl` path first-class. The MCP is an accelerator, never a gate.

**A note on the edge.** None of these tools fetches from a crawler's IP. A WAF or CDN that verifies bots by IP can treat them differently from Googlebot or an AI crawler, so pair them with Search Console URL Inspection or verified log lines when a block is suspected (see `skills/1-reach-indexation/references/edge-cdn-and-bot-access.md`).

---

*Optional throughout. The pack's verification, on every rung, runs on `curl` / `Invoke-WebRequest` and inspection; these servers only sharpen it. Per-host install guides live in [`claude-code.md`](claude-code.md), [`cursor.md`](cursor.md), and [`agents-md.md`](agents-md.md).*
