# The programmatic quality bar

Read this to keep programmatic SEO on the right side of the line. The whole discipline hinges on one judgement: **does each page earn its place?** This file is how you decide, and how you control scale so it helps rather than harms.

---

## Google's spam policies that apply

Source: Google Search Central, "Spam policies for Google web search" (`https://developers.google.com/search/docs/essentials/spam-policies`), verified 2026-10; the page was last updated 2026-08-28. Re-read it before any large launch, because these policies change.

| Policy | What Google describes | How a programmatic plan trips it |
|---|---|---|
| **Scaled content abuse** | Many pages generated for the primary purpose of manipulating rankings and not helping users, whatever the method | Thousands of pages from a thin dataset, padded with model-written filler or stitched snippets |
| **Doorway abuse** | Sites or pages created to rank for specific, similar queries that lead users to intermediate pages less useful than the final destination | "{service} in {town}" for towns the business does not serve, or pages that differ only by the swapped term |
| **Site reputation abuse** | Third-party content on a host site mainly to exploit the host's ranking signals rather than add integrated value | Letting a partner publish generated coupon, review or comparison sets under your strong domain |
| **Expired domain abuse** | An expired domain bought and repurposed mainly to manipulate rankings with low-value content | Buying an aged domain to launch a generated page set on its old reputation |

Two other policies on the same page also come up: **thin affiliation** (affiliate pages that add nothing beyond the merchant's own content) and **scraping** (republishing others' content without adding value). If a plan resembles any row above, stop and say which policy and why. The fact of templating is never the problem; the absence of genuine per-page value is.

---

## Doorway pages vs legitimate pSEO

| Legitimate programmatic SEO | Doorway / thin spam (refuse) |
|---|---|
| Each page has real, distinct data a user wants (a real product's real specs; a city's real data) | Pages differ only by a swapped keyword/city; same content otherwise |
| Built from a substantive dataset | "Built" by spinning a template over a word list |
| Solves a real search intent with real demand | Targets query permutations no one meaningfully searches |
| Page count = entities with enough real data | Page count = however many keywords you want to rank for |
| Unique value per page; consolidates where thin | Mass-published regardless of substance |

Examples of the good kind: a weather/tool site with genuinely different data per location; an e-commerce catalogue with real, distinct products; honest, data-backed "X vs Y" comparisons. Examples of the bad kind: "{service} in {town}" pages that are one paragraph with the town name swapped, across 5,000 towns.

---

## The quality gate (apply per page before publishing)

Every threshold below is a default chosen by judgement. Google publishes no field count or similarity score. Set the numbers per dataset, write them into `.seo/context.md` or the PR description, and report them.

### Gate 1: required and distinct data fields
A field adds substance to a page only if it is populated and its value is specific to that entity. A column where most rows share one value ("Region: North") is template text. `field_gate.py` counts, per row, the populated fields whose value is shared by no more than 20% of rows, and checks the required fields.

```python
# Usage: python field_gate.py dataset.csv > gate.csv
# Counts, per row, the populated fields whose value is specific enough to make the
# page differ from its siblings, and applies the gate. All thresholds are judgement.
import csv, sys
from collections import Counter

KEY = "slug"                                   # the column that becomes the URL
IGNORE = {"slug", "name", "release_wave"}      # identity and control columns
REQUIRED = {"plumber_count", "median_callout_gbp", "postcodes_covered"}
MIN_DISTINCT_FIELDS = 5                        # judgement: set per dataset
MAX_SHARED = 0.20                              # a value on >20% of rows is template, not substance
EMPTY = {"", "n/a", "na", "null", "none", "-", "tbc"}

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
fields = [f for f in rows[0] if f not in IGNORE]
freq = {f: Counter(r[f].strip().lower() for r in rows) for f in fields}

out = csv.writer(sys.stdout)
out.writerow([KEY, "populated", "distinct_fields", "missing_required", "gate"])
for r in rows:
    populated = [f for f in fields if r[f].strip().lower() not in EMPTY]
    distinct = [f for f in populated
                if freq[f][r[f].strip().lower()] / len(rows) <= MAX_SHARED]
    missing = sorted(f for f in REQUIRED if f not in populated)
    ok = not missing and len(distinct) >= MIN_DISTINCT_FIELDS
    out.writerow([r[KEY], len(populated), len(distinct), " ".join(missing), "pass" if ok else "withhold"])
```

Adjust `KEY`, `IGNORE` and `REQUIRED` to the dataset. Limits to keep in mind:
- **Low-cardinality fields that matter** (a yes or no "emergency cover" flag) never count as distinct, even when they are useful. Count them in `REQUIRED` if they are core, not in the distinct total.
- **Long free-text fields** count as one field. A real 150-word local description written by someone who knows the place is worth more than five numbers; weigh that by reading, not by the script.
- **The script counts data, not quality.** A wrong value is still a value. Data accuracy is a provenance question for a person.

### Gate 2: near-duplicate text on the rendered page
Data can be distinct while the rendered pages still read the same, because the template's prose dominates. Measure on the served HTML: fetch the pages (`curl -s URL -o pages/slug.html`, or `Invoke-WebRequest URL -OutFile pages\slug.html -UseBasicParsing`) and compare them.

`near_dupes.py` takes the `<main>` text, masks the page's own h1 words and every digit (so pages that differ only by the swapped name or number are scored as the same template), builds 5-word shingles, and reports the Jaccard similarity of every pair.

```python
# Usage: python near_dupes.py pages/*.html > near-dupes.csv
# Compares the <main> text of every pair of pages using word 5-gram shingles.
# Words from each page's own <h1> and all digits are masked first, so pages that
# differ only by the swapped entity name or number score as the template they are.
import html, itertools, re, sys

K = 5            # shingle size in words
THRESHOLD = 0.6  # judgement, not a Google number: calibrate on pairs you have read

def words(fragment):
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.findall(r"\w+", text.lower())

def main_words(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    m = re.search(r"<main\b[^>]*>(.*?)</main>", raw, re.S | re.I)
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", raw, re.S | re.I)
    slot = set(words(h1.group(1))) if h1 else set()
    return ["<slot>" if w in slot else re.sub(r"\d", "#", w)
            for w in words(m.group(1) if m else raw)]

def shingles(ws):
    return {" ".join(ws[i:i + K]) for i in range(max(1, len(ws) - K + 1))}

docs = {p: shingles(main_words(p)) for p in sys.argv[1:]}
print("page_a,page_b,jaccard,flag")
for a, b in itertools.combinations(sorted(docs), 2):
    sa, sb = docs[a], docs[b]
    j = len(sa & sb) / len(sa | sb) if sa | sb else 1.0
    print(f"{a},{b},{j:.2f},{'near-duplicate' if j >= THRESHOLD else ''}")
```

Two short pages that differ only by a swapped town and postcode scored 0.75 with this script in testing; without masking the same pair scored 0.31, which is why the masking matters.

**Calibrating the threshold.** Start at 0.6. Read five pairs just above it and five just below. If pairs below it still read as the same page with a name swapped, lower it; if pairs above it are genuinely different pages with shared boilerplate, raise it or strip the boilerplate (shared FAQs, legal text) before comparing. Record the value you settle on.

**Scale.** Every pair is compared, so cost grows with the square of the page count: 200 pages is about 20,000 pairs and runs in seconds. For thousands of pages, compare a stratified sample of about 200 per template (rich, average and sparse rows), or use MinHash with locality-sensitive hashing (for example the `datasketch` Python library) to find candidate pairs first.

### Gate 3: honest schema
Every value in the JSON-LD appears in the visible content and comes from the dataset, never from a default. No `aggregateRating` without real reviews shown on the page (rung 3 rules).

### Gate 4: a person would choose it
Read three random passing pages. Would someone who searched for this entity be glad to land here rather than on the hub? If not, the measurable gates are set too low.

Pages below the bar are **withheld or consolidated**, not padded with fabricated text. Report how many passed vs were withheld — that honesty is part of doing it right.

---

## Generating and staging in Next.js (App Router)

Add a `gate` column (from `field_gate.py`) and a `release_wave` column to the dataset. The current wave lives in configuration, so releasing the next wave is a reviewed one-line change.

```ts
// lib/towns.ts
import rows from '@/data/towns.json'
type Town = { slug: string; gate: 'pass' | 'withhold'; release_wave: number; updated: string }

const CURRENT_WAVE = Number(process.env.PSEO_RELEASE_WAVE ?? 1)

export async function getReleasedTowns(): Promise<Town[]> {
  return (rows as Town[]).filter((t) => t.gate === 'pass' && t.release_wave <= CURRENT_WAVE)
}

export async function getTown(slug: string) {
  return (await getReleasedTowns()).find((t) => t.slug === slug)
}
```

Give each wave its own sitemap so the Page indexing report can be filtered to exactly that wave. With `generateSitemaps`, each id becomes `/plumbers/sitemap/[id].xml`; since Next.js 16 the `id` reaches the sitemap function as a promise resolving to a string (verified 2026-10).

```ts
// app/plumbers/sitemap.ts
import type { MetadataRoute } from 'next'
import { getReleasedTowns } from '@/lib/towns'

const BASE_URL = 'https://www.example.com'

export async function generateSitemaps() {
  const waves = new Set((await getReleasedTowns()).map((t) => t.release_wave))
  return [...waves].map((w) => ({ id: w }))
}

export default async function sitemap(props: { id: Promise<string> }): Promise<MetadataRoute.Sitemap> {
  const wave = Number(await props.id)
  return (await getReleasedTowns())
    .filter((t) => t.release_wave === wave)
    .map((t) => ({ url: `${BASE_URL}/plumbers/${t.slug}`, lastModified: t.updated }))
}
```

On Next.js 15 or earlier, the `id` is passed directly rather than as a promise; check the installed version. Submit each wave's sitemap in Search Console, or list it in a sitemap index referenced from `robots.txt`.

### Reading a wave
Filter the Page indexing report to the wave's sitemap (the report's sitemap filter, verified 2026-10) and record, with the date:
- the share indexed;
- "Crawled - currently not indexed": Google fetched the pages and chose not to index them, the clearest quality signal you will get;
- "Discovered - currently not indexed": not yet crawled, often a linking or crawl-capacity issue (check hubs and internal links);
- "Duplicate without user-selected canonical": Google sees the pages as copies of each other or of another page, so Gate 2 is too loose.

The go or no-go rule is judgement, agreed with the user before wave 1 ships, for example: release the next wave when most of the current wave is indexed after six weeks and some pages earn impressions; stop and revise when a large share sits in "Crawled - currently not indexed" or "Duplicate". Indexing takes time, so a quiet first fortnight is not a verdict.

---

## Indexation & crawl-budget control at scale

Thousands of pages can flood crawl budget and dilute quality signals. Decide deliberately (coordinate with Reach + Connect):
- **Index** the pages that clear the bar and serve real demand.
- **Don't generate** the low-value long tail and thin combinations at all; `noindex` only when a page must exist for users. Google's crawl budget guide notes that `noindex` pages are still fetched, so they do not save crawl.
- **Canonicalise** near-duplicate variants to the best version.
- **Don't generate faceted/parameter explosions** as crawlable URLs (the e-commerce faceted-nav problem applies — see the ecommerce profile).
- **Generate a sitemap** of the indexable set; **interlink** via hubs/categories so pages aren't orphaned.
- Roll out in **waves** (above) and watch indexation per wave, rather than dumping 10,000 pages at once. On a large set, `seo-log-analysis` shows whether crawlers actually reach the new pages.

---

## How it coordinates with the rest of the pack
- **Reach** — crawl-budget/indexation control; generated pages must be in the served HTML.
- **Read / content-audit** — the thinness and intent bar; content-audit's "consolidate/prune" applies if a generated set is already thin.
- **Understand** — honest schema per page from real data.
- **Connect** — hubs, internal linking, canonicals so the set is coherent, not an orphaned sprawl.
- **seo-log-analysis:** verified crawl coverage of the set on large launches.

Record gate results and wave decisions with the shared findings schema (`## Specialist findings` in `seo-orchestrator/references/audit-report-and-state.md`).

## The honest outcome
Sometimes the right recommendation is **"don't"** — or "generate 200 genuinely useful pages, not 20,000 thin ones." Saying that is the skill working correctly. Programmatic SEO is a force multiplier for *good* content and a fast way to get penalised with *thin* content; this skill only does the former.
