# Robots, meta directives, and sitemaps

Read this when the gatekeeper checks (Step 1c) turn up a `robots.txt`, `noindex`, status-code, or sitemap problem. A perfectly rendered page is still unreachable if a rule forbids it or a bad URL hides it.

---

## robots.txt — the crawl gate

`robots.txt` lives at the domain root (`/robots.txt`). It controls **crawling** (whether a bot fetches a URL), not **indexing** directly. Two consequences people get wrong:

- **`Disallow` does not guarantee de-indexing.** A disallowed URL can still appear in results (without a snippet) if other pages link to it. To keep a page *out of the index*, allow crawling and use a `noindex` meta tag/header instead — the crawler must be able to fetch the page to see the `noindex`.
- **Blocking a path you optimise is self-sabotage.** The most common accident is a leftover `Disallow: /` from a staging config, or disallowing a directory that holds real content (`/blog/`, `/products/`).
- **The `noindex` + `Disallow` conflict — the classic indexing mistake.** If a URL is *both* `Disallow`-ed in robots.txt *and* carries a `noindex`, the disallow stops the crawler ever fetching the page, so it **never sees the `noindex`** — and the URL can stay indexed (as a URL-only entry). To remove a page from the index, you must **allow crawling so the `noindex` is seen**; only `Disallow` it later, once it has actually dropped out. Getting this order wrong is why "I noindexed it but it's still in Google" happens.

### What to check
- Is there a stray `Disallow: /` or an over-broad rule blocking real content?
- Are CSS/JS assets blocked that the page needs to render? (Blocking these can stop a crawler rendering the page correctly.)
- Is the sitemap referenced? Add `Sitemap: https://example.com/sitemap.xml`.
- Are you accidentally blocking AI crawlers you *want* (or failing to block ones you don't)? That is a deliberate choice — see the Cite skill's `ai-crawlers-and-llms-txt.md`. Here, just surface it; don't decide it for the user.
- Is the live file the one in the repo? A CDN can rewrite it (Cloudflare's managed `robots.txt` prepends its own AI-crawler rules), and a WAF can block crawlers whatever the file says. Fetch the live `/robots.txt` and see `edge-cdn-and-bot-access.md`.

### A sane default for a content site
```
User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```
Add specific `Disallow` rules only for genuinely non-public paths (admin, cart, internal search results, faceted-filter URL explosions). Infer which paths those are from their names and role rather than asking; flag only a genuinely ambiguous case rather than blocking blind.

---

## Meta robots vs X-Robots-Tag — the silent de-lister

A single stray `noindex` removes a page from search entirely, and it is easy to leave one behind from a template or a "coming soon" phase.

- **`<meta name="robots" content="...">`** — in the page `<head>`. Common values: `index,follow` (default, no tag needed), `noindex` (keep out of index), `nofollow` (don't pass link signals).
- **`X-Robots-Tag` HTTP header** — same directives, but in the response header. Crucial: **you must check the headers, not just the HTML**, because a `noindex` here is invisible in the body. It is also the only way to set directives on non-HTML files (PDFs, images).

### What to check
- Fetch the page and inspect **both** the rendered `<head>` and the response headers for `noindex`.
- In Next.js App Router, `noindex` is usually set via the Metadata API (`robots: { index: false }` in `metadata` or `generateMetadata`). A `noindex` leaking from a shared layout or a default export will silently delist whole sections — trace where it comes from.
- Confirm any `noindex` is intentional before removing it (some pages *should* be noindexed: thank-you pages, internal search results, thin tag archives).

---

## HTTP status codes — reachability at the protocol level

| Code | Meaning | Action |
|---|---|---|
| `200` | OK | Good — content should be present. |
| `301` | Permanent redirect | Fine, but collapse chains (A→B→C should be A→C). |
| `302` | Temporary redirect | Often a mistake where `301` is meant; check intent. |
| `404` | Not found | Correct for missing pages — better than a soft 404. |
| `410` | Gone | Stronger "permanently removed" signal than 404. |
| `5xx` | Server error | Urgent — crawlers back off and can drop pages. |

**Soft 404** — a "page not found" message served with a `200` status. Crawlers may index the error page or waste crawl budget on it. Return a real `404`/`410` for genuinely missing content.

**Redirect chains/loops** — each hop loses a little signal and crawl efficiency; loops are fatal. Flatten to a single hop.

---

## Sitemaps — the URL inventory

An XML sitemap lists the canonical URLs you want crawled and indexed. It does not force indexing, but it helps discovery (especially for large sites or weakly-linked pages) and surfaces issues in Search Console.

### Correctness rules — a sitemap full of bad URLs hurts more than no sitemap
- List **canonical `200` URLs only** — no redirects, no 404s, no `noindex` pages, no parameter duplicates.
- Use the **production host and scheme** — a classic bug is a sitemap full of `http://localhost:3000/...` or a staging domain.
- Keep it current — stale sitemaps that list dead URLs erode trust in the file.
- One sitemap caps at 50,000 URLs / 50 MB uncompressed; beyond that, split and use a sitemap index.
- Reference it from `robots.txt` (a build-time fix). Optionally, once the site is live, the user can also submit it in Search Console to speed discovery — that's a runtime step on the live-data side, not part of the build.

### Framework-native generation (prefer this over hand-maintained XML)
- **Next.js App Router:** add `app/sitemap.ts` exporting a default function returning the URL array (Next serves it at `/sitemap.xml`). For large/dynamic sites, generate entries from your data source. Pair with `app/robots.ts` for `robots.txt`. This keeps the sitemap in sync with real routes automatically — the right answer for this user's stack.
- **Astro:** `@astrojs/sitemap` integration.
- **Nuxt:** `@nuxtjs/sitemap` module.
- **SvelteKit:** generate via an endpoint (`src/routes/sitemap.xml/+server.ts`).
- **Gatsby:** `gatsby-plugin-sitemap`.

Whatever generates it, **verify the output**: fetch `/sitemap.xml` and confirm the URLs are production, canonical, and `200`. A generator pointed at the wrong base URL produces a confidently wrong sitemap.

### Bulk status check from the sitemap
Spot checks miss the one template that redirects or carries `noindex`. Check every listed URL and write a CSV with `url, status, final_url, x_robots_tag, canonical`. Keep it polite: at most 4 requests in parallel with a pause after each, a cap on URLs (500 by default), and a production site only with the owner's agreement.

**bash** (macOS, Linux, Git Bash, WSL). Save as `sitemap-status.sh`, then run `bash sitemap-status.sh https://example.com/sitemap.xml 500 > status.csv`:
```bash
#!/usr/bin/env bash
SITEMAP="$1"; MAX="${2:-500}"
export UA='Mozilla/5.0 (compatible; site-audit)'
check() {
  local url="$1" tmp meta status final xrt canon
  tmp=$(mktemp -d)
  meta=$(curl -sL --compressed --max-redirs 5 --max-time 20 -A "$UA" \
    -D "$tmp/h" -o "$tmp/b" -w '%{http_code} %{url_effective}' "$url")
  status=${meta%% *}; final=${meta#* }
  # X-Robots-Tag from the last response in the redirect chain only
  xrt=$(tr -d '\r' < "$tmp/h" | awk '/^HTTP\//{v=""} tolower($0) ~ /^x-robots-tag:/{sub(/^[^:]*:[ \t]*/,""); v=(v=="" ? $0 : v"; "$0)} END{print v}')
  canon=$(grep -oiE '<link[^>]*rel=["'\'']?canonical["'\'']?[^>]*>' "$tmp/b" | head -n1 \
    | grep -oiE 'href=["'\'']?[^"'\'' >]+' | sed -E 's/^[hH][rR][eE][fF]=["'\'']?//')
  printf '"%s","%s","%s","%s","%s"\n' "$url" "$status" "$final" "${xrt//\"/}" "$canon"
  rm -rf "$tmp"; sleep 0.5
}
export -f check
echo 'url,status,final_url,x_robots_tag,canonical'
curl -sL --compressed -A "$UA" "$SITEMAP" | grep -oE '<loc>[^<]+</loc>' \
  | sed -E 's#</?loc>##g; s/&amp;/\&/g' | head -n "$MAX" \
  | xargs -P 4 -I{} bash -c 'check "$1"' _ {}
```

**PowerShell** (Windows PowerShell 5.1 or PowerShell 7). Runs one request at a time with a pause, so it is slower but gentle:
```powershell
$Sitemap = 'https://example.com/sitemap.xml'; $Max = 500
$UA = 'Mozilla/5.0 (compatible; site-audit)'
function Get-FinalUrl($resp) {
  if ($resp.ResponseUri) { $resp.ResponseUri.AbsoluteUri }      # Windows PowerShell 5.1
  else { $resp.RequestMessage.RequestUri.AbsoluteUri }           # PowerShell 7+
}
[xml]$xml = (Invoke-WebRequest -Uri $Sitemap -UserAgent $UA -UseBasicParsing).Content
$urls = @($xml.urlset.url.loc) | Select-Object -First $Max
$rows = foreach ($u in $urls) {
  $row = [ordered]@{ url = $u; status = ''; final_url = ''; x_robots_tag = ''; canonical = '' }
  try {
    $r = Invoke-WebRequest -Uri $u -UserAgent $UA -UseBasicParsing -MaximumRedirection 5 -TimeoutSec 20
    $row.status = [int]$r.StatusCode
    $row.final_url = Get-FinalUrl $r.BaseResponse
    $row.x_robots_tag = ($r.Headers['X-Robots-Tag'] -join '; ')
    $link = [regex]::Match($r.Content, '<link[^>]*rel=["'']?canonical["'']?[^>]*>', 'IgnoreCase').Value
    $row.canonical = [regex]::Match($link, 'href=["'']?([^"''\s>]+)', 'IgnoreCase').Groups[1].Value
  } catch {
    $resp = $_.Exception.Response
    if ($resp) { $row.status = [int]$resp.StatusCode; $row.final_url = Get-FinalUrl $resp }
    else { $row.status = 'error' }
  }
  [pscustomobject]$row
  Start-Sleep -Milliseconds 500
}
$rows | Export-Csv -Path status.csv -NoTypeInformation -Encoding UTF8
```

Notes:
- A **sitemap index** lists child sitemaps in its `<loc>` tags, not pages. Run the check on each child (in PowerShell, read `$xml.sitemapindex.sitemap.loc` first). A `.xml.gz` sitemap needs decompressing first.
- Windows PowerShell 5.1 does not follow `308` redirects, so a `308` row there is a redirect to look at, not a failure. Either way, a redirecting URL should not be in the sitemap.
- The canonical comes from the raw HTML. If it is set by JavaScript, it will be blank here, which is a finding in itself.
- The parallel bash output is unordered. Sort it before comparing runs.

**Read the CSV for:** any `status` other than `200`; `final_url` different from `url` (a redirect listed in the sitemap); any `noindex` in `x_robots_tag`; a `canonical` that is blank or points elsewhere (the sitemap should list the canonical itself). If a WAF rate-limits the run (`429`, `403`, `503` appearing partway through), stop, lower the concurrency, and see `edge-cdn-and-bot-access.md`.
