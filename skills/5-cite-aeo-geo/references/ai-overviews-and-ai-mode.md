# How AI search surfaces and cites sources

Read this to understand what you're actually optimising for at the Cite rung — and why it's different from classic ranking. The short version: classic search returns a list and lets the user choose; AI search **composes an answer** and **cites a few sources** it drew from. Your goal shifts from "rank in the list" to "be one of the cited sources."

---

## The landscape (as of 2026)

- **Google AI Overviews** — an AI-generated summary above the classic results for many queries, with links to cited sources.
- **Google AI Mode** — a fuller conversational search experience that synthesises across sources and cites them.
- **ChatGPT (with search)** — answers questions and cites web sources; also has a dedicated crawler for its index.
- **Perplexity** — answer-first engine built around citing sources inline.
- **Claude, Copilot, Gemini, and others** — assistant experiences that retrieve and cite web content.

These change frequently. Treat specifics as a moving target; the **principles** below are what endure.

---

## How a page becomes a cited source (the mental model)

An answer engine roughly: (1) interprets the user's question, (2) retrieves candidate passages from pages it has crawled/indexed, (3) synthesises an answer, and (4) cites the sources whose passages it used. To be cited you must clear every step:

1. **Be reachable and in the index** — the engine's crawler must have fetched your page and seen the content in the **served HTML** (rungs 1–2; doubly important because several AI crawlers run little/no JavaScript).
2. **Have a passage that cleanly answers the question** — self-contained, extractable, unambiguous (this rung's formatting work).
3. **Be understandable and trustworthy** — clear entities (rung 3), a coherent site (rung 4), and genuine attribution/expertise (this rung). Engines prefer sources they can attribute and trust.
4. **Match the query's intent** — the answer the engine needs must actually be on your page, phrased close to how it's asked.

You optimise steps 2–4 here; steps below them are the lower rungs, which is why they must pass first.

---

## What "eligibility" really means — set expectations honestly

- You can make a page **citable** (well-formatted, trustworthy, reachable). You **cannot guarantee** it will be cited.
- Citation is **probabilistic and query-dependent**: the same page may be cited for one phrasing and not another, today and not tomorrow, in one engine and not another.
- It is **not measurable at build time.** Whether you're cited, and how often, is live data — it requires monitoring across engines and queries over time. (This is the product-boundary handoff; see the SKILL's closing note.)
- So: never tell a user "you'll now appear in AI Overviews." Tell them "your pages are now formatted and trusted to be *eligible* to be cited; measuring whether they are is ongoing live work."

---

## What AI engines tend to favour (durable principles)

- **Direct, self-contained answers** to clear questions, near the top of the relevant section.
- **Specificity and substance** — concrete, accurate, genuinely useful content over generic filler. (Thin content fails here as it fails at Read.)
- **Attributable expertise** — named authors with real credentials, cited sources, evidence of first-hand experience. Anonymous, unsupported claims are weaker candidates.
- **Consistency** — the same entity described the same way across the site and the wider web, so the engine is confident who you are.
- **Structure it can parse** — headings that map to questions, lists, tables, definitions, clean semantic HTML.
- **Freshness where it matters** — genuine recency for time-sensitive topics.

---

## How this differs from classic SEO (and how it doesn't)

- **Same foundations.** AI search still depends on crawlability, readable content, structured data, and a coherent, trusted site. The Visibility Ladder's lower rungs are not optional for AEO — they're prerequisites. There is no "AI SEO" shortcut that skips them.
- **Different target.** The unit of success moves from a ranked link to a cited passage. You format for **extraction and attribution**, not just relevance.
- **Trust matters more, and fakery backfires harder.** These systems are explicitly built to weigh source trustworthiness and to discount manufactured authority. The white-hat rule isn't just ethics here — it's effectiveness.

The practical upshot for the agent: do the lower rungs properly, then format for self-contained answerability and surface *genuine* trust signals. That's the whole game, and it's covered in the other three references.
