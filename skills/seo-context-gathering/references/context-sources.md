# Where real context comes from

A source-by-source guide for `seo-context-gathering`. Work roughly in this order: what you already have, then what the user has connected, then what is publicly reachable. Stop when the pack is good enough to act on — completeness is not the goal, **grounding** is.

---

## Tier 1 — Inside the project (free, private, highest trust)

These are the most reliable sources you will get, because the business wrote them for itself rather than for search engines.

| Source | Uniquely good for |
|---|---|
| `README.md`, `docs/`, `AGENTS.md` / `CLAUDE.md` | What the product genuinely does, in the team's own words, usually without marketing gloss. |
| `CHANGELOG.md`, release notes, git history | What is actively developed, what was discontinued, and how fast the product moves. A feature page for something removed two years ago is a finding. |
| `package.json` / project manifest | Name, description, homepage, repository, licence. Cheap identity facts. |
| CMS content models, schemas, seed data | The real content types, and therefore the real information architecture. |
| Product and pricing data files | The actual offer and price points, which marketing copy often lags behind. |
| i18n / locale files | Which markets are genuinely served (and which are aspirational). |
| Support macros, sales FAQs, canned replies, issue templates | **The best source of customer vocabulary inside the building.** These are the questions people actually ask, phrased the way they actually ask them. |
| Test fixtures and example data | Frequently reveal real customer names or segments; use for understanding, never publish. |

## Tier 2 — The served site (free, public, authoritative for claims)

Read the rendered output, not just the source. This is what the business says publicly, so it is what may be treated as **established**.

- **Home, product/service, pricing** — the offer, the positioning, the claims currently being made.
- **About, team, careers** — real people, real credentials, company age, size, values, and the tone the business uses when describing itself.
- **Legal pages** — terms and privacy usually name the **registered legal entity**, company number and jurisdiction. Often the only place the formal identity appears.
- **Contact / footer** — NAP (name, address, phone) for local businesses; must match anything you later put in schema.
- **Case studies, testimonials, logos, reviews** — the proof-asset inventory. Note precisely what is verifiable and attributable; a first-name-only quote is weaker proof than a named, titled, linked one.
- **Blog and docs** — the topical territory already covered, the depth, the authors, and the house voice with real examples you can quote.
- **Existing structured data** — canonical entity names, spellings, `sameAs` links and identifiers you must stay consistent with.

## Tier 3 — Connected data (optional, the user's own keys)

Only if configured; never required, never a gate. See `seo-orchestrator/references/live-data-integrations.md` for the security rules — read keys from environment variables, never store them anywhere.

- **Google Search Console.** The highest-value context source there is, and free. The query report is *the literal language of people who already reach this site*. Use it for audience vocabulary, the questions they arrive with, the mismatch between how the business talks and how its readers search, and which segments actually show up. Page-level impressions and position also tell you what the market already rewards.
- **Analytics (GA4).** Which content earns engagement, where visitors come from, which segments convert. Behavioural context that copy alone cannot give you.
- **DataForSEO / Ahrefs / Semrush.** Real demand volumes, competitor coverage, and content-gap data. Turns "we should probably cover X" into a sized opportunity.
- **Bing Webmaster Tools.** A second view of indexation and query data.

## Tier 4 — Free public sources (no key, use politely)

Genuinely useful, and available to everyone:

- **Search suggestions and related searches.** Autocomplete and related-search modules expose real phrasing and adjacent intents for a seed term. Excellent for audience vocabulary when Search Console is not connected.
- **"People also ask" style question sets.** Real question phrasing, which is the raw material for answer-first formatting in `cite-aeo-geo`.
- **Public reference entries** (encyclopaedic and structured-data sources). Best for **entity disambiguation**: the canonical spelling of an organisation, industry, place or technology, and how it relates to other entities. Useful when the same product name means several things.
- **Community discussion** (forums, Q&A sites, subreddits relevant to the sector). The unfiltered version of how the audience describes its problem, including the words they use before they know the industry jargon. Read for vocabulary and pain points; never lift text, and never quote an identifiable individual.
- **Competitor sites.** Read for coverage, depth and positioning: what topics they own, how they frame the category, which claims they lean on. This maps the territory so you can find the genuine gap.

### Etiquette, and the lines that do not move

- **Respect `robots.txt`, rate limits and terms of service.** Fetch slowly and identify yourself honestly. If a site asks not to be crawled, do not crawl it.
- **Nothing behind a login.** No authenticated scraping, no paywalled content, no private APIs.
- **No personal data.** Do not compile information about identifiable individuals. Public professional facts about a *named author on the client's own site* are context; anything else is not.
- **Read competitors, do not copy them.** Their copy is theirs. You are mapping what is covered, never harvesting phrasing.
- **External calls are outward actions.** Only use services the user has connected or that are ordinary public web requests. Tell the user what you fetched.

## Tier 5 — The human (last, shortest, most respectful)

Everything above runs first. Whatever remains genuinely unknown *and* materially changes the work becomes a short ranked list of questions, **each with a proposed default**, so the user confirms rather than composes. Typical residue after a thorough pass:

- Which audience segment matters most commercially this quarter.
- Whether a claim you found is still accurate and still permitted.
- Whether named people are willing to be bylined, and with what credentials.
- Which competitors they consider real rivals, as opposed to who happens to rank.
- Any compliance or legal constraint on what can be said.

Anything unanswered stays **unknown**. Downstream skills must degrade gracefully rather than assume.

---

## Sector notes

- **Regulated sectors** (health, finance, legal, insurance): what may be claimed is a hard constraint, not a style preference. Record it prominently in the pack's *claims and constraints* section, and treat YMYL expectations for real expertise and sourcing as binding.
- **Local businesses**: NAP consistency, service areas and opening hours are context and must match schema and directory listings exactly.
- **E-commerce**: catalogue structure, brands carried, shipping and returns policy, and stock reality shape both content and schema.
- **Documentation and developer products**: the audience's vocabulary is in the docs, the issue tracker and the support channel; the "keyword research" is largely already written down.
- **International**: which locale genuinely gets original content versus a translation, and which market each domain or subfolder actually serves.
