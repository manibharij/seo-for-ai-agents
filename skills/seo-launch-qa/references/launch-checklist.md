# The launch checklist: every check, with the command

Read this when you run [`seo-launch-qa`](../SKILL.md). Each check has a reason, an exact command in bash and in PowerShell, what counts as a pass, and its class: **B** (launch blocker) or **W** (fix this week). Run them in order. The order follows the ladder, so a failure near the top makes the later checks unreliable.

> Run every command against the **production URL after the deploy**. Results from a preview, a local build or the source code are provisional at best.

Facts marked "verified 2026-10" were checked against the named primary source in October 2026. Re-check them if you are reading this much later.

---

## Setup

Set the production origin (preferred protocol and host, no trailing slash) and one URL per key template. The setup fetches each page once, **without following redirects**, and saves the body and headers, so later checks can read them without refetching.

The working folder `.launch-qa/` holds throwaway output. Delete it when you finish and never commit it.

**bash** (macOS, Linux, Git Bash, WSL):
```bash
SITE="https://www.example.com"                 # production origin, no trailing slash
PAGES="/ /blog/a-real-post /pricing"           # one URL per key template
UA="Mozilla/5.0 (compatible; launch-qa/1.0)"
mkdir -p .launch-qa
for p in $PAGES; do
  f=".launch-qa/$(printf '%s' "$p" | tr -c 'A-Za-z0-9' '_')"
  curl -s -A "$UA" -D "$f.headers" -o "$f.html" "$SITE$p"
  printf '%s  %s\n' "$(head -1 "$f.headers" | tr -d '\r')" "$p"
done
# The home page is saved as .launch-qa/_.html and .launch-qa/_.headers
```

**PowerShell** (Windows PowerShell 5.1 and PowerShell 7). `Invoke-WebRequest` follows redirects and throws on `4xx`, which hides exactly what this pass needs to see, so the helper uses `HttpClient` with redirects off:
```powershell
$Site  = 'https://www.example.com'             # production origin, no trailing slash
$Pages = @('/', '/blog/a-real-post', '/pricing')
$UA    = 'Mozilla/5.0 (compatible; launch-qa/1.0)'
Add-Type -AssemblyName System.Net.Http
$handler = New-Object System.Net.Http.HttpClientHandler
$handler.AllowAutoRedirect = $false
$client  = New-Object System.Net.Http.HttpClient($handler)

# One request, redirects not followed: status, Location, headers and body.
function Get-Hop([string]$Url, [string]$Agent = $UA) {
  $req = New-Object System.Net.Http.HttpRequestMessage([System.Net.Http.HttpMethod]::Get, $Url)
  [void]$req.Headers.TryAddWithoutValidation('User-Agent', $Agent)
  $res = $client.SendAsync($req).GetAwaiter().GetResult()
  $h = @{}
  foreach ($kv in $res.Headers)         { $h[$kv.Key.ToLower()] = ($kv.Value -join ', ') }
  foreach ($kv in $res.Content.Headers) { $h[$kv.Key.ToLower()] = ($kv.Value -join ', ') }
  $loc = $null
  if ($res.Headers.Location) { $loc = [System.Uri]::new([System.Uri]$Url, $res.Headers.Location).AbsoluteUri }
  [pscustomobject]@{ Url = $Url; Status = [int]$res.StatusCode; Location = $loc; Headers = $h
    Body = $res.Content.ReadAsStringAsync().GetAwaiter().GetResult() }
}

# Follows redirects one hop at a time (at most 10) and returns every hop.
function Get-Chain([string]$Url, [string]$Agent = $UA) {
  $hops = @()
  for ($i = 0; $i -lt 10; $i++) {
    $r = Get-Hop $Url $Agent
    $hops += $r
    if ($r.Status -lt 300 -or $r.Status -ge 400 -or -not $r.Location) { break }
    $Url = $r.Location
  }
  $hops
}

$Res = @{}
foreach ($p in $Pages) { $Res[$p] = Get-Hop "$Site$p"; '{0}  {1}' -f $Res[$p].Status, $p }
```
In PowerShell, call `curl.exe` rather than `curl` if you prefer curl: in Windows PowerShell 5.1, `curl` is an alias for `Invoke-WebRequest`.

The greps below are quick screens. Attribute order varies and some tags are injected by JavaScript, so confirm any surprising result in the parsed or rendered `<head>` before acting on it.

---

## Gate 1: staging blocks carried into production

### LQ-01 No `noindex` in the meta robots tag (B)
A leftover `noindex` from staging removes the page from Google once it is crawled. It is the most common launch failure on sites built behind a preview.
```bash
grep -ioE '<meta[^>]+name="?(robots|googlebot)"?[^>]*>' .launch-qa/*.html
```
```powershell
foreach ($p in $Pages) { [regex]::Matches($Res[$p].Body, '<meta[^>]+name="?(robots|googlebot)"?[^>]*>', 'IgnoreCase') | ForEach-Object { "$p  $($_.Value)" } }
```
**Pass:** no tag, or a tag without `noindex` or `none` on every key template. **Fail:** `noindex` or `none` on a page meant to be public.

### LQ-02 No `noindex` in the `X-Robots-Tag` header (B)
The header has the same effect as the meta tag, and a body grep cannot see it. Hosts and CDNs add it to protect previews, and it sometimes survives into production.
```bash
grep -i '^x-robots-tag' .launch-qa/*.headers
```
```powershell
foreach ($p in $Pages) { '{0}  [{1}]' -f $p, $Res[$p].Headers['x-robots-tag'] }
```
**Pass:** no header, or one without `noindex` or `none`. **Fail:** `noindex` on a public page. Vercel adds `X-Robots-Tag: noindex` to non-production deployments by default and leaves it off custom domains assigned to a preview branch (Vercel KB, verified 2026-10), so a staging domain on Vercel can be indexable unless you add the header yourself.

### LQ-03 `robots.txt` does not block the site (B)
`Disallow: /` under `User-agent: *` stops all compliant crawling. Google also treats a `robots.txt` that returns `5xx` as a reason to stop crawling the site for the first 12 hours, then falls back to a cached copy for up to 30 days (Google robots.txt spec, verified 2026-10).
```bash
curl -s -o /dev/null -w 'robots.txt status: %{http_code}\n' "$SITE/robots.txt"
curl -s "$SITE/robots.txt" | grep -inE '^[[:space:]]*(user-agent|allow|disallow|sitemap)[[:space:]]*:'
curl -s "$SITE/robots.txt" | grep -inE '^[[:space:]]*disallow[[:space:]]*:[[:space:]]*/[[:space:]]*$'
```
```powershell
$rb = Get-Hop "$Site/robots.txt"; "robots.txt status: $($rb.Status)"
$rb.Body -split "`n" | Select-String -Pattern '^\s*(user-agent|allow|disallow|sitemap)\s*:'
$rb.Body -split "`n" | Select-String -Pattern '^\s*disallow\s*:\s*/\s*$'
```
**Pass:** `200` (or `404`, which Google treats as no restrictions), and no `Disallow: /` in a group for `*`, Googlebot or a crawler the user wants. Read the group the line sits in: `Disallow: /` under a crawler the user chose to block is a decision, not a failure. **Fail:** `Disallow: /` for `*` or Googlebot, or a `5xx`.

### LQ-04 No password, basic auth or login wall (B)
Crawlers cannot log in. Platform password protection, HTTP basic auth and deployment protection all return `401`, `403` or a redirect to a login page, and Google cannot index the content behind them.
```bash
grep -iE '^(HTTP/|location:|www-authenticate:)' .launch-qa/*.headers
```
```powershell
foreach ($p in $Pages) { $r = $Res[$p]; '{0}  {1}  location=[{2}]  www-authenticate=[{3}]' -f $r.Status, $p, $r.Location, $r.Headers['www-authenticate'] }
```
**Pass:** `200` on every key template with no `WWW-Authenticate` header. **Fail:** `401`, `403`, or a `3xx` whose `Location` is a login, SSO or platform-auth URL.

---

## Gate 2: crawlers can get in and see the content

### LQ-05 Googlebot and wanted AI crawlers are not blocked at the CDN or WAF (B)
Bot-management modes, AI-bot toggles, rate limits and geo rules sit in front of the site, so the code can be perfect while crawlers get a challenge page. Fetch a key template with each crawler's user-agent token and compare.
```bash
KEY="/blog/a-real-post"
for bot in "Googlebot/2.1; +http://www.google.com/bot.html" "OAI-SearchBot/1.0" "GPTBot/1.0" \
           "ChatGPT-User/1.0" "Claude-SearchBot/1.0" "ClaudeBot/1.0" "Claude-User/1.0"; do
  code=$(curl -s -o .launch-qa/bot.out -w '%{http_code} %{size_download}B' -A "Mozilla/5.0 (compatible; $bot)" "$SITE$KEY")
  if grep -qiE 'just a moment|cf-chl|captcha|access denied|attention required' .launch-qa/bot.out; then v=CHALLENGE; else v=ok; fi
  printf '%-48s %s %s\n' "$bot" "$code" "$v"
done
```
```powershell
$Key = '/blog/a-real-post'
foreach ($bot in 'Googlebot/2.1; +http://www.google.com/bot.html', 'OAI-SearchBot/1.0', 'GPTBot/1.0', 'ChatGPT-User/1.0', 'Claude-SearchBot/1.0', 'ClaudeBot/1.0', 'Claude-User/1.0') {
  $r = Get-Hop "$Site$Key" "Mozilla/5.0 (compatible; $bot)"
  $v = if ($r.Body -match 'just a moment|cf-chl|captcha|access denied|attention required') { 'CHALLENGE' } else { 'ok' }
  '{0,-48} {1} {2} chars {3}' -f $bot, $r.Status, $r.Body.Length, $v
}
```
**Pass:** the same `200` and roughly the same body size as a normal fetch for Googlebot and every crawler the user wants. **Fail:** `403`, `429`, `503` or a challenge page for Googlebot, or for a crawler the user has chosen to allow.

This test only exercises rules keyed on the user-agent. Many CDNs check the requesting IP as well and block a spoofed "Googlebot" from your machine on purpose, so a `403` here is a lead, not proof. Confirm Googlebot access with the Search Console URL Inspection live test, and confirm AI crawlers in the CDN's firewall events or bot analytics. Google publishes its crawler IP ranges and the reverse-DNS method for verifying Googlebot; OpenAI and Anthropic publish their crawler tokens (OpenAI: `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`; Anthropic: `ClaudeBot`, `Claude-SearchBot`, `Claude-User`; all verified 2026-10). Whether to allow AI crawlers is the user's decision. The CDN detail is in [`1-reach-indexation/references/edge-cdn-and-bot-access.md`](../../1-reach-indexation/references/edge-cdn-and-bot-access.md).

### LQ-06 The primary content is in the served HTML (B)
This is Reach's core check. Many AI crawlers do not run JavaScript, so content that appears only after hydration is invisible to them. Pick a distinctive sentence of body copy from each key template.
```bash
grep -c "a distinctive sentence from the post" .launch-qa/_blog_a_real_post.html   # 0 means missing
grep -oE '<div id="(root|app)">[[:space:]]*</div>' .launch-qa/*.html              # an empty SPA shell
```
```powershell
$Res['/blog/a-real-post'].Body.Contains('a distinctive sentence from the post')
foreach ($p in $Pages) { if ($Res[$p].Body -match '<div id="(root|app)">\s*</div>') { "$p  empty SPA shell" } }
```
**Pass:** the sentence, the real `<h1>` and the real `<title>` are in the raw HTML of every key template. **Fail:** they appear only in the browser. Hand to [`1-reach-indexation`](../../1-reach-indexation/SKILL.md).

### LQ-07 Key templates return `200` directly (B)
The setup output already shows this. A key page that redirects, or returns `4xx` or `5xx`, is either the wrong URL in your list or a real problem.

**Pass:** every key template returns `200` without a redirect. **Fail:** `4xx` or `5xx`. A `3xx` means the URL you listed is not the canonical one: fix the list, then check LQ-08 and LQ-11.

---

## Gate 3: one host, one protocol, one URL form

### LQ-08 HTTPS and the preferred host (B, or W for two hops)
Every variant of the home page should reach the production origin in one permanent hop (`301` or `308`). Google prefers HTTPS pages as canonical and treats every permanent redirect method the same for canonicalisation (Google, consolidate duplicate URLs, verified 2026-10).
```bash
APEX="${SITE#https://}"; APEX="${APEX#www.}"
for u in "http://$APEX/" "http://www.$APEX/" "https://$APEX/" "https://www.$APEX/"; do
  curl -s -o /dev/null -w "first hop: %{http_code} -> %{redirect_url}\n" "$u"
  curl -s -o /dev/null -L --max-redirs 10 -w "  %{num_redirects} hop(s), final %{http_code} %{url_effective}\n" "$u"
done
```
```powershell
$Apex = ([Uri]$Site).Host -replace '^www\.', ''
foreach ($u in "http://$Apex/", "http://www.$Apex/", "https://$Apex/", "https://www.$Apex/") {
  try { $c = @(Get-Chain $u); '{0}: {1} hop(s), codes {2}, final {3}' -f $u, ($c.Count - 1), (($c | ForEach-Object { $_.Status }) -join ' > '), $c[-1].Url }
  catch { "$u  ERROR $($_.Exception.InnerException.Message)" }
}
```
**Pass:** each variant ends at `$SITE/` with `200`, in one hop using `301` or `308` (the preferred origin itself in zero). **Fail (B):** HTTPS does not work, a variant ends somewhere else, serves the site with `200` without redirecting (a duplicate host), or loops. **Warn (W):** two hops, for example `http://example.com` to `https://example.com` to `https://www.example.com`, or a temporary `302` or `307` where the move is permanent (a weaker signal for which host is canonical). A variant that does not resolve at all (curl prints `000`) is a WARN: add the DNS record and redirect if users are likely to type it.

### LQ-09 Trailing-slash consistency (W)
`/pricing` and `/pricing/` are different URLs. One should redirect permanently to the other. Next.js redirects `/about/` to `/about` by default, or the reverse with `trailingSlash: true` (Next.js docs, verified 2026-10).
```bash
P="/pricing"
for u in "$SITE$P" "$SITE$P/"; do
  printf '%s  ' "$u"; curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' "$u"
done
```
```powershell
$P = '/pricing'
foreach ($u in "$Site$P", "$Site$P/") { $r = Get-Hop $u; '{0}  {1} {2}' -f $u, $r.Status, $r.Location }
```
**Pass:** one form returns `200`, the other `301` or `308` to it, and canonicals and sitemap use the `200` form. **Warn:** both return `200`. Google can still pick one using the canonical, but the redirect is the stronger, cleaner signal.

### LQ-10 Missing pages return `404` (B if every URL returns `200`, otherwise W)
A "not found" page served with `200` is a soft 404. Google wants `404` or `410` for removed content and treats the two the same (Search Central, verified 2026-10). A catch-all route that answers `200` for every URL can flood the index with duplicates of the home page. Test a random path at the root and one under each dynamic route.
```bash
curl -s -o /dev/null -w "root:    %{http_code} %{redirect_url}\n" "$SITE/launch-qa-missing-$(date +%s)"
curl -s -o .launch-qa/missing.out -w "dynamic: %{http_code} %{redirect_url}\n" "$SITE/blog/launch-qa-missing-$(date +%s)"
grep -ioE '<meta[^>]+name="?robots"?[^>]*>' .launch-qa/missing.out
```
```powershell
$Stamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
foreach ($u in "$Site/launch-qa-missing-$Stamp", "$Site/blog/launch-qa-missing-$Stamp") {
  $r = Get-Hop $u
  $meta = ([regex]::Match($r.Body, '<meta[^>]+name="?robots"?[^>]*>', 'IgnoreCase')).Value
  '{0}  {1} {2} {3}' -f $u, $r.Status, $r.Location, $meta
}
```
**Pass:** `404` or `410` for both. **Fail (B):** `200` with normal content, or a redirect to the home page, for every missing URL. **Warn (W):** `200` with a `noindex` robots meta on a dynamic route. In Next.js App Router this happens when `notFound()` runs after the response has started streaming: the status is already `200`, so Next.js adds `noindex` instead. The page will not be indexed, but call `notFound()` before any `Suspense` boundary or `loading.tsx` to return a real `404` (Next.js docs, verified 2026-10).

### LQ-11 Canonicals are absolute and on the production host (B)
A canonical pointing at a staging host, `localhost` or another page tells Google to index something else. Google asks for absolute URLs in `rel="canonical"` (verified 2026-10).
```bash
for f in .launch-qa/*.html; do
  printf '%-40s ' "$f"
  grep -oiE '<link[^>]+rel="?canonical"?[^>]*>' "$f" | grep -oiE 'href="[^"]+"' || echo "NO CANONICAL"
done
```
```powershell
foreach ($p in $Pages) {
  $c = ([regex]::Match($Res[$p].Body, '<link[^>]+rel="?canonical"?[^>]*>', 'IgnoreCase')).Value
  $href = ([regex]::Match($c, 'href="([^"]+)"')).Groups[1].Value
  '{0,-28} {1}' -f $p, $(if ($href) { $href } else { 'NO CANONICAL' })
}
```
**Pass:** each canonical is absolute, starts with `$SITE` and is the page's own URL in its preferred slash form (or a deliberate consolidation target). **Fail (B):** another host, `http://`, a relative URL, or every page pointing at the home page. **Warn (W):** no canonical at all.

### LQ-12 No staging, localhost or preview hosts in self-references (B)
Open Graph URLs, `hreflang` alternates and JSON-LD `url`, `@id`, `image` and `logo` values should name the production host. A preview host here sends link signals and share previews to a URL that may be protected or gone tomorrow. First list every host the self-reference fields use, then screen for known non-production patterns.
```bash
for f in .launch-qa/*.html; do
  { grep -oiE '<link[^>]+rel="?(canonical|alternate)"?[^>]*>' "$f"
    grep -oiE '<meta[^>]+(property|name)="(og:url|og:image|twitter:image)"[^>]*>' "$f"
    grep -oiE '"(url|@id|image|logo)"[[:space:]]*:[[:space:]]*"[^"]+"' "$f"
  } | grep -oiE 'https?://[^"/<> ]+' | sort -u | sed "s#^#$f  #"
done
grep -oiE "https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|[a-z0-9.-]+\.(vercel\.app|netlify\.app|pages\.dev|herokuapp\.com|onrender\.com|fly\.dev|ngrok-free\.app|ngrok\.io)|(staging|stage|dev|preview|test)\.[a-z0-9.-]+)[^\"'<> ]*" .launch-qa/*.html | sort -u
```
```powershell
$self = '<link[^>]+rel="?(canonical|alternate)"?[^>]*>|<meta[^>]+(property|name)="(og:url|og:image|twitter:image)"[^>]*>|"(url|@id|image|logo)"\s*:\s*"[^"]+"'
foreach ($p in $Pages) {
  [regex]::Matches($Res[$p].Body, $self, 'IgnoreCase') | ForEach-Object { [regex]::Matches($_.Value, 'https?://[^"/<> ]+') } |
    ForEach-Object { $_.Value } | Sort-Object -Unique | ForEach-Object { "$p  $_" }
}
$leak = 'https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|[a-z0-9.-]+\.(vercel\.app|netlify\.app|pages\.dev|herokuapp\.com|onrender\.com|fly\.dev|ngrok-free\.app|ngrok\.io)|(staging|stage|dev|preview|test)\.[a-z0-9.-]+)[^"''<> ]*'
foreach ($p in $Pages) { [regex]::Matches($Res[$p].Body, $leak, 'IgnoreCase') | ForEach-Object { "$p  $($_.Value)" } | Sort-Object -Unique }
```
**Pass:** the self-reference hosts are the production host, plus image or asset CDNs you recognise and external profiles in `sameAs`. **Fail:** a preview, staging or local host in any self-reference field. The second grep scans the whole page, so it also catches ordinary links to other sites on those platforms: judge each hit. If the production site itself lives on a platform subdomain (a `*.vercel.app` or `*.github.io` site), that host is correct.

In Next.js, `metadataBase` turns relative metadata URLs into absolute ones. Vercel documents `VERCEL_URL` as the generated deployment URL and `VERCEL_PROJECT_PRODUCTION_URL` as the *shortest* production domain (verified 2026-10), so neither is guaranteed to be your preferred host. Set the origin explicitly.

### LQ-13 The sitemap lists only production, canonical `200` URLs (B if it lists another host, otherwise W)
The sitemap tells Google which URLs you want indexed. Google needs fully qualified URLs, ignores `priority` and `changefreq`, limits each file to 50,000 URLs or 50 MB uncompressed, and asks you not to name a different canonical in the sitemap than in `rel="canonical"` (Search Central, verified 2026-10).
```bash
curl -s "$SITE/robots.txt" | grep -i '^sitemap:'
curl -s -o .launch-qa/sitemap.xml -w 'sitemap status: %{http_code} %{content_type}\n' "$SITE/sitemap.xml"
if grep -q '<sitemapindex' .launch-qa/sitemap.xml; then
  for sm in $(grep -oE '<loc>[^<]+</loc>' .launch-qa/sitemap.xml | sed -E 's#</?loc>##g'); do curl -s "$sm"; done > .launch-qa/sitemap-all.xml
else
  cp .launch-qa/sitemap.xml .launch-qa/sitemap-all.xml
fi
grep -oE '<loc>[^<]+</loc>' .launch-qa/sitemap-all.xml | sed -E 's#</?loc>##g; s/&amp;/\&/g' > .launch-qa/urls.txt
printf '%s URLs\n' "$(wc -l < .launch-qa/urls.txt)"
grep -v "^$SITE" .launch-qa/urls.txt | head                     # anything not on the production origin
head -n 50 .launch-qa/urls.txt | while read -r u; do              # sample: raise for a full check
  printf '%s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -A "$UA" "$u")" "$u"
done | grep -v '^200 '
```
```powershell
$rb.Body -split "`n" | Select-String -Pattern '^\s*sitemap\s*:'
$sm = Get-Hop "$Site/sitemap.xml"; "sitemap status: $($sm.Status) $($sm.Headers['content-type'])"
$xml = $sm.Body
if ($xml -match '<sitemapindex') {
  $xml = ([regex]::Matches($xml, '<loc>\s*([^<\s]+)\s*</loc>') | ForEach-Object { (Get-Hop $_.Groups[1].Value).Body }) -join "`n"
}
$Urls = [regex]::Matches($xml, '<loc>\s*([^<\s]+)\s*</loc>') | ForEach-Object { $_.Groups[1].Value -replace '&amp;', '&' }
"$($Urls.Count) URLs"
$Urls | Where-Object { -not $_.StartsWith($Site) } | Select-Object -First 10
$Urls | Select-Object -First 50 | ForEach-Object { $s = (Get-Hop $_).Status; if ($s -ne 200) { "$s $_" } }
```
Gzipped sitemaps (`.xml.gz`) need decompressing first (`curl -s URL | gunzip`). If the sitemap lives somewhere other than `/sitemap.xml`, use the URL from the `Sitemap:` line.

**Pass:** the sitemap returns `200`, is referenced from `robots.txt` with an absolute production URL, every `<loc>` starts with `$SITE`, and the sample returns `200` with no redirects. **Fail (B):** URLs on another host. **Warn (W):** no sitemap, not referenced from `robots.txt`, or listing redirects, `404`s or `noindex` pages.

### LQ-14 Old-site URLs redirect to their equivalents (B when replacing a site)
If this launch replaces a site, every old URL with traffic or links must `301` or `308` to its closest new equivalent in one hop. This is a launch blocker and [`seo-migrations`](../../seo-migrations/SKILL.md) owns it. For a quick screen, put the old site's top URLs (from its sitemap, analytics or Search Console export) in `old-urls.txt`:
```bash
while read -r u; do
  curl -s -o /dev/null -L --max-redirs 10 -w "%{num_redirects} hop(s)  %{http_code}  $u -> %{url_effective}\n" "$u"
done < old-urls.txt
```
```powershell
Get-Content old-urls.txt | ForEach-Object {
  $c = @(Get-Chain $_); '{0} hop(s) {1}  {2} -> {3}' -f ($c.Count - 1), (($c | ForEach-Object { $_.Status }) -join '>'), $_, $c[-1].Url
}
```
**Pass:** one permanent hop to an equivalent page that returns `200`. **Fail:** `404`, a chain, a `302`, or everything landing on the home page. **N/A:** a brand-new site on a new domain.

---

## Gate 4: what the result looks like

### LQ-15 Real, distinct titles (B if a placeholder, otherwise W)
Google asks for a `<title>` on every page, distinct per page and not vague (Search Central, title links, verified 2026-10). A framework placeholder in the title of every page is the most visible launch mistake in search results.
```bash
grep -oiE '<title[^>]*>[^<]*</title>' .launch-qa/*.html
grep -ohiE '<title[^>]*>[^<]*</title>' .launch-qa/*.html | sort | uniq -d                # duplicates across templates
grep -liE '<title[^>]*>[[:space:]]*(Create Next App|Vite \+ React( \+ TS)?|React App|Untitled|Home)[[:space:]]*</title>' .launch-qa/*.html
```
```powershell
$titles = foreach ($p in $Pages) { [pscustomobject]@{ Page = $p; Title = ([regex]::Match($Res[$p].Body, '<title[^>]*>([^<]*)</title>', 'IgnoreCase')).Groups[1].Value.Trim() } }
$titles | Format-Table -AutoSize
$titles | Group-Object Title | Where-Object Count -gt 1 | ForEach-Object { "DUPLICATE: $($_.Name)" }
$titles | Where-Object { $_.Title -match '^(Create Next App|Vite \+ React( \+ TS)?|React App|Untitled|Home)$' -or -not $_.Title } | ForEach-Object { "PLACEHOLDER/EMPTY: $($_.Page)" }
```
**Pass:** each key template has a real title that describes the page, and templates differ. **Fail (B):** a framework placeholder or an empty title. **Warn (W):** the same title on several templates, or a bare "Home".

### LQ-16 Meta descriptions (W)
Google may use the description for the snippet. A missing one is not a blocker; a placeholder is embarrassing.
```bash
for f in .launch-qa/*.html; do
  d=$(grep -oiE '<meta[^>]+name="description"[^>]*>' "$f" | head -1)
  printf '%-40s %s\n' "$f" "${d:-NONE}"
done
grep -li 'Generated by create next app' .launch-qa/*.html
```
```powershell
foreach ($p in $Pages) { $d = ([regex]::Match($Res[$p].Body, '<meta[^>]+name="description"[^>]*>', 'IgnoreCase')).Value; '{0,-28} {1}' -f $p, $(if ($d) { $d } else { 'NONE' }) }
foreach ($p in $Pages) { if ($Res[$p].Body -match 'Generated by create next app') { "PLACEHOLDER: $p" } }
```
**Pass:** present, specific to the page, no placeholder. **Warn:** missing, duplicated across templates, or a placeholder.

### LQ-17 A real `<h1>` (W)
Google uses visible headings among its sources for title links (verified 2026-10), and the `<h1>` tells readers and crawlers what the page is.
```bash
for f in .launch-qa/*.html; do
  printf '%s  h1 count: %s\n' "$f" "$(grep -oiE '<h1[ >]' "$f" | wc -l)"
  grep -oiE '<h1[^>]*>.{0,120}' "$f" | head -1
done
```
```powershell
foreach ($p in $Pages) {
  $b = $Res[$p].Body
  '{0}  h1 count: {1}' -f $p, ([regex]::Matches($b, '<h1[\s>]', 'IgnoreCase')).Count
  $m = [regex]::Match($b, '<h1[^>]*>.{0,120}', 'IgnoreCase'); if ($m.Success) { '  ' + $m.Value }
}
```
**Pass:** each key template has a meaningful `<h1>` in the served HTML. **Warn:** none, an `<h1>` holding only a logo, or the same `<h1>` on every template. Several `<h1>`s are not a failure on their own; check they make sense.

### LQ-18 No mixed content; HSTS set (W)
An `http://` script, stylesheet or image on an HTTPS page is blocked or flagged by browsers. HSTS tells browsers to use HTTPS from the first request.
```bash
grep -oiE '(src|srcset)="http://[^"]+"|<link[^>]+href="http://[^"]+"[^>]*>' .launch-qa/*.html | head
grep -i '^strict-transport-security' .launch-qa/_.headers || echo "NO HSTS"
```
```powershell
foreach ($p in $Pages) { [regex]::Matches($Res[$p].Body, '(src|srcset)="http://[^"]+"|<link[^>]+href="http://[^"]+"[^>]*>', 'IgnoreCase') | ForEach-Object { "$p  $($_.Value)" } }
$hsts = $Res['/'].Headers['strict-transport-security']; if ($hsts) { $hsts } else { 'NO HSTS' }
```
**Pass:** no `http://` subresources, and an HSTS header. **Warn:** either missing. Start HSTS with a short `max-age` if the user is unsure every subdomain serves HTTPS, because it is hard to undo.

### LQ-19 Open Graph and Twitter images (W)
The share preview is what people see when the launch link is posted. The Open Graph protocol requires `og:title`, `og:type`, `og:image` and `og:url`, with `og:url` as the canonical URL (ogp.me, verified 2026-10). X falls back to Open Graph tags when its own are missing, and `summary_large_image` needs `twitter:card` set (X developer docs, verified 2026-10).
```bash
grep -oiE '<meta[^>]+(property|name)="(og|twitter):[a-z:_]+"[^>]*>' .launch-qa/_.html
IMG=$(grep -oiE '<meta[^>]+property="og:image"[^>]*>' .launch-qa/_.html | head -1 | sed -E 's/.*content="([^"]+)".*/\1/; s/&amp;/\&/g')
echo "og:image = ${IMG:-NONE}"
[ -n "$IMG" ] && curl -s -o /dev/null -w '%{http_code} %{content_type} %{size_download} bytes\n' "$IMG"
```
```powershell
$homeHtml = $Res['/'].Body      # not $home: that is a read-only automatic variable
[regex]::Matches($homeHtml, '<meta[^>]+(property|name)="(og|twitter):[a-z:_]+"[^>]*>', 'IgnoreCase') | ForEach-Object { $_.Value }
$img = ([regex]::Match($homeHtml, '<meta[^>]+property="og:image"[^>]+content="([^"]+)"', 'IgnoreCase')).Groups[1].Value -replace '&amp;', '&'
if ($img) { $i = Get-Hop ([System.Uri]::new([System.Uri]"$Site/", $img).AbsoluteUri); 'og:image = {0}  {1} {2}' -f $img, $i.Status, $i.Headers['content-type'] } else { 'NO og:image' }
```
Repeat for one inner template. **Pass:** the four `og:` tags and `twitter:card` are present, `og:url` matches the canonical, and `og:image` is absolute, on the production host or an image CDN, and returns `200` with an `image/*` type. **Warn:** missing tags, a relative image URL, or an image that returns `401`, `403` or `404` (often because it lives on a protected preview host). Next.js fails the build when an `opengraph-image` file exceeds 8 MB or a `twitter-image` file exceeds 5 MB (Next.js docs, verified 2026-10).

### LQ-20 Favicon (W)
Google shows the favicon beside results. It needs a `rel="icon"` (or `shortcut icon`, `apple-touch-icon`) link on the home page, a square image, ideally larger than 48x48 px, and both the home page and the icon file must be crawlable (Search Central, favicon, verified 2026-10).
```bash
grep -oiE '<link[^>]+rel="(icon|shortcut icon|apple-touch-icon)"[^>]*>' .launch-qa/_.html
curl -s -o /dev/null -w 'favicon.ico: %{http_code} %{content_type}\n' "$SITE/favicon.ico"
```
```powershell
[regex]::Matches($homeHtml, '<link[^>]+rel="(icon|shortcut icon|apple-touch-icon)"[^>]*>', 'IgnoreCase') | ForEach-Object { $_.Value }
$f = Get-Hop "$Site/favicon.ico"; 'favicon.ico: {0} {1}' -f $f.Status, $f.Headers['content-type']
```
Fetch each linked `href` the same way. **Pass:** linked from the home page, returns `200` with an image type, square (check `sizes` or open the file), not disallowed in `robots.txt`. **Warn:** missing, `404`, non-square, or the framework's default icon.

### LQ-21 Web app manifest (W, N/A if not linked)
A manifest is optional for search. If one is linked, it should load and parse, or browsers log errors and install prompts break.
```bash
MF=$(grep -oiE '<link[^>]+rel="manifest"[^>]*>' .launch-qa/_.html | sed -E 's/.*href="([^"]+)".*/\1/')
echo "manifest = $MF"
[ -n "$MF" ] && curl -s "$SITE${MF#$SITE}" | jq -e '.name // .short_name' && echo "valid JSON"
```
```powershell
$mf = ([regex]::Match($homeHtml, '<link[^>]+rel="manifest"[^>]+href="([^"]+)"', 'IgnoreCase')).Groups[1].Value
"manifest = $mf"
if ($mf) { $m = Get-Hop ([System.Uri]::new([System.Uri]"$Site/", $mf).AbsoluteUri); $m.Status; ($m.Body | ConvertFrom-Json).name }
```
The bash check assumes `href` is a path or a full URL on `$SITE`, and needs `jq`. **Pass:** `200`, valid JSON with a `name` or `short_name`, and the icons it lists return `200`. **Warn:** `404` or invalid JSON.

### LQ-22 Analytics and Search Console verification (W, but do it on launch day)
Without them nobody can see whether the launch worked. This pass only checks they are present; [`seo-measurement-setup`](../../seo-measurement-setup/SKILL.md) installs and fixes them.
```bash
grep -oiE 'googletagmanager\.com/(gtag/js|gtm\.js)\?id=[A-Z0-9-]+|/_vercel/insights|plausible\.io/js|static\.cloudflareinsights\.com' .launch-qa/_.html | sort | uniq -c
grep -oiE '<meta[^>]+name="google-site-verification"[^>]*>' .launch-qa/_.html
nslookup -type=TXT "$APEX" | grep -i 'google-site-verification'
```
```powershell
[regex]::Matches($homeHtml, 'googletagmanager\.com/(gtag/js|gtm\.js)\?id=[A-Z0-9-]+|/_vercel/insights|plausible\.io/js|static\.cloudflareinsights\.com', 'IgnoreCase') | Group-Object Value | ForEach-Object { '{0} x{1}' -f $_.Name, $_.Count }
([regex]::Match($homeHtml, '<meta[^>]+name="google-site-verification"[^>]*>', 'IgnoreCase')).Value
Resolve-DnsName -Type TXT $Apex | Where-Object { $_.Strings -match 'google-site-verification' } | ForEach-Object { $_.Strings }
```
Tags loaded after consent or by a tag manager will not appear in the raw HTML: confirm in a browser's network panel. **Pass:** one analytics tag, and a Search Console token (meta tag, HTML file or DNS record) in place. Search Console keeps a property verified only while the token stays in place (Search Console Help, verified 2026-10), so do not remove it in a later deploy. **Warn:** no analytics, the same tag twice, or no verification.

---

## Scorecard format

Report one row per check, in order. Keep evidence to one line of served output.

```text
Launch QA: https://www.example.com  (production, run 2026-10-06, post-deploy)
Verdict: BLOCKED, 2 launch blockers

ID     Check                               Result  Class  Evidence
LQ-01  Meta robots noindex                 FAIL    B      /: <meta name="robots" content="noindex, nofollow"/>
LQ-02  X-Robots-Tag                        PASS    B
...
LQ-21  Manifest                            N/A     W      no rel="manifest"
LQ-22  Analytics + Search Console          WARN    W      GA4 present; no verification token

Launch blockers (fix before launch):
  1. LQ-01 ...  owner: code
Fix this week:
  1. LQ-08 ...  owner: host settings
Hand-offs: seo-measurement-setup (LQ-22)
```

In quick-wins mode, report only the blocker rows that fail, at most five, then one line on what you skipped.

---

## Launch day and the first week

- [ ] Every **B** check passes on production (re-run after the final deploy).
- [ ] Search Console property verified; a Domain property (DNS) covers every protocol and subdomain.
- [ ] Sitemap submitted in Search Console; the Sitemaps report reads it without errors.
- [ ] URL Inspection live test passes on the home page and one URL per key template; indexing requested for those few. Google notes there is a quota and that repeat requests do not speed things up (verified 2026-10).
- [ ] The robots.txt report in Search Console shows the production file.
- [ ] Analytics records a visit, once.
- [ ] Old domain or old URLs still redirect (if a site was replaced); Change of Address filed for a domain move.
- [ ] Days 1 to 7: blocker checks re-run after every deploy.
- [ ] Days 1 to 7: Page indexing report watched for "URL marked 'noindex'", "URL blocked by robots.txt", "Blocked due to unauthorized request (401)", "Soft 404" and "Duplicate, Google chose different canonical than user".
- [ ] Days 1 to 7: CDN or server logs checked for `404`s on old URLs and for blocked or challenged crawler requests.

Google says crawling can take from a few days to a few weeks (Search Central, verified 2026-10). An empty Page indexing report in the first days is normal; a URL listed under one of the reasons above is not.

---

## Definition of done

The launch passes QA only when all of these hold on the **production URL, after the final deploy**:

- [ ] LQ-01 to LQ-07 pass on every key template: no `noindex` in meta or header, `robots.txt` open, no auth wall, crawlers not challenged (confirmed in URL Inspection for Googlebot), content in the served HTML, `200` responses.
- [ ] LQ-08: HTTPS works and every host and protocol variant reaches the production origin.
- [ ] LQ-10: missing URLs do not all return `200`.
- [ ] LQ-11 to LQ-13: canonicals, self-references and the sitemap name only the production host.
- [ ] LQ-14: old-site URLs redirect (or N/A).
- [ ] LQ-15: no placeholder titles.
- [ ] Every **W** item passes, or has an owner and a date in the report.
- [ ] The launch-day steps above are done or handed to the user with exact instructions.
- [ ] You re-fetched after each fix and saw the change in the served output. A source edit is not a pass.

---

## Worked example (illustrative)

A fictional bakery, `https://www.example.com`, built with Next.js App Router, hosted on Vercel with Cloudflare in front, replacing nothing. The user says "we go live tomorrow, anything that will stop us ranking?", so the agent runs quick-wins mode on the release deployment, now assigned to the production domain.

**Findings, blockers only:**
```text
Verdict: BLOCKED, 3 launch blockers
LQ-01  FAIL  /, /menu/sourdough, /visit: <meta name="robots" content="noindex, nofollow"/>
LQ-12  FAIL  og:url and JSON-LD "url" on https://bakery-git-main-acme.vercel.app
LQ-05  FAIL  Googlebot UA: 403 "Just a moment..." (CHALLENGE); normal UA: 200
Skipped: all W checks (quick-wins mode).
```

**Causes and fixes:**
- **LQ-01.** `app/layout.tsx` still had `robots: { index: false, follow: false }` from the private beta. The agent removed it. Previews stay protected by Vercel's default `X-Robots-Tag: noindex`; the custom staging domain did not get that header, so the agent flagged it for the user to protect separately.
- **LQ-12.** `metadataBase` was built from `VERCEL_URL`, which is the deployment URL. The agent set the origin explicitly:
  ```ts
  // app/layout.tsx
  import type { Metadata } from 'next'

  export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://www.example.com'

  export const metadata: Metadata = {
    metadataBase: new URL(SITE_URL),
  }
  ```
  and built the JSON-LD `url` and `sitemap.ts` entries from `SITE_URL`. Each page sets its own `alternates.canonical` (for example `'/menu/sourdough'`). The canonical stays out of the root layout on purpose: every page that did not override it would inherit the home page's canonical.
- **LQ-05.** A Cloudflare rule challenged every request with "bot" in the user-agent. The spoofed test alone could not prove Googlebot was affected, so the agent asked the user to run the URL Inspection live test, which failed with a blocked fetch. The fix was a CDN setting, so the agent gave the user the exact rule to change and did not touch the account.

**Verification after redeploy:**
```text
LQ-01  PASS  no robots meta on 3 templates; no X-Robots-Tag
LQ-12  PASS  self-reference hosts: https://www.example.com only
LQ-05  PASS  URL Inspection live test: page can be indexed; Googlebot UA 200, 48 KB, ok
```

**Report:** ready to launch, with the fix-this-week list from the full pass the next morning (a two-hop `http://example.com` redirect, no meta description on `/visit`, Search Console not yet verified, handed to `seo-measurement-setup`). The boundary stated plainly: nothing now stops Google from indexing the site; when and how well it ranks is live data to watch over the coming weeks.
