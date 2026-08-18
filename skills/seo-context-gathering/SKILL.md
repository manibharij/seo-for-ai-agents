---
name: seo-context-gathering
description: >-
  Build the CONTEXT the rest of the SEO work depends on — what this business
  actually is, what it really sells, who it serves and in their own words, what it
  can truthfully claim, what proof exists (real authors, data, case studies,
  credentials), how it writes, and who it competes with — gathered from the
  codebase, the served site, connected data, and free public sources, then written
  to a reusable context pack at .seo/context.md. Use before any content, positioning,
  schema, or E-E-A-T work, and when you say "understand my business", "gather
  context", "what's our brand voice", "who are we writing for", "onboard yourself",
  "before you write anything". Every fact is labelled established / inferred /
  unknown with its source — inferences may shape strategy, but only established
  facts may reach published copy or schema. It gathers and records; it never
  invents, and never fills a gap with a plausible guess.
---

# Context Gathering — learn the business before you touch the words

Every judgement further up the pack depends on context the agent usually does not have. "Does this page match intent?" needs to know who the reader is. "Is this E-E-A-T credible?" needs to know which credentials are real. "What topics should we own?" needs to know what the business actually does. "Is this claim honest?" needs to know what is true.

Without that, an agent does the only thing it can: it guesses, in a generic voice, about a business it has half-understood. That is exactly how well-intentioned SEO work turns into bland, fabricated content — the failure mode this whole pack exists to prevent.

So this skill does the unglamorous work first. It **gathers real context, records where each fact came from, and writes it down once** in `.seo/context.md`, so every later skill and every later run reads the same grounded picture instead of re-deriving a shallow one.

> **The rule that makes this safe: record provenance, never invent.** Every entry in the pack is marked **established** (the business states it), **inferred** (you concluded it, and from what), or **unknown** (you do not know). An inference may shape strategy. Only an **established** fact may appear in published copy, structured data, or a trust signal. "Unknown" stays unknown — it is never rounded up to a plausible guess.

Work: **Gather what you have → Gather what you can reach → Corroborate and label → Write the pack → Ask only what's left.**

---

## Step 1 — Gather from what is already in front of you

Cost nothing, needs no permission, and usually answers most of it. Read widely before concluding anything (full source list in `references/context-sources.md`):

- **The repository.** README, `docs/`, CHANGELOG, `package.json` description, code comments, CMS content models, product/pricing data files, i18n strings, seed data, and any `AGENTS.md`/`CLAUDE.md` the team wrote for themselves.
- **The served site.** Home, about, pricing, product and service pages, docs, blog, FAQ, careers, and the legal pages — terms and privacy usually name the **registered entity**, jurisdiction, and sometimes the real trading history. Footers and contact pages carry NAP for local businesses.
- **Existing structured data.** Whatever `Organization`, `Product`, `Person` or `LocalBusiness` entities the site already declares: names, spellings, identifiers and `sameAs` links are context, and they must stay consistent with whatever you write later.
- **The team's own words.** Support macros, sales FAQs, onboarding emails, changelog entries and issue templates are the most honest description of what customers actually ask and what the product actually does.

## Step 2 — Gather what you can reach

- **Connected data, if present** (optional, the user's own keys — see `seo-orchestrator/references/live-data-integrations.md`). **Search Console query data is the single richest source of audience vocabulary in existence for this site**: it is the literal phrasing of people who already arrive. Use it to learn how they speak, not just what ranks.
- **Free public sources, no key required.** Search suggestions and related searches, "people also ask" style questions, and public reference entries for entity names and spellings. These give you real question phrasing cheaply. See `references/context-sources.md` for the list and the etiquette.
- **Competitors.** The ones the site names, plus whoever actually appears for its core terms. Read them for **coverage and positioning** — what they cover, how they frame it, what they claim. Never copy their words; you are mapping the territory, not harvesting it.
- **Paid tools, if connected.** DataForSEO, Ahrefs or Semrush for real demand and competitor coverage, when the user has them.

**Etiquette is not optional:** respect `robots.txt` and rate limits, fetch politely, take nothing behind a login, and never collect personal data about individuals. Sending a query to an external service is an outward action — only use services the user has connected or that the site's own visitors would hit anyway.

## Step 3 — Corroborate and label

For each fact, record **what it is, where it came from, and how confident you are**:

| Label | Meaning | May be used for |
|---|---|---|
| **Established** | The business states it, in its own copy, repo, or structured data. Quote or cite the location. | Anything, including published copy, schema and trust signals. |
| **Inferred** | You concluded it from evidence. Record the evidence. | Strategy, prioritisation, briefs, internal planning. **Not** published claims. |
| **Unknown** | You could not determine it. | Nothing. It becomes a question for the human. |

Two disciplines make this real:

- **Corroborate before promoting.** If the site says one thing and the repo says another (an old tagline, a discontinued product, a price that moved), that is a **conflict** — record both and flag it, rather than silently picking one. Stale context confidently applied is worse than no context.
- **Never upgrade a label to make the work easier.** If a founder's credentials are not stated anywhere, "founder is an expert" is unknown, not inferred. That distinction is what stops the pack manufacturing E-E-A-T later.

## Step 4 — Write the context pack

Write `.seo/context.md` in the user's project, alongside `audit.md`, `state.json` and `log.md`. The full section-by-section format, with a worked example, is in `references/context-pack-format.md`. It covers:

**Identity** (what this is, the legal entity, NAP where relevant) · **Offer** (what is actually sold, and how it is priced) · **Audience** (segments, the job they are hiring the site to do, and **their vocabulary in their own words**) · **Differentiators** (only ones that are true and provable, each with its proof) · **Proof assets** (real case studies, data, testimonials, credentials, named authors and what they are genuinely expert in — the raw material for honest E-E-A-T) · **Voice** (tone, person, reading level, habits and banned words, **with real quoted examples from existing copy**) · **Claims and constraints** (what this business may not say: regulated sector, YMYL, compliance, competitor-naming policy) · **Topical territory** (what it should own, and what is deliberately out of scope) · **Competitors** · **Entities** (canonical names and spellings for consistency and schema) · **Open questions**.

Two rules for the file itself: **no credentials, no private customer data.** It is committed to the user's repository, so it holds conclusions, never secrets, and never anything about an identifiable individual who did not publish it themselves.

## Step 5 — Ask only what genuinely remains

The pack's standing principle is *work it out yourself; don't interrogate the user* — and a context skill is exactly where that principle is most easily broken. Do not turn this into an onboarding form.

Infer everything you can. Then present **a short, ranked list of only the questions that you genuinely could not answer and that would materially change the work**, each with **a proposed default** so the user can confirm rather than compose. Three good questions beat twenty thorough ones. Anything they do not answer stays **unknown**, and the downstream skills treat it accordingly.

---

## How the rest of the pack uses this

Once `.seo/context.md` exists, every other skill reads it first and stops guessing:

- **`seo-content-audit`** judges intent match and quality against a real audience rather than an imagined one.
- **`seo-content-editing`** writes in a voice it can quote examples of, and knows which claims are permitted.
- **`5-rank-relevance`** and **`cite-aeo-geo`** ground E-E-A-T and answer formatting in proof assets that actually exist.
- **`seo-positioning-strategy`** plans topical territory from real differentiators instead of generic category coverage.
- **`3-understand-schema`** uses the recorded entity names and spellings, so the markup matches the business.
- **`seo-proposal-roadmap`** can describe the business back to its owner correctly, which is what makes a proposal credible.

## Keeping it current

Context rots. On a **progression run**, re-read `.seo/context.md` before using it and re-check the volatile parts: the offer, pricing, positioning, people, and anything labelled inferred. Update what changed, note the date, and re-flag conflicts. A confidently-applied stale context pack produces confidently wrong content, which is worse than starting cold.

## What this skill will not do

- It will not **invent** a mission, an audience, a differentiator, a credential, or a statistic to complete a section.
- It will not **promote an inference to a fact** to make later work easier.
- It will not **collect personal data** about individuals, scrape behind logins, or ignore `robots.txt`.
- It will not **store secrets** — no API keys, no credentials, no private customer data in `.seo/context.md`.
- It will not **interrogate the user** in place of doing the reading.

## Reference files
- `references/context-sources.md` — every source worth reading, what each one is uniquely good for, the free no-key options, and the fetching etiquette and legal lines.
- `references/context-pack-format.md` — the `.seo/context.md` format section by section, with a worked example and the provenance labelling in practice.
