---
job: migrate
title: The URLs are changing
situation: >-
  A redesign, a replatform, a domain move, a restructure, or a merge of two
  sites. Something that already works is about to be addressed differently, and
  the risk is losing everything that was earned against the old addresses.
roles: [technical-engineer, account-reporter]
data:
  required: []
  helpful: [search-console, analytics, server-logs, backlink-data, crawl-history]
guardrails: [do-not-regress, no-url-change-without-approval, inventory-before-change]
default_autonomy: 2
stop_when: >-
  A complete, approved, one-to-one redirect map exists and has been tested
  against the old URL inventory.
done_when: >-
  Every old URL with traffic, links or index presence resolves in one hop to its
  genuine equivalent, verified on served output after cutover, and the
  post-migration watch list is running.
---

# Migrate

This is the highest-stakes job in the pack and the one where autonomy is lowest. Every
other job can be retried. A migration that ships without redirects destroys, in an
afternoon, authority that took years to accumulate, and the recovery is partial at best.

The whole job is one discipline: **inventory before you change anything.** Once the old
site is gone you cannot enumerate what it had, and a redirect map built from the new
site's structure will silently omit exactly the pages nobody remembered.

The most common way this job goes wrong is redirecting everything that does not have an
obvious match to the homepage. Google treats a redirect to an irrelevant page as a soft
404, so a thousand URLs pointed at the homepage is a thousand URLs thrown away, with the
added cost that it looks handled.

## Order of work

### 1. Inventory, from every source, before touching anything
`access/migrations`, `demand/search-data`, `access/logs`.

Build one list of old URLs from **all** of these, because each one knows about pages the
others do not:
- The existing sitemap, and any older sitemaps still reachable.
- A full crawl of the live site.
- Search Console: every URL with impressions or clicks, and the index coverage report.
- Analytics: every URL with sessions in the last twelve months, which catches seasonal
  pages a shorter window misses.
- Server logs: what crawlers and users actually request, which catches URLs that are
  linked from outside but not from the site.
- Backlink data: every URL with external links pointing at it. These are irreplaceable,
  because you cannot ask the whole web to update its links.

Deduplicate, then annotate each URL with traffic, impressions, external links and index
status. That annotation is what makes the next step a judgement rather than a guess.

### 2. Map one to one, and justify every exception
`access/migrations`, `access/redirects`.

For each old URL, the genuine equivalent on the new site. One hop, `301`, no chain.

Where there is no equivalent, the choice is explicit and recorded per URL:
- The closest genuinely relevant page, where one exists and a user arriving there would
  be served.
- A `410` where the content is truly gone and no equivalent exists. An honest gone is
  better than a dishonest redirect.
- Never the homepage as a default. If a page has no relevant destination, say so.

Pages with external links get the most care, because that is where the transferable
authority actually lives.

### 3. Get the map approved before cutover
This is the approval gate, and it does not move. A human signs off the map, with
particular attention to the highest-traffic and most-linked URLs, before anything is
deployed. The agent presents the map sorted by what is at risk, not alphabetically.

### 4. Preserve the signals that are not redirects
`access/canonicalisation`, `access/hreflang`, `access/architecture`.

A migration breaks more than addresses:
- Canonicals on the new site point at new URLs, self-referentially.
- `hreflang` clusters are rebuilt completely. A half-migrated cluster is worse than none,
  and these fail silently.
- Internal links point at the new URLs directly, not through the redirects. Redirect
  chains in internal navigation waste crawl budget and slow every page.
- Deliberate `noindex` rules and blocked paths from the old site are carried over, having
  first been confirmed as deliberate.
- Structured data and entity `@id`s stay consistent, so the entity survives the move.

### 5. Cut over, then verify on served output
`access/redirects`, `operations/launch-qa`.

Immediately after cutover, test the actual old URLs against the live site. Not the map,
not the config: the requests. Sample across the whole inventory and test every
high-value URL individually. Confirm one hop, correct status, correct destination.

For a domain move, submit the change of address in Search Console, keep the old domain's
redirects live indefinitely, and keep its Search Console property so you can watch both
sides.

### 6. Watch for longer than feels necessary
`operations/regression-detection`.

Migrations recover over weeks, and the signal is noisy early. Record a watch list:
index coverage on both properties, 404s in logs, traffic per old-URL cluster against its
own before, and crawl stats. A dip in the first fortnight is normal. A dip still there
at six weeks is a fault to find, and the inventory is how you find it.

## What this job must never do

- Change a URL before the inventory is complete. There is no recovering an unknown page.
- Redirect unmatched URLs to the homepage in bulk.
- Chain redirects, or leave the old chain in place underneath the new one.
- Delete the old sitemap before the migration is verified. It is the checklist.
- Report success from a configuration diff. The evidence is the response to a request
  for an old URL on the live site.
- Take the opportunity to also restructure something else. One change at a time, or no
  drop can ever be attributed.

## Output

The annotated old-URL inventory, the one-to-one map with every exception justified, and
an explicit sign-off request ordered by what is at risk. After cutover, served-output
verification per URL for the high-value set and a sample of the rest, plus the watch
list with dates.

If the migration is already done and the redirects were not, this is a `rescue` job and
the inventory has to be rebuilt from Search Console, analytics, logs and backlink data.
It is recoverable, partially, and the honest framing is that some of it is not.
