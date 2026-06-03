# Entity consistency and attribution (the trust layer)

Read this for the trust half of the Cite rung: making an answer engine confident *who you are* and *why you can be believed*. This is where the white-hat rule is most important and most tempting to break — so it's spelled out in full. The principle: **surface every genuine trust signal; fabricate none.**

---

## Entity consistency — be unmistakably one entity

An answer engine needs to resolve "this organisation / author / product" to a single, coherent entity. Inconsistency makes it unsure, and uncertainty loses citations.

### Make these agree everywhere
- **Name & brand:** identical spelling, casing, and form across every page, the schema, and external profiles. "Acme Ltd", "Acme", and "ACME Limited" scattered around read as possibly-different entities.
- **Schema `@id`:** reuse one consistent `@id` for the organisation/person across all JSON-LD (rung 3), so every block refers to the same node.
- **Core facts:** address, phone, founding details, logo — consistent across the site, schema, and listings.

### `sameAs` — connect to the wider web (real profiles only)
Add `sameAs` links in your `Organization`/`Person` schema to the entity's **genuine** external presences:

```json
"sameAs": [
  "https://www.linkedin.com/company/real-company",
  "https://en.wikipedia.org/wiki/Real_Company",
  "https://www.crunchbase.com/organization/real-company"
]
```

This corroborates your identity against independent sources — a strong trust and disambiguation signal. **Only link profiles that genuinely belong to the entity.** Never link to profiles you don't control or that aren't really yours.

---

## E-E-A-T — Experience, Expertise, Authoritativeness, Trust

Answer engines favour content they can attribute to real, credible sources. The four signals:

- **Experience** — genuine first-hand experience with the subject (used the product, did the thing, visited the place).
- **Expertise** — real knowledge/qualifications of the author.
- **Authoritativeness** — recognition of the author/site as a go-to source (real citations, mentions, reputation).
- **Trust** — accuracy, transparency, honesty; the overarching one.

### Surface the genuine signals you have (safe — do this)
- **Visible bylines** with the **real** author's name.
- **Author bios** stating **real** credentials, experience, and qualifications, ideally linking to the author's **real** profiles (and mirrored in `Person` schema with `sameAs`).
- **Citations and references** to **real** sources, linked.
- **"Reviewed by [real expert]"** where a genuine review actually happened.
- **Transparency**: real contact details, about page, editorial policy where applicable.
- **Evidence of experience**: genuine first-hand detail, original photos, real case studies/results.

Mirror these in schema (`author` as a real `Person`, `reviewedBy`, `citation`) — only where they're real.

---

## The white-hat line — what you must NEVER do

This is the hard boundary. When a genuine signal is **missing**, the correct action is to **flag it as a human task**, never to invent it:

- ❌ Inventing an author or a persona ("Dr. Jane Smith, expert") who doesn't exist.
- ❌ Adding credentials, qualifications, or years of experience that aren't real.
- ❌ Fabricating "reviewed by" / "medically reviewed by" / "fact-checked by".
- ❌ Inventing statistics, study results, or citations, or linking to sources that don't say what you claim.
- ❌ Creating fake testimonials, reviews, ratings, awards, or case studies.
- ❌ Adding `sameAs` to profiles that aren't genuinely the entity's.

Two reasons this line is absolute:
1. **It's dishonest** and can mislead real people on consequential topics (health, finance, legal).
2. **It backfires.** AI answer engines and search systems are increasingly built to detect and discount manufactured authority. Faking E-E-A-T doesn't just risk penalties — it tends not to work, while poisoning the genuine trust the rest of the ladder builds.

### How to flag, concretely
Tell the user exactly what's missing and why it matters, and offer to surface/mark up the real thing if they provide it:
> "These articles are anonymous. AI answer engines favour content attributed to real, credentialled authors. I won't invent an author. If a real person wrote or can vouch for these, give me their name and genuine credentials and I'll add a visible byline, a bio, and `Person` schema with links to their real profiles."

---

## Verifying the trust layer

- **Consistency:** names, `@id`s, and core facts agree across pages, schema, and `sameAs` targets — and the `sameAs` targets are genuinely the entity's.
- **Reality check (the one that outranks the rest):** every author, credential, citation, statistic, review, and award you surfaced or marked up is **real and verifiable.** If you can't verify it, it shouldn't be there.
- **Served HTML:** visible trust signals (bylines, bios, citations) and their schema are in the served output, not client-only.

If anything was fabricated, remove it and flag the gap. A page with honest "we don't have this yet" is worth more than a page with convincing lies — to users, to search, and to the answer engines this rung targets.
