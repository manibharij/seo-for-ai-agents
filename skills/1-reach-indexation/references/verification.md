# Verification: prove Reach on the rendered output

This is the file that makes the skill honest. Editing source and asserting success is forbidden. A Reach fix is done only when you have **fetched the URL and seen the content in what is actually served.** Read this for the exact checks.

> Golden principle: compare **raw HTML** (no JavaScript executed — what a basic crawler sees first) against **rendered HTML** (after JavaScript). If the content is only in the rendered version, the page fails Reach.

---

## The core check: is the content in the raw served HTML?

### Pick the right URL
Test a representative **content** page — an article, product, or deep page — not just the homepage. Homepages are often static even on sites whose content pages are client-rendered, so they hide the problem. Test more than one template type if the site has several.

### Get the RAW response (no JS)
This is the first view a crawler gets. Use whichever tool is available:

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
- **Agent built-in fetch / WebFetch:** retrieve the page; treat the returned markup as the raw view.

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
- [ ] A **sitemap** exists, lists production/canonical/`200` URLs, and is referenced from `robots.txt`.
- [ ] The **canonical** tag points to a sensible production URL.
- [ ] You re-fetched **after** the fix and confirmed the content is now present — you did not infer success from a source edit.

If any box is unchecked, Reach has not passed — return to Diagnose. Only when every box holds may you climb to rung 2 (Read).
