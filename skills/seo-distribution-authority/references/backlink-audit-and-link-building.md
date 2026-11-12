# Backlink audit & white-hat link-building

Read this for the off-page detail. Two halves: **auditing** what you have (needs data), and **earning** more (strategy, white-hat only). The governing rule: links are *earned by being worth linking to*. Anything that tries to shortcut that earns penalties.

---

## Reading a backlink profile

Quality, not count. Assess:
- **Referring domains over total links.** 50 links from 50 relevant sites beats 5,000 from one spammy widget. Count unique linking domains and weigh their quality.
- **Authority & relevance.** Strong, *topically relevant* domains pass the most value. A link from a respected site in your field beats a high-authority but irrelevant one.
- **Anchor-text distribution.** Natural profiles are mostly brand and URL anchors, with some generic ("click here", "this guide") and a minority of descriptive/partial-match. A **spike of exact-match commercial anchors** ("buy cheap widgets") is the classic manipulation footprint and a risk.
- **Link velocity.** Steady, organic growth is healthy; sudden unexplained spikes can signal a paid campaign or a negative-SEO attack.
- **Toxicity signals.** Link farms, sitewide footer/template links at scale, PBN footprints (same hosting/owner/templates across "different" sites), irrelevant foreign-language directories, links from hacked or adult/gambling spam.
- **Competitor gap.** The referring domains and content types competitors earn that you don't, filtered to ones you could *realistically and relevantly* earn too.
- **Unlinked mentions & lost links.** Mentions without a link (reclaim) and links that have dropped (recover).

Without connected data (Search Console links report, or Ahrefs/DataForSEO/Semrush), you can't do this honestly. Say so and point to the source to connect; don't estimate a profile.

Search Console's Links report shows top linked pages, top linking sites and top linking text. Each table holds up to 1,000 rows, and the export from the report's landing page offers "Latest links" and "More sample links", each up to 100,000 rows (verified 2026-10, [Links report](https://support.google.com/webmasters/answer/9049606)). On a large profile it is a sample, so say so in the report.

### Anchor-text distribution checks

Count anchors **per referring domain**, not per link, so one sitewide footer link does not swamp the picture. Put each anchor in one bucket:

| Bucket | Examples |
|---|---|
| Brand | "Northfield Tool Company", "Northfield" |
| URL | "northfield-tools.example", "https://northfield-tools.example/chisels" |
| Generic | "here", "this guide", "website" |
| Partial match | "Northfield's guide to sharpening", "their bevel-up plane" |
| Exact-match commercial | "buy hand forged chisels", "cheap chisel set" |
| Empty or image | no text, or alt text only |

Then look closer when one of these holds. **Every threshold here is judgement.** Google publishes no anchor ratios, and a site's niche, age and size shift what is normal.
- Exact-match commercial anchors account for more than about one in ten referring domains.
- One commercial phrase repeats across many unrelated domains. Real editors rarely choose the same words.
- Brand and URL anchors together fall below about half of referring domains.
- Commercial anchors arrived in a burst: many new domains in a short window, all with keyword anchors.

Two cautions keep this honest. With fewer than about 30 referring domains, percentages are noise, so describe the anchors instead of scoring them. And the best baseline is a competitor's distribution from the same data provider, which is worth more than any fixed number. A tripped threshold is a reason to inspect those links, never proof of manipulation, and never on its own a reason to disavow.

### Link audit CSV

Export the audit as `.seo/link-audit.csv`, one row per linking domain (or per linking URL where the source provides it). Fill only what the data source gives you; leave a cell blank rather than estimating it. Quote any field that contains a comma, quote or line break.

```csv
domain,linking_url,target_url,anchor,anchor_bucket,rel,first_seen,last_seen,source,relevance,assessment,action,reason,status
woodworking-forum.example,https://woodworking-forum.example/t/best-chisels,/chisels,Northfield,brand,follow,,2026-09-12,"GSC Links export 2026-10-01",high,healthy,keep,"Relevant community thread, editorial mention",open
```

- `rel` is `follow`, `nofollow`, `sponsored` or `ugc`, as the source reports it.
- `assessment` is `healthy`, `review` or `toxic`. Use `toxic` only with a stated pattern in `reason` (link farm, PBN footprint, hacked page, paid-link footprint).
- `action` is `keep`, `reclaim` (a lost link worth recovering), `remove-request` (the user asks the site owner), `disavow-candidate`, or `monitor`.
- `status` uses the shared schema values, so the CSV can merge into `.seo/state.json`.

The rows that matter go into the report as findings in the shared schema. The CSV is the working file behind them.

---

## Disavow: rarely, and carefully

Google's algorithms now **ignore most spammy links automatically**, so the disavow tool is a **last resort**, not routine maintenance. Use it only when there's a genuine, clear problem: a real negative-SEO attack, or a legacy of paid/manipulative links you can't get removed.

- **Format:** a plain-text file, one domain or URL per line, `domain:` prefix for whole domains:
  ```
  # Toxic link farm, attempted manual removal 2026-05, no response
  domain:spammy-link-farm.example
  domain:pbn-footprint.example
  https://hacked-site.example/specific-spam-page
  ```
- Submit it in Search Console's disavow tool. It's the one concrete artifact this skill produces.
- **Google's file rules** (verified 2026-10, [Disavow links to your site](https://support.google.com/webmasters/answer/2648487)):
  - a `.txt` file, encoded in UTF-8 or 7-bit ASCII;
  - one URL or one `domain:example.com` entry per line, with `#` starting a comment line;
  - at most 100,000 lines (blank and comment lines count) and 2 MB, with URLs no longer than 2,048 characters;
  - uploading a new list **replaces** the property's existing list, so download the current one first and merge;
  - Google says it can take a few weeks for the list to be taken into account.
- **Google's own caution, from the same page:** most sites will not need the tool. Google describes it as an advanced feature to use with caution, for a site with considerable spammy, artificial or low-quality links pointing to it that have caused, or are likely to cause, a manual action. That is the bar. A long list of low-quality links that Google is already ignoring does not meet it.
- **Check the file before handing it over:**
  ```bash
  wc -l disavow.txt                      # under 100,000 lines
  grep -viE '^(#|domain:[a-z0-9.-]+|https?://)' disavow.txt   # prints any malformed line
  ```
  ```powershell
  (Get-Content disavow.txt).Count
  Get-Content disavow.txt | Where-Object { $_ -notmatch '^(#|domain:[a-z0-9.-]+|https?://)' }
  ```
  Blank lines also print; they are allowed, but remove them to keep the file tidy.
- **Risk:** over-disavowing removes links that were *helping*. Disavow only what's genuinely toxic, document why (comments), and prefer removal/outreach first. When unsure, don't.

---

## Earning links, white-hat (the durable half)

You don't "build" links; you make things worth linking to and put them in front of the right people.

- **Linkable assets.** Original research and data, free tools/calculators, definitive/canonical guides, strong original opinion or analysis. Recommend what *this* site is uniquely positioned to create that others in its field would cite.
- **Digital PR.** Newsworthy angles, data-led stories, surveys, expert commentary (responding to journalist requests). Earns editorial links and brand mentions, the highest-quality kind.
- **Unlinked-mention reclamation.** Find mentions of the brand/people without a link; polite outreach to add one. High conversion, low effort.
- **Broken-link building & resource pages.** Find relevant broken links or resource lists where the site *genuinely belongs*, and suggest it as a replacement/addition.
- **Relationships & genuine guest contributions** on real, relevant publications (for audience and authority, not link-farming).
- Prioritise by the **competitor gap** and genuine relevance, not vanity volume.

### Outreach target list (advisory)

Hand the user a list they can work through. The agent finds and prioritises targets; the user decides, writes and sends. Never send a message, submit a form, or offer payment or a link in return. Save as `.seo/outreach-targets.csv`.

```csv
priority,site,page,type,why_relevant,evidence,suggested_angle,asset,contact_route,status,notes
1,toolmaking-history.example,https://toolmaking-history.example/sheffield-makers,unlinked-mention,"Names the business in a list of Sheffield makers, no link","Fetched 2026-10-06",Ask whether they would link the existing mention to /how-we-make-them,/how-we-make-them,Contact page on the site,idea,
```

- `type` is `unlinked-mention`, `lost-link`, `broken-link`, `resource-page`, `digital-pr` or `guest-contribution`.
- `evidence` records how you know the target is real and relevant: the fetched page and date, or the data source.
- `suggested_angle` and `asset` must rest on `[established]` facts from `.seo/context.md` and on content that exists. Do not pitch a study, a statistic or an expert the business does not have.
- `contact_route` names a public route such as the site's contact page or editorial submissions page. Do not harvest personal email addresses.
- `status` is the user's to move: `idea`, `approved`, `sent by user`, `linked`, `declined`.

Rank by relevance first, then by the realistic chance of a link (an unlinked mention of the business is the easiest), then by the authority of the site.

---

## The black-hat tactics this skill refuses (always)
- **Buying or selling links** (including "sponsored" links that pass PageRank without `rel="sponsored"`/`nofollow`).
- **Link schemes / exchanges** at scale ("link to me and I'll link to you").
- **Private blog networks (PBNs).**
- **Comment, forum, profile, or directory spam.**
- **Paid guest-post networks** and mass low-quality guest posting for links.
- **Automated link generation** of any kind.

These are exactly what search engines penalise. They are never recommended here. If the user asks for them, explain why they're harmful and offer the white-hat alternative instead.

---

## The honest boundary
This skill **audits and strategises**; it does not execute outreach, create the content, or build relationships, those are ongoing, off-site, human (or managed-service) work. Final authority is *earned over time*, and where you rank as a result is live data. The agent gives you the map and the priorities; earning the authority is the journey.
