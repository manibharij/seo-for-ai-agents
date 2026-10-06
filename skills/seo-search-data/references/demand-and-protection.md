# Protecting traffic, logging changes, and mapping demand

Recipes behind Jobs 2 and 3. API details are in `seo-orchestrator/references/data/search-console.md`; any tool that provides search performance by query and page works the same way.

---

## Protecting what earns traffic

### Pull the baseline

For the pages about to change (or the template), over the last 90 days ending 3 days ago:
- per page: clicks, impressions, CTR, average position (`dimensions: ["page"]`);
- per page and query: the top queries by clicks (`dimensions: ["page","query"]`, filtered to the page);
- if available: sessions, key events and revenue for those landing pages (GA4 or CRM).

### Set the threshold (judgement)

There is no universal number. Pick one that fits the site and say which you used:
- **Share of clicks:** any page with more than about 5% of site organic clicks, or in the top 10% of pages by clicks.
- **Absolute floor for small sites:** on a site with a few hundred clicks a month, any page with steady clicks matters.
- **Business value:** any page with attributed leads or revenue, regardless of clicks.
- **Template rule:** a change to a template is above the threshold if the template's pages together are.

### The sign-off record

Above the threshold, present this and wait for a yes:

```markdown
**Change needs sign-off:** /pricing
- Earns: 2,140 clicks, 61,000 impressions, avg position 4.2 (GSC, 2026-07-01 to 2026-09-28); 96 key events "demo_request" (GA4, same range)
- Top queries: "acme pricing" (880 clicks), "acme cost" (210), "acme plans" (170)
- Proposed: title "Pricing | Acme" -> "Acme pricing: plans from £29 a month"
- Risk: title rewrites can change CTR either way; the brand query should hold.
- Rollback: revert the title in app/pricing/page.tsx metadata.
```

### The change log entry

Append to `.seo/log.md` for every change to a live page, signed off or not:

```markdown
## 2026-10-04: change
- **What:** rewrote titles on /pricing and /pricing/teams
- **Where:** app/pricing/page.tsx, app/pricing/teams/page.tsx (commit abc1234)
- **Baseline:** /pricing 2,140 clicks, CTR 3.5%, pos 4.2; /pricing/teams 310 clicks, CTR 2.1%, pos 6.8 (GSC 2026-07-01 to 2026-09-28)
- **Control:** /features/* (unchanged)
- **Sign-off:** Sam, 2026-10-03
- **Measure after:** 2026-11-01
```

The date of deploy, not the date of the commit, is the change date. If they differ, log the deploy.

---

## Mapping demand

### Striking distance

From `dimensions: ["query","page"]` over 90 days:
- keep rows with average position between about 8 and 20 (judgement) and impressions above a floor that fits the site;
- sort by impressions;
- for each, check the served page: does it answer the query's intent, in the title, H1 and the opening of the body? If not, that is the work. If it already does, the gap is more likely depth, internal links or authority.

Hand to `5-rank-relevance` or `seo-content-editing`. Never rewrite to repeat a query; match the intent.

### Cannibalisation

- From the same rows, group by query and keep queries where two or more pages have meaningful impressions.
- Look at position by date for each page: alternating rankings (pages swapping places) are the clearest sign.
- Fetch both pages: if they serve the same intent, propose consolidation (merge, 301, update links) to `seo-content-audit`; if the intents differ, sharpen each page so the difference is clear.
- A brand query matching several pages is normal, not cannibalisation.

### Gaps

- **Weak match:** queries with impressions where the ranking page is a tangent.
- **No page:** topics in `.seo/context.md`, sales conversations or competitor coverage with no page on the site. Search Console cannot show demand you do not touch; a keyword tool (tier 3) can estimate it.

### Adding tier 3 demand

If a keyword tool is available, add volume, difficulty and the top-ranking competitors for each opportunity, labelled with the vendor, country database and date. Batch requests and announce the units before spending. Without a tool, rank by Search Console impressions and write "volume unknown".

### Anonymised queries

Query rows never add up to page totals, because rare queries are withheld for privacy. When a page has many impressions but few listed queries, say the long tail is hidden rather than calling the page low-demand.
