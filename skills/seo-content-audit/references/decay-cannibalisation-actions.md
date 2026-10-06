# Decay, cannibalisation, and the action decision

Read this to build the inventory, spot the two most common content problems, and assign each page a single clear action. This is the decision layer of the content audit. Every threshold below is a default chosen by judgement, not a number Google publishes; change it when the site's size or traffic makes it wrong, and say that you did.

---

## The inventory CSV

One row per page, exactly these columns, in this order:

```csv
url,template,topic,intent,verdict,action,basis,clicks_12m,impressions_12m,change_pct,inbound_links,evidence
```

| Column | What goes in it |
|---|---|
| `url` | The canonical, served URL. Gap rows use the proposed path, prefixed `new:` |
| `template` | The route pattern, e.g. `/blog/[slug]` |
| `topic` | The cluster the page belongs to, in a few words |
| `intent` | `informational`, `commercial`, `transactional` or `navigational` |
| `verdict` | `strong`, `adequate`, `weak`, `gap`, or `unsampled` on large sites |
| `action` | `keep`, `improve`, `refresh`, `consolidate`, `prune` or `create` |
| `basis` | `gsc+content`, `gsc`, `content`, or `sampled-estimate` |
| `clicks_12m`, `impressions_12m` | Search Console totals for the last 12 full months; empty without GSC |
| `change_pct` | Clicks, last 3 full months against the same 3 months a year earlier; empty if the earlier window had under 10 clicks |
| `inbound_links` | Distinct internal pages linking to this URL, from the crawl |
| `evidence` | One line a person can check: the numbers or the observation that drove the action |

Keep `evidence` short and checkable: "0 clicks/12m; 0 inbound; 84 words; superseded by /guides/boiler-pressure" beats "low quality".

---

## Collecting the facts

### Page facts from the served HTML
`page_facts.py` fetches each URL as a crawler first sees it (no JavaScript runs) and records status, title, h1, a main-content word count and inbound internal links. It uses only the Python standard library.

```python
# Usage: python page_facts.py urls.txt > page-facts.csv
# Fetches each URL's served HTML (no JavaScript runs) and records status, title, h1,
# a main-content word count (inside <main>, else the body minus nav, header and
# footer) and the internal links each page makes, then counts inbound internal
# links per URL from the pages in the list. One request per second by default.
import csv, sys, time, urllib.error, urllib.parse, urllib.request
from collections import defaultdict
from html.parser import HTMLParser

DELAY = 1.0
UA = "Mozilla/5.0 (compatible; content-audit; +https://example.com/your-contact)"

class Facts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = self.h1 = ""
        self.links, self.main_words, self.body_words = set(), 0, 0
        self._in = []
    def handle_starttag(self, tag, attrs):
        self._in.append(tag)
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.add(href)
    def handle_endtag(self, tag):
        while self._in and self._in.pop() != tag:
            pass
    def handle_data(self, data):
        if "title" in self._in and not self.title:
            self.title = data.strip()
        if "h1" in self._in:
            self.h1 = (self.h1 + " " + data).strip()
        if {"head", "script", "style", "nav", "header", "footer"} & set(self._in):
            return
        n = len(data.split())
        self.body_words += n
        if "main" in self._in:
            self.main_words += n

def norm(base, href):
    u = urllib.parse.urljoin(base, href)
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))

urls = [u.strip() for u in open(sys.argv[1], encoding="utf-8-sig") if u.strip()]
host = urllib.parse.urlsplit(urls[0]).netloc
inbound, rows = defaultdict(set), []
for url in urls:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            status, final, body = r.status, r.geturl(), r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        status, final, body = e.code, url, ""
    except (urllib.error.URLError, TimeoutError) as e:
        status, final, body = "fetch-error", url, ""
    f = Facts(); f.feed(body)
    for href in f.links:
        target = norm(final, href)
        if urllib.parse.urlsplit(target).netloc == host and target != url:
            inbound[target].add(url)
    rows.append([url, status, final, f.title, f.h1, f.main_words or f.body_words])
    time.sleep(DELAY)

w = csv.writer(sys.stdout)
w.writerow(["url", "status", "final_url", "title", "h1", "main_words", "inbound_links"])
for url, status, final, title, h1, words in rows:
    w.writerow([url, status, final, title, h1, words, len(inbound.get(url, ()))])
```

Limits to state in the report:
- **Inbound links only count pages in the list.** Feed it the full URL list even when you sample for judgement, or use a crawler export (for example a "unique inlinks" column) instead.
- **Sitewide navigation inflates counts.** A page linked only from the footer still shows hundreds of inbound links. Compare counts within a template, and treat "linked only from navigation" as weak linking.
- **Word count is a hint, not a verdict.** A 150-word answer can be complete; a 3,000-word post can be padding. Use it to find pages to read, never to decide alone.
- **Served HTML only.** If content is client-rendered, the counts are wrong. Fix Reach first.

### Search Console pulls
Get the data through whatever capability exists, in the order set out in `seo-orchestrator/references/live-data-integrations.md`: a tool in the environment, then the Search Console API with the user's own credentials, then an export the user points to, then nothing. The API recipe (auth with the read-only scope, `siteUrl` formats, paging past 25,000 rows, data lag, quotas and pitfalls, in bash, PowerShell, Python and Node) lives in `seo-orchestrator/references/data/search-console.md`. Do not copy it here; `seo-search-data` owns it.

What this audit needs is three request bodies. With a tool, ask it for the same dimensions and windows:

```json
{"startDate": "2025-10-01", "endDate": "2026-09-30", "dimensions": ["page"], "type": "web", "rowLimit": 25000, "startRow": 0}
{"startDate": "2026-07-01", "endDate": "2026-09-30", "dimensions": ["page"], "type": "web", "rowLimit": 25000, "startRow": 0}
{"startDate": "2026-07-03", "endDate": "2026-09-30", "dimensions": ["date", "query", "page"], "type": "web", "rowLimit": 25000, "startRow": 0}
```

The first gives `clicks_12m` and `impressions_12m` (the last 12 full months before the audit). The second, repeated with the same months a year earlier, gives `change_pct`. The third is the 90-day cannibalisation export, saved as `gsc-daily.csv` with columns `date,query,page,clicks,impressions,position`. Page each one with `startRow` until a response returns fewer rows than `rowLimit`. Save the page-level results as `gsc-pages-12m.csv` (`page,clicks,impressions`) and join them to `page-facts.csv` on URL to fill the inventory. On a large site the API returns only the top rows per day, so query the cannibalisation export a day or a section at a time (the recipe's Paging and completeness). Keep any token in the environment, never in a file or in `.seo/`.

- **`change_pct`:** pull clicks per page for the last 3 full months and for the same 3 months a year earlier (Search Console keeps 16 months, so both windows exist). Comparing the same months removes most seasonality. For pages younger than 15 months, compare the last 3 months with the 3 before and note it in `evidence`.
- **Cannibalisation:** pull `"dimensions":["date","query","page"]` for the last 90 days. This export is large; page through it. Queries Google anonymises for privacy are omitted from query rows, and only the most important rows are kept, so totals here will be lower than the page totals (verified 2026-10). That is expected.

---

## The decision rules

Evaluate in this order; the first rule that matches sets the action. Pages with a business purpose from `.seo/context.md` (pricing, contact, legal, core service pages) skip rule 2.

1. **Consolidate** when the page is in a confirmed cannibalisation cluster (see below) and is not the cluster's strongest page. The strongest page is the one with the most clicks; if clicks are close, the one with more inbound links and the better content. The survivor goes on to rules 3 to 5.
2. **Prune candidate** when all of these hold: `clicks_12m` is 0; `inbound_links` is 0 (or only sitewide navigation); no external links are known (from a backlink tool if connected, otherwise say "unknown"); the verdict is `weak`; and the page has no business purpose. The status is always `needs-human`. Without GSC, this rule cannot fire: "no clicks" is unknown, not zero.
3. **Refresh** when `change_pct` is -30 or lower and the earlier window was above the site's median clicks per page, or when the page states facts that are now outdated on a time-sensitive topic. The baseline condition stops a fall from 4 clicks to 2 from looking like a crisis.
4. **Improve** when the verdict is `weak` or `adequate`, or the intent is mismatched, and the page has something worth keeping: impressions above the site median, inbound links, or a business purpose. High impressions with a low click-through rate or an average position between 5 and 20 is the classic improve signal.
5. **Keep** when the verdict is `adequate` or `strong`, the intent matches, and traffic is stable or growing.
6. **Create** is not a rule over existing pages. Add a gap row (`url` = `new:/proposed-path`, `verdict` = `gap`) for each real topic with demand and no page.

### Scaling the thresholds
The defaults suit a site with meaningful search traffic. Adjust them out loud:
- **Low-traffic sites** (most pages under 10 clicks a year): absolute click rules are noise. Use "bottom traffic decile" instead of "0 clicks", rely more on verdict, intent and purpose, and expect more `improve` than `prune`.
- **Large sites** (tens of thousands of pages): "0 clicks in 12 months" may hold for thousands of pages. Treat them as a template-level question ("should `/tag/` pages be indexed at all?") rather than thousands of page decisions.
- **Seasonal or news content:** a 30% fall may be the season. Year-on-year windows handle most of this; read the page before calling it decay.

---

## Stratified sampling (sites over 1,000 pages)

Data-driven columns are cheap, so fill them for every page. Judgement columns (`verdict`, `intent`) cost reading time, so sample. Stratify by template and by traffic decile, with zero-click pages as stratum 0 because they tie and would distort the deciles.

```sql
-- DuckDB: duckdb audit.duckdb < sample.sql
COPY (
  WITH pages AS (
    SELECT *,
      CASE WHEN clicks_12m = 0 THEN 0
           ELSE ntile(10) OVER (PARTITION BY clicks_12m > 0 ORDER BY clicks_12m) END AS traffic_decile
    FROM read_csv('inventory.csv', header = true)
  ),
  ranked AS (
    SELECT *, row_number() OVER (PARTITION BY template, traffic_decile ORDER BY random()) AS rn,
              count(*) OVER (PARTITION BY template, traffic_decile) AS stratum_size
    FROM pages
  )
  SELECT url, template, traffic_decile, stratum_size, clicks_12m
  FROM ranked
  WHERE rn <= greatest(5, ceil(0.05 * stratum_size))
  ORDER BY template, traffic_decile
) TO 'audit-sample.csv' (HEADER);
```

Five pages or 5% per stratum, whichever is larger, is a starting point (judgement). Without GSC, stratify by template alone. When most of a stratum's sample shares a verdict, apply it to the stratum with `basis` = `sampled-estimate`, and read every page before any prune or consolidate action is confirmed.

---

## Content decay

**Decay** is content that used to perform and is slowly losing traffic/rankings — usually because it's gone stale, competitors improved, or the SERP/intent shifted. It's often a site's biggest, cheapest opportunity: refreshing a decaying page that already has authority beats writing a new one.

- **With Search Console:** use `change_pct` and rule 3 above.
- **Without GSC:** infer from outdated content on time-sensitive topics (old dates, superseded facts, "in 2022…"), and flag that you're inferring.
- **Action:** **Refresh** — genuinely update the content (new information, current examples, re-verify claims), then update `dateModified` truthfully. Never just bump the date without updating the substance.

---

## Keyword cannibalisation

**Cannibalisation** is multiple pages targeting the same intent/query, so they compete with each other — splitting signals and confusing engines about which to rank. Common on content sites that published several overlapping posts over the years.

### With Search Console: query and page pairs
A query is a candidate when two or more URLs each take at least 10% of its impressions at an average position of 20 or better. It is a strong candidate when the best-placed URL keeps changing day to day. Load the 90-day `date,query,page,clicks,impressions,position` export as `gsc-daily.csv`:

```sql
-- DuckDB: duckdb audit.duckdb < cannibalisation.sql
CREATE TABLE qp AS
SELECT query, page, sum(clicks) AS clicks, sum(impressions) AS impressions,
       sum(position * impressions) / sum(impressions) AS avg_position
FROM read_csv('gsc-daily.csv', header = true) GROUP BY query, page;

CREATE TABLE shared AS
SELECT *, impressions / sum(impressions) OVER (PARTITION BY query) AS imp_share FROM qp;

CREATE TABLE candidates AS
SELECT query FROM shared
WHERE imp_share >= 0.10 AND avg_position <= 20
GROUP BY query HAVING count(*) >= 2;

-- How often the best-placed URL for the query changes from one day to the next
CREATE TABLE swaps AS
WITH daily AS (
  SELECT date, query, arg_min(page, position) AS top_page
  FROM read_csv('gsc-daily.csv', header = true)
  WHERE query IN (SELECT query FROM candidates)
  GROUP BY date, query
)
SELECT query, count(*) FILTER (WHERE top_page <> prev) AS swaps, count(*) AS days
FROM (SELECT *, lag(top_page) OVER (PARTITION BY query ORDER BY date) AS prev FROM daily)
GROUP BY query;

COPY (
  SELECT s.query, s.page, s.clicks, s.impressions, round(s.avg_position, 1) AS avg_position,
         round(100 * s.imp_share, 1) AS imp_share_pct, w.swaps, w.days
  FROM shared s JOIN swaps w USING (query)
  WHERE s.imp_share >= 0.10
  ORDER BY w.swaps DESC, s.query, s.impressions DESC
) TO 'cannibalisation.csv' (HEADER);
```

The 10% share, position 20 and "several swaps" cut-offs are judgement. Weight by the query's value: a split on a query with 20 impressions is not worth a merge. Branded and navigational queries often show several URLs legitimately (home, about, contact); exclude them.

### Without Search Console: title and h1 overlap
Flag pairs whose titles or h1s share most of their meaningful words, then read both pages. Feed it `url,title,h1` from `page-facts.csv`.

```python
# Usage: python title_overlap.py titles.csv > title-overlap.csv
# titles.csv columns: url,title,h1 (from your crawl). Flags pairs whose title or h1
# share most of their meaningful words. A flag is a lead for a person to read, not a verdict.
import csv, itertools, re, sys

THRESHOLD = 0.75  # judgement: overlap of the shorter title's words
STOP = set("a an and are as at be by for from how in is it of on or the to vs what why with your you".split())

def stem(w):
    for suffix in ("ing", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 4:
            return w[: -len(suffix)]
    return w

def tokens(s):
    s = re.sub(r"\s[|\-:]\s[^|\-:]+$", "", s or "")   # drop a trailing " | Brand"
    return {stem(w) for w in re.findall(r"\w+", s.lower()) if w not in STOP and len(w) > 2}

def overlap(a, b):
    return len(a & b) / min(len(a), len(b)) if a and b else 0.0

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
print("url_a,url_b,title_overlap,h1_overlap")
for a, b in itertools.combinations(rows, 2):
    t = overlap(tokens(a["title"]), tokens(b["title"]))
    h = overlap(tokens(a["h1"]), tokens(b["h1"]))
    if max(t, h) >= THRESHOLD:
        print(f'{a["url"]},{b["url"]},{t:.2f},{h:.2f}')
```

It compares every pair, so on large sites run it within a topic or template. It misses overlaps phrased differently ("bleed a radiator" and "release trapped air from heating"), so also read the titles within each topic cluster.

### Confirm, then act
A flagged pair is cannibalisation only if a person reading both agrees they serve the **same intent**. Then:
- **Consolidate** (usual): merge the useful substance into the strongest page and `301` the others to it. Hand the redirect map to `seo-migrations` so equity is preserved.
- **Differentiate** (sometimes): if the intents are genuinely distinct but blurred, sharpen each page's title, h1 and content so each serves its own intent, and link between them.
- Don't "fix" cannibalisation by `noindex`-ing one of two genuinely useful, distinct pages — only consolidate true overlaps.

---

## The action decision (one per page)

Assign exactly one:

| Action | When | Then |
|---|---|---|
| **Keep** | Performs well, good quality, right intent | Leave it; maybe add internal links to it |
| **Improve** | Good topic/bones, but thin, unclear, weak intent match, or weak E-E-A-T | Hand to `seo-content-editing` (edit real content; brief the human for missing substance/E-E-A-T) |
| **Refresh** | Decaying or outdated, but fundamentally worth keeping | Genuinely update content + truthful `dateModified` |
| **Consolidate** | Cannibalising / overlapping thin pages | Merge into one strong page; `301` the rest (`seo-migrations`) |
| **Prune** | Genuinely valueless, no traffic, no purpose | Remove or `noindex` — carefully; `301` if it has any equity (`seo-migrations`) |
| **Create** | A real, in-demand topic gap with no page | Write a **content brief** for a human; this skill briefs, it does not auto-generate articles |

### Choosing a prune disposal
- **Has any external links or meaningful inbound internal links:** `301` to the closest relevant page. Google's site-move guidance warns that redirecting many old URLs to one irrelevant destination, such as the home page, might be treated as a soft 404 (verified 2026-10), so pick a real match or use `404`/`410`.
- **No links, no traffic, no relevant target:** `404` or `410`, and remove internal links to it.
- **Useful to users but not to searchers** (for example a thin tag page people browse): `noindex`, keep it, and decide separately whether the template should be indexed at all.

### Prioritise the actions
- **With GSC:** weight by real traffic and opportunity — refresh the high-traffic decayers and improve the high-impression/low-click pages first.
- **Without:** weight by topical importance, intent value, and effort (quick wins first).
- Record each page's action and basis in the CSV, and the grouped findings in the shared schema (`## Specialist findings` in `seo-orchestrator/references/audit-report-and-state.md`), so the lifecycle tracks the content backlog alongside the technical one.

---

## The white-hat lines (same as ever)
- **Create = brief, not generate.** The content audit identifies gaps and writes briefs for a human (or a human-supervised process). It does not silently auto-generate articles to fill the index — mass-generated thin content is exactly what engines now discount.
- **Prune carefully.** Don't delete pages with traffic or links without confirming and redirecting. On an existing site, treat removals as high-risk (see `seo-orchestrator/references/existing-site-safety.md`).
- **Refresh honestly.** Update the content, then the date — never the date alone.
- **Don't fabricate the missing substance, sources, or E-E-A-T** — flag those as human tasks.
- **Never present a threshold as a rule from Google.** They are this pack's defaults; say so.
