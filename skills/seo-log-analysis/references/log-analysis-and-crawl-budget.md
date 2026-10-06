# Log analysis & crawl budget

Read this for the how. Server logs are the only place you see what crawlers *actually* did (not what you hope they do). The two payoffs: find **important pages crawlers ignore**, and find **budget wasted on junk**.

Every command here was written for real formats; check field positions against a few lines of the user's own logs before trusting any output, because servers are often configured with custom formats.

---

## 1. Parsing

Reduce every source to the same columns: `ip, ts, uri, path, status, ua`. `uri` keeps the query string; `path` drops it.

### Combined log format (Nginx and Apache default)
Apache defines it as `%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"`, which gives lines like:

```text
66.249.66.1 - - [05/Oct/2026:10:00:01 +0000] "GET /products/blue-widget HTTP/1.1" 200 5120 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
```

Splitting on double quotes puts the request in `$2`, the status and size in `$3`, and the user agent in `$6`:

```bash
# IP, URI and status for every request whose user agent claims Googlebot
awk -F'"' 'tolower($6) ~ /googlebot/ { split($1,a," "); split($2,r," "); split($3,s," ");
  printf "%s,%s,%s\n", a[1], r[2], s[1] }' access.log > googlebot-claims.csv

# Gzipped rotations
zcat access.log*.gz | awk -F'"' '...same program...' >> googlebot-claims.csv
```

A URI containing a comma or a double quote will break this CSV. That is rare for crawler traffic; the DuckDB route below handles it properly.

### JSON lines from a CDN (Cloudflare Logpush example)
Cloudflare's `http_requests` dataset names the fields `ClientIP`, `ClientRequestURI` (path plus query), `ClientRequestPath` (path only), `EdgeResponseStatus`, `OriginResponseStatus`, `ClientRequestUserAgent` and `EdgeStartTimestamp` (verified 2026-10). Other CDNs use other names; map them to the same columns.

```bash
gunzip -c logs/*.json.gz | jq -r 'select(.ClientRequestUserAgent | test("googlebot"; "i"))
  | "\(.ClientIP),\(.ClientRequestURI),\(.EdgeResponseStatus)"' > googlebot-claims.csv
```

Use `EdgeResponseStatus` for what crawlers received. `OriginResponseStatus` is only what your server returned to the CDN.

### DuckDB (any shell, any size)
DuckDB runs the same on Windows, macOS and Linux, reads gzipped files directly, and handles tens of millions of lines on a laptop. Save as `logs.sql` and run `duckdb crawl.duckdb < logs.sql`.

```sql
-- 1. Load. Option A: combined log format.
CREATE OR REPLACE TABLE hits AS
SELECT m.ip,
       strptime(m.ts, '%d/%b/%Y:%H:%M:%S %z') AS ts,
       m.uri, m.path, CAST(m.status AS INTEGER) AS status, m.ua
FROM (
  SELECT regexp_extract(line,
    '^(\S+) \S+ \S+ \[([^\]]+)\] "\S+ ((\S*?)(\?\S*)?) [^"]*" (\d{3}) \S+ "[^"]*" "([^"]*)"',
    ['ip', 'ts', 'uri', 'path', 'qs', 'status', 'ua']) AS m
  FROM read_csv('access.log*', columns = {'line': 'VARCHAR'}, header = false,
                delim = '\t', quote = '', escape = '', auto_detect = false)
) WHERE m.ip <> '';

-- 1. Load. Option B: Cloudflare Logpush JSON lines (use instead of option A).
-- CREATE OR REPLACE TABLE hits AS
-- SELECT ClientIP AS ip, CAST(EdgeStartTimestamp AS TIMESTAMPTZ) AS ts,
--        ClientRequestURI AS uri, ClientRequestPath AS path,
--        CAST(EdgeResponseStatus AS INTEGER) AS status, ClientRequestUserAgent AS ua
-- FROM read_json('logs/*.json.gz', format = 'newline_delimited');
-- If EdgeStartTimestamp is an integer of nanoseconds, use
-- make_timestamp(EdgeStartTimestamp // 1000) for ts instead.

-- 2. Verified IPs from section 2 (ip,verdict,detail with no header row).
CREATE OR REPLACE TABLE ip_verdicts AS
SELECT * FROM read_csv('ip-verdicts.csv', header = false,
  columns = {'ip': 'VARCHAR', 'verdict': 'VARCHAR', 'detail': 'VARCHAR'});

CREATE OR REPLACE VIEW googlebot AS
SELECT h.*,
  CASE WHEN h.uri LIKE '%?%' THEN 'parameter'
       ELSE '/' || split_part(h.path, '/', 2) END AS section,
  (h.status // 100)::VARCHAR || 'xx' AS status_class
FROM hits h JOIN ip_verdicts v ON v.ip = h.ip AND v.verdict IN ('verified', 'in-range')
WHERE h.ua ILIKE '%googlebot%';

-- 3. Crawl share by section and status.
COPY (
  SELECT section, status_class, count(*) AS hits,
         round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS share_pct
  FROM googlebot GROUP BY ALL ORDER BY hits DESC
) TO 'crawl-share.csv' (HEADER);

-- 4. Sitemap URLs with their verified hits and last crawl (0 hits = never crawled).
COPY (
  SELECT s.url, max(g.ts) AS last_crawled, count(g.path) AS hits
  FROM read_csv('sitemap-urls.txt', header = false, columns = {'url': 'VARCHAR'}) s
  LEFT JOIN googlebot g ON g.path = regexp_replace(s.url, '^https?://[^/]+', '')
  GROUP BY s.url ORDER BY hits, s.url
) TO 'sitemap-coverage.csv' (HEADER);

-- 5. Top wasted URLs: parameters, redirects and errors, most-hit first.
COPY (
  SELECT uri, status, count(*) AS hits
  FROM googlebot
  WHERE uri LIKE '%?%' OR status >= 300
  GROUP BY ALL ORDER BY hits DESC LIMIT 200
) TO 'crawl-waste-top.csv' (HEADER);
```

Adapt the `section` expression to the site: the first path segment works for `/blog/`, `/products/`; a site with locale prefixes (`/en-gb/products/`) needs the second segment. Repeat the view for Bingbot or an AI crawler by changing the user-agent filter and the verified IP list.

Get `sitemap-urls.txt` with the commands in `1-reach-indexation/references/robots-and-sitemaps.md`, or:

```bash
curl -s https://example.com/sitemap.xml | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' > sitemap-urls.txt
```
```powershell
([xml](Invoke-WebRequest https://example.com/sitemap.xml -UseBasicParsing).Content).urlset.url.loc |
  Set-Content -Encoding ascii sitemap-urls.txt
```

---

## 2. Verify the crawler is real (never trust the user-agent)

A user-agent string saying `Googlebot` proves nothing: spoofing is trivial and common. Before attributing any behaviour to a search engine, use one of two methods.

### Reverse DNS plus forward confirmation
Google's documented steps (verified 2026-10): run a reverse DNS lookup on the IP with `host`, check that the name is in `googlebot.com`, `google.com` or `googleusercontent.com`, run a forward lookup on that name, and check it returns the original IP. The suffix also tells you the category:

| Name pattern | Google category |
|---|---|
| `crawl-*.googlebot.com`, `geo-crawl-*.geo.googlebot.com` | Common crawlers (Googlebot and others that obey robots.txt) |
| `rate-limited-proxy-*.google.com` | Special-case crawlers |
| `*.gae.googleusercontent.com`, `google-proxy-*.google.com` | User-triggered fetchers |

Bing documents the same two-step check with names ending in `search.msn.com`, and asks you to cache verified IPs rather than look up every request (verified 2026-10).

```bash
# Bash (needs the host command: bind-utils or dnsutils)
cut -d, -f1 googlebot-claims.csv | sort -u > ips.txt
while read -r ip; do
  name=$(host "$ip" | awk '/domain name pointer/ {print $NF}' | sed 's/\.$//' | head -n1)
  case "$name" in
    *.googlebot.com|*.google.com|*.googleusercontent.com)
      if host "$name" | awk -v ip="$ip" '$NF==ip {f=1} END {exit !f}'; then
        echo "$ip,verified,$name"; else echo "$ip,forward-mismatch,$name"; fi ;;
    *) echo "$ip,unverified,${name:-none}" ;;
  esac
done < ips.txt > ip-verdicts.csv
```
```powershell
# PowerShell (Windows): Resolve-DnsName ships with Windows
Get-Content ips.txt | ForEach-Object {
  $ip = $_
  $ptr = (Resolve-DnsName -Name $ip -Type PTR -ErrorAction SilentlyContinue | Select-Object -First 1).NameHost
  $verdict = 'unverified'
  if ($ptr -and ($ptr -match '\.(googlebot|google|googleusercontent)\.com$')) {
    $fwd = (Resolve-DnsName -Name $ptr -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress }).IPAddress
    if ($fwd -contains $ip) { $verdict = 'verified' } else { $verdict = 'forward-mismatch' }
  }
  "$ip,$verdict,$ptr"
} | Set-Content -Encoding ascii ip-verdicts.csv
```

For Bingbot, change the suffix check to `search.msn.com`. Write the file as ASCII: a UTF-8 byte-order mark on the first line would stop that IP matching later. IPv6 addresses can be written in more than one form; if a forward lookup "mismatches" on IPv6, compare the expanded forms before calling it a spoofer.

### Published IP ranges (faster at scale)
Matching against published lists avoids thousands of DNS lookups. Lists verified 2026-10:
- Google, one JSON file per category, linked from Google's "Verifying Googlebot and other Google crawlers" page: `https://developers.google.com/static/crawling/ipranges/common-crawlers.json`, `special-crawlers.json`, `user-triggered-fetchers.json`, `user-triggered-fetchers-google.json` and `user-triggered-agents.json` in the same folder.
- Bing: `https://www.bing.com/toolbox/bingbot.json`.
- OpenAI: `https://openai.com/searchbot.json` (OAI-SearchBot), `https://openai.com/gptbot.json` (GPTBot), `https://openai.com/chatgpt-user.json` (ChatGPT-User), `https://openai.com/adsbot.json` (OAI-AdsBot).
- Other AI crawlers: check each operator's own documentation; do not trust third-party lists.

The files change, so download them at the start of each analysis and note the date.

```bash
curl -s https://developers.google.com/static/crawling/ipranges/common-crawlers.json -o google-common.json
curl -s https://www.bing.com/toolbox/bingbot.json -o bingbot.json
python match_ranges.py ips.txt google-common.json bingbot.json > ip-verdicts.csv
```
```powershell
Invoke-WebRequest https://developers.google.com/static/crawling/ipranges/common-crawlers.json -OutFile google-common.json -UseBasicParsing
Invoke-WebRequest https://www.bing.com/toolbox/bingbot.json -OutFile bingbot.json -UseBasicParsing
python match_ranges.py ips.txt google-common.json bingbot.json > ip-verdicts.csv
```

```python
# match_ranges.py: usage python match_ranges.py ips.txt ranges1.json [ranges2.json ...]
# Prints ip,in-range|not-in-range,source-file for each IP. The JSON files use
# {"prefixes": [{"ipv4Prefix": ...} or {"ipv6Prefix": ...}]}.
import ipaddress, json, sys

nets = []
for path in sys.argv[2:]:
    with open(path, encoding="utf-8-sig") as f:
        for p in json.load(f)["prefixes"]:
            cidr = p.get("ipv4Prefix") or p.get("ipv6Prefix")
            nets.append((ipaddress.ip_network(cidr), path))

with open(sys.argv[1], encoding="utf-8-sig") as f:
    for line in f:
        ip = line.strip()
        if not ip:
            continue
        addr = ipaddress.ip_address(ip)
        hit = next((src for net, src in nets if addr.version == net.version and addr in net), "")
        print(f"{ip},{'in-range' if hit else 'not-in-range'},{hit}")
```

Some CDNs also label verified bots (Cloudflare's `VerifiedBotCategory` field). Use that as a cross-check, not a replacement, unless the user accepts the CDN's verification.

### Bucket the traffic
Bucket every hit into: **verified search crawlers**, **verified AI crawlers**, **other bots**, **spoofers** (claims a crawler, fails verification) and **humans**. Only reason about SEO from the verified-crawler buckets. A large spoofer bucket is a security note for the user, not an SEO finding.

## Privacy: logs are sensitive
Access logs contain IPs and can contain PII. Analyse locally, keep **conclusions not raw logs**, never paste raw logs into a chat or commit them (add log paths to `.gitignore`). Respect that this is the user's data. The `ip-verdicts.csv` file holds only crawler IPs, but keep it out of the repo too.

---

## 3. What to extract

From the verified-crawler requests over a representative window:
- **Per-URL crawl frequency** — how often each URL/section is fetched.
- **Coverage gap:** sitemap/key URLs with **zero or near-zero** crawler hits — important pages going undiscovered.
- **Status distribution to crawlers** — `200` vs `3xx` vs `4xx`/`5xx`; spikes of errors or redirects waste budget and signal problems.
- **Junk magnets** — URL patterns soaking up hits: `?`-parameter and faceted URLs, session IDs, calendar/filter "infinite spaces", duplicate variants, redirect chains.
- **Importance vs frequency mismatch** — are trivial URLs crawled more than money pages?
- **Crawler mix over time** — classic vs AI crawlers, and which sections each favours (feeds the Cite rung's AI-crawler decisions).

## 4. No logs: the Crawl Stats fallback

Search Console's Crawl Stats report is at **Settings > Crawl stats**, and only for root-level properties (a Domain property, or a URL-prefix property at the root). It covers the last 90 days and shows Googlebot requests by response code, file type, purpose (discovery or refresh) and Googlebot type, plus host status for robots.txt fetching, DNS resolution and server connectivity (verified 2026-10).

Use it to answer the same questions more coarsely:
- **Status waste:** the share of requests by response. A large `301` or `404` share points at links and sitemaps to fix.
- **Host problems:** any host-status warning for robots.txt, DNS or server connectivity comes before any other crawl work.
- **Discovery against refresh:** a site publishing many new pages but showing mostly refresh crawls may have a discovery problem (Connect).
- **Example URLs:** each breakdown lists sample URLs; look for parameter and filter patterns.

Pair it with the Page indexing report filtered to a sitemap: many submitted URLs in "Discovered - currently not indexed" is the coverage-gap signal you would otherwise get from logs (verified 2026-10). Record the figures with the date as the baseline, because the report only keeps 90 days.

Neither report is in the Search Console API. Read them through a tool whose description covers them, or from the user's export or screenshot. What the API does give, per URL, is URL Inspection's `lastCrawlTime` and `coverageState`, which can stand in for "when was this key page last crawled" on a sample of URLs. Use the recipe in `seo-orchestrator/references/data/search-console.md` (URL Inspection) and the sampling method in `seo-search-data/references/indexing-triage.md`; do not write separate API code here. Bing's `GetCrawlStats` and `GetCrawlIssues` are in `data/bing-webmaster.md`.

---

## 5. Crawl-budget waste patterns → fixes

| Pattern in the logs | Fix (owned by) |
|---|---|
| Crawlers hammering faceted/parameter URLs | Stop exposing low-value combinations as crawlable links; block the pattern in `robots.txt` once any indexed copies have dropped out; canonicalise near-duplicates (Reach + Connect; ecommerce profile) |
| Many redirect hops to crawlers | Collapse to single-hop `301`/`308`, and update internal links to the final URL (`seo-migrations`, Connect) |
| Repeated `404`/soft-404 fetches | Return correct `404`/`410`; fix broken internal links (Reach + Connect) |
| `noindex` URLs still crawled heavily | Reduce links to them; consider robots disallow once de-indexed. `noindex` does not save crawl budget |
| Important pages rarely/never crawled | Improve internal links + crawl depth + sitemap inclusion (Connect) |
| Infinite spaces (calendars, filters) | Block the pattern in robots; stop generating links into the trap |
| `5xx`, `429` or slow responses to crawlers | Fix capacity or errors: Google crawls less when a site slows down or returns `5xx` or `429` (crawl budget guide) |

Google's crawl budget guide (verified 2026-10) is the source for two of these: eliminate soft 404s, and use `robots.txt` rather than `noindex` for pages you do not want crawled, because Google still requests a `noindex` page before dropping it.

> Crawl budget mainly matters at **scale** (large e-commerce, big publishers, huge programmatic sets). For a small site, "crawl budget" is rarely the bottleneck — say so rather than over-engineering.

Before shipping any `Disallow`, test the pattern against `sitemap-urls.txt` so it blocks no key URL:

```bash
grep -E '\?(.*&)?size=' sitemap-urls.txt | head   # should print nothing
```
```powershell
Select-String -Path sitemap-urls.txt -Pattern '\?(.*&)?size=' | Select-Object -First 10   # should print nothing
```

---

## 6. Re-sample and compare (the Verify step)

After fixes ship and crawlers have had time to react, pull a new window of the same length, run the identical pipeline into `crawl-share-after.csv`, keep the original as `crawl-share-before.csv`, and compare:

```sql
COPY (
  SELECT section, status_class,
         coalesce(b.share_pct, 0) AS before_pct,
         coalesce(a.share_pct, 0) AS after_pct,
         round(coalesce(a.share_pct, 0) - coalesce(b.share_pct, 0), 1) AS delta_pts
  FROM read_csv('crawl-share-after.csv', header = true) a
  FULL OUTER JOIN read_csv('crawl-share-before.csv', header = true) b USING (section, status_class)
  ORDER BY abs(delta_pts) DESC
) TO 'crawl-share-delta.csv' (HEADER);
```

Re-run the coverage query too, and count key URLs that moved from 0 hits to at least 1. Shares can move for reasons other than your fix (a site-wide recrawl, a seasonal change, a deploy), so report what changed and what else happened in the window. Do not claim causation from one comparison.

---

## 7. How findings map to the rungs
Log analysis **diagnoses**; the fixes live in the rungs/specialists:
- Waste reduction & indexation control → **Reach** + **Connect** (+ ecommerce/programmatic for faceted/at-scale).
- Redirect/error cleanup → **seo-migrations**.
- Under-crawled key pages → **Connect** (linking/depth) + sitemap.
- AI-crawler access decisions → **cite-aeo-geo**.
- Prioritisation → weight by real clicks where a search-performance capability exists (a tool, the API with the user's credentials, or an export; recipes in `seo-orchestrator/references/data/search-console.md`, owned by **seo-search-data**).
- Spoofers and `200` responses on paths the site never made → `seo-orchestrator/references/security-and-spam.md`.

Record each finding with the shared schema (`## Specialist findings` in `seo-orchestrator/references/audit-report-and-state.md`), with `evidence` quoting the window, the verified-hit counts and the share.

## The honest boundary
This is a **point-in-time** analysis of the logs provided. Crawl behaviour shifts continuously, so **ongoing crawl monitoring is live/continuous work** (and any rankings effect of fixes is live data) — outside a one-off build-time read. Record the conclusions and recommended fixes in `.seo/`; re-analyse periodically (or automate a log pull) if crawl budget is an ongoing concern.
