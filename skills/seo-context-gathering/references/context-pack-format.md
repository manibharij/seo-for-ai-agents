# The context pack: `.seo/context.md`

The format for the file `seo-context-gathering` writes, and every other skill reads. It lives in the user's project beside `audit.md`, `state.json` and `log.md`, and is committed to version control like the rest of `.seo/`.

Two things make it useful rather than decorative:

1. **Every fact carries its provenance.** Nothing sits in the file without a label saying how much weight it can take.
2. **It is written to be read by a skill mid-task**, so it is short, scannable, and specific. A long, hedging document gets skimmed and ignored.

---

## Provenance labels

Use these inline, everywhere:

- **`[established]`** — the business states it, on its own site, in its repo, or in its structured data. Include where. Usable in published copy, schema, and trust signals.
- **`[inferred]`** — you concluded it. Include the evidence. Usable for strategy, prioritisation and briefs. **Never** for a published claim.
- **`[unknown]`** — you could not determine it. Usable for nothing; it belongs in *Open questions*.
- **`[conflict]`** — two sources disagree. Record both and flag it; do not silently pick a winner.

The single most important line in this file: **an inference never becomes a published claim.** If a section has nothing established in it, that is a finding to report, not a gap to fill with reasonable-sounding text.

---

## Sections

Keep every section, even when thin — an empty section with `[unknown]` is information. Drop nothing to make the file look complete.

| Section | What goes in it | Why later skills need it |
|---|---|---|
| **Identity** | What this business is in one plain sentence; legal entity and jurisdiction; NAP if local; founded/size if stated. | Schema entities, `Organization` markup, local consistency, and describing the business back to its owner correctly. |
| **Offer** | What is actually sold, the product or service lines, the pricing model, what is free versus paid. | Intent matching, commercial-page quality, `Product`/`Offer` schema, and spotting pages that describe a discontinued offer. |
| **Audience** | Segments, the job each is hiring the site to do, their level of expertise, and **their vocabulary in their own words** with real examples. | Every judgement about search intent, reading level, and whether a page answers what the reader came for. |
| **Differentiators** | Only claims that are true *and* provable, each paired with its proof. | Positioning, `5-rank-relevance`, and any copy that needs to say why this and not a competitor. |
| **Proof assets** | Real case studies, original data, named testimonials, credentials, certifications, awards, and named authors with what they are genuinely expert in. | The raw material for honest E-E-A-T. If it is not here, it does not go on the page. |
| **Voice** | Tone, person (we/you/I), reading level, sentence habits, formatting conventions, words the business uses and avoids — **with quoted examples from real existing copy**. | `seo-content-editing` preserving voice, and any drafting staying recognisably theirs. |
| **Claims and constraints** | What this business may not say: regulatory limits, YMYL considerations, compliance sign-off, competitor-naming policy, embargoed or confidential material. | Keeping the work legal and safe, and knowing when a human must approve. |
| **Topical territory** | What the site should credibly own, adjacent areas it could earn, and what is deliberately out of scope. | `seo-positioning-strategy`, content briefs, and refusing topics the business has no standing to cover. |
| **Competitors** | Who they actually compete with, who ranks for their terms, and how each frames the category. | Gap analysis and differentiation that is not generic. |
| **Entities** | Canonical names and spellings: product names, brand capitalisation, people, places, and any `sameAs` identifiers already in use. | Consistency across copy and schema; entity clarity for search and answer engines. |
| **Open questions** | The short ranked list of unknowns that materially matter, each with a proposed default. | The only thing the human is asked to do. |
| **Freshness** | When gathered, when last re-checked, and what is known to be volatile. | Progression runs knowing what to re-verify. |

---

## Worked example

Abbreviated, to show the shape and the labelling rather than the length.

```markdown
# Context — northfield-tools.example
_Gathered: 2026-08-18 · Last re-checked: 2026-08-18 · Sources: repo, served site, Search Console_

## Identity
Sells hand-forged woodworking tools direct to makers. `[established: home, /about]`
Legal entity: Northfield Tool Company Ltd, England and Wales. `[established: /terms]`
NAP: Unit 4 Mill Road, Sheffield S3 8DE · 0114 496 0182 `[established: /contact, footer]`
Trading since 2009. `[established: /about]` Team size `[unknown]`.

## Offer
Three lines: chisels, planes, marking tools. `[established: /shop]`
Direct-to-consumer only; no trade or wholesale pricing. `[established: /faq]`
£45–£320 per tool; free UK delivery over £75. `[established: product data in `src/data/products.ts`]`
**`[conflict]`** `/about` still advertises a sharpening service; it is absent from the shop
and from the product data. Confirm whether it still runs before writing about it.

## Audience
1. **Hobbyist woodworkers**, intermediate and up, buying their first quality tool.
   Job: "buy a tool that will outlast the cheap one I regret." `[inferred: product reviews, FAQ themes]`
2. **Professional joiners** replacing worn tools. `[inferred: Search Console — "replacement plane iron", "professional chisel set"]`
Vocabulary: they say **"plane iron"** not "blade", **"bevel-up"**, **"tool roll"**, and search
"how to sharpen" far more than "sharpening service". `[established: Search Console query report]`

## Differentiators
- Forged in-house in Sheffield, not badge-engineered. `[established: /how-we-make-them, with workshop photos]`
- Lifetime sharpening guarantee. `[established: /guarantee]`
- Steel spec published per tool. `[established: product pages]`
Everything else read as category-standard; do not claim uniqueness that is not here.

## Proof assets
- Workshop process photographs, owned. `[established]`
- 340 named product reviews on-site. `[established]`
- Founder Ray Alderton, 30 years as a toolmaker. `[established: /about]` — usable byline.
- Independent testing or awards `[unknown]` — do not imply any.

## Voice
Plain, unshowy, second person, short sentences. Assumes competence; never talks down.
Real example, quoted from `/products/bevel-up-plane`:
> "The iron arrives sharp. You will still want to hone it before the first cut."
Avoids: "revolutionary", "game-changing", exclamation marks. `[inferred: no instance across 40 pages]`

## Claims and constraints
Not a regulated sector. Do not claim "the best in Britain" or similar superlatives —
unsupported and inconsistent with the voice. `[inferred]`
Competitors are never named on-site; keep it that way unless told otherwise. `[inferred]`

## Topical territory
Own: tool care, sharpening technique, choosing a first quality tool, Sheffield toolmaking.
Could earn: joinery technique where a tool is central.
Out of scope: power tools, general DIY. No standing, no products. `[inferred]`

## Competitors
Two named UK toolmakers rank for the core terms; both lead on heritage, neither
publishes steel spec per tool. `[inferred: SERP for "hand forged chisel uk"]`

## Entities
"Northfield Tool Company" (no ampersand) · "bevel-up" hyphenated · Ray Alderton.
Existing `Organization` schema on all pages, `@id` `/#org`. `[established]`

## Open questions
1. Is the sharpening service still running? Default if unanswered: treat as discontinued
   and remove it from `/about` rather than writing new content about it.
2. Will Ray be bylined on technique articles? Default: yes, attributed as toolmaker,
   no credentials claimed beyond the 30 years already published.
3. Trade customers a target this year? Default: no — consumer only.

## Freshness
Volatile: pricing, the sharpening service, delivery thresholds. Re-check each run.
```

---

## Discipline

- **Specific beats complete.** One quoted line of real voice is worth a paragraph describing the voice.
- **Cite where you found things.** A fact whose source you cannot name is an inference; label it as one.
- **Record conflicts rather than resolving them silently.** The conflict is often the most valuable finding in the file.
- **Never store secrets or personal data.** No keys, no credentials, no information about identifiable individuals who did not publish it themselves. The file is committed to the user's repository.
- **Re-check before you rely on it.** On a progression run, verify the volatile sections before using the pack, and update the freshness line.
