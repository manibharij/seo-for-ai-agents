# Validating structured data

Read this to confirm your JSON-LD is (1) present in the served HTML, (2) technically valid, and (3) honest. All three must hold. Validity without honesty is a trust risk; honesty without presence in the served output is invisible.

---

## 1. Presence — is it in the served HTML?

Schema injected only client-side may never be seen by engines that don't run your JavaScript (the same failure mode as Reach). Fetch the raw served output and confirm the block is there:

```bash
curl -sL https://example.com/page | grep -i "application/ld+json"
```
```powershell
(Invoke-WebRequest -Uri "https://example.com/page" -UseBasicParsing).Content |
  Select-String -Pattern "application/ld\+json"
```

If it's missing from the raw HTML, render it server-side (Next.js: emit the `<script>` from a server component — see the SKILL). Check each template type; schema is usually added per template.

---

## 2. Validity — does it parse and conform?

### If a schema-validator MCP is available
Use it — it's the sharpest check. Feed it the served HTML or the JSON-LD block and read off the errors/warnings. Otherwise, validate manually as below.

### Manual validation
- **JSON parses.** Extract the block and parse it (e.g. `node -e "JSON.parse(require('fs').readFileSync('block.json','utf8'))"` or paste into a parser). A trailing comma or unescaped quote breaks the whole block.
- **`@context` and `@type` are correct.** `@context` is `https://schema.org`; `@type` is a real schema.org type spelled correctly (case-sensitive: `BlogPosting`, not `Blogposting`).
- **Required & recommended properties present** for the type and the rich result you want. The authoritative references:
  - Google's structured-data feature docs (per type: Article, Product, Breadcrumb, FAQ, LocalBusiness, etc.) define what's *required* vs *recommended* for **rich-result eligibility**.
  - schema.org defines the full vocabulary.
- **Values are well-formed.** ISO 8601 dates; absolute URLs; `priceCurrency` as an ISO code (`GBP`); `availability` as a schema.org URL (`https://schema.org/InStock`).
- **`@id` references resolve.** Every `{ "@id": "..." }` reference points to an entity actually defined (in the same `@graph` or a known URL).

### Two layers, don't confuse them
- **Schema.org-valid** = the vocabulary is used correctly. A page can be valid here yet ineligible for a rich result.
- **Rich-result-eligible** = it also meets Google's stricter per-feature requirements. Eligibility is **not** a guarantee of display — Google decides per query. Tell the user "eligible", never "you will get a rich result".

---

## 3. Honesty — does it mirror the visible, true page?

This check is unique to doing schema *right*, and it's the one lazy packs skip. For every property in the JSON-LD:
- Is this information **visible on the page**? (Schema should describe shown content, not hidden facts.)
- Is it **true**? (Real author, real price, real rating, real opening hours.)
- Did the agent **invent** anything to fill a "recommended" slot? If so, remove it and flag the gap to the user.

Reject and fix on sight:
- `aggregateRating`/`review` with no real reviews on the page.
- An `author` (`Person`) who doesn't exist or isn't credited on the page.
- Prices/availability that don't match what's shown.
- An `FAQPage` of questions invented to chase a rich result rather than genuine on-page FAQs.

Fabricated structured data risks a manual action and undermines exactly the trust that the Cite rung depends on. When real data is missing, the correct output is a flagged human task, not a plausible-looking lie.

---

## Definition of done — the Understand checklist

- [ ] The JSON-LD block is present in the **raw served HTML** for each relevant template.
- [ ] JSON parses; `@context`/`@type` valid; required & recommended properties present for the chosen type.
- [ ] Values well-formed (ISO dates, absolute URLs, ISO currency, schema.org enum URLs).
- [ ] `@id` references resolve; the same real entity uses a consistent `@id`, name, URL and logo across blocks.
- [ ] **Every value mirrors visible, true content** — nothing fabricated; missing trust data flagged to the user, not invented.
- [ ] Validated via MCP or against Google's per-type requirements; eligibility (not guaranteed display) reported honestly.

If any box is unchecked, Understand has not passed. Only then climb to rung 4 (Connect).
