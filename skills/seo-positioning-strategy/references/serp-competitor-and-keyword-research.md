# SERP, competitor and keyword research

Read this when the positioning work needs evidence about the search landscape: who competes for a topic, what format wins, and how the audience's queries group together. It covers where that evidence may honestly come from, how to fetch competitor pages without being a nuisance, how to read search results without scraping them, the intent and format table that ties it together, and keyword clustering with and without demand data.

The rule behind every section: **each claim in the plan carries its basis.** Live data is cited with its source and date. Fetched pages are cited by URL. Anything else is labelled inference.

---

## Where evidence may come from

| Source | What it can tell you | What it cannot |
|---|---|---|
| `.seo/context.md` | The audience's vocabulary, named competitors, the topical territory, and what is out of scope. | Demand, or who actually ranks. |
| The site's own content and Search Console | Which queries already reach the site, with impressions, clicks and average position. These are footholds. | Demand for queries the site does not yet appear for. |
| Competitor pages, fetched directly | Format, depth, angle, headings, structured data, and what each page covers or leaves out. | Whether that page ranks, or for what. |
| A connected SERP or keyword provider (DataForSEO, Ahrefs, Semrush), on the user's own key | Who ranks for a query, the result types on the page, and the provider's volume estimate. | Exact demand. Volumes are modelled estimates; label them with the provider and date. |
| What the user saw and pasted in | A labelled observation of one results page, at one place and time. | A representative picture of the results. |

Setting up a provider and handling keys safely is covered in `seo-orchestrator/references/live-data-integrations.md`.

### Never scrape Google
Do not send automated queries to Google or parse its results pages with `curl`, a headless browser or a fetch tool. Google's spam policies define "machine-generated traffic" as sending automated queries to Google, including scraping results for rank-checking, and say it violates both the spam policies and the Google Terms of Service (verified 2026-10, [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies)). Treat other engines' results pages the same way (judgement). If no provider is connected, the plan goes ahead without SERP data and says so.

---

## Fetching competitor pages politely

Competitor URLs come from `.seo/context.md` (Competitors), from the user, or from a connected SERP provider. Without provider data you know who the business competes with, not who ranks; label them "named competitors".

The rules:
- **Read `robots.txt` first** and skip any path it disallows for your user agent.
- **Identify yourself honestly** with a user-agent string that names the purpose and a contact URL. Do not pose as Googlebot or a browser.
- **Go slowly and fetch little:** one request at a time, a pause of several seconds between them (judgement), and only the handful of pages that represent each competitor's offer on the topic. Save each page once and work from the saved copy.
- **Take nothing behind a login or a paywall**, collect no personal data, and never copy competitor wording into the plan or the site. You are studying shape and coverage, not lifting text.

```bash
UA="site-research/1.0 (+https://your-site.example/contact)"
curl -s -A "$UA" https://competitor.example/robots.txt
i=0
while read -r u; do
  i=$((i+1))
  curl -sL -A "$UA" -o "competitor-$i.html" "$u"
  sleep 5
done < urls.txt
# headings and title
grep -oiE '<(title|h1|h2|h3)[^>]*>[^<]*' competitor-1.html | sed -E 's/<[^>]*>//'
# structured data types
grep -oE '"@type" *: *"[^"]*"' competitor-1.html | sort | uniq -c
```
```powershell
$ua = "site-research/1.0 (+https://your-site.example/contact)"
(Invoke-WebRequest "https://competitor.example/robots.txt" -UserAgent $ua -UseBasicParsing).Content
$i = 0
Get-Content urls.txt | ForEach-Object {
  $i++
  Invoke-WebRequest $_ -UserAgent $ua -UseBasicParsing -OutFile "competitor-$i.html"
  Start-Sleep -Seconds 5
}
# headings and title
Select-String -Path competitor-1.html -Pattern '<(title|h1|h2|h3)[^>]*>([^<]*)' -AllMatches |
  ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[2].Value }
# structured data types
Select-String -Path competitor-1.html -Pattern '"@type"\s*:\s*"([^"]*)"' -AllMatches |
  ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value } | Group-Object | Select-Object Count, Name
```

If a page is client-rendered, the raw HTML will be thin. Use the rendering MCP or headless browser for that page rather than concluding the competitor has no content.

For each page, record: the URL and fetch date, the format (guide, comparison, category page, tool, product page), the questions its headings answer, what it covers that the site does not, what it leaves out, and any visible proof (original data, named authors, specifications). The gaps it leaves are often where a differentiated angle lives.

---

## SERP analysis through a connected provider

With a SERP provider connected, pull the results for one representative query per cluster. Results vary by location, language and device, so fix those parameters to the audience in `.seo/context.md` and record them with the date.

Record for each query:
- the top ten organic URLs, and which of them are the site's or a named competitor's;
- the result types on the page that the provider reports (for example a featured snippet, people-also-ask questions, video, a local pack, shopping results, or an AI Overview);
- the dominant format among the top results, and the dominant intent that format implies.

Read the results as evidence of what the engine thinks the searcher wants. If eight of the top ten are comparison pages, a product page is unlikely to win that query however good it is. Better copy will not change that; the decision is about format.

With Search Console only, you have the site's own queries and positions but not the results page. That is enough to find footholds and to cluster, but the "format that wins" column stays `unknown (no SERP data)` unless fetched competitor pages give a labelled inference.

---

## The intent and format table

Build one row per query cluster. It turns research into decisions the rest of the pack can act on: which page owns the cluster, what shape it must take, and whether it exists yet.

| Cluster | Example queries (customer's words) | Dominant intent | Format that wins | Result types seen | Site's page | Fit or gap | Basis |
|---|---|---|---|---|---|---|---|
| A name for the cluster | Two or three real queries | informational / commercial / transactional / navigational | guide, comparison, category, tool, product | from the provider, or `unknown` | URL, or `none` | `fits`, `wrong format`, `thin`, `gap` | `SERP data <provider, date>`, `GSC <date range>`, `fetched pages`, or `inference` |

Read the table across:
- **Wrong format** goes to `seo-content-editing` or a restructure, because better copy will not fix a page of the wrong type.
- **Thin** goes to `seo-content-audit` as an improve action.
- **Gap** becomes a create-brief for a human, never an auto-generated article.
- **Two of the site's pages on one cluster** is a cannibalisation candidate for `seo-content-audit`.

---

## Keyword clustering with data

1. **Collect.** Export the site's queries from Search Console and, if a keyword tool is connected, the related queries for each pillar topic. Keep the source and date on every row.
2. **Normalise.** Lower-case, trim, and merge exact duplicates and plural or spelling variants.
3. **Group by shared results** where SERP data exists: two queries whose top ten results overlap heavily want the same page. A threshold of three or four shared URLs out of ten is a common working rule (judgement); tune it by checking a few borderline pairs by eye.
4. **Split by intent** where the results disagree, even if the words look alike. "plane iron" (a buyer) and "how to sharpen a plane iron" (a learner) belong to different clusters.
5. **Assign one primary page** per cluster, existing or planned.
6. **Size honestly.** Sum the provider's volume estimates for a cluster and label the total with the provider and date. Search Console impressions measure the site's own visibility, not the market; never present them as demand.

## Keyword clustering without data

Without a keyword tool or Search Console you still have strong evidence of how customers speak. Use it, and never write a search volume you did not read from a tool. Not "est. 1k/mo", not "high volume", not a guessed range.

1. **Gather the customer's own words** from `.seo/context.md` (Audience vocabulary), site search terms, support tickets, sales FAQs, reviews, and the questions the site already answers.
2. **Group by the job the searcher is doing:** learning how, choosing between options, buying, or finding a specific page. Modifiers give it away: "how to", "what is", "best", "vs", "price", "near me", a product or brand name.
3. **Name each cluster in the customer's language,** not the industry's, and keep two or three real phrasings as examples.
4. **Mark every cluster `un-sized`** and prioritise on what you do know: fit with the topical territory, an existing foothold on the site, value to the business, and effort.
5. **Say what data would change the plan,** for example "connect Search Console to see which of these clusters already earns impressions".

---

## Worked example

The business is the one in `seo-context-gathering/references/context-pack-format.md`: Northfield Tool Company, hand-forged woodworking tools from Sheffield. Search Console is connected; no keyword tool or SERP provider is.

**1. Read the context.** The territory to own is tool care, sharpening technique, choosing a first quality tool, and Sheffield toolmaking. The audience says "plane iron", "bevel-up" and "how to sharpen". Two UK toolmakers are named as competitors, both leading on heritage. The `[established]` differentiators are in-house forging, a lifetime sharpening guarantee, and a published steel specification for every tool. Those three, and nothing else, may appear in positioning copy.

**2. Fetch the competitors.** Check each `robots.txt`, then fetch each competitor's chisel category page and their sharpening guide if one exists: four pages, five seconds apart. Record that both category pages lead on heritage and neither lists steel specification, which matches the `[inferred]` note in the context file and is now backed by fetched pages.

**3. Cluster.** Pull the query report from Search Console and group it, using the audience's own words. There is no SERP data, so "Format that wins" is either `unknown` or a labelled inference from the fetched pages.

| Cluster | Example queries | Intent | Format that wins | Site's page | Fit or gap | Basis |
|---|---|---|---|---|---|---|
| Sharpening technique | how to sharpen a chisel; honing a plane iron | informational | `unknown (no SERP data)` | none | gap | GSC queries; no page |
| Choosing a first quality tool | best first chisel set; bevel-up vs bevel-down plane | commercial | comparison guide (inferred from one competitor's guide) | `/chisels` | wrong format | GSC queries, fetched pages |
| Buying a plane iron | replacement plane iron; plane iron uk | transactional | `unknown (no SERP data)` | `/products/plane-irons` | fits | GSC queries |
| Sheffield toolmaking | sheffield hand forged tools | commercial and navigational | `unknown (no SERP data)` | `/how-we-make-them` | thin | GSC queries |

No row carries a volume. Search Console impressions for each cluster can be quoted from the export as the site's current visibility, with the date range, but not as market demand.

**4. Decide.**
- **Sharpening technique** is a gap at the centre of the territory, and the lifetime sharpening guarantee gives the business standing. It becomes the first pillar: a create-brief for a guide bylined by Ray Alderton, whose 30 years as a toolmaker is `[established]`.
- **Choosing a first tool** is a format problem: a category page cannot answer "bevel-up vs bevel-down". Brief a comparison guide that links to the category, and leave the category page to sell.
- **Sheffield toolmaking** is thin. Pass it to `seo-content-audit` as an improve action, using the workshop photographs listed as proof assets.
- **Open question for the user:** is the sharpening service still running? The context file records a `[conflict]`, and the answer changes whether the sharpening pillar can mention it.

**5. Report the basis.** "Clusters come from your Search Console queries for the last three months. Competitor observations come from four pages fetched on the date shown. No search volumes are given, because no keyword tool is connected; connecting one would let us size the sharpening and comparison clusters before you commit to them."
