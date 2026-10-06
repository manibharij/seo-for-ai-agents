# Verification: prove Reach on the rendered output

This is the file that makes the skill honest. Editing source and asserting success is forbidden. A Reach fix is done only when you have **fetched the URL and seen the content in what is actually served.** Read this for the exact checks.

> Golden principle: compare **raw HTML** (no JavaScript executed — what a basic crawler sees first) against **rendered HTML** (after JavaScript). If the content is only in the rendered version, the page fails Reach.

---

## The core check: is the content in the raw served HTML?

### Pick the right URL
Test a representative **content** page — an article, product, or deep page — not just the homepage. Homepages are often static even on sites whose content pages are client-rendered, so they hide the problem. Test more than one template type if the site has several.

### Choose the strongest tool you have (the tool ladder)
Work down this list and use the first rung available. Say in the report which rung you used, because it sets how much weight the findings can bear.

| Rung | Tool | Gives you | Confidence |
|---|---|---|---|
| 1 | A rendering MCP or a headless browser (Playwright, headless Chrome) | The rendered DOM after JavaScript, and the raw response if you also request it | High for both views |
| 2 | `curl` or `Invoke-WebRequest` | The exact raw bytes, status, redirect chain and headers | High for raw HTML and headers; cannot render |
| 3 | A fetch tool built into the agent (WebFetch and similar) | Usually page text, often converted to Markdown or summarised by a model | **Low** |

A fetch tool is not a raw view. Many convert the page to Markdown, drop the `<head>` (title, meta robots, canonical, JSON-LD), hide response headers and status codes, follow or refuse redirects on their own terms, and cache results. Use it only to confirm that visible body text is reachable. Never use it to judge `<head>` tags, headers, `noindex`, canonicals, or raw versus rendered. If it is all you have, say so and mark those checks as unverified.

The edge can also treat your tool differently from a crawler. If a WAF or CDN sits in front of the site, run the bot-UA comparison in `edge-cdn-and-bot-access.md` as well.

### Get the RAW response (no JS)
This is the first view a crawler gets.

- **curl (most reliable for raw HTML):**
  ```bash
  curl -sL https://example.com/a-real-content-page -o raw.html
  curl -sIL https://example.com/a-real-content-page   # headers + redirect chain
  ```
- **PowerShell (Windows):**
  ```powershell
  Invoke-WebRequest -Uri "https://example.com/a-real-content-page" -UseBasicParsing |
    Select-Object -ExpandProperty Content | Out-File raw.html -Encoding utf8
  (Invoke-WebRequest -Uri "https://example.com/a-real-content-page" -Method Head).Headers
  ```
  `-UseBasicParsing` returns the raw body without running scripts — exactly what you want here.
- **Agent built-in fetch / WebFetch:** not a substitute for the two above. See the tool ladder: it may hand you converted Markdown with the `<head>` and headers gone.

### Inspect the raw HTML for real content
Search `raw.html` for evidence the content is present, not just the shell:
- A **distinctive sentence** of the page's actual body copy (pick a phrase you can see in the browser).
- The real **`<h1>`** text (not a generic site name).
- The real **`<title>`**.
- The main content container with text inside it — **not** an empty `<div id="root"></div>` / `<div id="app"></div>` followed only by `<script>` tags.

```bash
grep -i "a distinctive sentence from the page" raw.html   # present?
grep -i "<h1" raw.html                                    # real heading text?
grep -i "id=\"root\"" raw.html                            # empty shell?
```
```powershell
Select-String -Path raw.html -Pattern "a distinctive sentence from the page"
Select-String -Path raw.html -Pattern "<h1"
```

**Interpretation:**
- Distinctive content present in raw HTML → Reach-rendering passes.
- Raw HTML is an empty shell + scripts, content only appears in the browser → **client-rendering blind spot.** This is the fix target.

### Confirm with the rendered view (optional but clarifying)
If a render/fetch MCP or headless browser is available, fetch the **JS-executed** HTML and diff it against the raw HTML. A large gap — content only in the rendered version — is the smoking gun. If raw and rendered are essentially equal and both contain the content, you are in good shape.

**Rendered HTML with Playwright** (`npm i -D playwright` then `npx playwright install chromium`). Save as `render.mjs` and run `node render.mjs <url> > rendered.html`:
```js
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
const response = await page.goto(process.argv[2], { waitUntil: 'networkidle' });
console.error('status', response?.status());
process.stdout.write(await page.content());
await browser.close();
```

**Rendered HTML with headless Chrome**, when Chrome is installed and Playwright is not:
```bash
google-chrome --headless --dump-dom https://example.com/a-real-content-page > rendered.html
# macOS: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --dump-dom ...
```
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --dump-dom "https://example.com/a-real-content-page" |
  Out-File rendered.html -Encoding utf8
```

**Diff raw against rendered.** Split on tags so the diff is readable, then count what only the rendered DOM has and check the distinctive sentence in each:
```bash
tr '>' '\n' < raw.html > raw.lines
tr '>' '\n' < rendered.html > rendered.lines
diff raw.lines rendered.lines | grep -c '^>'                 # lines only in the rendered DOM
grep -c "a distinctive sentence from the page" raw.html rendered.html
```
```powershell
$raw = (Get-Content raw.html -Raw -Encoding UTF8) -split '>'
$ren = (Get-Content rendered.html -Raw -Encoding UTF8) -split '>'
(Compare-Object $raw $ren | Where-Object SideIndicator -eq '=>').Count   # only in the rendered DOM
(Select-String -Path raw.html -Pattern "a distinctive sentence from the page" -SimpleMatch).Count
(Select-String -Path rendered.html -Pattern "a distinctive sentence from the page" -SimpleMatch).Count
```
Some difference is normal (hydration attributes, injected scripts). What matters is whether the body copy, `<h1>`, links and `<head>` tags exist only in the rendered file. For per-framework causes, see `javascript-seo.md`.

---

## Gatekeeper verification

- **Status & redirects:** `curl -sIL` (or the PowerShell `Head` call) — confirm a final `200`, and that any redirects are a single clean hop, not a chain or loop.
- **HTTPS & security headers:** confirm the page is served over `https://` (and `http://` redirects to it), with no mixed `http://` assets. In the response headers, check for `Strict-Transport-Security` (HSTS); note `Content-Security-Policy` / `X-Content-Type-Options` if relevant. `curl -sI https://example.com/ | grep -iE "strict-transport|content-security|x-content-type"`.
- **`noindex` — check the meta tag AND headers (a bare `grep noindex` false-positives on body copy):**
  ```bash
  # meta robots/googlebot noindex in <head> — target the tag, not the word
  grep -iE '<meta[^>]+name=["'\'']?(robots|googlebot)["'\'']?[^>]*noindex' raw.html
  # header directive — also delists, and a meta grep can't see it
  curl -sI https://example.com/page | grep -i "x-robots-tag"
  ```
  A `noindex` in either place delists the page. Greps are a quick screen: attribute order can vary (`content` before `name`), and directives can be header-set or JS-injected, so for certainty confirm against the parsed/rendered `<head>`. Confirm any you find is intentional.
- **Edge and bot access:** fetch the page and `/robots.txt` as a browser, as Googlebot and as the AI crawlers the user wants, and compare status and size. A difference points to a WAF, CDN or deployment-protection rule. UA spoofing only reveals UA-based rules, so confirm with URL Inspection or verified log lines. Commands and per-platform settings are in `edge-cdn-and-bot-access.md`.
- **robots.txt:** fetch `https://example.com/robots.txt`; confirm the tested path is not disallowed and the sitemap is referenced.
- **sitemap:** fetch `https://example.com/sitemap.xml`; confirm it lists **production, canonical, `200`** URLs — no localhost/staging hosts, no redirects, no 404s.
- **canonical:** confirm `<link rel="canonical">` points to a sensible self/production URL, not a dev host or an unrelated page.

---

## MCP-assisted checks (use if present — see `install/mcp.md`)
- **Render/fetch server:** raw vs JS-rendered comparison without a local headless setup.
- **Lighthouse / PageSpeed:** the SEO and crawlability audits flag blocked resources, `noindex`, non-`200`s, and missing canonicals.
- **Schema/structured-data validator:** not a Reach concern (that's rung 3), but if available it confirms the rendered HTML is parseable.
- **Search Console:** the only source of *real* indexation status — Coverage/Pages reports and the URL Inspection tool show what Google actually did. This is live data and optional; the build-time checks above stand on their own without it.

---

## Definition of done — the Reach checklist

A page passes Reach only when **all** of these hold, verified against the served output:

- [ ] The page's primary content (distinctive body copy, real `<h1>`, real `<title>`) is present in the **raw HTML**, before JavaScript runs.
- [ ] The URL returns a final **`200`** with no redirect chain or loop.
- [ ] No unintended **`noindex`** in the meta robots tag **or** the `X-Robots-Tag` header.
- [ ] **`robots.txt`** allows the path and does not block needed CSS/JS.
- [ ] No **WAF, CDN or deployment gate** blocks or challenges the crawlers the user wants (bot-UA comparison, confirmed with URL Inspection or verified logs).
- [ ] A **sitemap** exists, lists production/canonical/`200` URLs, and is referenced from `robots.txt`.
- [ ] The **canonical** tag points to a sensible production URL.
- [ ] You re-fetched **after** the fix and confirmed the content is now present — you did not infer success from a source edit.

If any box is unchecked, Reach has not passed — return to Diagnose. Only when every box holds may you climb to rung 2 (Read).
