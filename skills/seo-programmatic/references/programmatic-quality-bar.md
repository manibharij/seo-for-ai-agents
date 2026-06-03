# The programmatic quality bar

Read this to keep programmatic SEO on the right side of the line. The whole discipline hinges on one judgement: **does each page earn its place?** This file is how you decide, and how you control scale so it helps rather than harms.

---

## Doorway pages vs legitimate pSEO

Google's own guidance treats **doorway pages** — large numbers of near-duplicate pages created to rank for many queries, funnelling users to the same place with little unique value — as spam. The difference is **genuine per-page value**, not the fact of templating.

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

A page qualifies only if it clears a minimum bar. Define it explicitly for the dataset, e.g.:
- **Enough real data fields populated** (set a threshold — pages missing core data don't qualify).
- **Genuinely distinct content** vs sibling pages (not near-duplicate — see the dup check below).
- **Real, specific value** for the searcher's intent (would a human find *this* page useful, not just the category?).
- **Honest schema** populated from real data only.

Pages below the bar are **withheld or consolidated**, not padded with fabricated text. Report how many passed vs were withheld — that honesty is part of doing it right.

### Duplication check
Sample several generated pages and read them side by side. If they're near-identical but for the swapped variable, the gate is too low — raise the threshold, enrich the data, or cut the page type. Tools/`diff` or an embedding-similarity check can flag this at scale.

---

## Indexation & crawl-budget control at scale

Thousands of pages can flood crawl budget and dilute quality signals. Decide deliberately (coordinate with Reach + Connect):
- **Index** the pages that clear the bar and serve real demand.
- **`noindex`** (or don't generate) the low-value long tail and thin combinations.
- **Canonicalise** near-duplicate variants to the best version.
- **Don't generate faceted/parameter explosions** as crawlable URLs (the e-commerce faceted-nav problem applies — see the ecommerce profile).
- **Generate a sitemap** of the indexable set; **interlink** via hubs/categories so pages aren't orphaned.
- Roll out in **batches** on an existing site and watch indexation/quality (existing-site safety), rather than dumping 10,000 pages at once.

---

## How it coordinates with the rest of the pack
- **Reach** — crawl-budget/indexation control; generated pages must be in the served HTML.
- **Read / content-audit** — the thinness and intent bar; content-audit's "consolidate/prune" applies if a generated set is already thin.
- **Understand** — honest schema per page from real data.
- **Connect** — hubs, internal linking, canonicals so the set is coherent, not an orphaned sprawl.

## The honest outcome
Sometimes the right recommendation is **"don't"** — or "generate 200 genuinely useful pages, not 20,000 thin ones." Saying that is the skill working correctly. Programmatic SEO is a force multiplier for *good* content and a fast way to get penalised with *thin* content; this skill only does the former.
