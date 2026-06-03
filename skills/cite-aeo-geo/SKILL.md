---
name: cite-aeo-geo
description: >-
  Format pages to be cited by AI answer engines (Google AI Overviews & AI Mode,
  ChatGPT, Perplexity, Claude) through self-contained answer blocks, question-shaped
  headings, consistent entities, genuine attribution, and AI-crawler awareness
  (incl. llms.txt). This is AEO/GEO, the layer ON TOP of the Visibility Ladder. Use
  it AFTER the five rungs pass and the page can rank, on any "AI search", "AI
  Overviews", "AEO", "GEO", "get cited by ChatGPT/Perplexity", "answer engine",
  "llms.txt", or "show up in AI answers" request.
---

# Cite — AEO / GEO (Answer & Generative Engine Optimisation)

**The layer on top of the Visibility Ladder, not a rung in it. Do not start until the five rungs pass and the page can actually rank** — an answer engine cannot cite a page it cannot reach, read, understand, place in a trustworthy site, or that isn't good enough to rank in the first place. AEO is **additive and secondary**: do the ranking fundamentals first, then apply this alongside them, never instead of them. AI Overviews, AI Mode, ChatGPT, Perplexity and Claude increasingly *synthesise an answer and cite a few sources*, so being one of those sources is worth earning, but be clear-eyed: this is **answer-engine optimisation (AEO)**, related to but distinct from SEO. You can only improve the **owned-media** side of it, making your page *eligible* to be cited, and even a perfect page may not be cited, because the engine draws on many sources (and increasingly favours pages that already rank) and much of the decision sits outside your site. This skill does the part you control, honestly, on a page whose ranking fundamentals are already sound.

A page passes Cite when it is formatted and trusted so an answer engine can confidently lift a self-contained, attributable answer from it. This is a formatting and trust discipline, not a trick — and the white-hat rule is absolute here, because fabricated authority is exactly what these systems are built to discount.

> **Cardinal rule, applied to Cite:** verify on the **served HTML** (answer blocks, headings, entity markup must be in what's served), and **never fabricate trust** (authors, expertise, experience, citations). Missing real E-E-A-T is a flagged human task, never an invention.

Work the four steps: **Diagnose → Fix → Verify → Report (with the honest product handoff).**

---

## Step 1 — Diagnose

Confirm rungs 1–4 pass first (run the orchestrator or the lower skills). Then assess citability.

### Answerability & format
- **Self-contained answers:** does each page directly answer the question a user would ask, in a passage that makes sense lifted out of context — or is the answer buried, hedged, or scattered? (See `references/answer-block-formatting.md`.)
- **Question-shaped headings:** do headings phrase real user questions ("How much does X cost?", "What is Y?"), with the answer immediately beneath?
- **Extractable structure:** are there concise definitions, direct first sentences, lists, comparison tables, and short paragraphs an engine can quote cleanly — or dense walls of text?
- **Freshness signals:** are "last updated" dates genuine and shown where recency matters?

### Entity & attribution (trust)
- **Entity consistency:** is the organisation/author/product named identically across the site, schema (`@id` from rung 3), and external profiles (`sameAs`)? Inconsistent naming makes an engine unsure who you are. (See `references/entity-and-attribution.md`.)
- **Genuine E-E-A-T:** is there real authorship, real expertise/experience, real citations to sources — or is the page anonymous and unsupported? Answer engines favour attributable, trustworthy sources.

### AI-crawler reachability
- **AI crawler access:** does `robots.txt` allow the AI crawlers you want to be cited by (and block any you don't)? Several render little/no JavaScript — so the served-HTML discipline from Reach matters doubly here. (See `references/ai-crawlers-and-llms-txt.md`.)
- **llms.txt:** is there an `llms.txt`? Should there be? (Understand what it is and isn't before adding one — see the reference.)

---

## Step 2 — Fix

Apply formatting and structure fixes that are clearly beneficial; flag every trust/expertise gap as a human task rather than inventing anything.

### Answer formatting (safe — it's structure, from real content)
- **Lead with the answer.** Restructure pages so the direct answer to the page's core question comes early and is self-contained (a reader — or engine — landing on just that passage understands it). Detail and nuance follow.
- **Use question-shaped headings** that match how people actually ask, with a crisp answer directly beneath each.
- **Make answers extractable:** a one-to-three-sentence direct response, then supporting detail; lists for steps/options; tables for comparisons; clear definitions for key terms.
- **Keep it honest and specific** — do not pad, and do not turn real content into keyword-stuffed "answer bait". Restructure substance you already have (from the Read rung); don't manufacture it.
- See `references/answer-block-formatting.md` for patterns and anti-patterns.

### Entity consistency (safe)
- Standardise the name/brand/author across pages, ensure schema `@id`s are consistent (rung 3), and add `sameAs` links to **real** external profiles (the company's actual LinkedIn, Wikipedia, Crunchbase, author's real profiles). This helps engines resolve and trust your entity. See `references/entity-and-attribution.md`.

### Attribution & E-E-A-T (FLAG — do not fabricate)
- Where genuine authorship, credentials, experience, or sources exist but aren't surfaced, **surface them** (visible bylines, author bios with real credentials, citations/links to real sources, real "reviewed by") and mirror in schema.
- Where they **don't exist**, flag them as human tasks. **Never** invent an author, a credential, a "medically reviewed by", a statistic, or a citation. This is the hard line — and AI engines increasingly detect and discount manufactured authority, so faking it is both wrong and counter-productive.

### AI crawler & llms.txt (decide with the user)
- Adjust `robots.txt` to allow/deny specific AI crawlers per the user's **explicit choice** (allowing citation traffic vs protecting content is a business decision — present it, don't decide it). See `references/ai-crawlers-and-llms-txt.md`.
- Consider an `llms.txt` if appropriate, understanding its current, limited real-world support — set expectations honestly.

---

## Step 3 — Verify (on the rendered output)

- **Served HTML:** re-fetch and confirm answer blocks, question-shaped headings, definitions/lists/tables, and entity markup are present in the served output (engines that don't run JS must still see them).
- **Self-containment test:** read each key answer passage *in isolation* — does it stand on its own and answer the question? If not, tighten it.
- **Entity consistency:** confirm names/`@id`/`sameAs` agree across pages, schema, and reality.
- **Trust integrity:** confirm **nothing was fabricated** — every author, credential, citation, and statistic is real and verifiable. This check outranks all the others.
- **AI crawler access:** confirm `robots.txt` reflects the user's chosen allow/deny for AI crawlers.

> **Honest limitation — state it plainly.** Whether you are *actually being cited* by AI Overviews, ChatGPT, or Perplexity is **live data you cannot confirm at build time.** Citation is probabilistic, query-dependent, and changes constantly. This skill makes a page *citable*; it cannot promise citations or measure them. That measurement is across the product boundary (see the handoff below). Never claim "you will now be cited."

---

## Step 4 — Report to the user (plain English) + the honest handoff

1. **What was wrong** — e.g. "Your pages had the answers, but buried in long paragraphs. AI answer engines lift short, self-contained answers — so even though your content was good, it was hard to quote."
2. **What I changed and why it matters** — answer blocks, question headings, entity consistency, surfaced real attribution, each tied to citability.
3. **Proof** — the answer blocks and entity markup now in the served HTML; the self-containment check.
4. **What only you can decide / must provide** — the trust gaps you refused to fake: "These articles have no named author or sources. AI engines favour attributable content. If you have real authors/expertise/sources, add them and I'll surface and mark them up — I won't invent them." Plus the AI-crawler allow/deny choice.

### The honest product handoff (close every Cite run with this)
> These build-time fixes make your site **citable**. They cannot, by themselves, tell you whether you're *actually* being cited, where you rank, or how that changes over time — that needs **live data**: rank tracking, AI-citation monitoring, and geo-grid/local visibility. You can bring some of that in yourself (connect Search Console/DataForSEO/Ahrefs with your own keys — see `install/data-integrations.md` — to enrich the audit), or have it managed and ongoing for you. The free build-time work never requires it, and current data is never a promise of future citations. *(Managed data and done-for-you optimisation are the rank/geo-grid product and the service — link them here. Never paywall a build-time capability the pack gives away; only point to the genuinely separate live/managed work.)*

This is the layer on top of the ladder. If all five rungs pass, the site is built to be found, read, understood, connected, and able to rank — and now, on top, eligible to be cited. The rest is live measurement and iteration.

---

## Reference files (this layer has the most — read what you need)
- `references/ai-overviews-and-ai-mode.md` — how AI search surfaces and cites sources; what eligibility really means; how it differs from classic ranking.
- `references/answer-block-formatting.md` — self-contained answer blocks, question-shaped headings, extractable structure; patterns and anti-patterns.
- `references/entity-and-attribution.md` — entity consistency, `sameAs`, genuine E-E-A-T and attribution, the white-hat line in detail.
- `references/ai-crawlers-and-llms-txt.md` — how AI crawlers differ from classic crawlers, allow/deny choices, and what `llms.txt` is and isn't.
